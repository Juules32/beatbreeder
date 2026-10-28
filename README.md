# Beatbreeder

## Architecture
- Tone.js with CDN instead of NPM, so that building the frontend is not necessary
- JavaScript instead of TypeScript, for the same reason
- Flask for rapid development, and because having aesthetic visuals is not a priority

## Requirements
- Python 3.12+
- (Optional) uv or conda for easier package management
- (Optional) Node.js for better Tone.js intellisense

### uv setup
```sh
uv sync
uv run -m beatbreeder.app
```

### conda setup
```sh
conda create -n beatbreeder python=3.12 pip
conda activate beatbreeder
pip install -e .
python -m beatbreeder.app
```

## (Optional) Enable editor type-checking
`npm install` gets the Tone.js type definitions used by `jsconfig.json`.

## Explanation of stupid, seemingly unnecessary files
- `jsconfig.json`: Because Tone.js is in TS, it's needed to give the IDE type information
- `package.json` and `package-lock.json`: Node.js package files
- `pyproject.toml`: Modern replacement for `requirements.txt` files. Also makes imports easier (`import .models` instead of `import src.beatbreeder.models`).
- `uv.lock`: Created when using uv as python package manager
- `src/beatbreeder/__init__.py`: Tells python to treat the beatbreeder directory as a package
- `types.d.ts`: Exposes Tone.js types to `jsconfig.json`
