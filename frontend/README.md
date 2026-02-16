# Angular Frontend

Modern Angular application for interacting with Vanna AI through a user-friendly interface.

## Features

- **Train Page**: Interface for training the Vanna AI model
  - Train with DDL (Data Definition Language)
  - Train with documentation
  - Train with SQL query examples
  - Tabbed interface for different training types
  - Real-time feedback on training operations

- **Ask Page**: Interface for asking questions
  - Natural language question input
  - Generated SQL query display
  - Query results in table format
  - Error handling and loading states

## Local Development

### Prerequisites

- Node.js 20+
- npm 10+

### Setup and Run

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm start
```

The application will be available at `http://localhost:4200`

3. Build for production:
```bash
npm run build
```

Build output will be in `dist/vanna-app/browser/`

## Configuration

Backend API URL is configured in `src/environments/`:

### Development (`environment.ts`)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080/api'
};
```

### Production (`environment.prod.ts`)
```typescript
export const environment = {
  production: true,
  apiUrl: 'http://localhost:8080/api'
};
```

## Project Structure

```
src/
├── app/
│   ├── components/
│   │   ├── ask/              # Ask question component
│   │   │   ├── ask.component.ts
│   │   │   ├── ask.component.html
│   │   │   └── ask.component.css
│   │   └── train/            # Train model component
│   │       ├── train.component.ts
│   │       ├── train.component.html
│   │       └── train.component.css
│   ├── services/
│   │   └── vanna.service.ts  # API service
│   ├── app.component.*       # Root component
│   ├── app.config.ts         # App configuration
│   └── app.routes.ts         # Routing configuration
├── environments/             # Environment configs
├── assets/                   # Static assets
├── index.html               # Main HTML file
├── main.ts                  # Application bootstrap
└── styles.css               # Global styles
```

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run unit tests
- `npm run watch` - Build and watch for changes

## Docker

Build and run with Docker:

```bash
docker build -t vanna-frontend .
docker run -p 4200:80 vanna-frontend
```

The Dockerfile uses a multi-stage build:
1. Build stage: Compiles the Angular application
2. Production stage: Serves the app with Nginx

## Usage

### Training the Model

1. Navigate to the **Train** page
2. Choose a training type:
   - **DDL**: Paste CREATE TABLE statements
   - **Documentation**: Add context about tables/columns
   - **SQL Example**: Provide question-SQL pairs
3. Submit the form
4. Wait for confirmation

### Asking Questions

1. Navigate to the **Ask** page
2. Type a natural language question
3. Click "Ask" or press Enter
4. View the generated SQL and results

## Technology Stack

- Angular 17
- TypeScript 5
- RxJS 7
- Standalone components
- HttpClient for API calls
- Nginx (for Docker deployment)
