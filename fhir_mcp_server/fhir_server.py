"""
FHIR MCP Server

A Model Context Protocol server that provides access to Oracle Cerner's FHIR R4 APIs.
This server implements FHIR R4.0.1 specification for healthcare data exchange.
"""

import json
import argparse
import time
from typing import Dict, List, Optional, Any
import requests
from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("FHIR MCP Server")

# Global configuration variables
FHIR_API_BASE_URL = "https://fhir-ehr.cerner.com/r4"
FHIR_CLIENT_ID = None
FHIR_CLIENT_SECRET = None
FHIR_TENANT_ID = "ec2458f2-1e24-41c8-b71b-0e701af7583d"

# Token management
ACCESS_TOKEN = None
TOKEN_EXPIRES_AT = 0
TOKEN_ENDPOINT = "https://authorization.cerner.com/tenants/ec2458f2-1e24-41c8-b71b-0e701af7583d/hosts/fhir-ehr.cerner.com/protocols/oauth2/profiles/smart-v1/token"


def get_access_token() -> str:
    """
    Get a valid access token, refreshing if necessary.
    Uses OAuth 2.0 client credentials flow for system-to-system authentication.
    
    Returns:
        Valid access token string
        
    Raises:
        ValueError: If client credentials are not configured
        requests.RequestException: If token request fails
    """
    global ACCESS_TOKEN, TOKEN_EXPIRES_AT
    
    if not FHIR_CLIENT_ID or not FHIR_CLIENT_SECRET:
        raise ValueError("FHIR client ID and client secret must be provided via command line arguments")
    
    # Check if current token is still valid (with 5-minute buffer)
    if ACCESS_TOKEN and time.time() < (TOKEN_EXPIRES_AT - 300):
        return ACCESS_TOKEN
    
    # Request new token using client credentials flow
    token_data = {
        "grant_type": "client_credentials",
        "scope": "system/Patient.rs system/Observation.rs system/Condition.rs system/MedicationRequest.rs"
    }
    
    # Create Basic Auth header with client credentials
    import base64
    credentials = f"{FHIR_CLIENT_ID}:{FHIR_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "Authorization": f"Basic {encoded_credentials}"
    }
    
    try:
        response = requests.post(TOKEN_ENDPOINT, data=token_data, headers=headers, timeout=60)
        
        if response.status_code == 200:
            token_response = response.json()
            ACCESS_TOKEN = token_response["access_token"]
            expires_in = token_response.get("expires_in", 3600)  # Default to 1 hour
            TOKEN_EXPIRES_AT = time.time() + expires_in
            
            return ACCESS_TOKEN
        else:
            raise requests.RequestException(f"Token request failed: HTTP {response.status_code}: {response.text}")
            
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to obtain access token: {str(e)}")


def get_auth_headers() -> Dict[str, str]:
    """
    Get authentication headers for FHIR API requests.
    Uses OAuth 2.0 Bearer token authentication.
    """
    access_token = get_access_token()
    
    return {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/fhir+json",
        "Content-Type": "application/fhir+json"
    }


def make_fhir_request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make a request to the FHIR API with proper authentication and error handling.
    
    Args:
        endpoint: The FHIR API endpoint (e.g., "Patient", "Patient/123")
        params: Optional query parameters
        
    Returns:
        Dictionary containing the response data or error information
    """
    try:
        url = f"{FHIR_API_BASE_URL}/{FHIR_TENANT_ID}/{endpoint}"
        headers = get_auth_headers()
        
        response = requests.get(url, headers=headers, params=params, timeout=60)
        
        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json(),
                "message": "FHIR data retrieved successfully"
            }
        elif response.status_code == 401:
            return {
                "success": False,
                "error": "Authentication failed. Please check your FHIR client credentials and token.",
                "message": "Unauthorized access to FHIR API"
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "error": "Resource not found",
                "message": "The requested FHIR resource was not found"
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "message": "Failed to retrieve FHIR data"
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Network error occurred while accessing FHIR API"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Unexpected error occurred"
        }


@mcp.tool()
def get_patient_by_id(patient_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific patient by their FHIR patient ID.
    
    Args:
        patient_id: The FHIR patient ID to retrieve
        
    Returns:
        Dictionary containing the patient information
    """
    return make_fhir_request(f"Patient/{patient_id}")


