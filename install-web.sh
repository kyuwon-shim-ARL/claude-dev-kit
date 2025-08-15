#!/bin/bash
# Claude Dev Kit: Web Development Extension
# Adds Playwright, uv, and web development stack to existing claude-dev-kit project
# Usage: curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/install-web.sh | bash

set -e

echo "🌐 Installing Claude Dev Kit Web Extension"
echo "=========================================="
echo ""

# Check if this is a claude-dev-kit project
if [ ! -f "CLAUDE.md" ]; then
    echo "❌ Error: Not in a Claude Dev Kit project directory"
    echo "💡 Run the base installation first:"
    echo "   curl -sSL https://raw.githubusercontent.com/kyuwon-shim-ARL/claude-dev-kit/main/install.sh | bash"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "❌ Python 3.8+ required (found $PYTHON_VERSION)"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"
echo ""

# 1. Install uv (Python package manager)
echo "📦 Installing uv..."
if command -v uv &> /dev/null; then
    echo "  ✅ uv already installed: $(uv --version)"
else
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
    echo "  ✅ uv installed: $(uv --version)"
fi

# 2. Create web-specific directories
echo ""
echo "📁 Creating web project structure..."
for dir in "src/web" "src/web/frontend" "src/web/backend" "src/web/tests" \
           "public" "static" "templates"; do
    mkdir -p "$dir"
    echo "  ✅ Created: $dir"
done

# 3. Initialize uv project with web dependencies
echo ""
echo "📋 Setting up Python environment with uv..."
cat > pyproject.toml << 'EOF'
[project]
name = "claude-web-project"
version = "0.1.0"
description = "Claude Dev Kit Web Project"
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn[standard]>=0.23.0",
    "playwright>=1.40.0",
    "pytest>=7.4.0",
    "pytest-playwright>=0.4.0",
    "httpx>=0.25.0",
    "pydantic>=2.0.0",
    "jinja2>=3.1.0",
    "python-multipart>=0.0.6",
]

[project.optional-dependencies]
dev = [
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]

[tool.uv]
dev-dependencies = [
    "watchdog>=3.0.0",
]

[tool.ruff]
line-length = 88
target-version = "py38"

[tool.black]
line-length = 88
target-version = ["py38"]

[tool.pytest.ini_options]
testpaths = ["tests", "src/web/tests"]
python_files = ["test_*.py", "*_test.py"]
EOF

# Install dependencies
uv venv
echo "  ✅ Created virtual environment"

# Install packages
uv pip install -e ".[dev]"
echo "  ✅ Installed Python packages"

# 4. Install Playwright browsers
echo ""
echo "🎭 Installing Playwright browsers..."
uv run playwright install chromium
echo "  ✅ Chromium browser installed"

