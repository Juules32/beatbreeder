from flask import Flask, render_template, request
from pydantic import ValidationError

from .generate import generate_grooves
from .models import GenerateRequest, GenerateResponse
from .store import store

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/generate")
def generate():
    try:
        request_json = GenerateRequest.model_validate_json(request.data)
    except ValidationError as e:
        return {"error": str(e)}, 400

    generation = store.get(request_json.gid) if request_json.gid else None
    grooves = generate_grooves(request_json.algorithm, generation, request_json.pids)
    return GenerateResponse(grooves=grooves).model_dump()

if __name__ == "__main__":
    app.run(debug=True)
