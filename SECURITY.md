# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

### How to Report

1. **Email**: Send details to the repository owner via GitHub (see profile)
2. **Private Security Advisory**: Use GitHub's private vulnerability reporting feature
3. **Include**:
   - Type of vulnerability
   - Full paths of affected source files
   - Location of affected code (tag/branch/commit)
   - Step-by-step instructions to reproduce
   - Proof-of-concept or exploit code (if possible)
   - Impact of the issue

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Regular Updates**: Every week until resolved
- **Fix Timeline**: Critical issues within 30 days, others within 90 days
- **Disclosure**: Coordinated disclosure after patch is available

### Safe Harbor

We support responsible disclosure and will not pursue legal action against security researchers who:
- Make a good faith effort to avoid privacy violations and data destruction
- Report vulnerabilities responsibly and give reasonable time for fixes
- Do not exploit vulnerabilities beyond what is necessary to demonstrate the issue

## Security Considerations for Users

### Critical Security Requirements

⚠️ **IMPORTANT**: MetasploitMCP provides access to powerful penetration testing tools. Follow these security requirements:

### 1. Authorization & Legal Compliance

- ✅ **ONLY use on systems you own or have explicit written authorization to test**
- ✅ Obtain proper legal documentation before testing
- ✅ Comply with all applicable laws and regulations
- ❌ **NEVER** use against unauthorized systems (illegal and unethical)

### 2. Network Isolation

**Required Security Measures**:

```
┌─────────────────────────────────────┐
│   TESTING NETWORK (ISOLATED)       │
│  ┌──────────┐      ┌──────────┐   │
│  │ MCP      │──────│Metasploit│   │
│  │ Server   │      │ Server   │   │
│  └──────────┘      └──────────┘   │
│         │                          │
│  ┌──────────────┐                 │
│  │Target Systems│                 │
│  └──────────────┘                 │
└─────────────────────────────────────┘
        │ FIREWALL │
┌─────────────────────────────────────┐
│   PRODUCTION NETWORK                │
└─────────────────────────────────────┘
```

- ✅ Use separate isolated network for testing
- ✅ VLANs or physical network separation
- ✅ Firewall rules preventing access to production
- ❌ **NEVER** connect testing tools to production networks

### 3. Authentication & Access Control

**MSF RPC Security**:

```bash
# GOOD: Strong, random password
MSF_PASSWORD=$(openssl rand -base64 32)

# GOOD: SSL enabled
MSF_SSL=true

# GOOD: Bind to localhost only
msfrpcd -P $MSF_PASSWORD -S -a 127.0.0.1

# BAD: Weak password (DO NOT USE)
MSF_PASSWORD="password123"

# BAD: No SSL (DO NOT USE in production)
MSF_SSL=false

# BAD: Exposed to all interfaces (DO NOT USE)
msfrpcd -P $MSF_PASSWORD -a 0.0.0.0
```

**Best Practices**:
- ✅ Use 32+ character random passwords
- ✅ Enable SSL/TLS for all connections
- ✅ Rotate credentials regularly (weekly/monthly)
- ✅ Use SSH tunneling for remote access
- ✅ Implement IP whitelisting
- ❌ Never commit credentials to version control
- ❌ Never share passwords via unencrypted channels

### 4. API Security

**For Public Deployments**:

```python
# Required: Add authentication
API_KEY = os.getenv("MCP_API_KEY")

# Required: Rate limiting
@limiter.limit("10/minute")
async def endpoint():
    pass

# Required: IP whitelisting
ALLOWED_IPS = ["192.168.1.0/24"]

# Required: HTTPS only
if not request.url.scheme == "https":
    raise HTTPException(403)
```

**Configuration Checklist**:
- ✅ API key authentication
- ✅ Rate limiting (10 requests/minute recommended)
- ✅ IP whitelisting
- ✅ HTTPS/TLS encryption
- ✅ Audit logging
- ✅ Request validation
- ❌ Never expose without authentication

### 5. Environment Variables & Secrets

**Secure Storage**:

```bash
# GOOD: Use .env.local (in .gitignore)
echo "MSF_PASSWORD=..." > .env.local
chmod 600 .env.local

# GOOD: Use secret management services
# - AWS Secrets Manager
# - Azure Key Vault
# - HashiCorp Vault

# BAD: Hardcoded in code (NEVER DO THIS)
MSF_PASSWORD = "mypassword"

# BAD: In public repository
git add .env.local  # DON'T!
```

**Secret Management**:
- ✅ Use `.env.local` (never commit)
- ✅ Use secret management services in production
- ✅ Rotate secrets regularly
- ✅ Audit secret access
- ❌ Never hardcode credentials
- ❌ Never commit secrets to git

### 6. Payload Handling

**Safe Practices**:

```bash
# GOOD: Restricted directory with limited access
PAYLOAD_SAVE_DIR="/opt/payloads"
chmod 700 /opt/payloads

# GOOD: Scan generated payloads
clamscan /opt/payloads/*

# GOOD: Delete after use
rm -f /opt/payloads/*.exe

# BAD: World-writable directory
chmod 777 /opt/payloads  # DON'T!

# BAD: Storing in shared/public locations
PAYLOAD_SAVE_DIR="/tmp"  # DON'T!
```

