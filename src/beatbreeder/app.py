from flask import Flask, render_template, request
from pydantic import ValidationError

from .generate import generate_solutions
from .models import GenerateRequest, GenerateResponse
from .store import store

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/generate")
def generate():
    # e.g. {"algorithm": "random", "parents": []}
    
    try:
        request_json = GenerateRequest.model_validate_json(request.data)
    except ValidationError as e:
        return {"error": str(e)}, 400
    
    try:
        parents = [store.get(id) for id in request_json.parents]
    except KeyError as e:
        return {"error": f"Unknown or expired parent id: {e}"}, 404
    
    solutions = generate_solutions(request_json.algorithm, parents)
    return GenerateResponse(solutions=solutions).model_dump()

if __name__ == "__main__":
    app.run(debug=True)
