"""
LiveKit Voice Agent using Pipecat services.

This agent connects to LiveKit Cloud via WebSocket and uses Pipecat
for STT, LLM, and TTS processing.
"""

import asyncio
import os
from typing import Optional

from loguru import logger

from pipecat.audio.turn.smart_turn.local_smart_turn_v3 import LocalSmartTurnAnalyzerV3
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.livekit.transport import LiveKitParams, LiveKitTransport
from pipecat.runner.livekit import generate_token_with_agent

# LiveKit configuration
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")


class VoiceAgent:
    """Voice AI agent that connects to LiveKit rooms."""

    def __init__(
        self,
        room_name: str,
        participant_identity: str = "agent",
    ):
        """Initialize the voice agent.

        Args:
            room_name: Name of the LiveKit room to join.
            participant_identity: Identity for the agent participant.
        """
        self.room_name = room_name
        self.participant_identity = participant_identity
        self.transport: Optional[LiveKitTransport] = None
        self.task: Optional[PipelineTask] = None
        self.runner: Optional[PipelineRunner] = None

    async def start(self):
        """Start the agent and connect to LiveKit room."""
        try:
            logger.info(f"Starting agent for room: {self.room_name}")

            # Generate LiveKit token
            token = generate_token_with_agent(
                self.room_name,
                self.participant_identity,
                LIVEKIT_API_KEY,
                LIVEKIT_API_SECRET,
            )

            # Create LiveKit transport
            self.transport = LiveKitTransport(
                url=LIVEKIT_URL,
                token=token,
                room_name=self.room_name,
                params=LiveKitParams(
                    audio_in_enabled=True,
                    audio_out_enabled=True,
                    vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
                    turn_analyzer=LocalSmartTurnAnalyzerV3(),
                ),
            )

            # Initialize services
            stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))
            llm = OpenAILLMService(api_key=os.getenv("OPENAI_API_KEY"))
            tts = CartesiaTTSService(
                api_key=os.getenv("CARTESIA_API_KEY"),
                voice_id="71a7ad14-091c-4e8e-a314-022ece01c121",  # British Reading Lady
            )

            # Set up conversation context
            messages = [
                {
                    "role": "system",
                    "content": "You are a friendly AI assistant. Respond naturally and keep your answers conversational.",
                },
            ]

            context = LLMContext(messages)
            context_aggregator = LLMContextAggregatorPair(context)

            # Add RTVI processor (from bot.py)
            rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

            # Create pipeline (matching bot.py structure)
            pipeline = Pipeline(
                [
                    self.transport.input(),  # Transport user input
                    rtvi,  # RTVI processor
                    stt,  # Speech-to-text
                    context_aggregator.user(),  # User responses
                    llm,  # LLM
                    tts,  # Text-to-speech
                    self.transport.output(),  # Transport bot output
                    context_aggregator.assistant(),  # Assistant spoken responses
                ]
            )

            # Create task (matching bot.py structure)
            self.task = PipelineTask(
                pipeline,
                params=PipelineParams(
                    enable_metrics=True,
                    enable_usage_metrics=True,
                ),
                observers=[RTVIObserver(rtvi)],
            )

            # Set up event handlers
            @self.transport.event_handler("on_first_participant_joined")
            async def on_first_participant_joined(transport, participant_id):
                logger.info(f"First participant joined: {participant_id}")
                # Kick off the conversation
                messages.append(
                    {"role": "system", "content": "Say hello and briefly introduce yourself."}
                )
                await self.task.queue_frames([LLMRunFrame()])

            @self.transport.event_handler("on_participant_disconnected")
            async def on_participant_disconnected(transport, participant_id):
                logger.info(f"Participant disconnected: {participant_id}")
                await self.task.cancel()

            # Create runner
            self.runner = PipelineRunner()

            # Start the pipeline
            logger.info("Starting pipeline...")
            await self.runner.run(self.task)

        except Exception as e:
            logger.error(f"Error starting agent: {e}", exc_info=True)
            raise

    async def stop(self):
        """Stop the agent and disconnect from LiveKit room."""
        try:
            logger.info("Stopping agent...")
            if self.task:
                await self.task.cancel()
            if self.transport:
                await self.transport.output().stop()
            logger.info("Agent stopped")
        except Exception as e:
            logger.error(f"Error stopping agent: {e}", exc_info=True)


async def run_agent(room_name: str, participant_identity: str = "agent"):
    """Run a voice agent in a LiveKit room.

    Args:
        room_name: Name of the LiveKit room to join.
        participant_identity: Identity for the agent participant.
    """
    agent = VoiceAgent(room_name=room_name, participant_identity=participant_identity)
    try:
        await agent.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    finally:
        await agent.stop()


if __name__ == "__main__":
    # For testing: run agent directly
    import sys

    room_name = sys.argv[1] if len(sys.argv) > 1 else "test-room"
    asyncio.run(run_agent(room_name))

