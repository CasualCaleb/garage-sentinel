# Garage Sentinel 🗿

Garage Sentinel is a small FastAPI app deployed to a **very normal laptop that has been stripped of dignity and repurposed into an Ubuntu server in my garage**.

The app itself is intentionally simple. The fun part is the deployment pipeline:

## Deployment Pipeline 🚀

Every push to `main` automatically triggers the following process:

```text
Windows PC
    ↓
git push
    ↓
GitHub Actions
    ↓
Docker image build
    ↓
GitHub Container Registry
    ↓
Self-hosted GitHub runner
    ↓
Ubuntu laptop in the garage
    ↓
Old container replaced
    ↓
✅ New version live
```

No manual SSH deployment. No pulling the repo by hand.

Just:

```bash
git push
```
and the garage laptop sorts itself out.

## Stack 🧰

- Python
- FastAPI
- Uvicorn
- Docker
- GitHub Actions
- GitHub Container Registry
- Ubuntu Server
- Self-hosted GitHub Actions runner

## Run Locally 🧪

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the development server:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Run With Docker 🐳

Build the image:

```bash
docker build -t garage-sentinel .
```

Run the container:

```bash
docker run --rm -p 8000:8000 garage-sentinel
```

Then open:

```text
http://localhost:8000
```

## Updating Production 🔄

Make changes locally, then:

```bash
git add .
git commit -m "Describe the update"
git push
```

That's it.

GitHub Actions handles the rest.
