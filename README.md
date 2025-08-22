# Blackletter Systems - AI Contract Review

Simple, fast contract review using AI. Upload → Extract → Summarise → Show risks.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-red.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org/)

## 📚 Documentation

- **[Architecture Guide](ARCHITECTURE.md)** - System design and component details
- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference and examples
- **[Deployment Guide](DEPLOYMENT.md)** - Local, Docker, and cloud deployment options
- **[Contributing Guide](CONTRIBUTING.md)** - Development setup and contribution guidelines
- **[Security Policy](SECURITY.md)** - Security measures and vulnerability reporting
- **[Changelog](CHANGELOG.md)** - Version history and release notes

### 🤖 AI Agent Resources

- **[Agent Rules](AGENT_RULES.md)** - Mandatory rules for all AI agents working on this repository
- **[Agent Quick Reference](AGENT_QUICK_REFERENCE.md)** - Quick start guide for AI agents
- **[Repository To-Do List](TODO.md)** - Comprehensive running to-do list and roadmap

### 🤖 AI Agent Resources

- **[Agent Rules](AGENT_RULES.md)** - Mandatory rules for all AI agents working on this repository
- **[Agent Quick Reference](AGENT_QUICK_REFERENCE.md)** - Quick start guide for AI agents
- **[Repository To-Do List](TODO.md)** - Comprehensive running to-do list and roadmap

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker (optional, for containerized deployment)
- PostgreSQL 13+ (optional, for production)
- Redis 6+ (optional, for production)

### Backend Setup

```powershell
# Start the default Ollama server (https://ollama.ai)
ollama serve

cd backend
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

To use OpenAI instead of Ollama:

```powershell
setx LLM_PROVIDER "openai"
setx OPENAI_API_KEY "<YOUR_KEY>"
```

### Frontend Setup

```powershell
cd frontend
npm install
setx NEXT_PUBLIC_API_URL "http://localhost:8000"
npm run dev
```

### macOS/Linux Tesseract Setup

If you're running the backend on macOS or Linux, ensure the Tesseract
binary is installed and set the `TESSERACT_CMD` environment variable so
`pytesseract` can locate it:

```bash
# macOS (Homebrew)
export TESSERACT_CMD=/usr/local/bin/tesseract

# Linux
export TESSERACT_CMD=/usr/bin/tesseract
```

## 🏗️ System Architecture

Blackletter Systems uses a modern microservices architecture with:

- **Frontend**: Next.js 14 with React 18 and Tailwind CSS
- **Backend**: FastAPI with async processing and Celery workers
- **AI/ML**: Google Gemini LLM with OpenAI GPT fallback
- **Storage**: PostgreSQL for metadata, Redis for caching, Vector DB for embeddings
- **Infrastructure**: Docker containerization with cloud deployment options

For detailed architecture information, see [ARCHITECTURE.md](ARCHITECTURE.md).

## 📋 System Constraints

- **File Size**: Maximum 10MB per document
- **File Type**: PDF only (DOCX and TXT support planned)
- **Text Limit**: ~6,000 characters for LLM processing
- **Processing Time**: 30-60 seconds per document
- **Concurrent Users**: 100+ supported

## 🎯 Features

### Core Functionality
- ✅ Document upload with drag-and-drop interface
- ✅ OCR text extraction using Tesseract
- ✅ AI-powered contract analysis and risk assessment
- ✅ Real-time processing status updates
- ✅ Interactive dashboard with risk visualization
- ✅ Export capabilities (PDF, DOCX, JSON)

### AI/ML Capabilities
- ✅ Google Gemini LLM integration
- ✅ OpenAI GPT fallback support
- ✅ Custom NLP pipelines for legal analysis
- ✅ RAG (Retrieval-Augmented Generation) system
- ✅ Vector database integration

### Security & Compliance
- ✅ File validation and sanitization
- ✅ Encrypted data storage and transmission
- ✅ GDPR and SOC 2 compliance ready
- ✅ Comprehensive audit logging

## 🧪 Testing

Use the provided `scripts/test_upload.http` with VS Code REST Client extension to test the API directly:

```http
POST http://localhost:8000/api/review
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="test.pdf"
Content-Type: application/pdf

< ./test.pdf
------WebKitFormBoundary--
```

For comprehensive testing guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md#testing).

## 🚀 Deployment Options

### Local Development
- Simple setup with virtual environments
- Docker Compose for full stack development
- Hot reload for rapid development

### Production Deployment
- Docker containerization
- Cloud deployment guides (AWS, Azure, GCP)
- CI/CD pipeline with GitHub Actions
- Auto-scaling and load balancing

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for:

- Development setup instructions
- Coding standards and best practices
- Testing frameworks and examples
- Pull request process and guidelines
- Issue reporting templates

## 🔒 Security

We take security seriously. Please report vulnerabilities to `security@blacklettersystems.com` following our [Security Policy](SECURITY.md).

## 📈 Roadmap

### Version 1.1.0 (Q2 2024)
- Multi-format support (DOCX, TXT, scanned PDFs)
- Advanced OCR with handwritten text recognition
- User authentication and team collaboration
- Advanced analytics and machine learning insights

### Version 1.2.0 (Q3 2024)
- Third-party legal system integrations
- Mobile applications (iOS/Android)
- Advanced compliance rule engines
- Blockchain document verification

### Version 2.0.0 (Q4 2024)
- Enterprise features (SSO, LDAP)
- Custom AI model training
- Workflow automation
- White-label solutions

For detailed roadmap information, see [CHANGELOG.md](CHANGELOG.md#future-roadmap).

## 📞 Support

- **Documentation**: [docs.blacklettersystems.com](https://docs.blacklettersystems.com)
- **API Reference**: [api.blacklettersystems.com/docs](https://api.blacklettersystems.com/docs)
- **Issues**: [GitHub Issues](https://github.com/your-org/blackletter-systems/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/blackletter-systems/discussions)
- **Security**: [security@blacklettersystems.com](mailto:security@blacklettersystems.com)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini for advanced LLM capabilities
- OpenAI for GPT fallback support
- The open-source community for excellent tools and libraries
- All contributors and supporters of Blackletter Systems

---

**Built with ❤️ for the legal community**
