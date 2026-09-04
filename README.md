# Remarka - AI-Powered Content Platform

## Overview

Remarka is a modern web platform designed for building, deploying, and scaling AI-driven content applications with ease.

## Features

### Core Infrastructure
- **Task Queues**: Celery + Redis integration for reliable async task processing
- **Artifact Storage**: S3-compatible storage (R2/S3) for scalable file management
- **Vector Storage (RAG)**: Qdrant or pgvector for semantic search and retrieval-augmented generation
- **AI Provider**: Pluggable AI integrations (OpenAI, Anthropic, or local models)
- **News Aggregation**: RSS parsing and web scraping with robots.txt support
- **CI/CD Pipeline**: GitHub Actions automation for testing and deployment

### Architecture
```
Frontend (React/Next.js)
        ↓
    API (FastAPI/Python)
        ↓
Services (PostgreSQL, Redis, Qdrant)
        ↓
Infrastructure (Docker, Kubernetes, Cloud)
```

## Current: Marketing Website

This repository currently contains the **Remarka marketing website** — a static, responsive landing page built with HTML, CSS, and vanilla JavaScript.

### Quick Start

Simply open `index.html` in a browser to view the landing page, or serve it via:

```bash
# Using Python
python -m http.server 8000

# Using Node.js (http-server)
npx http-server
```

Then navigate to `http://localhost:8000/index.html`

## Repository Structure

### Current Files
```
├── index.html           # Marketing website landing page
│                        # Sections: hero, features, architecture, services, stats, CTA, contact, footer
├── script.js            # Interactive features
│                        # - Mobile menu toggle with ARIA accessibility
│                        # - Contact form validation with error messages
│                        # - Smooth scroll navigation
│                        # - Fade-in animations on scroll
│                        # - Button ripple effects
│                        # - Keyboard accessibility (Escape to close menu)
├── styles.css           # Responsive styling
│                        # - CSS Grid & Flexbox layouts
│                        # - Mobile breakpoints (768px, 480px)
│                        # - Smooth animations & transitions
│                        # - Theme variables (colors, spacing)
├── .gitignore           # Git ignore patterns for Python, Node.js, IDE, Docker
├── .github/
│   └── workflows/       # GitHub Actions CI/CD
├── README.md            # This file
└── LICENSE              # MIT License (coming soon)
```

## Website Sections

- **Hero** — Call-to-action with feature highlights
- **Features** — 6 core infrastructure components with icons
- **Architecture** — Layered system design diagram
- **Services** — Development, Deployment, Scaling, Integration
- **Stats** — Key metrics (uptime, support, projects, requests)
- **CTA** — Call-to-action to start a project
- **Contact** — Contact form with validation and contact info
- **Footer** — Links, social media, copyright

## Future: Full Platform

The repository is planned to evolve into a complete AI platform with the following structure:

```
├── apps/
│   ├── api/              # FastAPI Backend
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── README.md
│   └── frontend/         # Next.js Frontend
│       ├── package.json
│       ├── Dockerfile
│       └── README.md
├── infra/
│   └── packer/          # Machine image builder
│       └── README.md
├── docker-compose.yml   # Full-stack local development
└── [... additional files ...]
```

### Planned Components
- **Backend API** (FastAPI/Python) with task queue support
- **Frontend Application** (Next.js/React)
- **Infrastructure as Code** (Packer for custom images)
- **Docker Compose** orchestration for local development
- **Full CI/CD Pipeline** with GitHub Actions

## CI/CD Pipeline

The repository includes GitHub Actions workflows for:
- Automated testing (planned)
- Docker image building (planned)
- Machine image creation with Packer (planned)
- Deployment to cloud infrastructure (planned)
- GitHub Pages static site hosting

## Configuration

For future full-stack deployment, create a `.env` file:

```env
POSTGRES_PASSWORD=your_secure_password
API_URL=http://localhost:8000
REDIS_URL=redis://localhost:6379
QDRANT_URL=http://localhost:6333
```

## Support

- Email: info@remarka.com
- Phone: +1 (555) 123-4567
- Website: www.remarka.com

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

## Roadmap

- [x] Marketing website landing page
- [ ] Backend API (FastAPI)
- [ ] Frontend application (Next.js)
- [ ] Docker Compose orchestration
- [ ] NewsAPI integration
- [ ] Advanced RAG capabilities
- [ ] Multi-model AI provider support
- [ ] Real-time collaboration features
- [ ] Enhanced monitoring and observability
- [ ] GraphQL API

---

**Built with** ❤️ **by the Remarka team**
