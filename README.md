# RAG Knowledge Base

A comprehensive Retrieval-Augmented Generation (RAG) system designed for college students to create an AI-powered study assistant. This project combines advanced document processing, vector search, and AI response generation to provide contextual, subject-specific assistance for academic learning.

## 🏗️ Architecture Overview

This project consists of two main components:

### Backend (Python FastAPI)
- **Document Processing**: Advanced PDF processing with chunking and vector embeddings
- **Vector Search**: MongoDB-based vector search engine for intelligent document retrieval
- **AI Integration**: Google Gemini AI for generating contextual responses
- **API Layer**: RESTful API with authentication and session management
- **Database**: MongoDB for document storage and PostgreSQL for user sessions

### Frontend (Next.js)
- **Chat Interface**: Subject-organized chat system with unit-specific context
- **Authentication**: Clerk-based user authentication and session management
- **Responsive Design**: Modern UI with dark/light theme support
- **Real-time Chat**: Interactive chat interface with AI responses

## ✨ Key Features

### 🎓 Academic-Focused Design
- **Subject Organization**: Pre-configured subjects (Generative AI, Edge AI, NLP, Speech Processing, Computer Vision)
- **Unit-Based Learning**: Each subject divided into 5 units for structured learning
- **Contextual AI**: AI responses tailored to specific subjects and units
- **Study Materials Integration**: Document upload and processing for course materials

### 🔧 Technical Features
- **Vector Embeddings**: Advanced document chunking and embedding for semantic search
- **Real-time Chat**: WebSocket-like experience with instant AI responses
- **Multi-database Support**: MongoDB for documents, PostgreSQL for sessions, Redis for caching
- **Scalable Architecture**: Modular design with clear separation of concerns
- **Authentication**: Secure user authentication with Clerk
- **Theme Support**: Dark/light mode with consistent styling

### 🚀 AI Capabilities
- **Document Understanding**: Intelligent parsing and processing of academic documents
- **Contextual Responses**: AI responses based on uploaded course materials
- **Subject Expertise**: Specialized knowledge for different academic subjects
- **Learning Support**: Tailored assistance for college-level coursework

## 📋 Prerequisites

- **Python**: 3.12 or higher
- **Node.js**: 18 or higher
- **MongoDB**: 4.4 or higher
- **PostgreSQL**: 12 or higher (optional)
- **Redis**: 6 or higher (optional)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Kaus1kC0des/rag-knowledge-base.git
cd rag-knowledge-base
```

### 2. Backend Setup

#### Install Dependencies
```bash
# Using uv (recommended)
pip install uv
uv sync

# Or using pip
pip install -e .
```

#### Environment Configuration
```bash
cp .env.template .env.local
```

Edit `.env.local` with your configuration:
```env
# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# MongoDB Configuration
MONGO_URL=mongodb://localhost:27017
MONGO_USER=your_mongo_user
MONGO_PASSWORD=your_mongo_password
MONGO_DB=rag_knowledge_base

# PostgreSQL Configuration (Optional)
POSTGRES_URL=postgresql://user:password@localhost:5432/dbname
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=rag_sessions

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

#### Start the Backend
```bash
cd api
python main.py
```

The API will be available at `http://localhost:8000`

### 3. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Environment Configuration
Create `frontend/.env.local`:
```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# App Configuration
NEXT_PUBLIC_APP_NAME=RAG Knowledge Base
NEXT_PUBLIC_APP_VERSION=1.0.0

# Clerk Authentication (Optional)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
```

#### Start the Frontend
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📚 API Documentation

### Core Endpoints

#### Chat Management
```http
POST /chat/message
Content-Type: application/json

{
  "message": "Explain neural networks",
  "subject": "Generative AI",
  "unit": "Unit 1",
  "chat_id": "optional_chat_id"
}
```

#### Session Management
```http
GET /chat/sessions          # Get user chat sessions
POST /chat/sessions         # Create new chat session
PUT /chat/sessions/{id}     # Update chat session
DELETE /chat/sessions/{id}  # Delete chat session
```

#### Document Processing
```http
POST /documents/upload      # Upload and process documents
GET /documents/{id}         # Get document details
GET /search                 # Search documents
```

#### Health Check
```http
GET /health                 # API health status
```

### Response Format

