# Events Grasp

> **AI-Powered Event Knowledge Management Platform**

Events Grasp is an intelligent platform that helps you extract, organize, and interact with knowledge from event websites using AI. Scrape event content, store it in vector databases, and have meaningful conversations powered by RAG (Retrieval-Augmented Generation).

## 🎯 What It Does

1. **📄 Event Management** - Create and manage events from conference websites, meetups, or any web source
2. **🔍 Content Scraping** - Automatically scrape and extract content from event URLs
3. **🗄️ Vector Storage** - Store scraped content in vector databases for semantic search
4. **💬 AI Conversations** - Chat with your event data using RAG-powered conversations
5. **🔐 Credential Management** - Securely manage credentials for multiple cloud providers

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Events Grasp Platform                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │
│  │   Angular UI    │───▶│  FastAPI Backend │───▶│    SQLite DB    │  │
│  │  (Port 4200)    │    │   (Port 5000)    │    │                 │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘  │
│                                │                                      │
│                                ▼                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                     Vector Store Providers                      │  │
│  ├────────────┬────────────┬────────────┬────────────┬───────────┤  │
│  │    AWS     │   Azure    │    GCP     │   OpenAI   │  Others   │  │
│  │ OpenSearch │  AI Search │ Vertex AI  │  Vectors   │  Neo4j    │  │
│  │  Aurora    │ Cosmos DB  │  AlloyDB   │            │  MongoDB  │  │
│  │  pgvector  │            │            │            │  Pinecone │  │
│  └────────────┴────────────┴────────────┴────────────┴───────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## ✨ Features

### Event Management
- Create events from web URLs (conferences, meetups, documentation sites)
- Track event metadata and descriptions
- Organize events by customer/organization

### Web Scraping
- Automated content extraction from event URLs
- Track scraping history and execution logs
- View scraped files and their status

### Vector Store Integration
- **AWS**: OpenSearch, Aurora PostgreSQL (pgvector)
- **Azure**: AI Search, Cosmos DB (Coming Soon)
- **GCP**: Vertex AI Vector Search, AlloyDB (Coming Soon)
- **OpenAI**: Vector Stores (Assistants API)
- **Open Source**: Neo4j, MongoDB Atlas, Pinecone, Redis, Elasticsearch

### Credential Management
- Secure storage for cloud provider credentials
- Support for multiple authentication types:
  - API Keys
  - Access Key/Secret
  - IAM Roles
  - Service Principals
  - Environment Variables
- Provider-specific configurations

### AI Conversations (Coming Soon)
- RAG-powered conversations with event data
- Context-aware responses using vector search
- Conversation history and management

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### 1. Clone & Setup

```bash
git clone https://github.com/javakishore-veleti/LLM-FineTuning-Solutions.git
cd LLM-FineTuning-Solutions

# Setup Python environment and install dependencies
npm run setup
```

### 2. Start the Backend

```bash
npm run backend:start
```
Backend runs at: http://localhost:5000

### 3. Start the Frontend

```bash
npm run ui:start
```
Frontend runs at: http://localhost:4200

### 4. Access the Application

Open http://localhost:4200 in your browser:
1. **Sign up** for a new account
2. **Create an Event** with a source URL
3. **Add Credentials** for your vector store provider
4. **Create a Vector Store** and associate it with your event
5. **Run Scraping** to extract content
6. **Start Conversations** with your data

## 📁 Project Structure

```
LLM-FineTuning-Solutions/
├── backend/
│   └── microservices/
│       └── events_grasp_service/     # FastAPI backend
│           ├── app.py                 # Main application
│           ├── db_migrations/         # Database migrations
│           └── modules/
│               ├── api/               # REST API routes
│               │   ├── auth/          # Authentication
│               │   ├── credentials/   # Credential management
│               │   ├── dashboard/     # Dashboard data
│               │   ├── events/        # Event CRUD
│               │   ├── scraping/      # Scraping logs
│               │   └── vector_dbs/    # Vector store management
│               └── core/              # Business logic
│                   ├── credentials/   # Credential providers & schemas
│                   ├── services/      # Service implementations
│                   └── vector_stores/ # Vector store handlers
│
├── portals/
│   └── events_grasp_app/             # Angular frontend
│       └── src/app/
│           ├── core/                  # Services & guards
│           └── features/              # Feature modules
│               ├── administration/    # Admin pages
│               ├── auth/              # Login/Signup
│               ├── dashboard/         # Dashboard
│               └── home/              # Landing page
│
├── runtime_data/                      # Local database & logs
├── scripts/                           # Build & setup scripts
└── package.json                       # NPM scripts
```

## 🛠️ NPM Scripts

| Command | Description |
|---------|-------------|
| `npm run setup` | Setup Python environment and install dependencies |
| `npm run backend:start` | Start the FastAPI backend server |
| `npm run ui:start` | Start the Angular development server |
| `npm run ui:build` | Build Angular app for production |

## 🔒 Supported Credential Providers

| Provider | Auth Types |
|----------|-----------|
| **AWS** | Access Key, IAM Role, AWS Profile, Environment Variables |
| **Azure** | Service Principal, Managed Identity, Connection String, Environment Variables |
| **GCP** | Service Account, Application Default, Environment Variables |
| **OpenAI** | API Key, Environment Variables |
| **Neo4j** | Username/Password, Environment Variables |
| **MongoDB** | Connection String, Username/Password, Environment Variables |
| **Pinecone** | API Key, Environment Variables |
| **Elasticsearch** | Basic Auth, API Key, Environment Variables |
| **Redis** | Password, ACL, Environment Variables |
| **PostgreSQL** | Username/Password, Environment Variables |

## 🗄️ Database Schema

The application uses SQLite with the following main tables:
- `customers` - User accounts
- `events` - Event definitions with source URLs
- `event_scraping_logs` - Scraping execution history
- `event_vector_stores` - Vector store configurations
- `vector_store_files` - Indexed files
- `credentials` - Encrypted credential storage
- `conversations` - Chat sessions
- `chats` - Conversation messages

## 🔜 Roadmap

- [ ] GitHub Actions workflows for vector store provisioning
- [ ] RAG-powered conversations
- [ ] Multi-tenancy support
- [ ] Azure & GCP vector store implementations
- [ ] Scheduled scraping jobs
- [ ] Export/Import event data
- [ ] Webhook notifications

## 📝 API Documentation

Once the backend is running, access the interactive API docs at:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using FastAPI, Angular, and AI**
