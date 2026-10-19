from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request
from routes.auth import get_current_user

router = APIRouter()

@router.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    if await get_current_user(request) is not None:
        return RedirectResponse(url="/gallery")

    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="color-scheme" content="dark">
    <title>Sign In | Garage Sentinel</title>
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
        }
        body {
            min-height: 100vh;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                         BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: radial-gradient(circle at top, rgba(37, 99, 235, .08), transparent 45%), var(--bg);
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
            background: var(--accent-soft); border: 1px solid rgba(125,211,252,.22);
            border-radius: 11px; font-size: 20px;
        }
        .brand strong { font-size: 15px; letter-spacing: .02em; }
        .brand span { display: block; font-size: 12px; color: var(--muted); }
        main {
            min-height: calc(100vh - 400px);
            display: grid;
            place-items: center;
            padding: 60px 20px;
        }
        .content { width: 100%; max-width: 430px; animation: fadeUp .4s ease-out both; }
        .intro { text-align: center; margin-bottom: 28px; }
        .eyebrow {
            color: var(--accent); font-size: 12px; font-weight: 700;
            text-transform: uppercase; letter-spacing: .13em; margin-bottom: 12px;
        }
        h1 { font-size: clamp(34px, 5vw, 44px); line-height: 1.1; letter-spacing: -.04em; }
        .subtitle { margin-top: 13px; font-size: 15px; color: var(--muted); }
        .panel {
            border: 1px solid var(--border);
            border-radius: 16px;
            background: linear-gradient(180deg, rgba(17,24,33,.96), rgba(13,19,26,.96));
            box-shadow: 0 16px 40px rgba(0,0,0,.16);
            padding: 30px;
        }
        .panel h2 { font-size: 18px; letter-spacing: -.02em; margin-bottom: 5px; }
        .panel p { color: var(--muted); font-size: 13px; margin-bottom: 24px; }
        .oauth-button {
            display: flex; align-items: center; justify-content: center; gap: 12px;
            width: 100%; padding: 14px 18px; margin-top: 12px;
            border: 1px solid var(--border); border-radius: 10px;
            background: var(--panel-soft); color: var(--text);
            text-decoration: none; font-size: 15px; font-weight: 600;
            transition: background .2s, border-color .2s, transform .2s, box-shadow .2s;
        }
        .oauth-button:hover {
            background: var(--accent-soft); border-color: var(--accent);
            transform: translateY(-2px); box-shadow: 0 10px 28px rgba(0,0,0,.18);
        }
        .oauth-button:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
        .oauth-button svg { width: 20px; height: 20px; flex: none; }
        .footer-note { text-align: center; color: var(--muted); font-size: 12px; margin-top: 22px; }
        .home-link { color: var(--accent); text-decoration: none; }
        .home-link:hover { text-decoration: underline; }
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @media (max-width: 600px) {
            header { padding: 18px 20px; }
            .panel { padding: 24px 20px; }
        }
        @media (prefers-reduced-motion: reduce) {
            .content { animation: none; }
            .oauth-button { transition: none; }
        }
    </style>
</head>
<body>
    <header>
        <div class="brand">
            <div class="logo" aria-hidden="true">🛠️</div>
            <div>
                <strong>Garage Sentinel</strong>
                <span>Your garage, connected.</span>
            </div>
        </div>
    </header>
    <main>
        <div class="content">
            <div class="intro">
                <div class="eyebrow">Welcome back</div>
                <h1>Sign in to continue.</h1>
                <p class="subtitle">Choose an account to access your drive.</p>
            </div>
            <section class="panel" aria-labelledby="sign-in-title">
                <h2 id="sign-in-title">Continue with</h2>
                <p>Securely sign in with one of your connected accounts.</p>
                <a class="oauth-button" href="/api/auth/login/google">
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path fill="#4285F4" d="M21.35 12.22c0-.66-.06-1.3-.17-1.91H12v3.62h5.24a4.48 4.48 0 0 1-1.94 2.94v2.45h3.14c1.84-1.69 2.91-4.18 2.91-7.1Z"/>
                        <path fill="#34A853" d="M12 21.75c2.62 0 4.82-.87 6.43-2.43l-3.14-2.45c-.87.58-1.98.93-3.29.93-2.53 0-4.67-1.71-5.44-4.01H3.32v2.52A9.75 9.75 0 0 0 12 21.75Z"/>
                        <path fill="#FBBC05" d="M6.56 13.79A5.86 5.86 0 0 1 6.25 12c0-.62.11-1.22.31-1.79V7.69H3.32A9.75 9.75 0 0 0 2.25 12c0 1.57.38 3.04 1.07 4.31l3.24-2.52Z"/>
                        <path fill="#EA4335" d="M12 6.2c1.42 0 2.7.49 3.7 1.44l2.78-2.78A9.32 9.32 0 0 0 12 2.25a9.75 9.75 0 0 0-8.68 5.44l3.24 2.52C7.33 7.91 9.47 6.2 12 6.2Z"/>
                    </svg>
                    Continue with Google
                </a>
                <a class="oauth-button" href="/api/auth/login/discord">
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path fill="#5865F2" d="M19.73 5.05a18.7 18.7 0 0 0-4.65-1.45l-.57 1.16a17.3 17.3 0 0 0-5.02 0L8.92 3.6a18.7 18.7 0 0 0-4.65 1.45C1.33 9.43.54 13.71.94 17.93a18.7 18.7 0 0 0 5.71 2.87l1.23-2a12 12 0 0 1-1.94-.94l.48-.37c3.75 1.74 7.81 1.74 11.56 0l.48.37c-.62.36-1.26.67-1.94.94l1.23 2a18.7 18.7 0 0 0 5.71-2.87c.47-4.88-.8-9.12-3.73-12.88ZM8.65 15.37c-1.12 0-2.04-1.02-2.04-2.27 0-1.24.9-2.27 2.04-2.27 1.14 0 2.06 1.03 2.04 2.27 0 1.25-.9 2.27-2.04 2.27Zm6.7 0c-1.12 0-2.04-1.02-2.04-2.27 0-1.24.9-2.27 2.04-2.27 1.14 0 2.06 1.03 2.04 2.27 0 1.25-.9 2.27-2.04 2.27Z"/>
                    </svg>
                    Continue with Discord
                </a>
            </section>
            <div class="footer-note">Back to <a class="home-link" href="/">home</a></div>
        </div>
    </main>
</body>
</html>"""
