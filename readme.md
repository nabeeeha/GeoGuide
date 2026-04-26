# GeoGuide: AI Chatbot for Indian Mining Regulations

An intelligent chatbot powered by LLMs for retrieving information from Indian mining industry acts, rules, and regulations. Ask complex questions about mining policies and get instant, context-aware answers.

## Overview

GeoGuide simplifies navigation through complex mining regulations in India including:
- Mineral Conservation and Development Rules
- Environment Protection Act (Mining)
- Safety Rules for Mines Regulations
- Land Acquisition and Rehabilitation policies
- Environmental Impact Assessment guidelines
- State-specific mining regulations

## Features

- ✅ **AI-Powered Chat** - Ask questions in natural language; get answers from PDFs
- ✅ **User Authentication** - Secure login/signup system with bcrypt encryption
- ✅ **Session Persistence** - Chat history saved automatically per user
- ✅ **FAISS Vector Search** - Fast semantic search across large documents
- ✅ **Multi-PDF Support** - Upload and query multiple regulation documents
- ✅ **OpenAI Integration** - Uses GPT for accurate context-aware responses

## Tech Stack

- **Frontend:** Streamlit (interactive UI)
- **Backend:** Python, LangChain, OpenAI API
- **Database:** SQLite3
- **Vector DB:** FAISS
- **Authentication:** bcrypt

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- HuggingFace API token (optional)

### Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/nabeeeha/GeoGuide.git
   cd GeoGuide
   ```

2. **Create virtual environment**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # macOS/Linux
   myenv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r extra/req.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in root directory:
   ```
   OPENAI_API_KEY=your_openai_key_here
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
   ```

5. **Add mining regulation PDFs**
   - Place PDF files in the `files/` folder

## Usage

1. **Start the app**
   ```bash
   streamlit run app.py
   ```

2. **Sign up / Log in**
   - Create account with username and password
   - Credentials stored securely with bcrypt hashing

3. **Upload PDFs**
   - Click "Start" to initialize vector store
   - System loads embeddings from PDFs

4. **Ask Questions**
   - Type queries like:
     - "What are the safety requirements for underground mining?"
     - "What is the penalty for illegal mining in India?"
     - "Explain the Environmental Impact Assessment process"

## Project Structure

```
GeoGuide/
├── app.py                 # Main Streamlit app
├── auth.py               # User authentication
├── database.py           # SQLite database setup
├── chat.py               # Chat session management
├── process.py            # PDF processing & embeddings
├── htmlTemplates.py      # UI styling
├── files/                # Upload regulation PDFs here
├── faiss_index/          # Vector store
├── users.db              # User credentials (auto-created)
└── .env                  # API keys (not in git)
```

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application with UI |
| `process.py` | PDF loading, chunking, embedding generation |
| `auth.py` | User registration & login with password hashing |
| `database.py` | SQLite tables for users & chat sessions |
| `chat.py` | Chat history serialization & persistence |

## How It Works

1. **PDF Processing:** PDFs split into chunks (1000 tokens with 200-token overlap)
2. **Embeddings:** OpenAI embeddings convert text to vectors
3. **Vector Store:** FAISS indexes embeddings for fast retrieval
4. **Query:** User question → embedded → matched against documents
5. **Generation:** LLM generates response using retrieved context

## Security Notes

⚠️ **Important:**
- Never commit `.env` with real API keys
- Keep `users.db` private (contains password hashes)
- Regenerate API keys if repo goes public
- `.gitignore` protects sensitive files

## Future Enhancements

- [ ] Multi-language support
- [ ] Document upload UI
- [ ] Export chat as PDF
- [ ] Real-time chat analytics
- [ ] State-specific regulation filtering

## Contributing

Pull requests welcome! Please:
1. Fork the repo
2. Create feature branch
3. Commit changes
4. Push and create PR

## License

MIT License - See LICENSE file

## Support

For issues or questions, create a GitHub issue or contact the maintainer.

