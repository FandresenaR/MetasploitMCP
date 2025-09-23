#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test script for OpenRouter integration with MetasploitMCP.
Run this to verify your OpenRouter configuration works.
"""

import os
import sys
import asyncio
from pathlib import Path

# Load environment variables from .env.local if it exists
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent / '.env.local'
    if env_file.exists():
        load_dotenv(env_file)
        print(f"Loaded environment variables from {env_file}")
    else:
        print("No .env.local file found, using system environment variables")
except ImportError:
    print("python-dotenv not installed, using system environment variables only")
    print("Install with: pip install python-dotenv")

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from MetasploitMCP import get_openrouter_client, OPENROUTER_MODEL

async def test_openrouter_connection():
    """Test the OpenRouter API connection."""
    print("Testing OpenRouter API connection...")

    client = get_openrouter_client()
    if not client:
        print("❌ OpenRouter client not configured.")
        print("Please set the OPENROUTER_API_KEY environment variable.")
        print("Get your API key from: https://openrouter.ai/")
        return False

    try:
        print(f"Using model: {OPENROUTER_MODEL}")
        response = await asyncio.to_thread(
            lambda: client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[{
                    "role": "user",
                    "content": "Hello! Please respond with a brief test message confirming the OpenRouter integration works."
                }],
                max_tokens=100,
                temperature=0.1
            )
        )

        ai_response = response.choices[0].message.content.strip()
        print("✅ OpenRouter API connection successful!")
        print(f"AI Response: {ai_response}")
        return True

    except Exception as e:
        print(f"❌ OpenRouter API test failed: {e}")
        return False

async def main():
    """Main test function."""
    print("MetasploitMCP OpenRouter Integration Test")
    print("=" * 50)

    # Check environment variables
    api_key = os.getenv('OPENROUTER_API_KEY')
    if api_key:
        print(f"✅ OPENROUTER_API_KEY is set (length: {len(api_key)})")
    else:
        print("❌ OPENROUTER_API_KEY is not set")

    base_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
    print(f"OpenRouter Base URL: {base_url}")

    model = os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3-haiku:beta')
    print(f"Model: {model}")

    print()

    # Test connection
    success = await test_openrouter_connection()

    if success:
        print("\n🎉 OpenRouter integration is working correctly!")
        print("You can now use the AI-powered tools in MetasploitMCP:")
        print("- analyze_exploit_with_ai")
        print("- generate_metasploit_commands_with_ai")
        print("- analyze_vulnerability_with_ai")
    else:
        print("\n❌ OpenRouter integration test failed.")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    asyncio.run(main())