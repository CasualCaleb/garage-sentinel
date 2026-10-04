# Garage Sentinel

Garage Sentinel is a small FastAPI application used to experiment with Docker, GitHub Actions, container registries, and automated deployment to a self-hosted Ubuntu server.

The important bit isn't the app itself — it's the deployment pipeline.

## Deployment Pipeline

Every push to `main` automatically triggers the following process:

```text
Local Development
       ↓
    git push
       ↓
GitHub Actions
       ↓
Build Docker Image
       ↓
GitHub Container Registry
       ↓
Self-Hosted GitHub Runner
       ↓
Ubuntu Garage Server
       ↓
Pull Latest Image
       ↓
Replace Running Container
       ↓
New Version Live
```

Once code is pushed, no SSH or manual deployment is required.

## Stack

- Python
- FastAPI
- Uvicorn
- Docker
- GitHub Actions
- GitHub Container Registry
- Ubuntu Server
- Self-hosted GitHub Actions runner

## Project Structure

```text
garage-sentinel/
├── .github/
│   └── workflows/
│       └── docker-publish.yml
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Run Locally

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

## Run With Docker

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

## Production Deployment

The production Docker image is automatically built and published to:

```text
ghcr.io/casualcaleb/garage-sentinel:latest
```

The Ubuntu server is registered as a self-hosted GitHub Actions runner.

After a successful build, the deployment job automatically:

1. Authenticates with GitHub Container Registry.
2. Pulls the newest Docker image.
3. Stops and removes the currently running container.
4. Starts a new container from the latest image.

The production container runs with:

```text
--restart unless-stopped
```

so the application automatically returns after a server reboot as long as Docker starts normally.

## Updating Production

Make changes locally, then:

```bash
git add .
git commit -m "Describe the update"
git push
```

That's it.

GitHub Actions handles the rest.

## Current Deployment Architecture

```text
GitHub Repository
      │
      │ push to main
      ▼
GitHub Actions Runner
      │
      │ docker build
      ▼
GitHub Container Registry
      │
      │ docker pull
      ▼
Ubuntu Garage Server
      │
      ▼
garage-sentinel container
      │
      ▼
FastAPI
```

## Notes

Application source code does not need to be cloned onto the production Ubuntu server.

The server only needs:

- Docker
- The GitHub Actions self-hosted runner
- Access to GitHub Container Registry

The Docker image contains the application and its Python dependencies.

Persistent application data should be stored outside the container using Docker volumes or bind mounts rather than inside the container filesystem.

---

**GARAGE SENTINEL // STATUS: PROBABLY FINE**
