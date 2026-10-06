from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/documentation", response_class=HTMLResponse)
async def documentation():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >
        <title>Garage Sentinel API Docs</title>
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
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
                --green-soft: rgba(74, 222, 128, 0.12);
                --code: #080c11;
            }
            html {
                scroll-behavior: smooth;
            }
            body {
                font-family:
                    Inter,
                    ui-sans-serif,
                    system-ui,
                    -apple-system,
                    BlinkMacSystemFont,
                    "Segoe UI",
                    sans-serif;
                background:
                    radial-gradient(
                        circle at top,
                        rgba(37, 99, 235, 0.08),
                        transparent 35%
                    ),
                    var(--bg);
                color: var(--text);
                min-height: 100vh;
                line-height: 1.6;
            }
            a {
                color: inherit;
                text-decoration: none;
            }
            /* ========================================
               MAIN LAYOUT
            ======================================== */
            .layout {
                display: grid;
                grid-template-columns:
                    260px
                    minmax(0, 1fr);
                min-height: 100vh;
            }
            /* ========================================
               SIDEBAR
            ======================================== */
            .sidebar {
                position: sticky;
                top: 0;
                height: 100vh;
                border-right: 1px solid var(--border);
                background: rgba(11, 15, 20, 0.92);
                backdrop-filter: blur(16px);
                padding: 28px 22px;
            }
            .brand {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 34px;
            }
            .logo {
                width: 38px;
                height: 38px;
                display: grid;
                place-items: center;
                border-radius: 11px;
                background: var(--accent-soft);
                border:
                    1px solid
                    rgba(125, 211, 252, 0.22);
                font-size: 19px;
            }
            .brand h1 {
                font-size: 15px;
                font-weight: 700;
                letter-spacing: 0.02em;
            }
            .brand span {
                display: block;
                color: var(--muted);
                font-size: 12px;
                font-weight: 500;
            }
            .nav-label {
                color: #627386;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                margin:
                    24px
                    0
                    9px;
            }
            .nav-link {
                display: block;
                width: 100%;
                padding: 9px 10px;
                border: none;
                border-radius: 8px;
                color: var(--muted);
                background: transparent;
                font-family: inherit;
                font-size: 14px;
                text-align: left;
                cursor: pointer;
                transition:
                    color 0.15s ease,
                    background 0.15s ease;
            }
            .nav-link:hover {
                color: var(--text);
                background: var(--panel-soft);
            }
            .nav-link.active {
                color: var(--text);
                background: var(--accent-soft);
            }
            .nav-method {
                display: inline-block;
                min-width: 32px;
                margin-right: 5px;
                color: var(--green);
                font-family: monospace;
                font-size: 10px;
                font-weight: 800;
            }
            /* ========================================
               MAIN CONTENT
            ======================================== */
            .main {
                width: 100%;
                max-width: 1120px;
                padding:
                    60px
                    58px
                    100px;
            }
            /*
                Only one docs page is displayed at a time.
            */
            .doc-page {
                display: none;
                animation:
                    pageFade
                    0.22s ease;
            }
            .doc-page.active {
                display: block;
            }
            @keyframes pageFade {
                from {
                    opacity: 0;
                    transform: translateY(4px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            /* ========================================
               HERO
            ======================================== */
            .hero {
                margin-bottom: 55px;
            }
            .eyebrow {
                color: var(--accent);
                text-transform: uppercase;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 0.13em;
                margin-bottom: 12px;
            }
            .hero h2 {
                font-size:
                    clamp(
                        38px,
                        5vw,
                        64px
                    );
                line-height: 1.04;
                letter-spacing: -0.04em;
                margin-bottom: 18px;
            }
            .hero p {
                color: var(--muted);
                max-width: 720px;
                font-size: 17px;
            }
            .meta {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-top: 24px;
            }
            .pill {
                display: inline-flex;
                align-items: center;
                gap: 7px;
                padding: 7px 10px;
                border:
                    1px solid
                    var(--border);
                background: var(--panel);
                border-radius: 999px;
                color: #bcc8d4;
                font-size: 12px;
                font-weight: 600;
            }
            .dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: var(--green);
                box-shadow:
                    0
                    0
                    14px
                    var(--green);
            }
            /* ========================================
               PAGE HEADERS
            ======================================== */
            .page-header {
                margin-bottom: 32px;
            }
            .page-header h2 {
                font-size: 38px;
                letter-spacing: -0.035em;
                margin-bottom: 8px;
            }
            .page-header p {
                color: var(--muted);
                max-width: 700px;
                font-size: 15px;
            }
            /* ========================================
               SECTIONS
            ======================================== */
            section {
                margin-top: 45px;
            }
            .section-title {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 20px;
                margin-bottom: 18px;
            }
            .section-title h3 {
                font-size: 23px;
                letter-spacing: -0.02em;
            }
            .section-title p {
                color: var(--muted);
                font-size: 13px;
            }
            /* ========================================
               ENDPOINT CARDS
            ======================================== */
            .card {
                border:
                    1px solid
                    var(--border);
                background:
                    linear-gradient(
                        180deg,
                        rgba(17, 24, 33, 0.95),
                        rgba(13, 19, 26, 0.95)
                    );
                border-radius: 14px;
                overflow: hidden;
                margin-bottom: 18px;
                box-shadow:
                    0
                    16px
                    40px
                    rgba(0, 0, 0, 0.2);
            }
            .endpoint-header {
                padding: 20px 22px;
                display: flex;
                align-items: center;
                gap: 13px;
                border-bottom:
                    1px solid
                    var(--border);
            }
            .method {
                font-family: monospace;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: 0.07em;
                color: var(--green);
                border:
                    1px solid
                    rgba(74, 222, 128, 0.25);
                background: var(--green-soft);
                padding: 6px 8px;
                border-radius: 7px;
            }
            .path {
                font-family:
                    "SFMono-Regular",
                    Consolas,
                    monospace;
                font-size: 15px;
                font-weight: 600;
            }
            .endpoint-body {
                padding: 22px;
            }
            .endpoint-body p {
                color: var(--muted);
                margin-bottom: 16px;
            }
            .label {
                font-size: 11px;
                color: #718297;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                margin:
                    18px
                    0
                    8px;
            }
            pre {
                background: var(--code);
                border:
                    1px solid
                    #182331;
                border-radius: 10px;
                padding: 17px;
                overflow-x: auto;
                font-family:
                    "SFMono-Regular",
                    Consolas,
                    monospace;
                font-size: 13px;
                color: #cfe8f5;
                line-height: 1.7;
            }
            .response-row {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-top: 15px;
            }
            .status {
                font-family: monospace;
                color: var(--green);
                background: var(--green-soft);
                border:
                    1px solid
                    rgba(74, 222, 128, 0.2);
                border-radius: 6px;
                padding: 4px 7px;
                font-size: 12px;
                font-weight: 700;
            }
            .response-type {
                color: var(--muted);
                font-size: 13px;
            }
            /* ========================================
               LINK CARDS
            ======================================== */
            .link-card {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 20px;
                padding: 16px 18px;
                border:
                    1px solid
                    var(--border);
                background: var(--panel);
                border-radius: 10px;
                margin-top: 10px;
                transition:
                    border-color 0.15s ease,
                    transform 0.15s ease;
            }
            .link-card:hover {
                border-color: #36506b;
                transform:
                    translateY(-1px);
            }
            .link-card strong {
                font-size: 14px;
            }
            .link-card span {
                color: var(--muted);
                font-size: 13px;
            }
            .arrow {
                color: var(--accent);
                font-size: 18px;
            }
            /* ========================================
               INFO BLOCKS
            ======================================== */
            .info-grid {
                display: grid;
                grid-template-columns:
                    repeat(
                        auto-fit,
                        minmax(200px, 1fr)
                    );
                gap: 14px;
                margin-top: 24px;
            }
            .info-card {
                padding: 18px;
                border:
                    1px solid
                    var(--border);
                border-radius: 12px;
                background: var(--panel);
            }
            .info-card .info-label {
                color: #65788d;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                margin-bottom: 6px;
            }
            .info-card .info-value {
                color: var(--text);
                font-size: 15px;
                font-weight: 600;
            }
            /* ========================================
               FOOTER
            ======================================== */
            footer {
                margin-top: 80px;
                border-top:
                    1px solid
                    var(--border);
                padding-top: 25px;
                color: #617386;
                font-size: 12px;
            }
            /* ========================================
               MOBILE
            ======================================== */
            @media (max-width: 800px) {
                .layout {
                    display: block;
                }
                .sidebar {
                    position: relative;
                    width: 100%;
                    height: auto;
                    border-right: none;
                    border-bottom:
                        1px solid
                        var(--border);
                }
                .sidebar nav {
                    display: flex;
                    gap: 6px;
                    overflow-x: auto;
                    padding-bottom: 4px;
                }
                .nav-label {
                    display: none;
                }
                .nav-link {
                    width: auto;
                    white-space: nowrap;
                }
                .main {
                    padding:
                        40px
                        22px
                        80px;
                }
                .hero h2 {
                    font-size: 42px;
                }
            }
        </style>
    </head>
    <body>
        <div class="layout">
            <!-- =====================================
                 SIDEBAR
            ====================================== -->
            <aside class="sidebar">
                <div class="brand">
                    <div class="logo">
                        🗿
                    </div>
                    <div>
                        <h1>
                            Garage Sentinel
                        </h1>
                        <span>
                            Developer API
                        </span>
                    </div>
                </div>
                <nav>
                    <div class="nav-label">
                        Overview
                    </div>
                    <button
                        class="nav-link active"
                        onclick="showPage('introduction', this)"
                    >
                        Introduction
                    </button>
                    <button
                        class="nav-link"
                        onclick="showPage('openapi', this)"
                    >
                        OpenAPI
                    </button>
                    <div class="nav-label">
                        Endpoints
                    </div>
                    <button
                        class="nav-link"
                        onclick="showPage('home', this)"
                    >
                        <span class="nav-method">
                            GET
                        </span>
                        /
                    </button>
                    <button
                        class="nav-link"
                        onclick="showPage('telemetry', this)"
                    >
                        <span class="nav-method">
                            GET
                        </span>
                        /api/telemetry
                    </button>
                </nav>
            </aside>
            <!-- =====================================
                 MAIN CONTENT
            ====================================== -->
            <main class="main">
                <!-- =================================
                     INTRODUCTION
                ================================== -->
                <div
                    id="introduction"
                    class="doc-page active"
                >
                    <div class="hero">
                        <div class="eyebrow">
                            Garage Sentinel API
                        </div>
                        <h2>
                            Your garage has an API now.
                        </h2>
                        <p>
                            A lightweight FastAPI service running on a
                            very determined Ubuntu laptop somewhere in
                            a garage.
                            Query system telemetry, monitor services,
                            and eventually boss around whatever
                            questionable hardware gets connected next.
                        </p>
                        <div class="meta">
                            <div class="pill">
                                <span class="dot"></span>
                                API Online
                            </div>
                            <div class="pill">
                                v0.1.0
                            </div>
                            <div class="pill">
                                OpenAPI 3.1
                            </div>
                            <div class="pill">
                                FastAPI
                            </div>
                        </div>
                    </div>
                    <section>
                        <div class="section-title">
                            <div>
                                <h3>
                                    Welcome
                                </h3>
                                <p>
                                    The extremely necessary API
                                    powering Garage Sentinel.
                                </p>
                            </div>
                        </div>
                        <div class="card">
                            <div class="endpoint-body">
                                <p>
                                    Garage Sentinel provides a simple
                                    HTTP API for interacting with the
                                    systems, telemetry, devices, and
                                    services running around the garage.
                                </p>
                                <p>
                                    The API currently exposes host
                                    telemetry from the Ubuntu server,
                                    with support for additional services
                                    and hardware planned as the project
                                    grows.
                                </p>
                                <div class="info-grid">
                                    <div class="info-card">
                                        <div class="info-label">
                                            Protocol
                                        </div>
                                        <div class="info-value">
                                            HTTP / JSON
                                        </div>
                                    </div>
                                    <div class="info-card">
                                        <div class="info-label">
                                            Framework
                                        </div>
                                        <div class="info-value">
                                            FastAPI
                                        </div>
                                    </div>
                                    <div class="info-card">
                                        <div class="info-label">
                                            Version
                                        </div>
                                        <div class="info-value">
                                            0.1.0
                                        </div>
                                    </div>
                                    <div class="info-card">
                                        <div class="info-label">
                                            Status
                                        </div>
                                        <div class="info-value">
                                            Operational
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>
                    <footer>
                        Garage Sentinel API · v0.1.0 ·
                        Running somewhere between production
                        infrastructure and a laptop on a shelf
                        in the garage.
                    </footer>
                </div>
                <!-- =================================
                     OPENAPI
                ================================== -->
                <div
                    id="openapi"
                    class="doc-page"
                >
                    <div class="page-header">
                        <div class="eyebrow">
                            Specification
                        </div>
                        <h2>
                            OpenAPI
                        </h2>
                        <p>
                            Garage Sentinel automatically publishes
                            its machine-readable OpenAPI specification.
                        </p>
                    </div>
                    <section>
                        <div class="section-title">
                            <div>
                                <h3>
                                    OpenAPI Specification
                                </h3>
                                <p>
                                    Generated automatically by FastAPI.
                                </p>
                            </div>
                        </div>
                        <a
                            class="link-card"
                            href="/openapi.json"
                            target="_blank"
                        >
                            <div>
                                <strong>
                                    /openapi.json
                                </strong>
                                <br>
                                <span>
                                    View the generated OpenAPI schema
                                </span>
                            </div>
                            <div class="arrow">
                                ↗
                            </div>
                        </a>
                    </section>
                    <section>
                        <div class="card">
                            <div class="endpoint-body">
                                <div class="label">
                                    Specification
                                </div>
                                <pre>OpenAPI 3.1.0</pre>
                                <div class="label">
                                    Content Type
                                </div>
                                <pre>application/json</pre>
                            </div>
                        </div>
                    </section>
                    <footer>
                        Garage Sentinel API · OpenAPI 3.1
                    </footer>
                </div>
                <!-- =================================
                     HOME ENDPOINT
                ================================== -->
                <div
                    id="home"
                    class="doc-page"
                >
                    <div class="page-header">
                        <div class="eyebrow">
                            Endpoint
                        </div>
                        <h2>
                            Home
                        </h2>
                        <p>
                            Returns the primary Garage Sentinel
                            application page.
                        </p>
                    </div>
                    <div class="card">
                        <div class="endpoint-header">
                            <span class="method">
                                GET
                            </span>
                            <span class="path">
                                /
                            </span>
                        </div>
                        <div class="endpoint-body">
                            <p>
                                Returns the Garage Sentinel homepage.
                            </p>
                            <div class="label">
                                Parameters
                            </div>
                            <p>
                                This endpoint does not require any
                                parameters.
                            </p>
                            <div class="label">
                                Request
                            </div>
                            <pre>GET / HTTP/1.1
    Host: garage-sentinel</pre>
                            <div class="label">
                                Response
                            </div>
                            <div class="response-row">
                                <span class="status">
                                    200
                                </span>
                                <span class="response-type">
                                    text/html
                                </span>
                            </div>
                            <div class="label">
                                Example Response
                            </div>
                            <pre>&lt;!DOCTYPE html&gt;
    &lt;html lang="en"&gt;
        ...
    &lt;/html&gt;</pre>
                        </div>
                    </div>
                    <footer>
                        Garage Sentinel API · GET /
                    </footer>
                </div>
                <!-- =================================
                     TELEMETRY ENDPOINT
                ================================== -->
                <div
                    id="telemetry"
                    class="doc-page"
                >
                    <div class="page-header">
                        <div class="eyebrow">
                            Endpoint
                        </div>
                        <h2>
                            Telemetry
                        </h2>
                        <p>
                            Retrieve live system statistics from the
                            Linux host running Garage Sentinel.
                        </p>
                    </div>
                    <div class="card">
                        <div class="endpoint-header">
                            <span class="method">
                                GET
                            </span>
                            <span class="path">
                                /api/telemetry
                            </span>
                        </div>
                        <div class="endpoint-body">
                            <p>
                                Returns current CPU, memory, and
                                system telemetry collected directly
                                from the Ubuntu host.
                            </p>
                            <div class="label">
                                Parameters
                            </div>
                            <p>
                                This endpoint does not require any
                                parameters.
                            </p>
                            <div class="label">
                                Request
                            </div>
                            <pre>GET /api/telemetry HTTP/1.1
    Host: garage-sentinel
    Accept: application/json</pre>
                            <div class="label">
                                Response
                            </div>
                            <div class="response-row">
                                <span class="status">
                                    200
                                </span>
                                <span class="response-type">
                                    application/json
                                </span>
                            </div>
                            <div class="label">
                                Example Response
                            </div>
                            <pre>{
        "CPU": {
            "vendor_id": "GenuineIntel",
            "model_name": "Intel(R) Core(TM) i7-2630QM CPU @ 2.00GHz",
            "cpu_frequency_mhz": 800,
            "cpu_temp_c": 40
        },
        "MEMORY": {
            "mem_total_kb": 16352920,
            "mem_free_kb": 13535784,
            "mem_available_kb": 15479248,
            "mem_used_kb": 873672,
            "mem_usage_percent": 5.34
        },
        "SYSTEM": {
            "uptime_seconds": 131856.22,
            "load_15_min": 0.04
        }
    }</pre>
                        </div>
                    </div>
                    <section>
                        <div class="section-title">
                            <div>
                                <h3>
                                    Response Fields
                                </h3>
                                <p>
                                    Current host telemetry categories.
                                </p>
                            </div>
                        </div>
                        <div class="info-grid">
                            <div class="info-card">
                                <div class="info-label">
                                    CPU
                                </div>
                                <div class="info-value">
                                    Processor information,
                                    frequency and temperature
                                </div>
                            </div>
                            <div class="info-card">
                                <div class="info-label">
                                    Memory
                                </div>
                                <div class="info-value">
                                    RAM capacity,
                                    availability and usage
                                </div>
                            </div>
                            <div class="info-card">
                                <div class="info-label">
                                    System
                                </div>
                                <div class="info-value">
                                    Uptime and Linux load average
                                </div>
                            </div>
                        </div>
                    </section>
                    <footer>
                        Garage Sentinel API · GET /api/telemetry
                    </footer>
                </div>
            </main>
        </div>
        <!-- =========================================
             JAVASCRIPT
        ========================================== -->
        <script>
            function showPage(pageId, clickedLink) {
                /*
                    Hide every documentation page.
                */
                document
                    .querySelectorAll(".doc-page")
                    .forEach(page => {
                        page.classList.remove("active");
                    });
                /*
                    Remove the highlighted state
                    from every sidebar item.
                */
                document
                    .querySelectorAll(".nav-link")
                    .forEach(link => {
                        link.classList.remove("active");
                    });
                /*
                    Show the selected page.
                */
                const selectedPage =
                    document.getElementById(pageId);
                if (selectedPage) {
                    selectedPage.classList.add("active");
                }
                /*
                    Highlight the sidebar item
                    that was clicked.
                */
                if (clickedLink) {
                    clickedLink.classList.add("active");
                }
                /*
                    Bring the new page back to the top
                    on mobile / smaller screens.
                */
                window.scrollTo({
                    top: 0,
                    behavior: "smooth"
                });
                /*
                    Update the URL hash without
                    refreshing the page.
                    Example:
                    /docs#telemetry
                */
                history.replaceState(
                    null,
                    "",
                    "#" + pageId
                );
            }
            /*
                If somebody directly visits:
                /docs#telemetry
                open the correct section automatically.
            */
            window.addEventListener(
                "DOMContentLoaded",
                () => {
                    const pageId =
                        window.location.hash
                            .replace("#", "");
                    if (!pageId) {
                        return;
                    }
                    const page =
                        document.getElementById(pageId);
                    if (!page) {
                        return;
                    }
                    const links =
                        document.querySelectorAll(
                            ".nav-link"
                        );
                    let matchingLink = null;
                    links.forEach(link => {
                        const onclick =
                            link.getAttribute("onclick");
                        if (
                            onclick &&
                            onclick.includes(
                                "'" + pageId + "'"
                            )
                        ) {
                            matchingLink = link;
                        }
                    });
                    showPage(
                        pageId,
                        matchingLink
                    );
                }
            );
        </script>
    </body>
    </html>
    """