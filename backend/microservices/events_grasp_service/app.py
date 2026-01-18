from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
import json
import logging
import warnings
from sqlalchemy.exc import SAWarning

# Suppress SQLAlchemy SAWarning messages that appear when models are rebound to existing metadata
warnings.filterwarnings('ignore', category=SAWarning)
# Lower SQLAlchemy logging to ERROR to avoid noisy INFO/WARNING logs
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

# --- Core integrations and model factories (imported after logging configured) ---
from .modules.core.integrations.migrator import apply_migrations
from .modules.core.integrations.db import get_db_manager
from .modules.core.models.event import create_event_model
from .modules.core.models.provider import create_provider_model
from .modules.core.models.event_provider import create_event_provider_model
from .modules.core.models.customer import create_customer_model
from .modules.core.models.customer_session import create_customer_session_model

app = FastAPI(title="Events Grasp Service")
logger = logging.getLogger('events_grasp_service')

# Load config if available
if os.path.exists(os.path.join(os.getcwd(), 'backend-settings.json')):
    try:
        with open('backend-settings.json') as f:
            cfg = json.load(f)
            for k, v in cfg.items():
                app.state.__dict__[k] = v
    except Exception:
        pass

# allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure migrations applied for sqlite
try:
    apply_migrations()
except Exception as e:
    logger.exception('Failed to apply migrations')

# Initialize DB manager and models (use singleton to keep one Base/metadata)
DB = get_db_manager()
Base = DB.Base
# create ORM models bound to the declarative Base
Customer = create_customer_model(Base)
CustomerSession = create_customer_session_model(Base)
Event = create_event_model(Base)
Provider = create_provider_model(Base)
EventProvider = create_event_provider_model(Base)
# init tables
DB.init_db()

# Now import DAOs and routers (after models are bound to the shared Base)
from .modules.core.dao.impl.event_dao import EventDAO
from .modules.core.dao.impl.provider_dao import ProviderDAO
from .modules.api.events.routes import router as events_router
from .modules.api.auth import routes as auth_routes
from .modules.api.customer import routes as customer_routes

# register routers
app.include_router(events_router)
app.include_router(auth_routes.router)
app.include_router(customer_routes.router)

# --- Events endpoints moved to modules/api/events/routes.py ---
# The router above now provides all /api/events/* endpoints (CRUD via EventServiceSingleton).

# PROVIDERS
# instantiate DAOs for providers
provider_dao = ProviderDAO(DB, Provider, EventProvider)
# instantiate event DAO (used by publish endpoint)
event_dao = EventDAO(DB, Event)

class ProviderIn(BaseModel):
    provider_type: str
    display_name: str
    credentials_json: Optional[str] = None
    is_active: Optional[bool] = True

class ProviderOut(ProviderIn):
    provider_id: int
    created_at: Optional[str]

class EventProviderIn(BaseModel):
    provider_id: int
    provider_config_json: Optional[dict] = None
    is_active: Optional[bool] = True

class PublishResult(BaseModel):
    provider_id: int
    status: str
    message: Optional[str] = None

@app.post('/api/providers/', status_code=201, response_model=ProviderOut)
def api_create_provider(payload: ProviderIn):
    data = payload.dict()
    p = provider_dao.create_provider(data)
    return {
        'provider_id': p.provider_id,
        'provider_type': p.provider_type,
        'display_name': p.display_name,
        'credentials_json': p.credentials_json,
        'is_active': p.is_active,
        'created_at': p.created_at.isoformat() if p.created_at else None
    }

@app.get('/api/providers/', response_model=List[ProviderOut])
def api_list_providers():
    ps = provider_dao.list_providers()
    out = []
    for p in ps:
        out.append({
            'provider_id': p.provider_id,
            'provider_type': p.provider_type,
            'display_name': p.display_name,
            'credentials_json': p.credentials_json,
            'is_active': p.is_active,
            'created_at': p.created_at.isoformat() if p.created_at else None
        })
    return out

@app.get('/api/providers/{provider_id}', response_model=ProviderOut)
def api_get_provider(provider_id: int):
    p = provider_dao.get_provider(provider_id)
    if not p:
        raise HTTPException(status_code=404, detail='not found')
    return {
        'provider_id': p.provider_id,
        'provider_type': p.provider_type,
        'display_name': p.display_name,
        'credentials_json': p.credentials_json,
        'is_active': p.is_active,
        'created_at': p.created_at.isoformat() if p.created_at else None
    }

@app.put('/api/providers/{provider_id}')
def api_update_provider(provider_id: int, payload: ProviderIn):
    p = provider_dao.update_provider(provider_id, payload.dict())
    if not p:
        raise HTTPException(status_code=404, detail='not found')
    return {'provider_id': p.provider_id}

@app.delete('/api/providers/{provider_id}')
def api_delete_provider(provider_id: int):
    ok = provider_dao.delete_provider(provider_id)
    if not ok:
        raise HTTPException(status_code=404, detail='not found')
    return {'deleted': True}

# EVENT-PROVIDERS (associations)
@app.post('/api/events/{event_id}/providers', status_code=201)
def api_add_provider_to_event(event_id: int, payload: EventProviderIn):
    data = payload.dict()
    ep = provider_dao.add_provider_to_event(event_id, data.get('provider_id'), data.get('provider_config_json'))
    return {'id': ep.id}