**Guidelines**:
- ✅ Store in restricted directories (chmod 700)
- ✅ Delete payloads after use
- ✅ Never share generated payloads
- ✅ Scan with antivirus before moving
- ❌ Never store in public/shared folders
- ❌ Never upload to public services

### 7. Session Management

**Safe Operations**:

```python
# GOOD: Always terminate sessions when done
terminate_session(session_id)

# GOOD: Monitor active sessions
list_active_sessions()

# GOOD: Limit session lifetime
MAX_SESSION_AGE = 3600  # 1 hour

# BAD: Leaving sessions open indefinitely
# (increases detection risk)
```

**Best Practices**:
- ✅ Terminate sessions immediately after use
- ✅ Monitor session activity
- ✅ Set session timeouts
- ✅ Document all session actions
- ❌ Never leave sessions idle
- ❌ Never share session access

### 8. Logging & Auditing

**Required Logging**:

```python
import logging

# Log all tool executions
logger.info(f"Tool executed: {tool_name} by {user_id}")

# Log authentication attempts
logger.warning(f"Failed auth from {ip_address}")

# Log payload generation
logger.info(f"Payload generated: {payload_type}")

# Log session creation/termination
logger.info(f"Session {session_id} created/terminated")
```

**Audit Requirements**:
- ✅ Log all tool executions
- ✅ Log authentication events
- ✅ Log payload generation
- ✅ Log session activities
- ✅ Review logs regularly
- ✅ Retain logs for compliance period

### 9. Update & Patch Management

**Stay Current**:

```bash
# Update Metasploit Framework
msfupdate

# Update MetasploitMCP
cd /path/to/MetasploitMCP
git pull
pip install -r requirements.txt --upgrade

# Update OS packages
sudo apt update && sudo apt upgrade

# Check for security advisories
```

**Update Schedule**:
- ✅ Weekly: Check for updates
- ✅ Monthly: Apply non-breaking updates
- ✅ Immediately: Apply critical security patches
- ✅ Subscribe to security advisories

### 10. Deployment Security

**Production Checklist**:

- [ ] SSL/TLS enabled for all connections
- [ ] Strong authentication implemented
- [ ] Rate limiting configured
- [ ] IP whitelisting active
- [ ] Audit logging enabled
- [ ] Network isolation verified
- [ ] Firewall rules configured
- [ ] Regular backups scheduled
- [ ] Incident response plan documented
- [ ] Security monitoring active

## Vulnerability Classes

### High Severity

- Remote code execution
- Authentication bypass
- Privilege escalation
- SQL injection
- Credential exposure

### Medium Severity

- Cross-site scripting (XSS)
- Cross-site request forgery (CSRF)
- Information disclosure
- Denial of service
- Session hijacking

### Low Severity

- Information leakage
- Rate limit bypass
- Logging issues

## Security Features

### Current Implementations

✅ **SSL/TLS Support**: MSF_SSL option for encrypted connections  
✅ **Environment-based Configuration**: Secrets in .env.local  
✅ **Input Validation**: Sanitization of user inputs  
✅ **Error Handling**: No sensitive data in error messages  
✅ **Isolated Execution**: Separate network recommended  

### Planned Security Features

🔄 **API Key Authentication**: In development  
🔄 **Rate Limiting**: Planned for next release  
🔄 **IP Whitelisting**: Planned for next release  
🔄 **Audit Logging**: Enhanced logging planned  
🔄 **RBAC**: Role-based access control planned  

## Security Testing

### Testing Requirements

All security-related changes must include:
- [ ] Unit tests for security features
- [ ] Integration tests for authentication
- [ ] Penetration testing results
- [ ] Security review approval

### Test Coverage

```bash
# Run security-focused tests
python run_tests.py --security

# Check for common vulnerabilities
bandit -r MetasploitMCP.py

# Check dependencies for CVEs
safety check -r requirements.txt
```

## Compliance & Legal

### Authorized Use Only

This software is designed for:
- ✅ Authorized penetration testing
- ✅ Security research (authorized)
- ✅ Vulnerability assessment (authorized)
- ✅ Educational purposes (controlled environments)

### Prohibited Uses

❌ Unauthorized access to computer systems  
❌ Malicious hacking or cracking  
❌ Deployment of malware  
❌ Any illegal activities  

### User Responsibility

By using MetasploitMCP, you agree to:
1. Use only on authorized systems
2. Comply with all applicable laws
3. Obtain proper authorization
4. Follow ethical guidelines
5. Report vulnerabilities responsibly

## Resources

- **Metasploit Security**: https://docs.metasploit.com/docs/using-metasploit/advanced/security.html
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **CWE Top 25**: https://cwe.mitre.org/top25/
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework

## Contact

For security concerns, contact via:
- GitHub Security Advisories
- Repository owner's contact information
- Issue tracker (for non-sensitive issues)

---

**Remember**: Security is everyone's responsibility. Use this tool ethically and legally.

*Last Updated: October 18, 2025*
