# Contributing to Vanna AI Integration Application

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for frontend development)
- Java 17+ (for backend development)
- Python 3.11+ (for Vanna service development)
- Maven 3.6+ (for backend development)
- Git

### Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sb-db-vanna-bot.git
   cd sb-db-vanna-bot
   ```

3. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Project Structure

The project consists of three main components:

- `frontend/` - Angular application
- `backend/` - Spring Boot REST API
- `vanna-service/` - Python Vanna AI microservice

Each component has its own README with specific development instructions.

## Development Workflow

### Running Services Locally

#### Full Stack with Docker
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
docker compose up
```

#### Individual Services

**Frontend:**
```bash
cd frontend
npm install
npm start
```

**Backend:**
```bash
cd backend
mvn spring-boot:run
```

**Vanna Service:**
```bash
cd vanna-service
pip install -r requirements.txt
python app.py
```

## Code Standards

### General
- Write clear, self-documenting code
- Add comments for complex logic
- Keep functions small and focused
- Follow the existing code style

### Frontend (Angular)
- Use TypeScript strict mode
- Follow Angular style guide
- Use reactive programming patterns with RxJS
- Create reusable components

### Backend (Spring Boot)
- Follow Java naming conventions
- Use constructor injection for dependencies
- Add appropriate logging
- Handle exceptions properly

### Vanna Service (Python)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to functions
- Handle errors gracefully

## Testing

### Frontend
```bash
cd frontend
npm test
```

### Backend
```bash
cd backend
mvn test
```

### Integration Testing
Use the docker-compose setup to test end-to-end functionality.

## Commit Guidelines

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Keep commits focused on a single change
- Reference issues when applicable

Example:
```
Add user authentication to Ask page

- Implement JWT token validation
- Add login form component
- Update API service for auth headers

Fixes #123
```

## Pull Request Process

1. Update documentation if needed
2. Ensure all tests pass
3. Update the README.md if you add features
4. Create a pull request with a clear description
5. Link related issues
6. Wait for review and address feedback

## Security

- Never commit sensitive data (API keys, passwords)
- Use environment variables for configuration
- Report security vulnerabilities privately
- Follow security best practices

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on collaboration

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Documentation improvements
- General questions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