@mcp.tool()
def search_patients_by_name(
    given_name: Optional[str] = None,
    family_name: Optional[str] = None,
    count: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for patients by name using FHIR search parameters.
    
    Args:
        given_name: Patient's given (first) name
        family_name: Patient's family (last) name
        count: Maximum number of results to return (default: 10, max: 100)
        
    Returns:
        Dictionary containing the search results
    """
    params = {}
    
    if given_name:
        params["given"] = given_name
    if family_name:
        params["family"] = family_name
    if count:
        params["_count"] = min(count, 100)  # Cap at 100 as per FHIR spec
    
    # At least one search parameter is required
    if not params:
        return {
            "success": False,
            "error": "At least one search parameter (given_name or family_name) must be provided",
            "message": "Invalid search parameters"
        }
    
    return make_fhir_request("Patient", params)


@mcp.tool()
def search_patients_by_identifier(
    identifier_type: str,
    identifier_value: str,
    count: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for patients by identifier (e.g., MRN, SSN).
    
    Args:
        identifier_type: Type of identifier (e.g., "MR", "SS")
        identifier_value: The identifier value to search for
        count: Maximum number of results to return (default: 10, max: 100)
        
    Returns:
        Dictionary containing the search results
    """
    params = {
        "identifier": f"{identifier_type}|{identifier_value}"
    }
    
    if count:
        params["_count"] = min(count, 100)
    
    return make_fhir_request("Patient", params)


@mcp.tool()
def search_patients_by_birthdate(
    birthdate: str,
    count: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for patients by birth date.
    
    Args:
        birthdate: Patient's birth date in YYYY-MM-DD format
        count: Maximum number of results to return (default: 10, max: 100)
        
    Returns:
        Dictionary containing the search results
    """
    params = {
        "birthdate": birthdate
    }
    
    if count:
        params["_count"] = min(count, 100)
    
    return make_fhir_request("Patient", params)


@mcp.tool()
def search_patients_by_phone(
    phone_number: str,
    count: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for patients by phone number.
    
    Args:
        phone_number: Patient's phone number
        count: Maximum number of results to return (default: 10, max: 100)
        
    Returns:
        Dictionary containing the search results
    """
    params = {
        "phone": phone_number
    }
    
    if count:
        params["_count"] = min(count, 100)
    
    return make_fhir_request("Patient", params)


@mcp.tool()
def search_patients_by_email(
    email: str,
    count: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for patients by email address.
    
    Args:
        email: Patient's email address
        count: Maximum number of results to return (default: 10, max: 100)
        
    Returns:
        Dictionary containing the search results
    """
    params = {
        "email": email
    }
    
    if count:
        params["_count"] = min(count, 100)
    
    return make_fhir_request("Patient", params)


@mcp.tool()
def search_patients_by_address(
    postal_code: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    count: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for patients by address components.
    
    Args:
        postal_code: Patient's postal/ZIP code
        city: Patient's city
        state: Patient's state
        count: Maximum number of results to return (default: 10, max: 100)
        
    Returns:
        Dictionary containing the search results
    """
    params = {}
    
    if postal_code:
        params["address-postalcode"] = postal_code
    if city:
        params["address-city"] = city
    if state:
        params["address-state"] = state
    
    if count:
        params["_count"] = min(count, 100)
    
    # At least one address parameter is required
    if not params:
        return {
            "success": False,
            "error": "At least one address parameter (postal_code, city, or state) must be provided",
            "message": "Invalid search parameters"
        }
    
    return make_fhir_request("Patient", params)


@mcp.tool()
def get_patient_observations(patient_id: str, count: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieve observations for a specific patient.
    
    Args:
        patient_id: The FHIR patient ID
        count: Maximum number of results to return (default: 10, max: 100)
        
    Returns:
        Dictionary containing the patient's observations
    """
    params = {
        "subject": f"Patient/{patient_id}"
    }
    
    if count:
        params["_count"] = min(count, 100)
    
    return make_fhir_request("Observation", params)


@mcp.tool()
def get_patient_conditions(patient_id: str, count: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieve conditions for a specific patient.
    
    Args:
        patient_id: The FHIR patient ID
        count: Maximum number of results to return (default: 10, max: 100)
        
    Returns:
        Dictionary containing the patient's conditions
    """
    params = {
        "patient": f"Patient/{patient_id}"
    }
    
    if count:
        params["_count"] = min(count, 100)
    
    return make_fhir_request("Condition", params)


@mcp.tool()
def get_patient_medications(patient_id: str, count: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieve medication requests for a specific patient.
    
    Args:
        patient_id: The FHIR patient ID
        count: Maximum number of results to return (default: 10, max: 100)
        
    Returns:
        Dictionary containing the patient's medication requests
    """
    params = {
        "patient": f"Patient/{patient_id}"
    }
    
    if count:
        params["_count"] = min(count, 100)
    
    return make_fhir_request("MedicationRequest", params)


@mcp.tool()
def get_fhir_capabilities() -> Dict[str, Any]:
    """
    Retrieve the FHIR server's capability statement (metadata).
    This provides information about the server's capabilities and supported resources.
    
    Returns:
        Dictionary containing the FHIR server capabilities
    """
    return make_fhir_request("metadata")


def main():
    """Run the FHIR MCP Server"""
    global FHIR_API_BASE_URL, FHIR_CLIENT_ID, FHIR_CLIENT_SECRET, FHIR_TENANT_ID
    
    parser = argparse.ArgumentParser(description="FHIR MCP Server for Oracle Cerner FHIR R4 APIs")
    parser.add_argument("--client-id", required=True, help="FHIR API client ID")
    parser.add_argument("--client-secret", required=True, help="FHIR API client secret")
    parser.add_argument("--base-url", default="https://fhir-ehr.cerner.com/r4", 
                       help="FHIR API base URL (default: https://fhir-ehr.cerner.com/r4)")
    parser.add_argument("--tenant-id", default="ec2458f2-1e24-41c8-b71b-0e701af7583d",
                       help="FHIR tenant ID (default: ec2458f2-1e24-41c8-b71b-0e701af7583d)")
    
    args = parser.parse_args()
    
    # Set global configuration
    FHIR_CLIENT_ID = args.client_id
    FHIR_CLIENT_SECRET = args.client_secret
    FHIR_API_BASE_URL = args.base_url
    FHIR_TENANT_ID = args.tenant_id
    
    mcp.run()


if __name__ == "__main__":
    main()