# 5. Create FastAPI backend template
echo ""
echo "🚀 Creating FastAPI backend template..."
cat > src/web/backend/main.py << 'EOF'
"""
FastAPI backend for Claude Web Project
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI(title="Claude Web App")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Claude Web App"}
    )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "claude-web-app"}

@app.get("/api/version")
async def version():
    """Version endpoint"""
    return {"version": "0.1.0", "framework": "FastAPI"}
EOF

# 6. Create basic HTML template
cat > templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            margin-bottom: 1rem;
        }
        .status {
            display: inline-block;
            padding: 0.5rem 1rem;
            background: #10b981;
            color: white;
            border-radius: 6px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Claude Web App</h1>
        <p class="status">✅ Running</p>
        <p>Your web development stack is ready!</p>
        <ul>
            <li>FastAPI backend: <code>http://localhost:8000</code></li>
            <li>API docs: <code>http://localhost:8000/docs</code></li>
            <li>Playwright tests: <code>uv run pytest src/web/tests/</code></li>
        </ul>
    </div>
</body>
</html>
EOF

# 7. Create Playwright test example
cat > src/web/tests/test_e2e.py << 'EOF'
"""
End-to-end tests using Playwright
"""

import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """Navigate to the app before each test"""
    # Assuming app is running on localhost:8000
    page.goto("http://localhost:8000")

def test_home_page_loads(page: Page):
    """Test that home page loads successfully"""
    # Check title
    expect(page).to_have_title("Claude Web App")
    
    # Check main heading
    heading = page.locator("h1")
    expect(heading).to_contain_text("Claude Web App")
    
    # Check status indicator
    status = page.locator(".status")
    expect(status).to_be_visible()
    expect(status).to_contain_text("Running")

def test_api_health_check(page: Page):
    """Test API health check endpoint"""
    response = page.request.get("http://localhost:8000/api/health")
    assert response.ok
    data = response.json()
    assert data["status"] == "healthy"

def test_responsive_design(page: Page):
    """Test responsive design on different viewports"""
    # Desktop
    page.set_viewport_size({"width": 1920, "height": 1080})
    expect(page.locator(".container")).to_be_visible()
    
    # Mobile
    page.set_viewport_size({"width": 375, "height": 667})
    expect(page.locator(".container")).to_be_visible()
EOF

# 8. Create development scripts
echo ""
echo "📝 Creating development scripts..."

# Run script
cat > scripts/run-web.sh << 'EOF'
#!/bin/bash
# Start the web development server

echo "🚀 Starting FastAPI server..."
source .venv/bin/activate 2>/dev/null || uv venv && source .venv/bin/activate
uvicorn src.web.backend.main:app --reload --host 0.0.0.0 --port 8000
EOF
chmod +x scripts/run-web.sh

# Test script  
cat > scripts/test-web.sh << 'EOF'
#!/bin/bash
# Run web tests including E2E with Playwright

echo "🧪 Running web tests..."
source .venv/bin/activate 2>/dev/null || uv venv && source .venv/bin/activate

# Start server in background for E2E tests
echo "Starting test server..."
uvicorn src.web.backend.main:app --port 8000 &
SERVER_PID=$!
sleep 2

# Run tests
pytest src/web/tests/ -v

# Cleanup
kill $SERVER_PID
echo "✅ Tests completed"
EOF
chmod +x scripts/test-web.sh

# 9. Update CLAUDE.md with web development section
echo ""
echo "📚 Updating CLAUDE.md with web development documentation..."
cat >> CLAUDE.md << 'EOF'

## 🌐 Web Development Extension

### Web Stack
- **Backend**: FastAPI + Uvicorn
- **Testing**: Playwright + pytest
- **Package Manager**: uv (ultra-fast Python package manager)
- **Frontend**: Templates (expandable to React/Vue/Svelte)

### Web Commands

#### Development
```bash
# Start development server
./scripts/run-web.sh
# or
uv run uvicorn src.web.backend.main:app --reload

# Run E2E tests
./scripts/test-web.sh
# or
uv run pytest src/web/tests/

# Install new packages
uv pip install package-name

# Format and lint
uv run black src/web/
uv run ruff src/web/
```

#### Playwright Testing
```bash
# Run headed mode (see browser)
uv run pytest src/web/tests/ --headed

# Run specific browser
uv run pytest src/web/tests/ --browser chromium

# Generate test code
uv run playwright codegen http://localhost:8000
```

### Web Project Structure
```
src/web/
├── backend/            # FastAPI backend
│   └── main.py        # Main application
├── frontend/          # Frontend code (if needed)
└── tests/            # E2E tests with Playwright
    └── test_e2e.py   # Example E2E test

templates/            # HTML templates
static/              # Static files (CSS, JS, images)
public/              # Public assets
```

### Quick Start Web Development
1. Start the server: `./scripts/run-web.sh`
2. Open browser: http://localhost:8000
3. API documentation: http://localhost:8000/docs
4. Run tests: `./scripts/test-web.sh`
EOF

# 10. Create a simple web-based presentation example
echo ""
echo "📊 Creating web-based presentation example..."
cat > examples/web_presentation.py << 'EOF'
#!/usr/bin/env python3
"""
Example: Web-based presentation using reveal.js
This demonstrates how to create web-based slides programmatically
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/presentation", response_class=HTMLResponse)
async def presentation():
    """Serve a web-based presentation"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js/dist/reveal.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js/dist/theme/black.css">
    </head>
    <body>
        <div class="reveal">
            <div class="slides">
                <section>
                    <h1>Claude Web Presentation</h1>
                    <p>Built with FastAPI + Reveal.js</p>
                </section>
                <section>
                    <h2>Features</h2>
                    <ul>
                        <li>Web-based slides</li>
                        <li>Programmatic generation</li>
                        <li>Live reload</li>
                        <li>Export to PDF</li>
                    </ul>
                </section>
                <section>
                    <h2>Thank You!</h2>
                    <p>🚀 Powered by Claude Dev Kit</p>
                </section>
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/reveal.js/dist/reveal.js"></script>
        <script>
            Reveal.initialize({
                hash: true,
                controls: true,
                progress: true,
                center: true,
                transition: 'slide'
            });
        </script>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
EOF

# Final summary
echo ""
echo "✨ Web Extension Installation Complete!"
echo "======================================"
echo ""
echo "📦 Installed Components:"
echo "  ✅ uv (Python package manager)"
echo "  ✅ FastAPI + Uvicorn (Backend framework)"
echo "  ✅ Playwright (E2E testing & automation)"
echo "  ✅ Web project structure"
echo "  ✅ Example templates and tests"
echo ""
echo "🚀 Quick Start:"
echo "  1. Start server: ./scripts/run-web.sh"
echo "  2. Open browser: http://localhost:8000"
echo "  3. View API docs: http://localhost:8000/docs"
echo "  4. Run tests: ./scripts/test-web.sh"
echo ""
echo "📚 Examples:"
echo "  • Web app: src/web/backend/main.py"
echo "  • E2E tests: src/web/tests/test_e2e.py"
echo "  • Presentation: python examples/web_presentation.py"
echo ""
echo "💡 Next Steps:"
echo "  • Customize templates in templates/"
echo "  • Add more API endpoints in src/web/backend/"
echo "  • Write E2E tests in src/web/tests/"
echo "  • Install frontend framework (React/Vue/Svelte) if needed"