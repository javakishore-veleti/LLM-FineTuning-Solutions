from flask import Flask
from backend.microservices.events_grasp_service.modules.api import register_api_blueprints
from modules.core.integrations.db import init_db


def create_app():
    app = Flask(__name__)
    # Load settings if present (optional)
    try:
        import json, os
        if os.path.exists('backend-settings.json'):
            with open('backend-settings.json') as f:
                app.config.update(json.load(f))
    except Exception:
        pass

    # init DB
    init_db()

    # register blueprints
    register_api_blueprints(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
