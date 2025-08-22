# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a BaZi (八字, Chinese Four Pillars of Destiny) calculation tool implemented in Python. The tool calculates traditional Chinese astrology information including birth charts, solar time corrections, seasonal information, and fortune periods.

## Code Architecture

1. **bazi_tool.py** - Core calculation logic
   - Contains the `BaZiCalculator` class that performs all astrological calculations
   - Handles solar time correction based on longitude
   - Converts between Gregorian and lunar calendars
   - Calculates the four pillars (year, month, day, hour)
   - Computes seasonal and fortune period information

2. **mcp_server.py** - MCP (Model Context Protocol) server
   - Exposes the BaZi calculation as an MCP tool
   - Runs an HTTP server on port 8001
   - Provides a standardized interface for other tools to access BaZi functionality

3. **query_longitude.py** - City longitude lookup
   - Provides fuzzy matching for city names
   - Returns longitude values for time correction calculations
   - Uses data from region.json

4. **region.json** - Geographic data
   - Contains city/region information with coordinates
   - Used for solar time corrections

## Common Development Tasks

### Running the Service
```bash
python mcp_server.py
```
The service will be available at http://localhost:8001/mcp

### Running with Docker
```bash
docker-compose up --build
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Testing the Service
Use the provided test_mcp_client.py script to test the MCP service:
```bash
python test_mcp_client.py
```

### Troubleshooting
1. **503 Service Unavailable Error**: This error occurs when trying to access the MCP service with a regular HTTP client. MCP services require an MCP-compatible client to connect properly.

2. **Connection Refused**: Ensure the service is running and the port 8001 is not blocked by firewall.

3. **Docker Build Issues**: If you encounter network issues during Docker build, try using a different network or proxy.

### Key Dependencies
- `sxtwl` - Chinese calendar calculations
- `mcp` - Model Context Protocol server implementation

## Project Structure
```
bazi/
├── mcp_server.py         # MCP service endpoint
├── bazi_tool.py          # Core BaZi calculation logic
├── query_longitude.py    # City longitude lookup
├── region.json           # Geographic data
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker container definition
├── docker-compose.yml    # Docker deployment configuration
└── README.md             # Project documentation
```