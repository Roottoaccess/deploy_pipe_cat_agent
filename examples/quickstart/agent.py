"""
LiveKit Voice Agent using bot.py.

This agent connects to LiveKit Cloud and uses bot.py's run_bot function
for all the bot logic (STT, LLM, TTS processing).
"""

import os
from typing import Optional

from loguru import logger

from pipecat.audio.turn.smart_turn.local_smart_turn_v3 import LocalSmartTurnAnalyzerV3
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.runner.livekit import generate_token_with_agent
from pipecat.runner.types import RunnerArguments
from pipecat.transports.livekit.transport import LiveKitParams, LiveKitTransport

# Import bot.py's run_bot function
from bot import run_bot

# LiveKit configuration
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")


class SimpleRunnerArguments:
    """Simple RunnerArguments-like object for bot.py compatibility."""
    
    def __init__(self):
        self.handle_sigint = False


class VoiceAgent:
    """Voice AI agent that connects to LiveKit rooms and uses bot.py."""

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
        self.runner_args: Optional[RunnerArguments] = None

    async def start(self):
        """Start the agent and connect to LiveKit room using bot.py."""
        try:
            logger.info(f"Starting agent for room: {self.room_name} using bot.py")

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

            # Create runner arguments for bot.py
            self.runner_args = SimpleRunnerArguments()

            # Use bot.py's run_bot function with LiveKit transport
            logger.info("Calling bot.py's run_bot function...")
            await run_bot(self.transport, self.runner_args)

        except Exception as e:
            logger.error(f"Error starting agent: {e}", exc_info=True)
            raise

    async def stop(self):
        """Stop the agent and disconnect from LiveKit room."""
        try:
            logger.info("Stopping agent...")
            if self.transport:
                await self.transport.output().stop()
            logger.info("Agent stopped")
        except Exception as e:
            logger.error(f"Error stopping agent: {e}", exc_info=True)


async def run_agent(room_name: str, participant_identity: str = "agent"):
    """Run a voice agent in a LiveKit room using bot.py.

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
    import asyncio
    import sys

    room_name = sys.argv[1] if len(sys.argv) > 1 else "test-room"
    asyncio.run(run_agent(room_name))
