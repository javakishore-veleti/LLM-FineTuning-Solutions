# Angular UI Setup - Events Grasp Application

> **Copilot Instructions**: This file provides guidance for setting up an Angular-based RAG chat UI for the LLM-FineTuning-Solutions project. **Implementation is done piece-by-piece** - wait for user confirmation before proceeding to the next section.

---

## 📋 Overview

**Application Name**: `events_grasp_app`  
**Location**: `portals/events_grasp_app`

This Angular application provides:
- Event management with web scraping capabilities
- Multiple vector store provider support
- Chat interface for RAG conversations
- Administration panel for configuration

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     ANGULAR UI - events_grasp_app                            │
│                     Location: portals/events_grasp_app                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  TOP NAVIGATION BAR                                                          │
│  ┌──────────┐  ┌───────────────┐  ┌────────────────┐  ┌─────────────┐       │
│  │   Home   │  │ Conversations │  │ Administration │  │  Settings   │       │
│  └──────────┘  └───────────────┘  └───────┬────────┘  └─────────────┘       │
│                                           │                                  │
│                              ┌────────────┴────────────┐                     │
│                              │   LEFT SIDEBAR NAV      │                     │
│                              ├─────────────────────────┤                     │
│                              │  📅 Events Setup        │                     │
│                              │  🗄️ Vector Stores       │                     │
│                              │  📊 Scraping Logs       │                     │
│                              │  📈 Indexing Logs       │                     │
│                              └─────────────────────────┘                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PYTHON BACKEND (FastAPI/Flask)                       │
│                         Location: modules/api/                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  modules/api/                                                                │
│  ├── agents/           # AI Agent endpoints                                  │
│  ├── vector_dbs/       # Vector store management                             │
│  ├── web_scraping/     # Web scraping endpoints                              │
│  └── querying/         # RAG query endpoints                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE (SQLite/PostgreSQL)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  events │ event_vector_stores │ vector_store_files │ event_scraping_logs    │
│  event_vectorization_logs │ conversations │ conversation_files │ chats      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          VECTOR STORE PROVIDERS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  OpenAI Vector Store    │ Amazon OpenSearch Service │ Amazon RDS PostgreSQL │
│  Amazon MemoryDB Redis  │ Amazon S3 Vectors         │ Amazon DocumentDB     │
│  Neo4j                  │ MongoDB                   │ Azure Vector Store    │
│  Local FAISS            │ Local Chroma              │ Pinecone              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────────────────────┐
│          events             │
├─────────────────────────────┤
│ event_id (PK)               │
│ event_name                  │
│ event_description           │
│ source_url                  │◄─── HTTP URL for scraping
│ source_location_type        │     'http_url' | 'local_folder' | 'aws_s3'
│ created_at                  │
│ updated_at                  │
│ is_active                   │
└──────────────┬──────────────┘
               │
               │ 1:N
               ▼
┌─────────────────────────────┐       ┌─────────────────────────────┐
│   event_scraping_logs       │       │   event_vectorization_logs  │
├─────────────────────────────┤       ├─────────────────────────────┤
│ scraping_log_id (PK)        │       │ vectorization_log_id (PK)   │
│ event_id (FK)               │       │ event_id (FK)               │
│ source_location             │       │ vector_store_id (FK)        │
│ source_location_type        │       │ source_location             │
│ start_time                  │       │ source_location_type        │
│ end_time                    │       │ start_time                  │
│ status                      │       │ end_time                    │
│ output_location             │       │ status                      │
│ output_location_type        │       │ files_indexed               │
│ files_scraped               │       │ error_message               │
│ error_message               │       │ created_at                  │
│ created_at                  │       └─────────────────────────────┘
└─────────────────────────────┘
               │
               │ 1:N
               ▼
┌─────────────────────────────┐
│   event_vector_stores       │
├─────────────────────────────┤
│ vector_store_id (PK)        │
│ event_id (FK)               │
│ vector_store_provider       │◄─── See provider list below
│ vector_config_json          │
│ vector_store_db_name        │
│ vector_store_db_link        │
│ status                      │     'pending'|'active'|'error'|'deleted'
│ created_at                  │
│ updated_at                  │
│ is_active                   │
└──────────────┬──────────────┘
               │
               │ 1:N
               ▼
