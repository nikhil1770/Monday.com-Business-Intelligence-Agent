"""
Test Script - Run this to verify your setup
"""

import sys

print("="*70)
print("Monday.com BI Agent - Setup Verification")
print("="*70)

# Test 1: Check imports
print("\n1. Checking imports...")
try:
    import requests
    import anthropic
    import streamlit
    print("   ✅ All required packages installed")
except ImportError as e:
    print(f"   ❌ Missing package: {e}")
    print("   Run: pip install -r requirements.txt")
    sys.exit(1)

# Test 2: Check config
print("\n2. Checking configuration...")
try:
    from config import MONDAY_API_TOKEN, DEALS_BOARD_ID, CLAUDE_API_KEY
    
    if "YOUR_" in MONDAY_API_TOKEN or "YOUR_" in CLAUDE_API_KEY:
        print("   ⚠️  API keys not configured yet")
        print("   Edit config.py and add your actual API keys")
    else:
        print("   ✅ Configuration loaded")
        print(f"   Deals Board ID: {DEALS_BOARD_ID}")
except Exception as e:
    print(f"   ❌ Error loading config: {e}")
    sys.exit(1)

# Test 3: Test Monday.com connection
print("\n3. Testing Monday.com API...")
try:
    from monday_api import get_deals
    
    if "YOUR_" not in MONDAY_API_TOKEN:
        deals = get_deals(limit=1)
        if isinstance(deals, list):
            print(f"   ✅ Monday.com API working ({len(deals)} deal retrieved)")
        else:
            print(f"   ❌ Monday.com API error: {deals.get('error', 'Unknown')}")
    else:
        print("   ⏭️  Skipped (no API token configured)")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Test Claude connection
print("\n4. Testing Claude API...")
try:
    if "YOUR_" not in CLAUDE_API_KEY:
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            messages=[{"role": "user", "content": "Say 'API working'"}]
        )
        print("   ✅ Claude API working")
    else:
        print("   ⏭️  Skipped (no API token configured)")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Final summary
print("\n" + "="*70)
print("Setup Status:")
print("="*70)

if "YOUR_" in MONDAY_API_TOKEN or "YOUR_" in CLAUDE_API_KEY:
    print("\n⚠️  Action Required:")
    print("   1. Edit config.py")
    print("   2. Add your Monday.com API token")
    print("   3. Add your Claude API key")
    print("   4. Run this test again")
else:
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("   1. Test the agent: python agent.py")
    print("   2. Run the app: streamlit run app.py")

print("\n" + "="*70)