All API responses follow this structure:
```json
{
  "success": true,
  "data": {
    "response": "AI generated response",
    "sources": ["document1.pdf", "document2.pdf"],
    "chat_id": "unique_chat_identifier"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🏫 Supported Subjects

The system comes pre-configured with academic subjects:

### 1. **Generative AI** 🤖
- Unit 1: Fundamentals of Generative Models
- Unit 2: GANs and Variational Autoencoders
- Unit 3: Large Language Models
- Unit 4: Diffusion Models
- Unit 5: Applications and Ethics

### 2. **Edge AI** ⚡
- Unit 1: Edge Computing Fundamentals
- Unit 2: Model Optimization and Quantization
- Unit 3: Hardware Acceleration
- Unit 4: Deployment Strategies
- Unit 5: Performance Monitoring

### 3. **Statistical Natural Language Processing** 📝
- Unit 1: Text Preprocessing and Tokenization
- Unit 2: Language Models and N-grams
- Unit 3: Part-of-Speech Tagging
- Unit 4: Named Entity Recognition
- Unit 5: Sentiment Analysis

### 4. **Speech Processing** 🎤
- Unit 1: Signal Processing Fundamentals
- Unit 2: Feature Extraction
- Unit 3: Speech Recognition
- Unit 4: Speech Synthesis
- Unit 5: Speaker Recognition

### 5. **Computer Vision** 👁️
- Unit 1: Image Processing Basics
- Unit 2: Feature Detection and Matching
- Unit 3: Object Detection
- Unit 4: Image Classification
- Unit 5: Deep Learning for Vision

## 🛠️ Development Workflow

### Backend Development

#### Project Structure
```
api/
├── main.py                 # FastAPI application entry point
├── models/                 # Pydantic models and AI integrations
├── routes/                 # API route handlers
├── schemas/                # Database schemas
│   ├── mongodb/           # MongoDB document models
│   └── postgres/          # PostgreSQL table models
├── processors/            # Document processing logic
├── loaders/               # Data loading and retrieval
├── storage/               # Database connection utilities
└── utils/                 # Utility functions
```

#### Key Components

- **Document Processor**: Handles PDF parsing, chunking, and embedding generation
- **Vector Search Engine**: MongoDB-based semantic search
- **AI Response Generator**: Google Gemini integration for chat responses
- **Authentication**: User authentication and session management

#### Running Tests
```bash
cd api
python -m pytest tests/
```

#### Code Quality
```bash
# Format code
black api/
isort api/