┌─────────────────────────────┐
│   vector_store_files        │
├─────────────────────────────┤
│ file_id (PK)                │
│ vector_store_id (FK)        │
│ file_name                   │
│ file_display_name           │
│ row_created_dt              │
│ uploaded_to_datetime        │
│ status                      │
│ uploaded_flag               │
│ source_file_location        │
│ source_location_type        │
│ file_size_bytes             │
│ file_metadata_json          │
└─────────────────────────────┘

┌─────────────────────────────┐       ┌─────────────────────────────┐
│      conversations          │       │    conversation_files       │
├─────────────────────────────┤       ├─────────────────────────────┤
│ conversation_id (PK)        │◄──────│ conversation_id (FK)        │
│ event_id (FK)               │       │ file_id (FK)                │
│ conversation_name           │       │ added_at                    │
│ conversation_desc           │       └─────────────────────────────┘
│ created_at                  │
│ last_accessed_at            │
│ is_active                   │
└──────────────┬──────────────┘
               │
               │ 1:N
               ▼
┌─────────────────────────────┐
│          chats              │
├─────────────────────────────┤
│ chat_id (PK)                │
│ conversation_id (FK)        │
│ chat_log_json (TEXT/BLOB)   │◄─── Can be very large, supports multimedia
│ created_at                  │
│ updated_at                  │
└─────────────────────────────┘
```

### Vector Store Providers (Enum Values)

| Provider Code | Display Name |
|---------------|--------------|
| `openai` | OpenAI Vector Store |
| `aws_opensearch` | Amazon OpenSearch Service |
| `aws_rds_postgresql` | Amazon RDS and Aurora for PostgreSQL |
| `aws_memorydb_redis` | Amazon MemoryDB for Redis |
| `aws_s3_vectors` | Amazon S3 Vectors |
| `aws_documentdb` | Amazon DocumentDB (MongoDB compatibility) |
| `neo4j` | Neo4j |
| `mongodb` | MongoDB Atlas Vector Search |
| `azure_cognitive_search` | Azure Cognitive Search |
| `azure_cosmosdb` | Azure Cosmos DB |
| `local_faiss` | Local FAISS |
| `local_chroma` | Local Chroma |
| `pinecone` | Pinecone |

### SQL Schema Definition

```sql
-- ============================================
-- EVENTS TABLE
-- ============================================
CREATE TABLE events (
    event_id                INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name              VARCHAR(255) NOT NULL,
    event_description       TEXT,
    source_url              TEXT NOT NULL,              -- HTTP URL or folder path
    source_location_type    VARCHAR(50) DEFAULT 'http_url',  -- 'http_url', 'local_folder', 'aws_s3'
    created_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active               BOOLEAN DEFAULT TRUE
);

