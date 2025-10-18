# Changelog

All notable changes to the MetasploitMCP project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive project documentation cleanup
- CHANGELOG.md for tracking project changes
- Detailed Oracle Cloud deployment considerations in README

### Changed
- Updated README.md with Fly.io deployment information
- Consolidated deployment documentation
- Improved README structure and clarity

### Removed
- Redundant temporary documentation files (RESUME_COMPLET.md, DEPLOYMENT_SUCCESS.md, DEPLOYMENT_INFO.md, MSFRPCD_SETUP_COMPLETE.md)

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
- **Live Instance**: https://metasploit-mcp.fly.dev/
- **API Documentation**: https://metasploit-mcp.fly.dev/docs
- **Repository**: https://github.com/FandresenaR/MetasploitMCP

[Unreleased]: https://github.com/FandresenaR/MetasploitMCP/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/FandresenaR/MetasploitMCP/releases/tag/v1.0.0
