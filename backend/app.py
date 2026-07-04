from flask import Flask
from flask_cors import CORS
from routes.ideas import ideas_bp
from routes.sketch import sketch_bp
from routes.analyze import analyze_bp

app = Flask(__name__)
CORS(
    app,
    origins=["http://localhost:5173"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

app.register_blueprint(ideas_bp)
app.register_blueprint(sketch_bp)
app.register_blueprint(analyze_bp, url_prefix="/api")

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True, port=5000)