"""
Tests for FHIR MCP Server

Unit tests for the FHIR MCP Server that interfaces with Oracle Cerner's FHIR R4 APIs.
"""

import pytest
from unittest.mock import patch, Mock
import json
import sys
from fhir_server import (
    get_access_token,
    get_auth_headers,
    make_fhir_request,
    get_patient_by_id,
    search_patients_by_name,
    search_patients_by_identifier,
    search_patients_by_birthdate,
    search_patients_by_phone,
    search_patients_by_email,
    search_patients_by_address,
    get_patient_observations,
    get_patient_conditions,
    get_patient_medications,
    get_fhir_capabilities,
    FHIR_CLIENT_ID,
    FHIR_CLIENT_SECRET,
    FHIR_API_BASE_URL,
    FHIR_TENANT_ID
)


class TestFHIRServer:
    """Test cases for FHIR MCP Server functionality"""
    
    def setup_method(self):
        """Set up test configuration"""
        # Mock the global variables to simulate command line arguments
        import fhir_server
        fhir_server.FHIR_CLIENT_ID = "test_client_id"
        fhir_server.FHIR_CLIENT_SECRET = "test_client_secret"
        fhir_server.FHIR_API_BASE_URL = "https://fhir-test.cerner.com/r4"
        fhir_server.FHIR_TENANT_ID = "test-tenant-id"
        fhir_server.ACCESS_TOKEN = None
        fhir_server.TOKEN_EXPIRES_AT = 0
    
    def teardown_method(self):
        """Clean up test configuration"""
        import fhir_server
        fhir_server.FHIR_CLIENT_ID = None
        fhir_server.FHIR_CLIENT_SECRET = None
        fhir_server.FHIR_API_BASE_URL = "https://fhir-ehr.cerner.com/r4"
        fhir_server.FHIR_TENANT_ID = "ec2458f2-1e24-41c8-b71b-0e701af7583d"
        fhir_server.ACCESS_TOKEN = None
        fhir_server.TOKEN_EXPIRES_AT = 0
    
    @patch('fhir_server.get_access_token')
    def test_get_auth_headers(self, mock_get_token):
        """Test authentication header generation"""
        mock_get_token.return_value = "test_access_token"
        headers = get_auth_headers()
        
        assert "Authorization" in headers
        assert "Bearer" in headers["Authorization"]
        assert headers["Authorization"] == "Bearer test_access_token"
        assert "Accept" in headers
        assert "Content-Type" in headers
        assert headers["Accept"] == "application/fhir+json"
        assert headers["Content-Type"] == "application/fhir+json"
    
    def test_get_auth_headers_missing_credentials(self):
        """Test authentication header generation with missing credentials"""
        import fhir_server
        fhir_server.FHIR_CLIENT_ID = None
        
        with pytest.raises(ValueError, match="FHIR client ID and client secret must be provided via command line arguments"):
            get_access_token()
    
    @patch('fhir_server.requests.get')
    def test_make_fhir_request_success(self, mock_get):
        """Test successful FHIR API request"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"resourceType": "Patient", "id": "123"}
        mock_get.return_value = mock_response
        
        result = make_fhir_request("Patient/123")
        
        assert result["success"] is True
        assert "data" in result
        assert result["data"]["resourceType"] == "Patient"
        assert result["message"] == "FHIR data retrieved successfully"
    
    @patch('fhir_server.requests.get')
    def test_make_fhir_request_unauthorized(self, mock_get):
        """Test FHIR API request with unauthorized access"""
        # Mock unauthorized response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response
        
        result = make_fhir_request("Patient/123")
        
        assert result["success"] is False
        assert "Authentication failed" in result["error"]
        assert result["message"] == "Unauthorized access to FHIR API"
    
    @patch('fhir_server.requests.get')
    def test_make_fhir_request_not_found(self, mock_get):
        """Test FHIR API request with resource not found"""
        # Mock not found response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        
        result = make_fhir_request("Patient/999")
        
        assert result["success"] is False
        assert result["error"] == "Resource not found"
        assert result["message"] == "The requested FHIR resource was not found"
    
    @patch('fhir_server.make_fhir_request')
    def test_get_patient_by_id(self, mock_request):
        """Test getting patient by ID"""
        mock_request.return_value = {
            "success": True,
            "data": {"resourceType": "Patient", "id": "123"},
            "message": "Success"
        }
        
        result = get_patient_by_id("123")
        
        assert result["success"] is True
        mock_request.assert_called_once_with("Patient/123")
    
    @patch('fhir_server.make_fhir_request')
    def test_search_patients_by_name(self, mock_request):
        """Test searching patients by name"""
        mock_request.return_value = {
            "success": True,
            "data": {"resourceType": "Bundle", "entry": []},
            "message": "Success"
        }
        
        result = search_patients_by_name(given_name="John", family_name="Doe")
        
        assert result["success"] is True
        mock_request.assert_called_once_with("Patient", {"given": "John", "family": "Doe"})
    
    def test_search_patients_by_name_no_params(self):
        """Test searching patients by name with no parameters"""
        result = search_patients_by_name()
        
        assert result["success"] is False
        assert "At least one search parameter" in result["error"]
    
    @patch('fhir_server.make_fhir_request')
    def test_search_patients_by_identifier(self, mock_request):
        """Test searching patients by identifier"""
        mock_request.return_value = {
            "success": True,
            "data": {"resourceType": "Bundle", "entry": []},
            "message": "Success"
        }
        
        result = search_patients_by_identifier("MR", "12345")
        
        assert result["success"] is True
        mock_request.assert_called_once_with("Patient", {"identifier": "MR|12345"})
    
    @patch('fhir_server.make_fhir_request')
    def test_search_patients_by_birthdate(self, mock_request):
        """Test searching patients by birth date"""
        mock_request.return_value = {
            "success": True,
            "data": {"resourceType": "Bundle", "entry": []},
            "message": "Success"
        }
        
        result = search_patients_by_birthdate("1990-01-01")
        
        assert result["success"] is True
        mock_request.assert_called_once_with("Patient", {"birthdate": "1990-01-01"})
    
    @patch('fhir_server.make_fhir_request')
    def test_search_patients_by_phone(self, mock_request):
        """Test searching patients by phone number"""
        mock_request.return_value = {
            "success": True,
            "data": {"resourceType": "Bundle", "entry": []},
            "message": "Success"
        }
        
        result = search_patients_by_phone("555-1234")
        
        assert result["success"] is True
        mock_request.assert_called_once_with("Patient", {"phone": "555-1234"})
    
    @patch('fhir_server.make_fhir_request')
    def test_search_patients_by_email(self, mock_request):
        """Test searching patients by email"""
        mock_request.return_value = {
            "success": True,
            "data": {"resourceType": "Bundle", "entry": []},
            "message": "Success"
        }
        
        result = search_patients_by_email("john.doe@example.com")
        
        assert result["success"] is True
        mock_request.assert_called_once_with("Patient", {"email": "john.doe@example.com"})
    
    @patch('fhir_server.make_fhir_request')
    def test_search_patients_by_address(self, mock_request):
        """Test searching patients by address"""
        mock_request.return_value = {
            "success": True,
            "data": {"resourceType": "Bundle", "entry": []},
            "message": "Success"
        }
        
        result = search_patients_by_address(postal_code="12345", city="Anytown", state="CA")
        
        assert result["success"] is True
        expected_params = {
            "address-postalcode": "12345",
            "address-city": "Anytown",
            "address-state": "CA"
        }
        mock_request.assert_called_once_with("Patient", expected_params)
    
    def test_search_patients_by_address_no_params(self):
        """Test searching patients by address with no parameters"""
        result = search_patients_by_address()
        
        assert result["success"] is False
        assert "At least one address parameter" in result["error"]
    
    @patch('fhir_server.make_fhir_request')
    def test_get_patient_observations(self, mock_request):
        """Test getting patient observations"""
        mock_request.return_value = {
            "success": True,
            "data": {"resourceType": "Bundle", "entry": []},
            "message": "Success"
        }
        
        result = get_patient_observations("123")
        
        assert result["success"] is True
        mock_request.assert_called_once_with("Observation", {"subject": "Patient/123"})
    
    @patch('fhir_server.make_fhir_request')
    def test_get_patient_conditions(self, mock_request):
        """Test getting patient conditions"""
        mock_request.return_value = {
            "success": True,
            "data": {"resourceType": "Bundle", "entry": []},
            "message": "Success"
        }
        
        result = get_patient_conditions("123")
        
        assert result["success"] is True
        mock_request.assert_called_once_with("Condition", {"patient": "Patient/123"})
    
    @patch('fhir_server.make_fhir_request')
    def test_get_patient_medications(self, mock_request):
        """Test getting patient medications"""
        mock_request.return_value = {
            "success": True,
            "data": {"resourceType": "Bundle", "entry": []},
            "message": "Success"
        }
        
        result = get_patient_medications("123")
        
        assert result["success"] is True
        mock_request.assert_called_once_with("MedicationRequest", {"patient": "Patient/123"})
    
    @patch('fhir_server.make_fhir_request')
    def test_get_fhir_capabilities(self, mock_request):
        """Test getting FHIR server capabilities"""
        mock_request.return_value = {
            "success": True,
            "data": {"resourceType": "CapabilityStatement"},
            "message": "Success"
        }
        
        result = get_fhir_capabilities()
        
        assert result["success"] is True
        mock_request.assert_called_once_with("metadata")
    
    @patch('fhir_server.make_fhir_request')
    def test_count_parameter_limits(self, mock_request):
        """Test that count parameter is properly limited"""
        mock_request.return_value = {
            "success": True,
            "data": {"resourceType": "Bundle", "entry": []},
            "message": "Success"
        }
        
        # Test that count is capped at 100
        result = search_patients_by_name(given_name="John", count=150)
        
        assert result["success"] is True
        mock_request.assert_called_once_with("Patient", {"given": "John", "_count": 100})
    
    @patch('fhir_server.requests.post')
    def test_get_access_token_success(self, mock_post):
        """Test successful access token retrieval"""
        # Mock successful token response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        mock_post.return_value = mock_response
        
        token = get_access_token()
        
        assert token == "test_access_token"
        mock_post.assert_called_once()
        
        # Verify the request was made with Basic Auth header
        call_args = mock_post.call_args
        headers = call_args[1]['headers']
        assert 'Authorization' in headers
        assert headers['Authorization'].startswith('Basic ')
        
        # Verify the request data doesn't include client credentials
        data = call_args[1]['data']
        assert 'client_id' not in data
        assert 'client_secret' not in data
        assert data['grant_type'] == 'client_credentials'
    
    @patch('fhir_server.requests.post')
    def test_get_access_token_failure(self, mock_post):
        """Test access token retrieval failure"""
        # Mock failed token response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response
        
        with pytest.raises(requests.RequestException, match="Failed to obtain access token"):
            get_access_token()
    
    @patch('fhir_server.get_access_token')
    def test_get_access_token_caching(self, mock_get_token):
        """Test that access token is cached and reused"""
        import fhir_server
        import time
        
        # Set up a valid token
        fhir_server.ACCESS_TOKEN = "cached_token"
        fhir_server.TOKEN_EXPIRES_AT = time.time() + 3600  # Valid for 1 hour
        
        mock_get_token.return_value = "new_token"
        
        # First call should use cached token
        token1 = get_access_token()
        assert token1 == "cached_token"
        
        # Second call should also use cached token
        token2 = get_access_token()
        assert token2 == "cached_token"
        
        # get_access_token should not have been called
        mock_get_token.assert_not_called()
    
    @patch('fhir_server.mcp.run')
    @patch('fhir_server.argparse.ArgumentParser.parse_args')
    def test_main_function(self, mock_parse_args, mock_mcp_run):
        """Test the main function with command line arguments"""
        from fhir_server import main
        
        # Mock command line arguments
        mock_args = Mock()
        mock_args.client_id = "test_client_id"
        mock_args.client_secret = "test_client_secret"
        mock_args.base_url = "https://fhir-test.cerner.com/r4"
        mock_args.tenant_id = "test-tenant-id"
        mock_parse_args.return_value = mock_args
        
        # Import and call main
        import fhir_server
        fhir_server.main()
        
        # Verify global variables were set
        assert fhir_server.FHIR_CLIENT_ID == "test_client_id"
        assert fhir_server.FHIR_CLIENT_SECRET == "test_client_secret"
        assert fhir_server.FHIR_API_BASE_URL == "https://fhir-test.cerner.com/r4"
        assert fhir_server.FHIR_TENANT_ID == "test-tenant-id"
        
        # Verify mcp.run was called
        mock_mcp_run.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])