<div align="center">
  
  # Synapse^
  
  **Connect your research. The AI-powered workspace that synthesizes knowledge from the world's data.**
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Next.js](https://img.shields.io/badge/Next.js-16-black)](https://nextjs.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)](https://fastapi.tiangolo.com/)
  [![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
  [![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen)](https://github.com)
</div>

---

## 🚀 Overview

**Synapse** is a next-generation research assistant designed to help you navigate the ocean of academic papers with ease. It combines a beautiful, distraction-free interface with powerful AI capabilities to search, summarize, organize, and chat about research papers.

Whether you're a PhD student, researcher, or just curious, Synapse acts as your intelligent co-pilot for managing and understanding complex research.

## ✨ Features

### 🎯 Core Features (Live)

- **🔍 Smart Search**
  - Search millions of papers from arXiv and Semantic Scholar
  - Advanced filtering and sorting
  - Real-time results with rich metadata

- **📚 Collections & Library** *NEW!*
  - Organize papers into custom collections
  - Create unlimited collections for different projects/topics
  - Quick save papers from search results
  - Manage and browse your saved papers in the Library

- **💬 AI Chat with Context** *NEW!*
  - Multi-turn conversations with AI about papers
  - Chat history saved and accessible across sessions
  - Provide paper context for more accurate responses
  - Session management (create, load, delete chat sessions)

- **👶 ELI5 Mode**
  - "Explain Like I'm 5" - Get simple, analogy-filled explanations
  - Perfect for understanding complex abstracts quickly
  - Customizable prompts via templates

- **📝 AI Summaries**
  - Generate professional, academic summaries with one click
  - Powered by Google Gemini models
  - Adjustable tone and length (coming soon)

- **⚙️ Advanced Settings**
  - **Personal Profile**: Customize your name and avatar
  - **API Key Management**: Securely store your Gemini API key
  - **Model Selection**: Choose from available Gemini models (Flash, Pro, etc.)
  - **Prompt Templates**: Create custom system prompts for Chat, Summarize, and ELI5
  - Set active templates for different AI tasks

### 🚧 In Development

- **📊 Analytics Dashboard**
  - Track your reading patterns
  - Most-viewed papers and topics
  - Research activity timeline

- **🔗 Citation Management**
  - Export collections as BibTeX
  - Generate formatted citations
  - Citation graph visualization

- **🧠 Hive Mind**
  - Chat with multiple papers simultaneously
  - Find connections across your collection
  - AI-powered literature synthesis

### 🔮 Coming Soon

- **📄 Advanced PDF Integration**
  - Integrated PDF reader with highlighting
  - Smart search within PDFs
  - Annotation and note-taking

- **👥 Collaboration**
  - Share collections with team members
  - Collaborative notes and discussions
  - Public collection sharing

- **🔔 Smart Notifications**
  - New paper alerts for followed topics
  - Citation updates for saved papers
  - Weekly research digests

- **🌐 Multi-Language Support**
  - Translate papers and summaries
  - Support for non-English papers
  - Multi-language AI chat

- **🎨 Advanced Customization**
  - Dark/Light theme toggle
  - Custom color schemes
  - Layout preferences

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **State Management**: React Context API
- **HTTP Client**: Fetch API

### Backend
- **Framework**: FastAPI (Python)
- **AI Engine**: Google Gemini (Flash & Pro models)
- **Database**: SQLAlchemy with SQLite
- **Authentication**: JWT tokens
- **API Integration**: arXiv API, Semantic Scholar API
- **PDF Processing**: PyPDF

### Architecture
- **RESTful API** design
- **JWT-based authentication** with secure token handling
- **Modular router structure** for scalability
- **Pydantic models** for data validation
- **CORS-enabled** for cross-origin requests

## 📁 Project Structure

```
synapse/
├── backend/
│   ├── api/
│   │   ├── routers/
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── user.py          # User profile management
│   │   │   ├── research.py      # Paper search & AI features
│   │   │   ├── collections.py   # Collection CRUD
│   │   │   └── chat.py          # Chat sessions & history
│   │   └── deps.py              # Dependency injection
│   ├── db/
│   │   ├── models.py            # SQLAlchemy models
│   │   └── session.py           # Database session
│   ├── services/
│   │   ├── gemini_service.py    # AI integration
│   │   ├── arxiv_service.py     # arXiv API
│   │   └── pdf_service.py       # PDF processing
│   ├── main.py                  # FastAPI app
│   ├── reset_db.py              # Database reset utility
│   └── requirements.txt         # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx         # Home/Search page
│   │   │   ├── library/         # Collections UI
│   │   │   ├── settings/        # User settings
│   │   │   ├── login/           # Authentication
│   │   │   └── signup/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── PaperCard.tsx
│   │   │   ├── PaperDetailsModal.tsx
│   │   │   ├── SaveToCollectionModal.tsx
│   │   │   └── Navbar.tsx
│   │   └── context/
│   │       └── AuthContext.tsx  # Auth state management
│   ├── package.json
│   └── tailwind.config.ts
│
└── README.md
```

## ⚡ Getting Started

### Prerequisites
- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.9+ ([Download](https://www.python.org/))
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Mr-Dark-debug/synapse.git
cd synapse
```

### 2️⃣ Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Create a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

**Create `.env` file** in the `backend` directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_for_jwt  # Generate a random string
```

**Initialize the database:**
```bash
python reset_db.py
```

**Run the backend server:**
```bash
python -m uvicorn main:app --reload
```
✅ Backend running at `http://localhost:8000`

### 3️⃣ Frontend Setup

Open a **new terminal** and navigate to the frontend:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

**Run the development server:**
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```
✅ Frontend running at `http://localhost:3000`

## 📖 Usage Guide

### Getting Started
1. **Sign Up**: Create an account at `/signup`
2. **Configure API Key**: Go to Settings → AI Configuration → Enter your Gemini API key
3. **Start Searching**: Use the home page to search for papers

### Key Workflows

#### 📄 Searching for Papers
1. Enter a search query (e.g., "quantum computing")
2. Results appear with title, authors, abstract, and publication date
3. Click on any paper to view full details

#### 💾 Saving Papers to Collections
1. Click the "Save to Collection" button on any paper
2. Select an existing collection or create a new one
3. Access your collections anytime from the Library page

#### 💬 Chatting About Papers
1. Select one or more papers to use as context
2. Open the Chat interface
3. Ask questions about the papers
4. Chat history is automatically saved
5. Resume previous conversations from the sidebar

#### 🎨 Customizing AI Behavior
1. Go to Settings → Prompt Templates
2. Switch between Chat, Summarize, or ELI5 tabs
3. Create a new template with custom instructions
4. Mark as "Active" to use it as default
5. Optionally assign a specific model to each template

#### 🔧 Advanced Configuration
- **Profile**: Update your name and avatar URL
- **Preferred Model**: Select from available Gemini models
- **Template Management**: Create, edit, and delete custom prompts

## 🔐 Security & Privacy

- **Passwords** are hashed using bcrypt
- **API keys** are stored encrypted in the database
- **JWT tokens** expire after 7 days
- **Sessions** are user-isolated (cannot access other users' data)
- **No data sharing** - all your research stays private

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit your changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Development Guidelines
- Follow existing code style and conventions
- Write descriptive commit messages
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

## 📝 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints
- `POST /auth/signup` - Create new account
- `POST /auth/login` - Authenticate user
- `POST /research/search` - Search papers
- `POST /research/chat` - AI chat with context
- ✅ Chat history persistence
- ✅ Custom prompt templates
- 🔄 Analytics dashboard
- 🔄 Citation management
- 📅 PDF reader integration
- 📅 Collaboration features
- 📅 Mobile app (React Native)
- 📅 Browser extension
- 📅 Multi-language support
- 📅 Advanced search filters
- 📅 Paper recommendations
- 📅 Integration with Notion, Obsidian

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **arXiv** for open access to research papers
- **Semantic Scholar** for comprehensive paper metadata
- **Google Gemini** for powerful AI capabilities
- The open-source community for amazing tools and libraries

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/Mr-Dark-debug/synapse/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Mr-Dark-debug/synapse/discussions)
- **Email**: your.email@example.com

---

<div align="center">
  
  **Built with ❤️ by [Mr-Dark-debug](https://github.com/Mr-Dark-debug)**
  
  If you find Synapse helpful, please consider giving it a ⭐ on GitHub!
  
  [Report Bug](https://github.com/Mr-Dark-debug/synapse/issues) · [Request Feature](https://github.com/Mr-Dark-debug/synapse/issues) · [Documentation](https://github.com/Mr-Dark-debug/synapse/wiki)
  
</div>
