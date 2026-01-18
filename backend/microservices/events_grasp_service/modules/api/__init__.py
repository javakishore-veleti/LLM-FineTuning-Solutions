from importlib import import_module


def register_api_blueprints(app):
    """Discover and register blueprints under modules/api/*/routes.py"""
    import pkgutil
    import backend.microservices.events_grasp_service.modules.api as api_pkg

    package_path = api_pkg.__path__
    for finder, name, ispkg in pkgutil.iter_modules(package_path):
        try:
            mod = import_module(f"modules.api.{name}.routes")
            if hasattr(mod, 'bp'):
                app.register_blueprint(mod.bp)
        except Exception:
            # skip packages without routes
            continue
