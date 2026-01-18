"""Runner script for events_grasp_service.
This script adds the microservices parent folder to PYTHONPATH so imports work when starting the service,
and runs uvicorn with the package module path `events_grasp_service.app:app`.
"""
import os
import sys
from pathlib import Path

# Ensure repo microservices parent directory is on sys.path
# If run from project root, this will add backend/microservices to sys.path
HERE = Path(__file__).resolve().parent
MICROSERVICES_PARENT = str(HERE.parent)
if MICROSERVICES_PARENT not in sys.path:
    sys.path.insert(0, MICROSERVICES_PARENT)

if __name__ == '__main__':
    try:
        import uvicorn
    except Exception as e:
        print('uvicorn not installed in current Python environment:', e)
        sys.exit(1)

    # Run uvicorn pointing to the package-local FastAPI app
    uvicorn.run('events_grasp_service.app:app', host='127.0.0.1', port=5000, reload=True)
