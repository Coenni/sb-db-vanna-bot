# Security Policy

## Known Vulnerabilities and Mitigations

### Vanna AI Library (v0.5.5)

**Status**: Known vulnerability, no patch available  
**Severity**: High  
**CVE/Advisory**: Prompt injection leading to remote code execution

#### Description
The Vanna AI library (versions <= 0.6.2) has known vulnerabilities related to prompt injection that could lead to remote code execution. This is an inherent risk when using LLM-based SQL generation tools.

#### Why We Can't Upgrade
- Vanna 0.7+ introduces API breaking changes that are incompatible with the current codebase
- Vanna 2.0+ is a complete rewrite with a different architecture (agent framework vs SQL generation)
- Upgrading would require significant application refactoring

#### Mitigations
To minimize risk when using this application:

1. **Input Validation**: Never expose the Vanna AI service directly to untrusted users
2. **Authentication**: Always implement proper authentication and authorization
3. **Network Isolation**: Run the vanna-service in an isolated network environment
4. **Monitoring**: Monitor and log all queries sent to the Vanna AI service
5. **Database Permissions**: Use read-only database credentials when possible
6. **Review Generated SQL**: Always review generated SQL queries before execution in production

#### Recommended Actions
- Use this application only in controlled, trusted environments
- Do not expose the API endpoints to the public internet without proper security controls
- Consider implementing additional SQL query validation and sanitization
- Regularly review the Vanna AI project for security updates

### Security Updates Applied

#### Angular Upgraded (v17.3.12 → v19.2.18)
**Status**: ✅ Fixed  
**Previous Vulnerabilities**:
- XSRF Token Leakage via Protocol-Relative URLs (versions < 19.2.16)
- XSS Vulnerability via Unsanitized SVG Script Attributes (versions <= 18.2.14)
- Stored XSS via SVG Animation, SVG URL and MathML Attributes (versions <= 18.2.14)

**Resolution**: Upgraded all @angular/* packages to v19.2.18 which includes all security patches

**Dependencies Updated**:
- @angular/animations, @angular/common, @angular/compiler, @angular/core
- @angular/forms, @angular/platform-browser, @angular/platform-browser-dynamic, @angular/router
- @angular/cli, @angular-devkit/build-angular, @angular/compiler-cli
- zone.js (0.14.3 → 0.15.0) and TypeScript (5.4.2 → 5.7.0) for compatibility

#### Gunicorn Upgraded (v21.2.0 → v25.1.0)
**Status**: ✅ Fixed  
**Previous Vulnerabilities**:
- HTTP Request/Response Smuggling (CVE affecting < 22.0.0)
- Request smuggling leading to endpoint restriction bypass (< 22.0.0)

**Resolution**: Upgraded to gunicorn >= 22.0.0 (currently v25.1.0)

## Reporting Security Issues

If you discover a security vulnerability in this project, please report it by:

1. **Do NOT** create a public GitHub issue
2. Email the repository maintainers directly
3. Provide detailed information about the vulnerability
4. Allow reasonable time for a fix before public disclosure

## Security Best Practices

When deploying this application:

1. **Environment Variables**: Store all API keys and credentials in environment variables, never in code
2. **HTTPS**: Always use HTTPS in production
3. **Database Access**: Use principle of least privilege for database accounts
4. **Updates**: Regularly check for updates to dependencies
5. **Logging**: Enable comprehensive logging for security auditing
6. **Backups**: Maintain regular backups of data

## Version Support

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| < 1.0   | :x:                |

## Acknowledgments

We appreciate the security research community's efforts in identifying vulnerabilities in open-source projects.
