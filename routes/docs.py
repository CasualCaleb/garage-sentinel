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
    
            <aside class="sidebar">
                <div class="brand">
                    <div class="logo">🗿</div>
                    <div>
                        <h1>Garage Sentinel</h1>
                        <span>Developer API</span>
                    </div>
                </div>
    
                <nav>
                    <div class="nav-label">Endpoints</div>
    
                    <div id="endpoint-nav"></div>
                </nav>
            </aside>
    
            <main class="main">
    
                <!-- Keep your existing introduction page here -->
    
                <!-- Keep your existing OpenAPI page here -->
    
                <!-- Endpoint pages generated from JSON -->
                <div id="endpoint-pages"></div>
    
            </main>
        </div>
    

        <script>
            function showPage(pageId, clickedLink) {
                const selectedPage = document.getElementById(pageId);
        
                if (!selectedPage?.classList.contains("doc-page")) {
                    return;
                }
        
                document.querySelectorAll(".doc-page").forEach(page => {
                    page.classList.remove("active");
                });
        
                document.querySelectorAll(".nav-link").forEach(link => {
                    link.classList.remove("active");
                });
        
                selectedPage.classList.add("active");
                clickedLink?.classList.add("active");
        
                history.replaceState(null, "", "#" + pageId);
        
                window.scrollTo({
                    top: 0,
                    behavior: "smooth"
                });
            }
        
            // Create an element with optional class and text.
            function createElement(tag, className = "", text = null) {
                const element = document.createElement(tag);
        
                if (className) {
                    element.className = className;
                }
        
                if (text !== null && text !== undefined) {
                    element.textContent = String(text);
                }
        
                return element;
            }
        
            // Create a documentation label.
            function createLabel(text) {
                return createElement("div", "label", text);
            }
        
            // Create a formatted code block.
            function createCodeBlock(content) {
                const pre = createElement("pre");
        
                pre.textContent = typeof content === "string"
                    ? content
                    : JSON.stringify(content, null, 4);
        
                return pre;
            }
        
            // Create a response status and content-type row.
            function createResponseRow(endpoint) {
                const row = createElement("div", "response-row");
        
                const status = createElement(
                    "span",
                    "status",
                    endpoint.status ?? 200
                );
        
                const type = createElement(
                    "span",
                    "response-type",
                    endpoint.responseType ?? "application/json"
                );
        
                row.append(status, type);
        
                return row;
            }
        
            // Generate the sidebar navigation button.
            function createNavButton(endpoint) {
                const button = createElement("button", "nav-link");
                button.type = "button";
        
                const method = createElement(
                    "span",
                    "nav-method",
                    endpoint.method
                );
        
                button.append(
                    method,
                    document.createTextNode(" " + endpoint.path)
                );
        
                button.addEventListener("click", () => {
                    showPage(endpoint.id, button);
                });
        
                return button;
            }
        
            // Generate the parameters section.
            function createParametersSection(endpoint) {
                const section = document.createDocumentFragment();
        
                section.appendChild(createLabel("Parameters"));
        
                const parameters = endpoint.parameters ?? [];
        
                if (parameters.length === 0) {
                    section.appendChild(
                        createElement(
                            "p",
                            "",
                            "This endpoint does not require any parameters."
                        )
                    );
        
                    return section;
                }
        
                for (const parameter of parameters) {
                    const parameterCard = createElement(
                        "div",
                        "info-card"
                    );
        
                    const name = createElement(
                        "div",
                        "info-label",
                        parameter.name
                    );
        
                    const details = createElement(
                        "div",
                        "info-value"
                    );
        
                    const type = parameter.type ?? "string";
                    const location = parameter.in ?? "query";
                    const required = parameter.required
                        ? "Required"
                        : "Optional";
        
                    details.textContent =
                        `${type} · ${location} · ${required}`;
        
                    const description = createElement(
                        "p",
                        "",
                        parameter.description ?? ""
                    );
        
                    description.style.marginTop = "10px";
                    description.style.marginBottom = "0";
        
                    parameterCard.append(name, details, description);
        
                    if (parameter.default !== undefined) {
                        const defaultValue = createElement(
                            "p",
                            "",
                            `Default: ${parameter.default}`
                        );
        
                        defaultValue.style.marginTop = "8px";
                        defaultValue.style.marginBottom = "0";
        
                        parameterCard.appendChild(defaultValue);
                    }
        
                    parameterCard.style.marginBottom = "12px";
        
                    section.appendChild(parameterCard);
                }
        
                return section;
            }
        
            // Generate the request section.
            function createRequestSection(endpoint) {
                const section = document.createDocumentFragment();
        
                section.appendChild(createLabel("Request"));
        
                const method = endpoint.method.toUpperCase();
                const path = endpoint.path;
        
                let request = `${method} ${path} HTTP/1.1\n`;
                request += "Host: garage-sentinel";
        
                if (endpoint.requestType) {
                    request += `\nContent-Type: ${endpoint.requestType}`;
                }
        
                if (endpoint.responseType) {
                    const responseType = endpoint.responseType
                        .split(",")[0]
                        .trim();
        
                    request += `\nAccept: ${responseType}`;
                }
        
                section.appendChild(createCodeBlock(request));
        
                return section;
            }
        
            // Generate example response section.
            function createExampleResponseSection(endpoint) {
                const section = document.createDocumentFragment();
        
                if (endpoint.response === undefined) {
                    return section;
                }
        
                section.appendChild(createLabel("Example Response"));
        
                section.appendChild(
                    createCodeBlock(endpoint.response)
                );
        
                return section;
            }
        
            // Generate the response fields from example JSON.
            function createResponseFieldsSection(endpoint) {
                const response = endpoint.response;
        
                if (
                    response === null ||
                    typeof response !== "object" ||
                    Array.isArray(response)
                ) {
                    return null;
                }
        
                const entries = Object.entries(response);
        
                if (entries.length === 0) {
                    return null;
                }
        
                const section = createElement("section");
        
                const sectionTitle = createElement(
                    "div",
                    "section-title"
                );
        
                const headingWrapper = createElement("div");
        
                const heading = createElement(
                    "h3",
                    "",
                    "Response Fields"
                );
        
                const subtitle = createElement(
                    "p",
                    "",
                    "Fields returned by this endpoint."
                );
        
                headingWrapper.append(heading, subtitle);
                sectionTitle.appendChild(headingWrapper);
        
                const grid = createElement("div", "info-grid");
        
                for (const [key, value] of entries) {
                    const card = createElement("div", "info-card");
        
                    const label = createElement(
                        "div",
                        "info-label",
                        key
                    );
        
                    let description;
        
                    if (Array.isArray(value)) {
                        description = "Array";
                    } else if (value !== null && typeof value === "object") {
                        description = Object.keys(value).join(", ");
                    } else {
                        description = `${typeof value} · Example: ${value}`;
                    }
        
                    const content = createElement(
                        "div",
                        "info-value",
                        description
                    );
        
                    card.append(label, content);
                    grid.appendChild(card);
                }
        
                section.append(sectionTitle, grid);
        
                return section;
            }
        
            // Generate a complete endpoint documentation page.
            function createEndpointPage(endpoint) {
                const page = createElement("div", "doc-page");
                page.id = endpoint.id;
        
                // Page header
                const header = createElement("div", "page-header");
        
                const eyebrow = createElement(
                    "div",
                    "eyebrow",
                    "Endpoint"
                );
        
                const title = createElement(
                    "h2",
                    "",
                    endpoint.name
                );
        
                const description = createElement(
                    "p",
                    "",
                    endpoint.description
                );
        
                header.append(eyebrow, title, description);
        
                // Endpoint card
                const card = createElement("div", "card");
        
                const endpointHeader = createElement(
                    "div",
                    "endpoint-header"
                );
        
                const method = createElement(
                    "span",
                    "method",
                    endpoint.method
                );
        
                const path = createElement(
                    "span",
                    "path",
                    endpoint.path
                );
        
                endpointHeader.append(method, path);
        
                // Endpoint body
                const body = createElement("div", "endpoint-body");
        
                body.appendChild(
                    createElement(
                        "p",
                        "",
                        endpoint.description
                    )
                );
        
                body.appendChild(
                    createParametersSection(endpoint)
                );
        
                body.appendChild(
                    createRequestSection(endpoint)
                );
        
                if (endpoint.requestType) {
                    body.appendChild(createLabel("Request Content Type"));
        
                    body.appendChild(
                        createCodeBlock(endpoint.requestType)
                    );
                }
        
                body.appendChild(createLabel("Response"));
        
                body.appendChild(
                    createResponseRow(endpoint)
                );
        
                body.appendChild(
                    createExampleResponseSection(endpoint)
                );
        
                card.append(endpointHeader, body);
        
                page.append(header, card);
        
                // Response field descriptions
                const responseFields = createResponseFieldsSection(endpoint);
        
                if (responseFields) {
                    page.appendChild(responseFields);
                }
        
                // Footer
                const footer = createElement(
                    "footer",
                    "",
                    `Garage Sentinel API · ${endpoint.method} ${endpoint.path}`
                );
        
                page.appendChild(footer);
        
                return page;
            }
        
            // Fetch JSON and generate all endpoint documentation.
            async function loadEndpoints() {
                const nav = document.getElementById("endpoint-nav");
                const pages = document.getElementById("endpoint-pages");
        
                if (!nav || !pages) {
                    console.error("Documentation containers not found.");
                    return;
                }
        
                try {
                    const response = await fetch("/static/endpoints.json");
        
                    if (!response.ok) {
                        throw new Error(
                            `Failed to load endpoints: HTTP ${response.status}`
                        );
                    }
        
                    const endpoints = await response.json();
        
                    if (!Array.isArray(endpoints)) {
                        throw new Error(
                            "endpoints.json must contain an array."
                        );
                    }
        
                    // Clear previously generated content.
                    nav.replaceChildren();
                    pages.replaceChildren();
        
                    const navFragment = document.createDocumentFragment();
                    const pageFragment = document.createDocumentFragment();
        
                    for (const endpoint of endpoints) {
                        if (
                            !endpoint.id ||
                            !endpoint.name ||
                            !endpoint.method ||
                            !endpoint.path
                        ) {
                            console.warn("Skipping invalid endpoint:", endpoint);
                            continue;
                        }
        
                        navFragment.appendChild(
                            createNavButton(endpoint)
                        );
        
                        pageFragment.appendChild(
                            createEndpointPage(endpoint)
                        );
                    }
        
                    nav.appendChild(navFragment);
                    pages.appendChild(pageFragment);
        
                    console.log(
                        `Loaded ${pages.children.length} API endpoints.`
                    );
        
                    // Restore page selected in URL hash.
                    const pageId =
                        decodeURIComponent(window.location.hash.slice(1)) ||
                        "introduction";
        
                    const selectedPage = document.getElementById(pageId);
        
                    if (selectedPage?.classList.contains("doc-page")) {
                        const endpoint = endpoints.find(
                            item => item.id === pageId
                        );
        
                        let matchingButton = null;
        
                        if (endpoint) {
                            const index = endpoints.indexOf(endpoint);
                            matchingButton = nav.children[index] ?? null;
                        } else {
                            matchingButton = [
                                ...document.querySelectorAll(".nav-link")
                            ].find(link => {
                                const onclick =
                                    link.getAttribute("onclick") ?? "";
        
                                return onclick.includes(`'${pageId}'`);
                            });
                        }
        
                        showPage(pageId, matchingButton);
                    } else {
                        const introduction =
                            document.getElementById("introduction");
        
                        const firstPage =
                            introduction ?? pages.firstElementChild;
        
                        if (firstPage) {
                            firstPage.classList.add("active");
                        }
                    }
        
                } catch (error) {
                    console.error(
                        "Documentation loading failed:",
                        error
                    );
        
                    nav.replaceChildren();
        
                    nav.appendChild(
                        createElement(
                            "p",
                            "",
                            "Unable to load API endpoints."
                        )
                    );
                }
            }
        
            document.addEventListener(
                "DOMContentLoaded",
                loadEndpoints
            );
        </script>
    </body>
    </html>
    """