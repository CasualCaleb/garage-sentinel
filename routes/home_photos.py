from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get('/photos', response_class=HTMLResponse)
def photos():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Photo Gallery</title>
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
            padding: 48px 24px; border: 1px dashed #36506b;
            border-radius: 16px;
            background: linear-gradient(180deg, rgba(17, 24, 33, .96), rgba(13, 19, 26, .96));
            box-shadow: 0 16px 40px rgba(0,0,0,.15);
            transition: background .2s, border-color .2s, transform .2s;
        }
        .upload:hover, .upload.dragging {
            border-color: var(--accent); background: #172433; transform: translateY(-1px);
        }
        .upload-icon {
            width: 58px; height: 58px; display: grid; place-items: center;
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
            gap: 16px; margin-top: 37px;
        }
        .section-heading h2 { font-size: 23px; letter-spacing: -.02em; }
        #photoCount { font-size: 13px; color: var(--muted); }
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
        }
        .card:hover {
            border-color: #36506b; transform: translateY(-3px);
            box-shadow: 0 18px 42px rgba(0,0,0,.3);
        }
        .preview { height: 160px; background: var(--panel-soft); display: grid; place-items: center; }
        .preview img { width: 100%; height: 100%; object-fit: cover; }
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
        .home-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 10px 16px;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: var(--panel-soft);
            color: var(--text);
            font-size: 13px;
            font-weight: 600;
            text-decoration: none;
            white-space: nowrap;
            transition: background .2s, border-color .2s, transform .2s;
        }
        .home-button:hover {
            background: var(--accent-soft);
            border-color: var(--accent);
            transform: translateY(-1px);
        }
        .home-button:focus-visible {
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
    </style>
</head>
<body>
    <header>
        <div class="brand">
            <a class="home-button" href="/">⌂ Home</a>
            <div class="logo">📸</div>
            <div><strong>Photo Gallery</strong><span>Your personal photo collection</span></div>
        </div>
    </header>
    <main>
        <div class="eyebrow">Your collection</div>
        <h1>Every photo, one place.</h1>
        <p class="intro">Upload, browse, and revisit your favourite moments.</p>

        <div class="upload" id="dropzone" role="button" tabindex="0" aria-label="Upload photos">
            <div class="upload-icon">🖼️</div>
            <h2>Drop your photos here</h2>
            <p>Or click to browse your computer</p>
            <span class="formats">PNG · JPG · JPEG</span>
            <input type="file" id="fileInput" accept=".png,.jpg,.jpeg,image/png,image/jpeg" multiple hidden>
        </div>
        <div id="status" role="status" aria-live="polite"></div>

        <div class="section-heading">
            <h2>My Photos</h2>
            <span id="photoCount"></span>
        </div>
        <div class="grid" id="fileGrid"></div>
        <div id="show-more" class="show-more-container">
            <button class=show-more-button onClick=loadPhotos()>Show more</button>
        </div>
    </main>
    <script>
        const dropzone = document.getElementById('dropzone');
        const fileInput = document.getElementById('fileInput');
        const grid = document.getElementById('fileGrid');
        const status = document.getElementById('status');
        const photoCount = document.getElementById('photoCount');

        dropzone.onclick = () => fileInput.click();
        dropzone.onkeydown = (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                fileInput.click();
            }
        };
        fileInput.onchange = async () => {
            await uploadPhotos(fileInput.files);
            fileInput.value = '';
        };
        dropzone.ondragover = (event) => {
            event.preventDefault();
            dropzone.classList.add('dragging');
        };
        dropzone.ondragleave = () => dropzone.classList.remove('dragging');
        dropzone.ondrop = async (event) => {
            event.preventDefault();
            dropzone.classList.remove('dragging');
            await uploadPhotos(event.dataTransfer.files);
        };
        
        let visibleCount = 12;
        let files = [];
        let displayed = 0;
        
        async function getFiles() {
            const response = await fetch('/files');
            if (!response.ok) throw new Error('Could not load photos');
                    files = await response.json();
        }

        async function uploadPhotos(files) {
            for (const file of files) {
                const extension = file.name.split('.').pop().toLowerCase();
                if (!['png', 'jpg', 'jpeg'].includes(extension)) {
                    status.textContent = '❌ Unsupported photo format: ' + file.name;
                    return;
                }
                const data = new FormData();
                data.append('file', file);
                status.textContent = 'Uploading ' + file.name + '...';
                try {
                    const response = await fetch('/file', { method: 'POST', body: data });
                    if (!response.ok) {
                        const error = await response.json().catch(() => ({}));
                        throw new Error('Upload failed: ' + (error.detail || response.statusText));
                    }
                } catch (error) {
                    status.textContent = error.message;
                    return;
                }
            }
            status.textContent = '✅ Photos uploaded successfully!';
            await getFiles();
            await loadPhotos();
        }
        
        async function loadPhotos() {
            try {
                if (files.length === 0) {
                    await getFiles();
                }
                
                for (const photo of files.slice(displayed, displayed + visibleCount)) {
                    const name = typeof photo === 'string' ? photo : photo.storage_name;
                    if (typeof name !== 'string') continue;
                    const displayName = typeof photo === 'string' ? photo : (photo.filename || name);
                    const thumb_url = `/file/${encodeURIComponent(name)}?size=thumbnail`;
                    const original_url = `/file/${encodeURIComponent(name)}?`;
                    const card = document.createElement('div');
                    card.className = 'card';
                    card.tabIndex = 0;
                    card.setAttribute('role', 'link');
                    const preview = document.createElement('div');
                    preview.className = 'preview';
                    const img = document.createElement('img');
                    img.src = thumb_url;
                    img.alt = displayName;
                    img.loading = 'lazy';
                    preview.appendChild(img);
                    const label = document.createElement('div');
                    label.className = 'filename';
                    label.textContent = displayName;
                    label.title = displayName;
                    card.append(preview, label);
                    const openPhoto = () => window.open(original_url, '_blank', 'noopener,noreferrer');
                    card.onclick = openPhoto;
                    card.onkeydown = (event) => {
                        if (event.key === 'Enter') openPhoto();
                    };
                    grid.appendChild(card);
                    displayed++;
                }
                photoCount.textContent = displayed + (displayed === 1 ? ' photo' : ' photos');
                if (displayed === 0) {
                    const empty = document.createElement('p');
                    empty.className = 'empty';
                    empty.textContent = '📷 No photos uploaded yet.';
                    grid.appendChild(empty);
                }
            } catch (error) {
                status.textContent = error.message;
            }
            if (displayed === files.length) {
                document.getElementById('show-more')?.remove()
            }
        }
        loadPhotos();
    </script>
</body>
</html>"""

