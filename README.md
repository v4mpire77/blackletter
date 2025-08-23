# Blackletter Systems

*Old rules. New game.*

Blackletter Systems is a practical legal automation platform designed to streamline contract analysis, compliance checking, and legal research.

## Core Features

1. **AI Contract Review** – Upload → OCR → clause detect → risk score vs YAML playbook → redlines + summary
2. **Compliance Checklist** – Ingest ICO/FCA/EU/gov feeds → summarize → sector checklists → weekly PDF/email
3. **Research Assistant (RAG)** – Semantic search over BAILII + legislation.gov.uk → answers with paragraph-level citations

## Tech Stack

### Frontend
- Next.js 14 with TypeScript
- Tailwind CSS + shadcn/ui

### Backend
- FastAPI with Python 3.11
- NLP Libraries: Transformers, spaCy, NLTK

### Database
- PostgreSQL for structured data
- ChromaDB/Weaviate for vector storage

### Additional Tools
- AI/ML: OpenAI API, Google Gemini API, Ollama (local LLMs)
- Deployment: Render
- Automation: n8n for workflows and integrations

## Getting Started

### Prerequisites
- Windows 11 (Developer Mode ON)
- Docker Desktop
- Git
- Node.js 20+
- Python 3.11
- Tesseract OCR (`choco install tesseract`)
- Ollama (optional for local LLMs)

### Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/blackletter-systems.git
   cd blackletter-systems
   ```

2. Run the startup script:
   ```
   .\start.ps1
   ```

   This will:
   - Create a `.env` file if needed
   - Start required Docker containers
   - Set up Python virtual environment
   - Install dependencies
   - Start backend and frontend servers

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API docs: http://localhost:8000/docs
   - MinIO Console: http://localhost:9001 (admin/adminadmin)
   - n8n: http://localhost:5678 (admin/adminadmin)

## Project Structure

```
blackletter/
  src/
    backend/
      app/
        routers/       # API endpoints
        core/          # Core functionality adapters
        services/      # Business logic
        models/        # Data models
      main.py
      requirements.txt
  frontend/
    app/               # Next.js pages
    components/        # React components
    lib/               # Utility functions
  n8n/
    workflows/         # n8n automation workflows
  docs/
    PLAYBOOK_SAMPLE.yaml  # Contract review rules
  docker-compose.yml
  .env.example
```

## Documentation

- [Implementation Plan](docs/Implementation.md)
- [Project Structure](docs/project_structure.md)
- [UI/UX Design](docs/UI_UX_doc.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Copilot Instructions](docs/COPILOT_INSTRUCTIONS.md)
- [Context Engineering Workflow](docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md)

## Deployment

The application can be deployed to [Render.com](https://render.com) using the provided configuration:

1. Run the deployment script:
   ```
   # Windows
   .\deploy.ps1
   
   # Linux/macOS
   ./deploy.sh
   ```

2. Follow the prompts to log in to Render and deploy the application.

3. Once deployed, your application will be available at:
   - Frontend: `https://blackletter.onrender.com`
   - API: `https://blackletter-api.onrender.com`

For detailed deployment instructions, see [Deployment Guide](docs/DEPLOYMENT_GUIDE.md).

## License

[MIT License](LICENSE)