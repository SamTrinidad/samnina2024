from app import create_app
import os

# Create an instance of the Flask application
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)