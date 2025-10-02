#!/usr/bin/env python3
"""
Test script for the NPI MCP Server
This script demonstrates how to use the NPI server tools
"""

import requests
import json

# Base URL for the NPI Registry API (same as in server_npi.py)
NPI_API_BASE_URL = "https://npiregistry.cms.hhs.gov/api/"

def test_npi_lookup():
    """Test NPI lookup functionality"""
    print("Testing NPI lookup...")
    
    # Test with a known NPI number (this is a sample - replace with actual NPI)
    test_npi = "1234567890"  # This is just a test number
    
    params = {"number": test_npi, "version": "2.1"}
    url = f"{NPI_API_BASE_URL}?number={test_npi}&version=2.1"
    
    try:
        response = requests.get(url, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Result Count: {data.get('result_count', 0)}")
            if data.get('result_count', 0) > 0:
                print("Sample result found!")
                print(json.dumps(data['results'][0], indent=2))
            else:
                print("No results found (expected for test NPI)")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error testing NPI lookup: {e}")

def test_npi_search():
    """Test NPI search functionality"""
    print("\nTesting NPI search...")
    
    # Search for providers in a specific city and state
    params = {
        "city": "New York",
        "state": "NY", 
        "taxonomy_description": "Family Medicine",
        "limit": 5,
        "version": "2.1"
    }
    
    url = f"{NPI_API_BASE_URL}?" + "&".join([f"{k}={v}" for k, v in params.items()])
    
    try:
        response = requests.get(url, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Result Count: {data.get('result_count', 0)}")
            if data.get('result_count', 0) > 0:
                print("Search results found!")
                # Show first result
                first_result = data['results'][0]
                basic_info = first_result.get('basic', {})
                print(f"Provider: {basic_info.get('first_name', '')} {basic_info.get('last_name', '')} {basic_info.get('organization_name', '')}")
                print(f"Enumeration Type: {first_result.get('enumeration_type', 'Unknown')}")
            else:
                print("No results found")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error testing NPI search: {e}")

def test_api_connectivity():
    """Test basic API connectivity"""
    print("\nTesting API connectivity...")
    
    try:
        # Simple test request
        response = requests.get(f"{NPI_API_BASE_URL}?version=2.1&limit=1", timeout=10)
        print(f"API Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ NPI Registry API is accessible")
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Cannot connect to NPI Registry API: {e}")
        return False

if __name__ == "__main__":
    print("NPI MCP Server Test Suite")
    print("=" * 50)
    
    # Test API connectivity first
    if test_api_connectivity():
        # Run other tests
        test_npi_lookup()
        test_npi_search()
    
    print("\nTest suite completed!")
    print("\nTo run the actual MCP server:")
    print("uv run python server_npi.py")
