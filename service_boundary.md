# Service Boundary Diagram

## External Dependencies
- **AI Vision API**: External AI service for image processing
- **Database**: PostgreSQL for storing analysis results
- **Object Storage**: S3-compatible storage for images

## Internal Components
- **API Gateway**: FastAPI application
- **Authentication Service**: JWT token validation
- **Image Processing Service**: Core AI logic
- **Logging Service**: Structured logging

## Data Flow
```
Client -> API Gateway -> Auth Service -> Image Processing -> AI API -> Response
```

## API Boundaries
- **Public Endpoints**: /health
- **Protected Endpoints**: /vision/* (requires authentication)
- **Internal Services**: Communication via REST APIs
