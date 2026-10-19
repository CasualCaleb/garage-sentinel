from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request
from routes.auth import get_current_user

router = APIRouter()

@router.get('/clips', response_class=HTMLResponse)
async def clips(request: Request):
    if await get_current_user(request) is None:
        return RedirectResponse(url="/login")

    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clip Gallery</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #0b0f14;
            --panel: #111821;
            --panel-soft: #151e28;
            --border: #233041;
            --text: #edf3f8;
            --muted: #8fa0b3;
            --accent: #7dd3fc;
            --accent-soft: rgba(125, 211, 252, 0.12);
            --green: #4ade80;
        }
        body {
            min-height: 100vh;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                         BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: radial-gradient(circle at top, rgba(37, 99, 235, .08), transparent 35%), var(--bg);
            color: var(--text);
            line-height: 1.6;
        }
        header {
            padding: 22px max(24px, calc((100vw - 1120px) / 2));
            border-bottom: 1px solid var(--border);
            background: rgba(11, 15, 20, .88);
            backdrop-filter: blur(16px);
        }
        .brand { display: flex; align-items: center; gap: 12px; }
        .logo {
            width: 40px; height: 40px; display: grid; place-items: center;
            background: var(--accent-soft); border: 1px solid rgba(125, 211, 252, .22);
            border-radius: 11px; font-size: 20px;
        }
        .brand strong { font-size: 15px; letter-spacing: .02em; }
        .brand span { display: block; font-size: 12px; color: var(--muted); }
        main { max-width: 1120px; margin: 0 auto; padding: 54px 24px 100px; }
        .eyebrow {
            font-size: 12px; letter-spacing: .13em; text-transform: uppercase;
            font-weight: 700; color: var(--accent); margin-bottom: 12px;
        }
        h1 { font-size: clamp(38px, 5vw, 60px); line-height: 1.08; letter-spacing: -.04em; }
        .intro { color: var(--muted); font-size: 16px; margin-top: 14px; margin-bottom: 32px; }
        .upload {
            display: block; text-align: center; cursor: pointer;
            padding: 42px 24px; border: 1px dashed #36506b;
            border-radius: 16px;
            background: linear-gradient(180deg, rgba(17, 24, 33, .96), rgba(13, 19, 26, .96));
            box-shadow: 0 16px 40px rgba(0,0,0,.15);
            transition: background .2s, border-color .2s, transform .2s;
            animation: fadeDown 0.35s ease-out;
        }
        .upload:hover, .upload.dragging {
            border-color: var(--accent); background: #172433; transform: translateY(-1px);
        }
        .upload-icon {
            width: 48px; height: 48px; display: grid; place-items: center;
            margin: 0 auto 17px; border-radius: 16px;
            border: 1px solid rgba(125,211,252,.22); background: var(--accent-soft);
            font-size: 28px;
        }
        .upload h2 { font-size: 21px; letter-spacing: -.02em; }
        .upload p { color: var(--muted); margin-top: 5px; font-size: 14px; }
        .formats {
            display: inline-block; margin-top: 20px; padding: 7px 12px;
            border-radius: 999px; border: 1px solid var(--border);
            color: #bcc8d4; background: var(--panel-soft);
            font-size: 12px; font-weight: 600;
        }
        #status { min-height: 24px; margin-top: 15px; font-size: 14px; color: var(--accent); }
        .section-heading {
            display: flex; justify-content: space-between; align-items: baseline;
            gap: 16px;
        }
        .section-heading h2 { font-size: 23px; letter-spacing: -.02em; }
        #clipCount { font-size: 13px; color: var(--muted); }
        .grid {
            display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
            gap: 18px; margin-top: 20px;
        }
        .card {
            overflow: hidden; border-radius: 14px; cursor: pointer;
            border: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(17,24,33,.95), rgba(13,19,26,.95));
            box-shadow: 0 16px 40px rgba(0,0,0,.14);
            transition: border-color .18s, transform .18s, box-shadow .18s;
            animation: fadeUpScale 0.35s ease-out;
        }
        .card:hover {
            border-color: #36506b; transform: scale(1.2);
            box-shadow: 0 18px 42px rgba(0,0,0,.3);
        }
        .preview {
            height: 160px;
            background: var(--panel-soft);
            display: grid;
            place-items: center;
        }
        .preview img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .filename {
            padding: 13px 14px; font-size: 13px; font-weight: 500;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        }
        .empty { grid-column: 1 / -1; color: var(--muted); font-size: 14px; padding: 22px 0; }
        @media (max-width: 600px) {
            main { padding: 38px 20px 70px; }
            header { padding: 18px 20px; }
            .upload { padding: 40px 18px; }
            .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
            .preview { height: 135px; }
        }
        .nav-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            width: 150px;
            padding: 10px 16px;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: var(--panel-soft);
            color: var(--text);
            font-size: 16px;
            font-weight: 600;
            text-decoration: none;
            white-space: nowrap;
            transition: background .2s, border-color .2s, transform .2s;
        }
        .nav-button:hover {
            background: var(--accent-soft);
            border-color: var(--accent);
            transform: translateY(-1px);
        }
        .nav-button:focus-visible {
            outline: 2px solid var(--accent);
            outline-offset: 3px;
        }
        .show-more-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 14px 22px;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: var(--panel-soft);
            color: var(--text);
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            text-decoration: none;
            white-space: nowrap;
            transition: background .2s, border-color .2s, transform .2s;
        }
        .show-more-button:hover {
            background: var(--accent-soft);
            border-color: var(--accent);
            transform: translateY(-1px);
        }
        .show-more-button:focus-visible {
            outline: 2px solid var(--accent);
            outline-offset: 3px;
        }
        .show-more-container {
            width: fit-content;
            padding: 24px;
            margin: 0 auto;
            border-radius: 14px;
            cursor: pointer;
            transition: border-color .18s, transform .18s, box-shadow .18s;
        }
        video {
            display: block;
            width: 100%;
            max-width: 900px;
            aspect-ratio: 16 / 9;
            margin: 32px auto;
            background: #0a0a0f;
            border: 1px solid rgba(255, 255, 255, 0.12);
            object-fit: contain;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        video:hover {
            box-shadow:
                0 18px 50px rgba(0, 0, 0, 0.4),
                0 0 35px rgba(120, 100, 255, 0.15);
        }
        
        video:focus {
            outline: 2px solid rgba(120, 100, 255, 0.5);
            outline-offset: 4px;
        }
        
        .preview video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            pointer-events: none;
        }
        
        @media (max-width: 600px) {
            video {
                margin: 20px auto;
                border-radius: 12px;
            }
        }
        .eyebrow-container {
            animation: fadeDown 0.35s ease-out;
        }

        @keyframes fadeDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes fadeUpScale {
            from {
                opacity: 0;
                scale: 0;
                transform: translateY(15px);
            }
            to {
                opacity: 1;
                scale: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="brand">
            <a class="nav-button" href="/">🏠 Home</a>
            <a class="nav-button" href="/gallery">📸 Photos</a>
            <a class="nav-button" href="/clips">📹 Clips</a>
            <a class="nav-button" href="/documentation">🗿 Docs</a>
            <a class="nav-button"
                onclick="logout(event)"
                style="margin-left: auto; color: #f87171; border-color: rgba(248, 113, 113, 0.25); cursor: pointer;">
                Logout
            </a>
        </div>
    </header>
    <main>
        <div class="eyebrow-container">
            <div class="eyebrow">Your clips</div>
            <h1>Every clip, one place.</h1>
            <p class="intro">Upload, browse, and relive your favourite moments.</p>
        </div class="eyebrow-container">
        
        <div class="upload" id="dropzone" role="button" tabindex="0" aria-label="Upload videos">
            <div class="upload-icon">📹️</div>
            <h2>Drop your clips here</h2>
            <p>Or click to browse your computer</p>
            <span class="formats">MP4</span>
            <input type="file" id="fileInput" accept=".mp4,video/mp4" multiple hidden>
        </div>
        <div id="status" role="status" aria-live="polite"></div>
        
        <div class="section-heading">
        <h2>My Clips</h2>
        <span id="clipCount"></span>
        </div>
        <div class="grid" id="fileGrid"></div>
        <div id="show-more" class="show-more-container">
            <button class=show-more-button onClick=loadVideos()>Show more</button>
        </div>
        
    </main>
    <script>
        const grid = document.getElementById('fileGrid');
        const clipCount = document.getElementById('clipCount');
        const status = document.getElementById('status');
        const dropzone = document.getElementById("dropzone");
        const fileInput = document.getElementById("fileInput");
    
        // Click to browse
        dropzone.addEventListener("click", () => fileInput.click());
    
        // Upload selected files
        fileInput.addEventListener("change", () => {
            uploadClips(fileInput.files);
        });
    
        // Drag and drop
        dropzone.addEventListener("dragover", (e) => {
            e.preventDefault();
        });
    
        dropzone.addEventListener("drop", (e) => {
            e.preventDefault();
            uploadClips(e.dataTransfer.files);
        });
    
        async function uploadClips(files) {
            for (const file of files) {
                const extension = file.name.split('.').pop().toLowerCase();
                if (!['mp4'].includes(extension)) {
                    status.textContent = '❌ Unsupported video format: ' + file.name;
                    return;
                }
                const data = new FormData();
                data.append('file', file);
                status.textContent = 'Uploading ' + file.name + '...';
                try {
                    const response = await fetch("/api/file", {
                        method: 'POST',
                        body: data
                    });
    
                    if (!response.ok) {
                        const error = await response.json().catch(() => ({}));
                        throw new Error('Upload failed: ' + (error.detail || response.statusText));
                    }
                } catch (error) {
                    status.textContent = error.message;
                    return;
                }
            }
            status.textContent = '✅ Videos uploaded successfully!';
            await getFiles();
            await loadVideos();
        }
        
        const visibleCount = 15;
        let files = [];
        let displayed = 0;
        
        async function getFiles() {
        const response = await fetch('/api/videos');
        if (!response.ok) throw new Error('Could not load videos');
                files = await response.json();
        }
        
        async function loadVideos() {
            try {
                if (files.length === 0) {
                    await getFiles();
                }
        
                for (const video of files.slice(displayed, displayed + visibleCount)) {
                    // Staggered effect
                    await new Promise(resolve => setTimeout(resolve, 100));
                
                    const name = typeof video === 'string' ? video : video.storage_name;
                    if (typeof name !== 'string') continue;
        
                    const displayName = typeof video === 'string'
                        ? video
                        : (video.filename || name);
        
                    const url = `/api/file/${encodeURIComponent(name)}`;
        
                    // Create card
                    const card = document.createElement('div');
                    card.className = 'card';
                    card.tabIndex = 0;
                    card.setAttribute('role', 'link');
        
                    // Create video preview
                    const preview = document.createElement('div');
                    preview.className = 'preview';
        
                    const videoElement = document.createElement('video');
                    videoElement.src = url;
                    videoElement.preload = 'metadata';
                    videoElement.muted = true;
                    videoElement.playsInline = true;
                    videoElement.loop = true;
        
                    // Display a frame near the beginning
                    videoElement.addEventListener('loadedmetadata', () => {
                        if (Number.isFinite(videoElement.duration) && videoElement.duration > 1) {
                            videoElement.currentTime = 1;
                        }
                    });
        
                    // Play on hover
                    card.addEventListener('mouseenter', () => {
                        videoElement.play().catch(() => {});
                    });
        
                    // Pause and reset when leaving
                    card.addEventListener('mouseleave', () => {
                        videoElement.pause();
                        videoElement.currentTime = 0;
                    });
        
                    preview.appendChild(videoElement);
        
                    // Filename
                    const label = document.createElement('div');
                    label.className = 'filename';
                    label.textContent = displayName;
                    label.title = displayName;
        
                    card.append(preview, label);
        
                    // Open full video on click
                    const openVideo = () => window.open(
                        url,
                        '_blank',
                        'noopener,noreferrer'
                    );
        
                    card.onclick = openVideo;
                    card.onkeydown = (event) => {
                        if (event.key === 'Enter') openVideo();
                    };
        
                    grid.appendChild(card);
                    displayed++;
                }
        
                // Update clip count
                clipCount.textContent = displayed + (displayed === 1 ? ' video' : ' videos');
        
                // Empty gallery
                if (displayed === 0) {
                    const empty = document.createElement('p');
                    empty.className = 'empty';
                    empty.textContent = '📹 No videos uploaded yet.';
                    grid.appendChild(empty);
                }
        
                // Remove Show More when all videos are displayed
                if (displayed >= files.length) {
                    document.getElementById('show-more')?.remove();
                }
        
            } catch (error) {
                status.textContent = error.message;
            }
        }
        async function logout(event) {
            event.preventDefault();
        
            try {
                const response = await fetch('/api/auth/logout', {
                    method: 'POST'
                });
        
                if (!response.ok) {
                    throw new Error('Logout failed');
                }
        
                window.location.href = '/login';
        
            } catch (error) {
                console.error(error);
            }
        }
        loadVideos();
    </script>
</body>
</html>"""

