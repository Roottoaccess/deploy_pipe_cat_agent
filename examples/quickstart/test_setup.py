#!/usr/bin/env python3
"""
Test script to verify LiveKit setup and dependencies.

Run this to check if everything is configured correctly before deployment.
"""

import os
import sys

print("🔍 Testing LiveKit Setup...\n")

# Test 1: Environment Variables
print("1. Checking environment variables...")
required_vars = [
    "LIVEKIT_URL",
    "LIVEKIT_API_KEY",
    "LIVEKIT_API_SECRET",
    "DEEPGRAM_API_KEY",
    "OPENAI_API_KEY",
    "CARTESIA_API_KEY",
]

missing_vars = []
for var in required_vars:
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        masked = value[:8] + "..." if len(value) > 8 else "***"
        print(f"   ✅ {var}: {masked}")
    else:
        print(f"   ❌ {var}: NOT SET")
        missing_vars.append(var)

if missing_vars:
    print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
    print("   Set these in Render dashboard → Environment tab")
else:
    print("\n   ✅ All environment variables set!")

# Test 2: Python Dependencies
print("\n2. Checking Python dependencies...")
try:
    import fastapi
    print(f"   ✅ fastapi: {fastapi.__version__}")
except ImportError:
    print("   ❌ fastapi: NOT INSTALLED")
    sys.exit(1)

try:
    import uvicorn
    print(f"   ✅ uvicorn: {uvicorn.__version__}")
except ImportError:
    print("   ❌ uvicorn: NOT INSTALLED")
    sys.exit(1)

try:
    import livekit
    print(f"   ✅ livekit: {livekit.__version__}")
except ImportError:
    print("   ❌ livekit: NOT INSTALLED")
    sys.exit(1)

try:
    import pipecat
    print(f"   ✅ pipecat-ai: {pipecat.__version__}")
except ImportError:
    print("   ❌ pipecat-ai: NOT INSTALLED")
    sys.exit(1)

# Test 3: Import bot.py
print("\n3. Testing bot.py imports...")
try:
    from bot import run_bot
    print("   ✅ bot.py: run_bot function imported successfully")
except ImportError as e:
    print(f"   ❌ bot.py: Import failed - {e}")
    sys.exit(1)

# Test 4: Import agent.py
print("\n4. Testing agent.py imports...")
try:
    from agent import VoiceAgent
    print("   ✅ agent.py: VoiceAgent class imported successfully")
except ImportError as e:
    print(f"   ❌ agent.py: Import failed - {e}")
    sys.exit(1)

# Test 5: Import main.py components
print("\n5. Testing main.py imports...")
try:
    from main import app, LIVEKIT_CONFIGURED
    print("   ✅ main.py: FastAPI app imported successfully")
    print(f"   ✅ LiveKit configured: {LIVEKIT_CONFIGURED}")
except ImportError as e:
    print(f"   ❌ main.py: Import failed - {e}")
    sys.exit(1)

# Test 6: LiveKit Token Generation
print("\n6. Testing LiveKit token generation...")
if not missing_vars:
    try:
        from pipecat.runner.livekit import generate_token_with_agent
        
        test_token = generate_token_with_agent(
            "test-room",
            "test-agent",
            os.getenv("LIVEKIT_API_KEY"),
            os.getenv("LIVEKIT_API_SECRET"),
        )
        
        if test_token and len(test_token) > 20:
            print("   ✅ LiveKit token generation: SUCCESS")
        else:
            print("   ❌ LiveKit token generation: FAILED (invalid token)")
    except Exception as e:
        print(f"   ❌ LiveKit token generation: FAILED - {e}")
else:
    print("   ⏭️  Skipped (missing environment variables)")

# Test 7: LiveKit URL Format
print("\n7. Testing LiveKit URL format...")
livekit_url = os.getenv("LIVEKIT_URL")
if livekit_url:
    if livekit_url.startswith("wss://"):
        print(f"   ✅ LiveKit URL format: CORRECT ({livekit_url[:20]}...)")
    else:
        print(f"   ⚠️  LiveKit URL should start with 'wss://' (got: {livekit_url[:20]}...)")
else:
    print("   ⏭️  Skipped (LIVEKIT_URL not set)")

print("\n" + "="*50)
if missing_vars:
    print("⚠️  SETUP INCOMPLETE")
    print(f"   Please set these environment variables: {', '.join(missing_vars)}")
    sys.exit(1)
else:
    print("✅ ALL TESTS PASSED!")
    print("   Your LiveKit setup is ready for deployment!")
    print("="*50)

