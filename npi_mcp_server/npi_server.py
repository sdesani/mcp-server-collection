"""
NPI MCP Server

A Model Context Protocol server that provides access to the National Plan and 
Provider Enumeration System (NPPES) NPI Registry API.
"""

import json
from typing import Dict, List, Optional, Any
import requests
from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("NPI MCP Server")

# Base URL for the NPI Registry API
NPI_API_BASE_URL = "https://npiregistry.cms.hhs.gov/api/"


@mcp.tool()
def search_npi_by_number(npi_number: str) -> Dict[str, Any]:
    """
    Search for a provider by their NPI number.
    
    Args:
        npi_number: The 10-digit NPI number to search for
        
    Returns:
        Dictionary containing the provider information if found
    """
    try:
        url = f"{NPI_API_BASE_URL}?number={npi_number}&version=2.1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": data,
                "message": "NPI data retrieved successfully"
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "message": "Failed to retrieve NPI data"
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Network error occurred while fetching NPI data"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Unexpected error occurred"
        }


@mcp.tool()
def search_npi_by_name(first_name: str, last_name: str, city: Optional[str] = None, state: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for providers by name and optionally by location.
    
    Args:
        first_name: Provider's first name
        last_name: Provider's last name
        city: Optional city name for location filtering
        state: Optional state code (2 letters) for location filtering
        
    Returns:
        Dictionary containing the search results
    """
    try:
        # Build the query parameters
        params = {
            "first_name": first_name,
            "last_name": last_name,
            "version": "2.1"
        }
        
        if city:
            params["city"] = city
        if state:
            params["state"] = state
            
        # Build URL with parameters
        param_string = "&".join([f"{key}={value}" for key, value in params.items()])
        url = f"{NPI_API_BASE_URL}?{param_string}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": data,
                "message": f"Found {len(data.get('results', []))} provider(s) matching search criteria"
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "message": "Failed to search NPI database"
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Network error occurred while searching NPI database"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Unexpected error occurred"
        }


@mcp.tool()
def search_npi_by_taxonomy(taxonomy_description: str, city: Optional[str] = None, state: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for providers by taxonomy (specialty) and optionally by location.
    
    Args:
        taxonomy_description: Provider's taxonomy/specialty description (e.g., "Internal Medicine", "Cardiology")
        city: Optional city name for location filtering
        state: Optional state code (2 letters) for location filtering
        
    Returns:
        Dictionary containing the search results
    """
    try:
        # Build the query parameters
        params = {
            "taxonomy_description": taxonomy_description,
            "version": "2.1"
        }
        
        if city:
            params["city"] = city
        if state:
            params["state"] = state
            
        # Build URL with parameters
        param_string = "&".join([f"{key}={value}" for key, value in params.items()])
        url = f"{NPI_API_BASE_URL}?{param_string}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": data,
                "message": f"Found {len(data.get('results', []))} provider(s) with taxonomy '{taxonomy_description}'"
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "message": "Failed to search NPI database by taxonomy"
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Network error occurred while searching NPI database"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Unexpected error occurred"
        }


@mcp.tool()
def search_npi_by_organization_name(organization_name: str, city: Optional[str] = None, state: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for organization providers by name and optionally by location.
    
    Args:
        organization_name: Organization name to search for
        city: Optional city name for location filtering
        state: Optional state code (2 letters) for location filtering
        
    Returns:
        Dictionary containing the search results
    """
    try:
        # Build the query parameters
        params = {
            "organization_name": organization_name,
            "version": "2.1"
        }
        
        if city:
            params["city"] = city
        if state:
            params["state"] = state
            
        # Build URL with parameters
        param_string = "&".join([f"{key}={value}" for key, value in params.items()])
        url = f"{NPI_API_BASE_URL}?{param_string}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": data,
                "message": f"Found {len(data.get('results', []))} organization(s) matching '{organization_name}'"
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "message": "Failed to search NPI database for organization"
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Network error occurred while searching NPI database"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Unexpected error occurred"
        }


@mcp.tool()
def get_provider_details(npi_number: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific provider by their NPI number.
    This includes taxonomy information, addresses, and other provider details.
    
    Args:
        npi_number: The 10-digit NPI number
        
    Returns:
        Dictionary containing detailed provider information
    """
    try:
        url = f"{NPI_API_BASE_URL}?number={npi_number}&version=2.1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("results") and len(data["results"]) > 0:
                provider = data["results"][0]
                
                # Extract key information
                details = {
                    "basic_info": {
                        "npi": provider.get("number"),
                        "entity_type": provider.get("enumeration_type"),
                        "name": provider.get("basic", {}).get("first_name", "") + " " + provider.get("basic", {}).get("last_name", ""),
                        "organization_name": provider.get("basic", {}).get("organization_name"),
                        "credential": provider.get("basic", {}).get("credential"),
                        "sole_proprietor": provider.get("basic", {}).get("sole_proprietor"),
                        "gender": provider.get("basic", {}).get("gender"),
                        "enumeration_date": provider.get("basic", {}).get("enumeration_date"),
                        "last_updated": provider.get("basic", {}).get("last_updated"),
                        "certification_date": provider.get("basic", {}).get("certification_date"),
                        "status": provider.get("basic", {}).get("status")
                    },
                    "addresses": provider.get("addresses", []),
                    "taxonomies": provider.get("taxonomies", []),
                    "identifiers": provider.get("identifiers", []),
                    "other_names": provider.get("other_names", [])
                }
                
                return {
                    "success": True,
                    "data": details,
                    "message": "Provider details retrieved successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "No provider found with the given NPI number",
                    "message": "Provider not found"
                }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "message": "Failed to retrieve provider details"
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Network error occurred while fetching provider details"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Unexpected error occurred"
        }


def main():
    """Run the NPI MCP Server"""
    mcp.run()


if __name__ == "__main__":
    main()
