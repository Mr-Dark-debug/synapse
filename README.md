<div align="center">
  
  # Synapse^
  
  **Connect your research. The AI-powered workspace that synthesizes knowledge from the world's data.**
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)](https://fastapi.tiangolo.com/)
  [![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
</div>

---

## 🚀 Overview

**Synapse** is a next-generation research assistant designed to help you navigate the ocean of academic papers with ease. It combines a beautiful, distraction-free interface with powerful AI capabilities to search, summarize, and explain complex topics.

Whether you're a PhD student, a researcher, or just curious, Synapse acts as your intelligent co-pilot.

## ✨ Key Features

- **🔍 Smart Search**: Instantly search arXiv for millions of papers with advanced filtering.
- **👶 ELI5 Mode**: "Explain Like I'm 5" - Get simple, analogy-filled explanations of complex abstracts.
- **📝 AI Summaries**: Generate professional, academic summaries with a single click.
- **💬 Chat with Papers**: (Coming Soon) Have a conversation with your papers to extract specific insights.
- **🧠 Hive Mind**: (Coming Soon) Chat with a collection of papers simultaneously to find connections.
- **📄 PDF Reader**: (Coming Soon) Integrated reader with highlighting and smart search.

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Language**: TypeScript

### Backend
- **Framework**: FastAPI
- **AI Engine**: Google Gemini Pro
- **PDF Processing**: PyPDF
- **Database**: SQLAlchemy (SQLite/PostgreSQL)

## ⚡ Getting Started

Follow these steps to set up Synapse locally.

### Prerequisites
- Node.js 18+
- Python 3.9+
- A Google Gemini API Key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/synapse.git
cd synapse
```

### 2. Backend Setup
Navigate to the backend directory and set up the Python environment.

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Environment Variables:**
Create a `.env` file in the `backend` directory:
```env
GEMINI_API_KEY=your_api_key_here
```

**Run the Server:**
```bash
python -m uvicorn main:app --reload
```
The backend will start at `http://localhost:8000`.

### 3. Frontend Setup
Open a new terminal and navigate to the frontend directory.

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```
The frontend will start at `http://localhost:3000`.

## 📖 Usage Guide

1.  **Search**: Use the main search bar to find papers by topic (e.g., "Quantum Computing").
2.  **View Details**: Click on any paper card to view the abstract and authors.
3.  **AI Tools**:
    *   Click **👶 Explain Like I'm 5** for a simple explanation.
    *   Click **📝 Summarize** for a formal academic summary.
4.  **Read**: Click "Read PDF" to open the original paper.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

<div align="center">
  Built with ❤️ by the Synapse Team
</div>
