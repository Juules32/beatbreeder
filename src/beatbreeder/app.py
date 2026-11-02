from flask import Flask, render_template, request
from pydantic import ValidationError

from .generate import create_ga
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

    if request_json.gid is None:
        ga = create_ga(request_json.algorithm)
        gid = store.add(ga)
    else:
        gid = request_json.gid
        ga = store.get(gid)
        if ga is None:
            return {"error": f"Unknown or expired generation id: {gid}"}, 404
        ga.evolve(request_json.pids)

    return GenerateResponse(gid=gid, grooves=ga.grooves()).model_dump()

if __name__ == "__main__":
    app.run(debug=True)
