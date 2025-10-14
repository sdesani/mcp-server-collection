# mcp-server-collection

A curated collection of Model Context Protocol (MCP) server tools for personal projects and development workflows.

## Available MCP Servers

This repository contains a collection of specialized MCP servers, each designed to interface with different external APIs and services:

### [NPI MCP Server](npi_mcp_server/README.md)
A comprehensive MCP server that provides access to the National Plan and Provider Enumeration System (NPPES) NPI Registry API. This server allows you to search and retrieve information about healthcare providers and organizations using their National Provider Identifier (NPI) numbers.

**Features:**
- Search providers by NPI number
- Name-based provider searches with location filtering
- Taxonomy/specialty-based searches
- Organization and facility searches
- Comprehensive provider detail retrieval

**Use Cases:**
- Healthcare provider verification
- Medical practice research
- Healthcare network analysis
- Provider credentialing workflows

### [FHIR MCP Server](fhir_mcp_server/README.md)
A Model Context Protocol server that provides access to Oracle Cerner's FHIR R4 APIs. This server implements the FHIR R4.0.1 specification for healthcare data exchange, enabling seamless integration with healthcare systems.

**Features:**
- Patient management and search capabilities
- Clinical data access (observations, conditions, medications)
- FHIR R4.0.1 compliant implementation
- Oracle Cerner API integration
- Comprehensive error handling and authentication

**Use Cases:**
- Electronic Health Record (EHR) integration
- Clinical data retrieval and analysis
- Patient information management
- Healthcare application development

## Getting Started

Each MCP server in this collection is self-contained and can be run independently. Refer to the individual server README files for specific installation and usage instructions.

### Prerequisites

- Python 3.13 or higher
- pip or uv package manager

### Quick Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd mcp-server-collection
   ```

2. Install dependencies:
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

3. Run a specific server:
   ```bash
   # Example: Run the NPI MCP Server
   uv run python npi_mcp_server/npi_server.py
   ```

## Contributing

We welcome contributions to expand this collection of MCP servers. Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to:

- Add new MCP servers
- Improve existing servers
- Report issues and bugs
- Suggest new features

## License

This project is licensed under the terms specified in the repository's license file.

## Support

For questions, issues, or contributions related to this MCP server collection, please:

1. Check the individual server documentation
2. Review existing issues in the repository
3. Create a new issue with detailed information about your request