-- ============================================
-- EVENT SCRAPING LOGS TABLE
-- Logs each web scraping operation
-- ============================================
CREATE TABLE event_scraping_logs (
    scraping_log_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id                INTEGER NOT NULL,
    source_location         TEXT NOT NULL,              -- URL or path that was scraped
    source_location_type    VARCHAR(50) NOT NULL,       -- 'http_url', 'aws_s3', 'local_folder'
    start_time              DATETIME NOT NULL,
    end_time                DATETIME,
    status                  VARCHAR(50) DEFAULT 'in_progress',  -- 'in_progress', 'completed', 'failed'
    output_location         TEXT,                       -- Where scraped files are stored
    output_location_type    VARCHAR(50),                -- 'local_folder', 'aws_s3', 'azure_blob', 'gcp_blob', 'database'
    files_scraped           INTEGER DEFAULT 0,
    error_message           TEXT,
    created_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- ============================================
-- EVENT VECTOR STORES TABLE
-- ============================================
CREATE TABLE event_vector_stores (
    vector_store_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id                INTEGER NOT NULL,
    vector_store_provider   VARCHAR(100) NOT NULL,
    vector_config_json      TEXT,
    vector_store_db_name    VARCHAR(255) NOT NULL,
    vector_store_db_link    TEXT,
    status                  VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'active', 'error', 'deleted'
    created_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active               BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- ============================================
-- EVENT VECTORIZATION LOGS TABLE
-- Logs each vectorization/indexing operation
-- ============================================
CREATE TABLE event_vectorization_logs (
    vectorization_log_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id                INTEGER NOT NULL,
    vector_store_id         INTEGER NOT NULL,
    source_location         TEXT NOT NULL,              -- Location of files to index
    source_location_type    VARCHAR(50) NOT NULL,
    start_time              DATETIME NOT NULL,
    end_time                DATETIME,
    status                  VARCHAR(50) DEFAULT 'in_progress',
    files_indexed           INTEGER DEFAULT 0,
    error_message           TEXT,
    created_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (vector_store_id) REFERENCES event_vector_stores(vector_store_id) ON DELETE CASCADE
);

-- ============================================
-- VECTOR STORE FILES TABLE
-- ============================================
CREATE TABLE vector_store_files (
    file_id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    vector_store_id         INTEGER NOT NULL,
    file_name               VARCHAR(500) NOT NULL,
    file_display_name       VARCHAR(255),
    row_created_dt          DATETIME DEFAULT CURRENT_TIMESTAMP,
    uploaded_to_datetime    DATETIME,
    status                  VARCHAR(50) DEFAULT 'pending',
    uploaded_flag           BOOLEAN DEFAULT FALSE,
    source_file_location    TEXT NOT NULL,
    source_location_type    VARCHAR(50) NOT NULL,
    file_size_bytes         BIGINT,
    file_metadata_json      TEXT,
    FOREIGN KEY (vector_store_id) REFERENCES event_vector_stores(vector_store_id) ON DELETE CASCADE
);

-- ============================================
-- CONVERSATIONS TABLE
-- ============================================
CREATE TABLE conversations (
    conversation_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id                INTEGER NOT NULL,
    conversation_name       VARCHAR(255) NOT NULL,
    conversation_desc       TEXT,
    created_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_accessed_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active               BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- ============================================
-- CONVERSATION FILES TABLE
-- ============================================
CREATE TABLE conversation_files (
    conversation_id         INTEGER NOT NULL,
    file_id                 INTEGER NOT NULL,
    added_at                DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (conversation_id, file_id),
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES vector_store_files(file_id) ON DELETE CASCADE
);

-- ============================================
-- CHATS TABLE
-- ============================================
CREATE TABLE chats (
    chat_id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id         INTEGER NOT NULL,
    chat_log_json           TEXT NOT NULL,
    created_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE
);

-- ============================================
-- INDEXES
-- ============================================
CREATE INDEX idx_events_active ON events(is_active);
CREATE INDEX idx_scraping_logs_event ON event_scraping_logs(event_id);
CREATE INDEX idx_vectorization_logs_event ON event_vectorization_logs(event_id);
CREATE INDEX idx_vector_stores_event ON event_vector_stores(event_id);
CREATE INDEX idx_vector_files_store ON vector_store_files(vector_store_id);
CREATE INDEX idx_conversations_event ON conversations(event_id);
CREATE INDEX idx_conversations_accessed ON conversations(last_accessed_at DESC);
CREATE INDEX idx_chats_conversation ON chats(conversation_id);
```

---

## 🎨 Angular UI - Multi-Module Structure

### Project Location & Structure

```
portals/
└── events_grasp_app/
    ├── src/
    │   ├── app/
    │   │   │
    │   │   ├── core/                           # Core Module (Singleton services)
    │   │   │   ├── core.module.ts
    │   │   │   ├── services/
    │   │   │   │   ├── api.service.ts
    │   │   │   │   ├── auth.service.ts
    │   │   │   │   └── toast.service.ts
    │   │   │   ├── interceptors/
    │   │   │   │   ├── http-error.interceptor.ts
    │   │   │   │   └── loading.interceptor.ts
    │   │   │   └── guards/
    │   │   │       └── auth.guard.ts
    │   │   │
    │   │   ├── shared/                         # Shared Module (Reusable components)
    │   │   │   ├── shared.module.ts
    │   │   │   ├── components/
    │   │   │   │   ├── navbar/
    │   │   │   │   ├── sidebar/
    │   │   │   │   ├── loading-spinner/
    │   │   │   │   ├── confirmation-dialog/
    │   │   │   │   ├── data-table/
    │   │   │   │   └── status-badge/
    │   │   │   ├── pipes/
    │   │   │   │   ├── date-format.pipe.ts
    │   │   │   │   └── file-size.pipe.ts
    │   │   │   └── directives/
    │   │   │       └── click-outside.directive.ts
    │   │   │
    │   │   ├── features/                       # Feature Modules (Lazy Loaded)
    │   │   │   │
    │   │   │   ├── home/                       # HOME MODULE
    │   │   │   │   ├── home.module.ts
    │   │   │   │   ├── home-routing.module.ts
    │   │   │   │   └── pages/
    │   │   │   │       └── home-page/
    │   │   │   │
    │   │   │   ├── conversations/              # CONVERSATIONS MODULE
    │   │   │   │   ├── conversations.module.ts
    │   │   │   │   ├── conversations-routing.module.ts
    │   │   │   │   ├── services/
    │   │   │   │   │   └── conversation.service.ts
    │   │   │   │   ├── models/
    │   │   │   │   │   └── conversation.model.ts
    │   │   │   │   └── pages/
    │   │   │   │       ├── conversation-list/
    │   │   │   │       ├── conversation-detail/
    │   │   │   │       ├── conversation-create/
    │   │   │   │       └── file-selector/
    │   │   │   │
    │   │   │   ├── administration/             # ADMINISTRATION MODULE
    │   │   │   │   ├── administration.module.ts
    │   │   │   │   ├── administration-routing.module.ts
    │   │   │   │   ├── services/
    │   │   │   │   │   ├── event.service.ts
    │   │   │   │   │   ├── vector-store.service.ts
    │   │   │   │   │   ├── scraping.service.ts
    │   │   │   │   │   └── vectorization.service.ts
    │   │   │   │   ├── models/
    │   │   │   │   │   ├── event.model.ts
    │   │   │   │   │   ├── vector-store.model.ts
    │   │   │   │   │   └── log.model.ts
    │   │   │   │   └── pages/
    │   │   │   │       ├── admin-layout/        # Layout with sidebar
    │   │   │   │       ├── events/
    │   │   │   │       │   ├── event-list/
    │   │   │   │       │   ├── event-detail/
    │   │   │   │       │   └── event-create/
    │   │   │   │       ├── vector-stores/
    │   │   │   │       │   ├── vector-store-list/
    │   │   │   │       │   └── vector-store-detail/
    │   │   │   │       ├── scraping-logs/
    │   │   │   │       └── vectorization-logs/
    │   │   │   │
    │   │   │   ├── chat/                       # CHAT MODULE
    │   │   │   │   ├── chat.module.ts
    │   │   │   │   ├── services/
    │   │   │   │   │   └── chat.service.ts
    │   │   │   │   └── components/
    │   │   │   │       ├── chat-panel/
    │   │   │   │       ├── message-bubble/
    │   │   │   │       └── chat-input/
    │   │   │   │
    │   │   │   └── settings/                   # SETTINGS MODULE
    │   │   │       ├── settings.module.ts
    │   │   │       └── pages/
    │   │   │           └── settings-page/
    │   │   │
    │   │   ├── app.component.ts
    │   │   ├── app.module.ts
    │   │   └── app-routing.module.ts
    │   │
    │   ├── assets/
    │   │   ├── images/
    │   │   │   ├── logo.png
    │   │   │   └── favicon.ico
    │   │   └── icons/
    │   │
    │   ├── environments/
    │   │   ├── environment.ts
    │   │   └── environment.prod.ts
    │   │
    │   └── styles/
    │       ├── styles.scss
    │       ├── _variables.scss
    │       ├── _bootstrap-overrides.scss
    │       └── _components.scss
    │
    ├── angular.json
    ├── package.json
    └── tsconfig.json
```

---

## 📱 UI Wireframes

### Administration - Events Setup Page

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🏠 Home    📝 Conversations    ⚙️ Administration    🔧 Settings             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────────────────────────────────────┐   │
│  │ ADMINISTRATION  │  │                                                  │   │
│  │                 │  │  📅 Events Setup                  [+ New Event]  │   │
│  │ ┌─────────────┐ │  │                                                  │   │
│  │ │📅 Events    │ │  │  ┌───────────────────────────────────────────┐   │   │
│  │ │   Setup     │◄│  │  │ 🔍 Search events...                       │   │   │
│  │ └─────────────┘ │  │  └───────────────────────────────────────────┘   │   │
│  │ ┌─────────────┐ │  │                                                  │   │
│  │ │🗄️ Vector   │ │  │  ┌───────────────────────────────────────────┐   │   │
│  │ │   Stores    │ │  │  │ NAME              │ URL           │STATUS │   │   │
│  │ └─────────────┘ │  │  ├───────────────────┼───────────────┼───────┤   │   │
│  │ ┌─────────────┐ │  │  │ AWS re:Invent 2025│ aws.amazon... │Active │   │   │
│  │ │📊 Scraping  │ │  │  │ Google I/O 2025   │ google.com... │Active │   │   │
│  │ │   Logs      │ │  │  │ Microsoft Build   │ microsoft...  │Pending│   │   │
│  │ └─────────────┘ │  │  └───────────────────┴───────────────┴───────┘   │   │
│  │ ┌─────────────┐ │  │                                                  │   │
│  │ │📈 Indexing  │ │  │                                                  │   │
│  │ │   Logs      │ │  │                                                  │   │
│  │ └─────────────┘ │  │                                                  │   │
│  └─────────────────┘  └─────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Event Detail Page

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🏠 Home    📝 Conversations    ⚙️ Administration    🔧 Settings             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────────────────────────────────────┐   │
│  │ ADMINISTRATION  │  │                                                  │   │
│  │                 │  │  ← Back to Events                                │   │
│  │ ┌─────────────┐ │  │                                                  │   │
│  │ │📅 Events    │◄│  │  📅 AWS re:Invent 2025                          │   │
│  │ │   Setup     │ │  │  ─────────────────────────────────────────────  │   │
│  │ └─────────────┘ │  │                                                  │   │
│  │ ...             │  │  Source URL:                                     │   │
│  └─────────────────┘  │  https://aws.amazon.com/blogs/aws/top-announce...│   │
│                       │                                                  │   │
│                       │  Source Type: HTTP URL                           │   │
│                       │  Created: Jan 18, 2026 10:00 AM                  │   │
│                       │                                                  │   │
│                       │  ┌─────────────────────────────────────────────┐ │   │
│                       │  │                    ACTIONS                   │ │   │
│                       │  ├─────────────────────────────────────────────┤ │   │
│                       │  │  [🔄 Run Web Scraping]   [📊 View Logs]     │ │   │
│                       │  │                                              │ │   │
│                       │  │  [➕ Initialize Vector Store]                │ │   │
│                       │  │     Select Provider: [OpenAI Vector Store ▼] │ │   │
│                       │  └─────────────────────────────────────────────┘ │   │
│                       │                                                  │   │
│                       │  VECTOR STORES (2)                [+ Add Store]  │   │
│                       │  ┌─────────────────────────────────────────────┐ │   │
│                       │  │ Provider        │ Name          │ Status    │ │   │
│                       │  ├─────────────────┼───────────────┼───────────┤ │   │
│                       │  │ OpenAI          │ LLM-Fine...   │ Active    │ │   │
│                       │  │ AWS OpenSearch  │ aws-reinv...  │ Pending   │ │   │
│                       │  └─────────────────┴───────────────┴───────────┘ │   │
│                       │                                                  │   │
│                       │  [✏️ Edit]  [🗑️ Delete]                          │   │
│                       └─────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Vector Store Detail Page

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🏠 Home    📝 Conversations    ⚙️ Administration    🔧 Settings             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ← Back to Event: AWS re:Invent 2025                                        │
│                                                                              │
│  🗄️ Vector Store: LLM-FineTuning-Solutions                                  │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  Provider: OpenAI Vector Store                                               │
│  Status: ✅ Active                                                           │
│  Store ID: vs_696cf8bd0d8481919b53f73a1d1ac59b                              │
│  Files Indexed: 37                                                           │
│  Created: Jan 18, 2026 10:04 AM                                              │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                           FILES (37)                                 │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │ File Name                                    │ Size    │ Status     │    │
│  ├─────────────────────────────────────────────┼─────────┼────────────┤    │
│  │ Top_announcements_of_AWS_reInvent_2025.txt  │ 12 KB   │ ✅ Active  │    │
│  │ Introducing_Amazon_Nova_Forge.txt           │ 6 KB    │ ✅ Active  │    │
│  │ AWS_Lambda_Managed_Instances.txt            │ 9 KB    │ ✅ Active  │    │
│  │ ...                                         │         │            │    │
│  └─────────────────────────────────────────────┴─────────┴────────────┘    │
│                                                                              │
│  [🔄 Re-index Files]  [🗑️ Delete Vector Store]                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Implementation Plan (Piece by Piece)

### Phase 1: Project Setup & Core Module
- [ ] Create Angular project with Bootstrap
- [ ] Set up favicon and branding
- [ ] Create Core module with services
- [ ] Set up routing structure

### Phase 2: Shared Module
- [ ] Create reusable components (navbar, sidebar, etc.)
- [ ] Create pipes and directives
- [ ] Set up Bootstrap theming

### Phase 3: Administration Module - Events
- [ ] Admin layout with sidebar
- [ ] Events list page (CRUD)
- [ ] Event detail page
- [ ] Event create/edit forms

### Phase 4: Administration Module - Scraping
- [ ] Web scraping trigger button
- [ ] Scraping logs list
- [ ] Scraping progress indicator

### Phase 5: Administration Module - Vector Stores
- [ ] Vector store list per event
- [ ] Initialize vector store (provider selection)
- [ ] Vector store detail with files
- [ ] Vectorization logs

### Phase 6: Conversations Module
- [ ] Conversations list
- [ ] Conversation create/detail
- [ ] File selector for conversation

### Phase 7: Chat Module
- [ ] Chat panel component
- [ ] Message bubbles
- [ ] Chat input with attachments

### Phase 8: Home Module
- [ ] Default conversation display
- [ ] Quick access to recent conversations

---

## 🔧 Setup Commands

**Wait for confirmation before running these commands.**

### Step 1: Create Angular Project

```bash
# Navigate to project root
cd /path/to/LLM-FineTuning-Solutions

# Create portals directory
mkdir -p portals

# Create Angular application with routing
cd portals
ng new events_grasp_app --routing --style=scss

# Navigate to app
cd events_grasp_app
```

### Step 2: Install Dependencies

```bash
# Install Bootstrap and Bootstrap Icons
npm install bootstrap bootstrap-icons

# Install ngx-bootstrap for Bootstrap components
npm install ngx-bootstrap

# Install additional utilities
npm install @fortawesome/fontawesome-free
```

### Step 3: Configure angular.json for Bootstrap

Add to `angular.json` styles and scripts:

```json
{
  "styles": [
    "node_modules/bootstrap/dist/css/bootstrap.min.css",
    "node_modules/bootstrap-icons/font/bootstrap-icons.css",
    "src/styles.scss"
  ],
  "scripts": [
    "node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"
  ]
}
```

---

## ✅ Ready to Start?

**Please confirm to proceed with Phase 1: Project Setup & Core Module**

I will:
1. Create the Angular project structure
2. Set up Bootstrap integration
3. Create the Core module with base services
4. Set up the main routing

Type "proceed" or "yes" to continue with Phase 1.
