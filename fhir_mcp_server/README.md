# FHIR MCP Server

A Model Context Protocol (MCP) server that provides access to Oracle Cerner's FHIR R4 APIs. This server implements the FHIR R4.0.1 specification for healthcare data exchange, enabling seamless integration with healthcare systems.

## Features

### Patient Management
- **Get Patient by ID**: Retrieve specific patient information using FHIR patient ID
- **Search by Name**: Find patients using given (first) and family (last) names
- **Search by Identifier**: Locate patients using medical record numbers (MRN), SSN, or other identifiers
- **Search by Birth Date**: Find patients by their date of birth
- **Search by Contact Info**: Search using phone numbers or email addresses
- **Search by Address**: Find patients using postal code, city, or state

### Clinical Data Access
- **Patient Observations**: Retrieve clinical observations and vital signs
- **Patient Conditions**: Access patient diagnoses and medical conditions
- **Patient Medications**: Get medication requests and prescriptions

### System Information
- **FHIR Capabilities**: Retrieve server capabilities and supported resources

## Prerequisites

- Python 3.13 or higher
- Valid Oracle Cerner FHIR API client credentials (Client ID and Client Secret)
- Access to Oracle Cerner's FHIR R4 endpoint
- Registered application in Oracle Cerner's code console

## Installation

1. Install dependencies:
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

## Usage

### Running the Server

```bash
# Run the FHIR MCP Server with required client credentials
uv run python fhir_mcp_server/fhir_server.py --client-id "your_client_id" --client-secret "your_client_secret"

# Run with custom base URL and tenant ID
uv run python fhir_mcp_server/fhir_server.py \
  --client-id "your_client_id" \
  --client-secret "your_client_secret" \
  --base-url "https://fhir-custom.cerner.com/r4" \
  --tenant-id "your-tenant-id"
```

### Available Tools

#### Patient Retrieval
```python
# Get a specific patient by ID
get_patient_by_id("patient_id_123")

# Search patients by name
search_patients_by_name(given_name="John", family_name="Doe")

# Search by identifier (e.g., MRN)
search_patients_by_identifier("MR", "12345")

# Search by birth date
search_patients_by_birthdate("1990-01-01")

# Search by phone number
search_patients_by_phone("555-1234")

# Search by email
search_patients_by_email("john.doe@example.com")

# Search by address
search_patients_by_address(postal_code="12345", city="Anytown", state="CA")
```

#### Clinical Data Access
```python
# Get patient observations
get_patient_observations("patient_id_123")

# Get patient conditions
get_patient_conditions("patient_id_123")

# Get patient medications
get_patient_medications("patient_id_123")
```

#### System Information
```python
# Get FHIR server capabilities
get_fhir_capabilities()
```

## OAuth 2.0 Setup

This server uses OAuth 2.0 client credentials flow for system-to-system authentication, following Oracle Cerner's SMART Backend Services specification.

### Application Registration

Before using this server, you must register your application with Oracle Cerner:

