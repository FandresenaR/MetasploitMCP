# Changelog

All notable changes to the MetasploitMCP project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive project documentation cleanup
- CHANGELOG.md for tracking project changes
- Detailed Oracle Cloud deployment considerations in README
- **MCP_INTEGRATION_GUIDE.md** - Complete guide for making MetasploitMCP available to all AI projects:
  - MCP Registry submission process
  - NPM package distribution
  - Docker Hub publishing
  - Integration examples for Claude, Copilot, LangChain, AutoGPT
  - Public API deployment considerations
  - Security best practices for public deployment
  - Complete checklist and roadmap
- **FREE_HOSTING_ALTERNATIVES.md** - Comprehensive guide to sustainable free hosting:
  - 7 free hosting platforms compared (Railway, Render, Koyeb, Oracle Cloud, Deta Space, Cyclic, Glitch)
  - Detailed setup instructions for each platform
  - Oracle Cloud + Cloudflare Tunnel guide (recommended - free forever, HTTPS, no domain needed)
  - Oracle Cloud + Nginx + Let's Encrypt guide (free with custom domain)
  - Security recommendations for public deployments
  - Cost comparison and sustainability ratings
  - Best choice recommendations for different use cases
- **FREE_HOSTING_QUICK_START.md** - Quick reference for free hosting setup:
  - Top recommendation: Oracle Cloud + Cloudflare Tunnel
  - Comparison table of all free options
  - Step-by-step setup for Oracle Cloud with systemd service
  - Backup options (Railway, Render, Koyeb)
  - Security reminder and action items checklist
- **mcp.json** - MCP manifest file for registry submission
- **SECURITY.md** - Comprehensive security policy:
  - Authorization and legal compliance requirements
  - Network isolation guidelines
  - Authentication best practices
  - API security recommendations
  - Payload handling procedures
  - Session management guidelines
  - Audit logging requirements
  - Vulnerability reporting process
- **QUICK_START_CONFIG.md** - Ready-to-use configuration examples:
  - Claude Desktop configs (Windows/macOS/Linux)
  - VS Code MCP extension setup
  - Remote server configurations
  - Public API connection examples
  - Step-by-step installation guide
- **BEGINNER_GUIDE.md** - Complete beginner-friendly guide covering:
  - All project functionality explained simply
  - Connected systems and architecture diagrams
  - 13 MCP tools with examples
  - Data flow explanations
  - Common workflows and use cases
  - Troubleshooting guide
  - Step-by-step getting started guide
- **TOOLS.md** - Complete reference guide for all 13 MCP tools:
  - Detailed documentation for each tool with parameters and examples
  - Natural language usage examples for AI assistants
  - Complete usage workflows (4 full examples)
  - Security best practices and operational guidelines
  - Comprehensive troubleshooting guide with diagnostic commands
  - Quick reference tables and categorized tool listing
- **SETUP_VERIFICATION.md** - Production deployment verification report:
  - Complete configuration summary (remote server, msfrpcd, MCP server)
  - Detailed verification tests with actual results
  - Usage examples with real commands
  - Maintenance procedures and monitoring commands
  - Security notes and troubleshooting guide
- **manage-services.sh** - Service management automation script:
  - Check status of msfrpcd and MetasploitMCP services
  - Start/stop/restart operations for both services
  - Network connectivity testing
  - Quick health checks and diagnostics
  - SSH integration for remote msfrpcd management
- SSH configuration improvements:
  - Added "metasploit-mcp" alias to ~/.ssh/config
  - Simplified remote server access with oracle_metasploit_key

### Changed
- Updated README.md with Fly.io deployment information
- Consolidated deployment documentation
- Improved README structure and clarity
- Added beginner's guide reference in README
- Fixed .env.local SSL configuration (MSF_SSL: false → true)
- Enhanced manage-services.sh to properly detect msfrpcd process (using pgrep -f)

### Fixed
- msfrpcd SSL configuration mismatch (server uses SSL by default)
- Service detection in manage-services.sh (Ruby process name vs msfrpcd)
- Virtual environment setup for Kali Linux (externally-managed Python)
- Password mismatch between .env.local and running msfrpcd daemon

### Removed
- Redundant temporary documentation files (RESUME_COMPLET.md, DEPLOYMENT_SUCCESS.md, DEPLOYMENT_INFO.md, MSFRPCD_SETUP_COMPLETE.md)

### Deployment
- **Remote Metasploit Server**: Oracle Cloud Ubuntu 22.04 (168.110.55.210)
- **msfrpcd Status**: Running on port 55553 with SSL (PID: 264782)
- **MetasploitMCP Server**: Running on port 8085 (PID: 50417)
- **Available Modules**: 2,565 exploits, 1,675 payloads
- **Framework Version**: Metasploit 6.4.95-dev, API v1.0

## [1.0.0] - 2025-10-04

### Added
- Initial release of MetasploitMCP server
- Model Context Protocol (MCP) integration for Metasploit Framework
- HTTP/SSE and STDIO transport modes
- OpenRouter AI integration for exploit analysis
- Comprehensive test suite with pytest
- Docker support with optimized Dockerfile
- Fly.io deployment configuration
- Mock mode for testing without Metasploit
- Automated msfrpcd management scripts
- Makefile for common operations

### Core Features
- **Module Information**: list_exploits, list_payloads
- **Exploitation**: run_exploit, run_auxiliary_module, run_post_module
- **Payload Generation**: generate_payload with configurable save directory
- **Session Management**: list_active_sessions, send_session_command, terminate_session
- **Handler Management**: list_listeners, start_listener, stop_job
- **AI-Powered Tools**: analyze_exploit_with_ai, generate_metasploit_commands_with_ai, analyze_vulnerability_with_ai

### Security
- Secure password generation using OpenSSL
- Environment-based configuration with .env.local
- Secrets management for cloud deployment
- SSL/TLS support for RPC connections

### Documentation
- Comprehensive README with usage examples
- Deployment guide for Fly.io
- msfrpcd management documentation
- Testing documentation with coverage reporting
- API documentation via Swagger UI

### Testing
- Unit tests for core functionality
- Integration tests with mocked Metasploit backend
- Options parsing tests
- Helper function tests
- Coverage reporting with HTML output
- CI/CD integration support

---

## Version History

### Versioning Strategy
- **Major version**: Breaking changes or significant architectural updates
- **Minor version**: New features, backwards-compatible
- **Patch version**: Bug fixes and minor improvements

### Deployment Information
- **Live Instance**: https://metasploitmcp.onrender.com/
- **API Documentation**: https://metasploitmcp.onrender.com/docs
- **Repository**: https://github.com/FandresenaR/MetasploitMCP

[Unreleased]: https://github.com/FandresenaR/MetasploitMCP/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/FandresenaR/MetasploitMCP/releases/tag/v1.0.0
