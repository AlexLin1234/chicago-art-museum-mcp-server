#!/usr/bin/env python3
"""
Simple test script to verify the Art Institute of Chicago MCP server is working.

This script tests the API connection and basic functionality without running
the full MCP server.
"""

import asyncio
import sys
from server import make_api_request, format_artwork_response


async def test_api_connection():
    """Test basic API connectivity"""
    print("Testing Art Institute of Chicago API connection...")
    print("-" * 60)

    try:
        # Test 1: Search for artworks
        print("\n1. Testing artwork search...")
        data = await make_api_request("artworks/search", {"q": "Monet", "limit": 3})
        print("✓ Artwork search successful")
        print(f"  Found {data.get('pagination', {}).get('total', 0)} total results")

        # Test 2: Get specific artwork
        print("\n2. Testing artwork retrieval...")
        # Get the first artwork ID from search results
        if data.get("data") and len(data["data"]) > 0:
            artwork_id = data["data"][0].get("id")
            artwork_data = await make_api_request(f"artworks/{artwork_id}")
            print(f"✓ Successfully retrieved artwork: {artwork_data.get('data', {}).get('title', 'Unknown')}")

        # Test 3: Search for agents
        print("\n3. Testing agent search...")
        agent_data = await make_api_request("agents/search", {"q": "Picasso", "limit": 1})
        print("✓ Agent search successful")
        print(f"  Found {agent_data.get('pagination', {}).get('total', 0)} total results")

        # Test 4: List galleries
        print("\n4. Testing gallery listing...")
        gallery_data = await make_api_request("galleries", {"limit": 5})
        print("✓ Gallery listing successful")
        print(f"  Found {gallery_data.get('pagination', {}).get('total', 0)} total galleries")

        # Test 5: Search exhibitions
        print("\n5. Testing exhibition search...")
        exhibition_data = await make_api_request("exhibitions/search", {"q": "impressionism", "limit": 1})
        print("✓ Exhibition search successful")
        print(f"  Found {exhibition_data.get('pagination', {}).get('total', 0)} total results")

        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
        print("\nYour server is ready to use with Claude Desktop.")
        print("Follow the README instructions to configure Claude Desktop.")

        return True

    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        print("\nPlease check:")
        print("  1. Your internet connection")
        print("  2. That api.artic.edu is accessible")
        print("  3. Your firewall settings")
        return False


async def main():
    """Run tests"""
    success = await test_api_connection()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    print("Art Institute of Chicago MCP Server - Connection Test")
    print("=" * 60)
    asyncio.run(main())
