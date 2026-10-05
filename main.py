from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

THERMAL_ZONE = Path("/sys/class/thermal/thermal_zone0/temp")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Garage Sentinel</title>

        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background:
                    radial-gradient(circle at 20% 20%, #172554 0%, transparent 35%),
                    radial-gradient(circle at 80% 80%, #3b0764 0%, transparent 35%),
                    #050505;
                color: white;
                font-family: Arial, Helvetica, sans-serif;
                overflow: hidden;
            }

            .glow {
                position: absolute;
                width: 500px;
                height: 500px;
                background: #2563eb;
                filter: blur(180px);
                opacity: 0.15;
                border-radius: 50%;
            }

            .card {
                position: relative;
                width: min(700px, 90%);
                padding: 50px;
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 24px;
                background: rgba(255,255,255,0.05);
                backdrop-filter: blur(18px);
                box-shadow:
                    0 30px 80px rgba(0,0,0,0.6),
                    inset 0 1px 0 rgba(255,255,255,0.08);
            }

            .status {
                display: inline-flex;
                align-items: center;
                gap: 10px;
                padding: 8px 14px;
                border-radius: 100px;
                background: rgba(34,197,94,0.12);
                border: 1px solid rgba(34,197,94,0.3);
                color: #86efac;
                font-size: 14px;
                margin-bottom: 30px;
            }

            .dot {
                width: 9px;
                height: 9px;
                border-radius: 50%;
                background: #22c55e;
                box-shadow: 0 0 15px #22c55e;
                animation: pulse 1.5s infinite;
            }

            @keyframes pulse {
                0%, 100% {
                    opacity: 1;
                    transform: scale(1);
                }

                50% {
                    opacity: 0.4;
                    transform: scale(0.75);
                }
            }

            h1 {
                font-size: clamp(42px, 7vw, 72px);
                letter-spacing: -3px;
                margin-bottom: 20px;
                background: linear-gradient(135deg, #ffffff, #93c5fd);
                -webkit-background-clip: text;
                color: transparent;
            }

            p {
                color: #a1a1aa;
                font-size: 18px;
                line-height: 1.7;
                margin-bottom: 35px;
            }

            .warning {
                color: #fca5a5;
                font-family: monospace;
                border-left: 3px solid #ef4444;
                padding-left: 16px;
                margin-bottom: 35px;
            }

            .buttons {
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
            }

            a {
                text-decoration: none;
                padding: 13px 20px;
                border-radius: 10px;
                font-weight: bold;
                transition: 0.2s;
            }

            .primary {
                background: white;
                color: black;
            }

            .primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 30px rgba(255,255,255,0.15);
            }

            .secondary {
                border: 1px solid rgba(255,255,255,0.15);
                color: white;
            }

            .secondary:hover {
                background: rgba(255,255,255,0.08);
            }

            footer {
                margin-top: 40px;
                font-family: monospace;
                color: #52525b;
                font-size: 12px;
            }
        </style>
    </head>

    <body>

        <div class="glow"></div>

        <div class="card">

            <div class="status">
                <div class="dot"></div>
                SYSTEM ONLINE
            </div>

            <h1>GARAGE<br>SENTINEL</h1>

            <p>
                A suspiciously overengineered server running from a laptop
                somewhere in Caleb's garage.
            </p>

            <div class="warning">
                WARNING: THE GARAGE SERVER HAS ACHIEVED SENTIENCE.<br>
                DO NOT UNPLUG IT.
            </div>

            <div class="buttons">
                <a class="primary" href="/api/temp">
                    CPU Temp
                </a>

                <a class="secondary" href="/docs">
                    API Docs
                </a>
            </div>

            <footer>
                GARAGE-SENTINEL // FASTAPI // STATUS: PROBABLY FINE
            </footer>

        </div>

    </body>
    </html>
    """

@app.get("/api/temp")
async def get_cpu_temp():
    try:
        raw_temp = THERMAL_ZONE.read_text().strip()
        temp_c = int(raw_temp) / 1000

        return {
            "cpu_temp_c": round(temp_c, 1)
        }

    except (FileNotFoundError, ValueError, PermissionError):
        raise HTTPException(
            status_code=500,
            detail="Unable to read CPU temperature"
        )


