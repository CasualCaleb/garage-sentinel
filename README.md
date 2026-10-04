# Garage Sentinel 🗿

Garage Sentinel is a small FastAPI app deployed to a **very normal laptop that has been stripped of dignity and repurposed into an Ubuntu server in my garage**.

The app itself is intentionally simple. The fun part is the deployment pipeline:

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

No manual SSH deployment. No pulling the repo by hand. No remembering which Python command starts the thing.

Just:

```bash
git push
```
and the garage laptop sorts itself out.

## Deployment Pipeline 🚀

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

## Production Deployment 🏭

The production Docker image is automatically built and published to:

```text
ghcr.io/casualcaleb/garage-sentinel:latest
```

After a successful build, the deployment job automatically:

1. Authenticates with GitHub Container Registry.
2. Pulls the newest Docker image.
3. Stops and removes the currently running container.
4. Starts a new container from the latest image.

## Updating Production 🔄

Make changes locally, then:

```bash
git add .
git commit -m "Describe the update"
git push
```

That's it.

GitHub Actions handles the rest.

## Current Deployment Architecture 🧠

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