1. **Create a CernerCare Account**: Sign up at [code console](https://code.cerner.com/)
2. **Register Your Application**: 
   - Log in to code console
   - Register a new application with application type "System" or application privacy "Confidential"
   - Complete the registration process
3. **Obtain Credentials**: After registration, you'll receive:
   - Client ID
   - Client Secret (managed through Cerner Central system accounts)

### Token Endpoint

The server uses Oracle Cerner's OAuth 2.0 token endpoint:
```
https://authorization.cerner.com/tenants/ec2458f2-1e24-41c8-b71b-0e701af7583d/hosts/fhir-ehr.cerner.com/protocols/oauth2/profiles/smart-v1/token
```

### Scopes

The server requests the following FHIR scopes:
- `system/Patient.read` - Read access to patient resources
- `system/Observation.read` - Read access to observation resources  
- `system/Condition.read` - Read access to condition resources
- `system/MedicationRequest.read` - Read access to medication request resources

For more information about Oracle Cerner's authorization framework, see the [official documentation](https://docs.oracle.com/en/industries/health/millennium-platform-apis/fhir-authorization-framework/#requesting-authorization-on-behalf-of-a-system).

## Configuration

### Command Line Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `--client-id` | Oracle Cerner FHIR API client ID | Yes | - |
| `--client-secret` | Oracle Cerner FHIR API client secret | Yes | - |
| `--base-url` | Base URL for FHIR API | No | `https://fhir-ehr.cerner.com/r4` |
| `--tenant-id` | Tenant ID for FHIR API | No | `ec2458f2-1e24-41c8-b71b-0e701af7583d` |

### MCP Configuration

Add the FHIR MCP Server to your MCP configuration:

```json
{
  "mcpServers": {
    "fhir": {
      "command": "uv",
      "args": [
        "run", 
        "python", 
        "fhir_mcp_server/fhir_server.py",
        "--client-id", "your_client_id",
        "--client-secret", "your_client_secret"
      ]
    }
  }
}
```

For custom configurations:

```json
{
  "mcpServers": {
    "fhir": {
      "command": "uv",
      "args": [
        "run", 
        "python", 
        "fhir_mcp_server/fhir_server.py",
        "--client-id", "your_client_id",
        "--client-secret", "your_client_secret",
        "--base-url", "https://fhir-custom.cerner.com/r4",
        "--tenant-id", "your-tenant-id"
      ]
    }
  }
}
```

## FHIR R4 Compliance

This server implements the FHIR R4.0.1 specification and supports:

- **RESTful API**: All interactions use HTTP GET requests
- **JSON Format**: All data is exchanged in FHIR JSON format
- **Search Parameters**: Standard FHIR search parameters are supported
- **Pagination**: Results are paginated according to FHIR specifications
- **OAuth 2.0 Authentication**: Uses SMART Backend Services for system-to-system authentication
- **Token Management**: Automatic token refresh and caching

### Supported Resources

- **Patient**: Core patient demographic information
- **Observation**: Clinical observations and vital signs
- **Condition**: Patient diagnoses and medical conditions
- **MedicationRequest**: Medication prescriptions and requests
- **CapabilityStatement**: Server metadata and capabilities

## Error Handling

The server provides comprehensive error handling for:

- **Authentication Errors**: Invalid credentials or expired tokens
- **Resource Not Found**: Non-existent patient IDs or resources
- **Network Issues**: Connection timeouts and network failures
- **Invalid Parameters**: Missing required search parameters
- **Rate Limiting**: API rate limit exceeded

## Testing

Run the test suite to verify functionality:

```bash
# Run all tests
uv run python -m pytest fhir_mcp_server/test_fhir_server.py

# Run with verbose output
uv run python -m pytest fhir_mcp_server/test_fhir_server.py -v
```

## Security Considerations

- **OAuth 2.0**: Uses secure OAuth 2.0 client credentials flow for system-to-system authentication
- **Token Management**: Automatic token refresh and secure caching
- **HTTPS**: All API communications use HTTPS encryption
- **Client Credentials**: Pass FHIR API client credentials securely via command line arguments
- **Data Privacy**: Ensure compliance with healthcare data privacy regulations (HIPAA, etc.)
- **MCP Configuration**: Store credentials securely in your MCP configuration file
- **SMART Compliance**: Follows SMART Backend Services specification for healthcare applications

## Oracle Cerner FHIR API

This server is designed to work with Oracle Cerner's FHIR R4 implementation. For more information:

- [Oracle Cerner FHIR R4 Overview](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/r4_overview.html)
- [FHIR R4 Specification](https://hl7.org/fhir/R4/)

## Contributing

Contributions are welcome! Please see the main project's [Contributing Guidelines](../CONTRIBUTING.md) for details.

## License

This project is licensed under the same terms as the main repository.

## Support

For questions or issues related to the FHIR MCP Server:

1. Check the [FHIR R4 documentation](https://hl7.org/fhir/R4/)
2. Review Oracle Cerner's [API documentation](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/r4_overview.html)
3. Create an issue in the repository with detailed information