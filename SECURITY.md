# Security Considerations

## Overview

This document outlines security considerations for the Vanna AI Integration Application.

## Known Vulnerabilities and Mitigations

### 1. Vanna AI Prompt Injection (CVE-2024-XXXXX)

**Status**: No patched version available as of latest update

**Vulnerability**: Vanna library versions <= 0.6.2 are vulnerable to remote code execution via prompt injection attacks.

**Risk Level**: HIGH

**Mitigations Implemented**:

1. **Input Validation**: 
   - Limit question length to prevent excessively long prompts
   - Sanitize user input before passing to Vanna
   - Block dangerous SQL keywords in training data

2. **Least Privilege**:
   - Database user has read-only permissions (recommended)
   - Service runs in isolated Docker container
   - No shell access from Vanna service

3. **Network Isolation**:
   - Vanna service only accessible from backend
   - Not exposed to public internet directly

4. **Monitoring**:
   - Log all queries and training data
   - Monitor for suspicious patterns

**Recommended Additional Mitigations**:

```python
# Add to vanna-service/app.py before processing

BLOCKED_PATTERNS = [
    r'DROP\s+TABLE',
    r'DELETE\s+FROM',
    r'UPDATE\s+.*\s+SET',
    r'INSERT\s+INTO',
    r'EXEC',
    r'EXECUTE',
    r'xp_cmdshell',
    r'--',  # SQL comments
]

def sanitize_input(text):
    """Sanitize user input to prevent injection attacks."""
    import re
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            raise ValueError("Input contains potentially dangerous content")
    return text
```

**Action Required**:
- ⚠️ Use only in trusted environments
- ⚠️ Implement additional input validation
- ⚠️ Monitor for security updates to Vanna library
- ⚠️ Consider running with read-only database user

### 2. Angular XSS Vulnerabilities (Fixed)

**Status**: FIXED by upgrading to Angular 19.2.18

**Previous Version**: Angular 17.3.12 (vulnerable)
**Current Version**: Angular 19.2.18 (patched)

**Vulnerabilities Fixed**:
- XSRF Token Leakage via Protocol-Relative URLs
- XSS via Unsanitized SVG Script Attributes  
- Stored XSS via SVG Animation, SVG URL and MathML Attributes

**Action Taken**: Upgraded all Angular packages to 19.2.18

No further action required for Angular vulnerabilities.

### 3. Gunicorn HTTP Smuggling (Fixed)

**Status**: FIXED in version 23.0.0

**Previous Version**: 21.2.0 (vulnerable)
**Current Version**: 23.0.0 (patched)

**Vulnerability**: HTTP Request/Response Smuggling

## Security Best Practices

### For Production Deployment

1. **Environment Variables**:
   - Never commit API keys or secrets
   - Use secure secret management (e.g., AWS Secrets Manager, HashiCorp Vault)
   - Rotate credentials regularly

2. **Database Security**:
   - Create a read-only database user for Vanna queries
   - Use strong passwords
   - Enable SSL/TLS for database connections
   - Implement IP whitelisting

3. **Network Security**:
   - Use HTTPS for all connections
   - Implement rate limiting
   - Use a WAF (Web Application Firewall)
   - Keep services in private network

4. **Docker Security**:
   - Don't run containers as root
   - Use minimal base images
   - Scan images for vulnerabilities
   - Keep images updated

5. **Input Validation**:
   - Validate all user inputs
   - Implement length limits
   - Sanitize special characters
   - Use parameterized queries

6. **Monitoring and Logging**:
   - Log all SQL queries
   - Monitor for unusual patterns
   - Set up alerts for suspicious activity
   - Regular security audits

### Recommended CSP Header

Add to frontend nginx.conf:
```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self' http://localhost:8080;" always;
```

### Database User Configuration

Create a read-only user for Vanna:

```sql
-- Create read-only user
CREATE USER vanna_readonly WITH PASSWORD 'strong_password_here';

-- Grant connect permission
GRANT CONNECT ON DATABASE vanna_db TO vanna_readonly;

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO vanna_readonly;

-- Grant select only on all tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO vanna_readonly;

-- Grant select on future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO vanna_readonly;
```

Update `.env`:
```env
DB_USER=vanna_readonly
DB_PASSWORD=strong_password_here
```

## Security Updates

- **Last Updated**: 2024-02-16
- **Next Review**: Check monthly for dependency updates

## Reporting Security Issues

If you discover a security vulnerability, please:
1. Do NOT open a public issue
2. Email security concerns to: [your-security-email]
3. Include detailed description and steps to reproduce
4. Allow reasonable time for patch before disclosure

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Angular Security Guide](https://angular.io/guide/security)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/latest/security/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
