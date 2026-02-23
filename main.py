import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Property Tool Live</h1><p>Yield logic loading...</p>", 200

if __name__ == "__main__":
    # Railway's dynamic port assignment
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