# Type checking
mypy api/
```

### Frontend Development

#### Project Structure
```
frontend/src/
├── app/                   # Next.js app router
│   ├── chat/             # Chat interface pages
│   ├── sign-in/          # Authentication pages
│   ├── sign-up/
│   └── profile/
├── components/           # Reusable UI components
├── lib/                  # Utility libraries
└── styles/              # Global styles and themes
```

#### Key Features

- **Subject Dashboard**: Main interface for selecting subjects and units
- **Advanced Chat**: Feature-rich chat interface with context
- **Theme Support**: Dark/light mode with Tailwind CSS
- **Authentication**: Clerk integration for user management

#### Development Commands
```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Linting
npm run lint
```

#### Adding New Subjects

To add a new subject, update the subjects array in:
- `frontend/src/app/chat/page.tsx`
- `frontend/src/app/chat/advanced/page.tsx`

```typescript
const newSubject = {
  id: "quantum-computing",
  name: "Quantum Computing",
  description: "Quantum algorithms and hardware",
  icon: <Atom className="w-8 h-8" />,
  color: "indigo",
  units: [
    "Unit 1: Quantum Fundamentals",
    "Unit 2: Quantum Gates",
    "Unit 3: Quantum Algorithms",
    "Unit 4: Quantum Error Correction",
    "Unit 5: Quantum Hardware"
  ]
};
```

## 🗃️ Database Schema

### MongoDB Collections

#### Subjects
```javascript
{
  "_id": ObjectId,
  "subject_code": "CS501",
  "subject_name": "Generative AI",
  "description": "Advanced generative AI techniques",
  "created_at": ISODate,
  "updated_at": ISODate
}
```

#### Units
```javascript
{
  "_id": ObjectId,
  "unit_code": "CS501-U1",
  "unit_name": "Unit 1: Fundamentals",
  "subject_id": ObjectId,
  "description": "Basic concepts",
  "created_at": ISODate
}
```

#### Chunks
```javascript
{
  "_id": ObjectId,
  "content": "Document content chunk",
  "embedding": [0.1, 0.2, ...],
  "metadata": {
    "source_document_id": ObjectId,
    "subject_id": ObjectId,
    "unit_id": ObjectId,
    "page_number": 1,
    "chunk_index": 0
  },
  "created_at": ISODate
}
```

#### Source Documents
```javascript
{
  "_id": ObjectId,
  "filename": "lecture_notes.pdf",
  "subject_id": ObjectId,
  "unit_id": ObjectId,
  "file_path": "/uploads/documents/...",
  "processed": true,
  "chunk_count": 45,
  "uploaded_at": ISODate
}
```

### PostgreSQL Tables (Optional)

#### Chat Sessions
```sql
CREATE TABLE chat_sessions (
  id UUID PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  subject_code VARCHAR(50),
  unit_code VARCHAR(50),
  title VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Chat Messages
```sql
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES chat_sessions(id),
  content TEXT NOT NULL,
  sender VARCHAR(10) CHECK (sender IN ('user', 'ai')),
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 📱 Usage Examples

### Basic Chat Interaction

1. **Select Subject**: Choose from available subjects on the dashboard
2. **Select Unit**: Pick a specific unit within the subject
3. **Start Chatting**: Ask questions related to the subject matter
4. **Get AI Responses**: Receive contextual answers based on uploaded materials

### Document Upload and Processing

```python
# Upload a document via API
import requests

files = {'file': open('textbook_chapter1.pdf', 'rb')}
data = {
    'subject_code': 'CS501',
    'unit_code': 'CS501-U1'
}

response = requests.post(
    'http://localhost:8000/documents/upload',
    files=files,
    data=data,
    headers={'Authorization': 'Bearer your_token'}
)
```

### Advanced Search

```python
# Search for specific content
search_response = requests.post(
    'http://localhost:8000/search',
    json={
        'query': 'explain backpropagation algorithm',
        'subject_code': 'CS501',
        'unit_code': 'CS501-U2',
        'limit': 5
    }
)
```

## 🚢 Deployment

### Using Docker (Recommended)

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - MONGO_URL=mongodb://admin:password@mongodb:27017
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    depends_on:
      - mongodb

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - api

volumes:
  mongodb_data:
```

```bash
# Start all services
docker-compose up -d
```

### Manual Deployment

#### Backend Deployment
```bash
# Install dependencies
pip install -e .

# Run with Gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### Frontend Deployment
```bash
# Build the application
npm run build

# Start production server
npm start
```

### Environment Variables for Production

```env
# Production API settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# Database URLs for production
MONGO_URL=mongodb://user:pass@mongo-cluster.example.com:27017/prod_db
POSTGRES_URL=postgresql://user:pass@postgres.example.com:5432/prod_db

# AI Service API Keys
GOOGLE_API_KEY=production_google_api_key
OPENAI_API_KEY=production_openai_api_key

# Frontend settings
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=production_clerk_key
```

## 🧪 Testing

### Backend Tests
```bash
cd api
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=api --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test

# E2E tests
npm run test:e2e
```

### Integration Tests
```bash
# Test full API flow
python tests/integration/test_chat_flow.py

# Test document processing
python tests/integration/test_document_upload.py
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Install development dependencies
4. Make your changes
5. Run tests and linting
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Style
- **Python**: Follow PEP 8, use Black for formatting
- **TypeScript**: Follow the project's ESLint configuration
- **Commits**: Use conventional commit messages

### Pull Request Process
1. Ensure all tests pass
2. Update documentation if needed
3. Add tests for new features
4. Get approval from maintainers
5. Squash commits before merging

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain**: For the RAG framework and document processing
- **FastAPI**: For the high-performance API framework
- **Next.js**: For the modern React framework
- **MongoDB**: For flexible document storage
- **Google Gemini**: For AI response generation
- **Clerk**: for authentication services
- **Tailwind CSS**: For utility-first styling

## 📞 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join community discussions in GitHub Discussions
- **Email**: Contact the maintainers at [your-email@example.com]

## 🗺️ Roadmap

### Phase 1: Core Features ✅
- [x] Basic chat interface
- [x] Document upload and processing
- [x] Vector search implementation
- [x] AI response generation
- [x] User authentication

### Phase 2: Enhanced Features 🚧
- [ ] Real-time collaboration
- [ ] Advanced document formats (DOCX, HTML)
- [ ] Performance analytics and insights
- [ ] Mobile responsive improvements
- [ ] Batch document processing

### Phase 3: Advanced Features 🔮
- [ ] Voice interaction support
- [ ] Multi-language support
- [ ] Integration with learning management systems
- [ ] Advanced analytics dashboard
- [ ] API rate limiting and scaling

---

**Built with ❤️ for enhanced learning experiences**

For more detailed information about specific components, check the individual README files in the `frontend/` and `api/` directories.