@app.get('/api/events/{event_id}/providers')
def api_list_event_providers(event_id: int):
    eps = provider_dao.list_event_providers(event_id)
    out = []
    for ep in eps:
        out.append({
            'id': ep.id,
            'event_id': ep.event_id,
            'provider_id': ep.provider_id,
            'provider_config_json': ep.provider_config_json,
            'is_active': ep.is_active,
            'created_at': ep.created_at.isoformat() if ep.created_at else None
        })
    return out

@app.delete('/api/events/{event_id}/providers/{ep_id}')
def api_remove_event_provider(event_id: int, ep_id: int):
    ok = provider_dao.remove_event_provider(ep_id)
    if not ok:
        raise HTTPException(status_code=404, detail='not found')
    return {'deleted': True}

# PUBLISH: publish scraped data for event to all configured providers
@app.post('/api/events/{event_id}/publish', response_model=List[PublishResult])
def api_publish_event(event_id: int):
    # find event
    e = event_dao.get_event(event_id)
    if not e:
        raise HTTPException(status_code=404, detail='event not found')

    eps = provider_dao.list_event_providers(event_id)
    results = []

    # placeholder publish logic: in future call provider-specific clients
    for ep in eps:
        try:
            # load provider
            p = provider_dao.get_provider(ep.provider_id)
            # provider-specific publish; for now we'll pretend success
            logger.info(f'Publishing event {event_id} to provider {p.provider_id} ({p.display_name})')
            # TODO: call provider client using p.credentials_json and ep.provider_config_json
            results.append({'provider_id': p.provider_id, 'status': 'ok', 'message': 'published (placeholder)'})
        except Exception as ex:
            logger.exception('failed to publish')
            results.append({'provider_id': ep.provider_id, 'status': 'error', 'message': str(ex)})

    return results

@app.get('/', response_class=HTMLResponse)
def root():
    html = """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Events Grasp Service</title>
        <meta name="viewport" content="width=device-width,initial-scale=1" />
        <style>
          body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial; background:#f7f9fb; color:#172b4d; padding:24px; }
          .container{ max-width:900px; margin:20px auto; background:#fff; border-radius:8px; padding:24px; box-shadow:0 6px 18px rgba(15,23,42,0.06);} 
          h1{ margin:0 0 8px; font-size:22px; }
          p.lead{ margin:8px 0 18px; color:#42526e }
          ul{ margin:8px 0 18px 20px }
          pre{ background:#0f1724; color:#e6eef8; padding:12px; border-radius:6px; overflow:auto }
          a.code{ font-family:monospace; color:#0b69ff }
          .note{ background:#f1f5f9; border-left:4px solid #60a5fa; padding:8px 12px; border-radius:4px }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Events Grasp — FastAPI Service</h1>
          <p class="lead">A small backend service to manage events, run scrapers and publish scraped content to multiple vector store providers (OpenAI, Pinecone, AWS, etc.).</p>

          <h3>Quick links</h3>
          <ul>
            <li><a href="/docs">OpenAPI (Swagger) UI</a> — interactive API docs.</li>
            <li><a href="/redoc">ReDoc</a> — alternate API docs.</li>
            <li><a href="/api/events/">/api/events/</a> — list/create events (JSON).</li>
            <li><a href="/api/providers/">/api/providers/</a> — list/create providers (JSON).</li>
            <li><a href="/api/events/1/providers">/api/events/{event_id}/providers</a> — manage event → provider associations.</li>
            <li><a href="/api/events/1/publish">/api/events/{event_id}/publish</a> — publish an event's scraped data to configured providers (POST).</li>
          </ul>

          <h3>Database</h3>
          <div class="note">
            By default this service uses SQLite for local development. Default file: <code>runtime_data/events.db</code> under the repo root.
            You can change the database by setting the <code>DATABASE_URL</code> environment variable (e.g. <code>postgresql://user:pass@host/dbname</code>).
          </div>

          <h3>Start the service</h3>
          <p>From the repository root you can run:</p>
          <pre>npm run backend:start</pre>
          <p>Or, activate your venv and run directly:</p>
          <pre>source ~/runtime_data/python_venvs/LLM-FineTuning-Solutions/bin/activate
python backend/microservices/events_grasp_service/run.py</pre>

          <h3>Example usage</h3>
          <p>Create an event (curl):</p>
          <pre>curl -X POST http://127.0.0.1:5000/api/events/ -H "Content-Type: application/json" -d '{"event_name":"AWS re:Invent 2025","source_url":"https://aws.amazon.com/blogs/aws/top-announcements-of-aws-reinvent-2025/"}'</pre>

          <h3>Notes & config files</h3>
          <ul>
            <li><code>backend-settings.json</code> — optional service config read at startup.</li>
            <li><code>portals-settings.json</code> — UI configuration (if present) for the frontend.</li>
            <li>Provider credentials are stored in the <code>providers</code> table (development). Use a secrets manager for production.</li>
          </ul>

          <h3>Where to go next</h3>
          <ul>
            <li>Open the API docs at <a href="/docs">/docs</a>.</li>
            <li>Use the Angular UI (if running) at <code>http://localhost:4200</code> to interact with events and providers visually.</li>
          </ul>

          <hr />
          <small>Service running as <code>events_grasp_service</code>. Backend organizational path: <code>backend/microservices/events_grasp_service</code>.</small>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)

if __name__ == '__main__':
    uvicorn.run('events_grasp_service.app:app', host='127.0.0.1', port=5000, reload=True)
