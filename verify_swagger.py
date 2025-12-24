from app import create_app
print("Importing app...")
try:
    app = create_app()
    print("App created successfully.")
    print("Blueprints:", list(app.blueprints.keys()))
    print("Swagger in extensions:", 'flasgger' in app.extensions) # It might use a different key
except Exception as e:
    print(f"Failed to create app: {e}")
    import traceback
    traceback.print_exc()
