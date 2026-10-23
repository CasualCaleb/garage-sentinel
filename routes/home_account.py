from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request
from routes.auth import get_current_user

router = APIRouter()

@router.get('/account', response_class=HTMLResponse)
async def clips(request: Request):
    if await get_current_user(request) is None:
        return RedirectResponse(url="/login")

    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account</title>
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
        .settings-section {
            margin-top: 36px;
            padding: 28px;
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 16px;
            animation: fadeDown 0.35s ease-out;
        }
        
        .section-heading {
            margin-bottom: 24px;
        }
        
        .section-heading h2 {
            font-size: 20px;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        .section-heading p {
            color: var(--muted);
            font-size: 13px;
            margin-top: 5px;
        }
        
        /* Connected accounts */
        
        .accounts-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .account-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding: 16px 18px;
            background: var(--panel-soft);
            border: 1px solid var(--border);
            border-radius: 12px;
        }
        
        .account-info {
            display: flex;
            align-items: center;
            gap: 14px;
            min-width: 0;
        }
        
        .account-info svg {
            width: 26px;
            height: 26px;
            flex-shrink: 0;
        }
        
        .account-details {
            min-width: 0;
        }
        
        .account-details strong {
            display: block;
            font-size: 14px;
        }
        
        .account-details span {
            display: block;
            color: var(--muted);
            font-size: 12px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .account-action {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            padding: 8px 14px;
            flex-shrink: 0;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--panel);
            color: var(--text);
            font-size: 12px;
            font-weight: 600;
            text-decoration: none;
            transition: background .2s, border-color .2s;
        }
        
        .account-action:hover {
            background: var(--accent-soft);
            border-color: var(--accent);
        }
        
        .account-connected {
            color: #4ade80;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
        }
        
        .account-connected svg {
            width: 16px;
            height: 16px;
            vertical-align: middle;
            margin-right: 4px;
        }
        
        @media (max-width: 600px) {
            .settings-section {
                padding: 20px;
            }
        
            .account-row {
                padding: 14px;
            }
        
            .account-action {
                padding: 8px 10px;
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
                style="width: 110px; margin-left: auto; color: #f87171; border-color: rgba(248, 113, 113, 0.25); cursor: pointer;">
                Logout
            </a>
            <a class="nav-button"
                href="/account"
                style="width: 110px; color: rgba(255, 255, 255); border-color: rgba(255, 255, 255, 0.25); cursor: pointer;">
                ⚙️ Account
            </a>
        </div>
    </header>
    <main>
        <div class="eyebrow-container">
            <h1 id="account-header"></h1>
            <p class="intro">Manage your profile, connected accounts, and preferences.</p>
        </div>
        <section class="settings-section">
            <div class="section-heading">
                <h2>Connected Accounts</h2>
                <p>Manage the accounts you use to sign in to Garage Sentinel.</p>
            </div>
    
            <div class="accounts-list" id="oauth-accounts">
                <!-- Populated by JavaScript -->
            </div>
        </section>
    </main>
    <script>
        const providers = [
            {
                id: 'google',
                name: 'Google',
                icon: `<svg viewBox="0 0 24 24" aria-hidden="true">
                    <path fill="#4285F4" d="M21.35 12.22c0-.66-.06-1.3-.17-1.91H12v3.62h5.24a4.48 4.48 0 0 1-1.94 2.94v2.45h3.14c1.84-1.69 2.91-4.18 2.91-7.1Z"/>
                    <path fill="#34A853" d="M12 21.75c2.62 0 4.82-.87 6.43-2.43l-3.14-2.45c-.87.58-1.98.93-3.29.93-2.53 0-4.67-1.71-5.44-4.01H3.32v2.52A9.75 9.75 0 0 0 12 21.75Z"/>
                    <path fill="#FBBC05" d="M6.56 13.79A5.86 5.86 0 0 1 6.25 12c0-.62.11-1.22.31-1.79V7.69H3.32A9.75 9.75 0 0 0 2.25 12c0 1.57.38 3.04 1.07 4.31l3.24-2.52Z"/>
                    <path fill="#EA4335" d="M12 6.2c1.42 0 2.7.49 3.7 1.44l2.78-2.78A9.32 9.32 0 0 0 12 2.25a9.75 9.75 0 0 0-8.68 5.44l3.24 2.52C7.33 7.91 9.47 6.2 12 6.2Z"/>
                </svg>`
            },
            {
                id: 'discord',
                name: 'Discord',
                icon: `<svg viewBox="0 0 24 24" aria-hidden="true">
                    <path fill="#5865F2" d="M19.73 5.05a18.7 18.7 0 0 0-4.65-1.45l-.57 1.16a17.3 17.3 0 0 0-5.02 0L8.92 3.6a18.7 18.7 0 0 0-4.65 1.45C1.33 9.43.54 13.71.94 17.93a18.7 18.7 0 0 0 5.71 2.87l1.23-2a12 12 0 0 1-1.94-.94l.48-.37c3.75 1.74 7.81 1.74 11.56 0l.48.37c-.62.36-1.26.67-1.94.94l1.23 2a18.7 18.7 0 0 0 5.71-2.87c.47-4.88-.8-9.12-3.73-12.88ZM8.65 15.37c-1.12 0-2.04-1.02-2.04-2.27 0-1.24.9-2.27 2.04-2.27 1.14 0 2.06 1.03 2.04 2.27 0 1.25-.9 2.27-2.04 2.27Zm6.7 0c-1.12 0-2.04-1.02-2.04-2.27 0-1.24.9-2.27 2.04-2.27 1.14 0 2.06 1.03 2.04 2.27 0 1.25-.9 2.27-2.04 2.27Z"/>
                </svg>`
            },
            {
                id: 'github',
                name: 'GitHub',
                icon: `<svg viewBox="0 0 24 24" aria-hidden="true">
                    <path fill="currentColor" d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56 0-.28-.01-1.02-.02-2-3.2.7-3.88-1.54-3.88-1.54-.52-1.33-1.28-1.68-1.28-1.68-1.05-.72.08-.71.08-.71 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.56-.29-5.26-1.28-5.26-5.7 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.47.11-3.06 0 0 .97-.31 3.16 1.18a11 11 0 0 1 5.76 0c2.2-1.49 3.16-1.18 3.16-1.18.63 1.59.23 2.77.11 3.06.74.81 1.19 1.84 1.19 3.1 0 4.43-2.71 5.4-5.29 5.69.41.35.78 1.04.78 2.1 0 1.52-.01 2.75-.01 3.13 0 .31.21.68.8.56A11.51 11.51 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5Z"/>
                </svg>`
            }
        ];
        
        async function loadConnectedAccounts() {
            const container = document.getElementById('oauth-accounts');
            container.textContent = 'Loading connected accounts...';
        
            try {
                const response = await fetch('/api/users/me');
        
                if (!response.ok) {
                    throw new Error('Unable to load account information');
                }
        
                const data = await response.json();
                const accounts = data.oauth_accounts || [];
        
                container.innerHTML = '';
        
                for (const provider of providers) {
                    const account = accounts.find(
                        account => account.provider === provider.id
                    );
        
                    const row = document.createElement('div');
                    row.className = 'account-row';
        
                    const info = document.createElement('div');
                    info.className = 'account-info';
                    info.innerHTML = provider.icon;
        
                    const details = document.createElement('div');
                    details.className = 'account-details';
        
                    const name = document.createElement('strong');
                    name.textContent = provider.name;
        
                    const description = document.createElement('span');
                    description.textContent = account
                        ? (account.provider_email || 'Account connected')
                        : 'Not connected';
        
                    details.append(name, description);
                    info.appendChild(details);
                    row.appendChild(info);
        
                    if (account) {
                        const status = document.createElement('div');
                        status.className = 'account-connected';
                        status.textContent = '✓ Connected';
                        row.appendChild(status);
                    } else {
                        const button = document.createElement('a');
                        button.className = 'account-action';
                        button.href = `/api/auth/login/${provider.id}`;
                        button.textContent = 'Connect';
                        row.appendChild(button);
                    }
        
                    container.appendChild(row);
                }
        
            } catch (error) {
                console.error(error);
                container.textContent = 'Unable to load connected accounts.';
            }
        }
        
        loadConnectedAccounts();
        
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
        async function loadUsername() {
            const response = await fetch("/api/users/me");
            const data = await response.json();
            
            console.log(data);
            
            document.getElementById("account-header").textContent = `${data.user.username}`;
        }
        loadUsername();
    </script>
</body>
</html>"""

