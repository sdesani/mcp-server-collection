# NPI MCP Server

A Model Context Protocol (MCP) server that provides access to the National Plan and Provider Enumeration System (NPPES) NPI Registry API. This server allows you to search and retrieve information about healthcare providers and organizations using their National Provider Identifier (NPI) numbers.

## Overview

The NPI MCP Server integrates with the CMS NPI Registry API to provide comprehensive healthcare provider information. It supports various search methods including NPI number lookup, name-based searches, taxonomy-based searches, and organization searches.

## Features

- **NPI Number Search**: Direct lookup by 10-digit NPI number
- **Provider Name Search**: Search by first and last name with optional location filtering
- **Taxonomy Search**: Find providers by specialty/medical taxonomy
- **Organization Search**: Search for healthcare organizations and facilities
- **Detailed Provider Information**: Comprehensive provider details including addresses, taxonomies, and identifiers
- **Error Handling**: Robust error handling with informative messages
- **Location Filtering**: Optional city and state filtering for location-based searches

## Installation

### Prerequisites

- Python 3.13 or higher
- pip or uv package manager

### Dependencies

The server requires the following Python packages:
- `fastmcp>=2.12.4` - FastMCP framework for MCP server implementation
- `requests>=2.31.0` - HTTP library for API calls

### Setup

1. **Install Dependencies**:

   ```bash
   # Using pip
   pip install fastmcp requests
   
   # Using uv (recommended)
   uv add fastmcp requests
   ```

2. **Run the Server**:

   ```bash
   # Using uv (recommended)
   uv run python npi_mcp_server/npi_server.py
   
   # Or using pip after installing dependencies
   python npi_mcp_server/npi_server.py
   ```

## Available Tools

### 1. `search_npi_by_number`

Search for a provider by their exact NPI number.

**Parameters:**
- `npi_number` (str): The 10-digit NPI number to search for

**Returns:**
- Dictionary containing the provider information if found

**Example:**
```python
search_npi_by_number("1234567890")
```

### 2. `search_npi_by_name`

Search for individual providers by name with optional location filtering.

**Parameters:**
- `first_name` (str): Provider's first name
- `last_name` (str): Provider's last name
- `city` (str, optional): City name for location filtering
- `state` (str, optional): State code (2 letters) for location filtering

**Returns:**
- Dictionary containing search results with matching providers

**Example:**
```python
search_npi_by_name("John", "Smith", city="New York", state="NY")
```

### 3. `search_npi_by_taxonomy`

Search for providers by medical specialty/taxonomy with optional location filtering.

**Parameters:**
- `taxonomy_description` (str): Provider's taxonomy/specialty (e.g., "Internal Medicine", "Cardiology")
- `city` (str, optional): City name for location filtering
- `state` (str, optional): State code (2 letters) for location filtering

**Returns:**
- Dictionary containing providers matching the taxonomy criteria

**Example:**
```python
search_npi_by_taxonomy("Internal Medicine", city="Boston", state="MA")
```

### 4. `search_npi_by_organization_name`

Search for healthcare organizations and facilities by name.

**Parameters:**
- `organization_name` (str): Organization name to search for
- `city` (str, optional): City name for location filtering
- `state` (str, optional): State code (2 letters) for location filtering

**Returns:**
- Dictionary containing matching organizations

**Example:**
```python
search_npi_by_organization_name("Mayo Clinic", state="MN")
```

### 5. `get_provider_details`

Get comprehensive detailed information about a specific provider.

**Parameters:**
- `npi_number` (str): The 10-digit NPI number

**Returns:**
- Dictionary containing detailed provider information including:
  - Basic information (name, credentials, status, etc.)
  - Addresses (practice locations)
  - Taxonomies (medical specialties)
  - Identifiers (other provider IDs)
  - Other names (aliases, DBA names)

**Example:**
```python
get_provider_details("1234567890")
```

## Response Format

All tools return responses in the following format:

```python
{
    "success": bool,        # Whether the operation was successful
    "data": dict,          # The actual data (varies by tool)
    "message": str,        # Human-readable message
    "error": str           # Error message (only present if success=False)
}
```

## NPI API Information

This server interfaces with the [NPI Registry API](https://npiregistry.cms.hhs.gov/api-page) provided by the Centers for Medicare & Medicaid Services (CMS). The API provides access to the National Plan and Provider Enumeration System (NPPES) data.

### Key Features of the NPI Registry:

- **Comprehensive Coverage**: Contains information on all healthcare providers and organizations in the United States
- **Real-time Data**: Updated regularly with current provider information
- **Multiple Search Options**: Supports various search criteria including NPI numbers, names, taxonomies, and locations
- **Detailed Information**: Provides extensive provider details including addresses, specialties, and identifiers

### Data Fields Available:

- **Basic Information**: NPI number, entity type, name, credentials, gender, enumeration date
- **Addresses**: Practice locations, mailing addresses with complete address details
- **Taxonomies**: Medical specialties and provider classifications
- **Identifiers**: Other provider identification numbers (Medicare, Medicaid, etc.)
- **Other Names**: Alternative names, DBA names, and aliases

## Usage Examples

### Finding a Provider by NPI Number

```python
# Search for a specific provider
result = search_npi_by_number("1234567890")
if result["success"]:
    provider_data = result["data"]
    print(f"Found provider: {provider_data}")
```

### Searching for Cardiologists in a Specific City

```python
# Find cardiologists in New York City
result = search_npi_by_taxonomy("Cardiology", city="New York", state="NY")
if result["success"]:
    providers = result["data"]["results"]
    print(f"Found {len(providers)} cardiologists in NYC")
```

### Getting Detailed Provider Information

```python
# Get comprehensive details for a provider
result = get_provider_details("1234567890")
if result["success"]:
    details = result["data"]
    print(f"Provider: {details['basic_info']['name']}")
    print(f"Specialties: {[t['desc'] for t in details['taxonomies']]}")
    print(f"Addresses: {len(details['addresses'])} locations")
```

## Error Handling

The server includes comprehensive error handling for:

- **Network Issues**: Connection timeouts, network failures
- **API Errors**: HTTP error responses from the NPI Registry API
- **Invalid Parameters**: Missing or malformed input parameters
- **Data Processing**: JSON parsing and data extraction errors

All errors are returned in a consistent format with descriptive error messages to help with debugging and user feedback.

## Rate Limiting

The NPI Registry API does not specify rate limits, but the server implements a 10-second timeout for all API requests to prevent hanging requests. For high-volume usage, consider implementing appropriate delays between requests.

## Contributing

To contribute to this MCP server:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the mcp-server-collection and follows the same licensing terms as the parent repository.

## Support

For issues related to:
- **NPI Registry API**: Consult the [official CMS documentation](https://npiregistry.cms.hhs.gov/api-page)
- **MCP Server**: Check the FastMCP documentation and this repository's issue tracker
- **Data Questions**: Refer to the [NPPES Data Dissemination](https://npiregistry.cms.hhs.gov/about-npi) page

## Related Links

- [NPI Registry API Documentation](https://npiregistry.cms.hhs.gov/api-page)
- [NPPES Data Dissemination](https://npiregistry.cms.hhs.gov/about-npi)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
