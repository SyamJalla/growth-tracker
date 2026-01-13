# API Documentation

This folder contains comprehensive documentation for the Growth Tracker API.

## Available Documentation Formats

### 1. **Markdown** (`API-Documentation.md`)
- Raw markdown format
- Easy to view in any text editor or GitHub
- Can be converted to other formats

### 2. **HTML** (`API-Documentation.html`)
- Styled, professional-looking documentation
- Can be opened directly in any web browser
- **Print to PDF directly from browser**

### 3. **Postman Collection** (`growth-tracker.postman_collection.json`)
- Import into Postman for interactive API testing
- Includes all endpoints with examples and documentation

---

## How to Convert to PDF

### Method 1: Print HTML to PDF (Easiest)

1. Open `API-Documentation.html` in any web browser (Chrome, Firefox, Edge)
2. Press `Ctrl+P` (or `Cmd+P` on Mac) to open print dialog
3. Select "Save as PDF" or "Microsoft Print to PDF" as printer
4. Adjust settings:
   - Enable "Background graphics" for colors
   - Set margins as needed
5. Click "Save" and choose location

**Result:** Professional PDF with styling intact

### Method 2: Using Pandoc (Best Quality)

```bash
# Install pandoc first
# Windows: choco install pandoc
# Mac: brew install pandoc
# Linux: apt-get install pandoc

# Convert to PDF
pandoc API-Documentation.md -o API-Documentation.pdf --pdf-engine=wkhtmltopdf

# Or with better styling
pandoc API-Documentation.md -o API-Documentation.pdf \
  --pdf-engine=wkhtmltopdf \
  --toc \
  --toc-depth=3 \
  --metadata title="Growth Tracker API Documentation"
```

### Method 3: Using Online Converters

1. Visit any markdown-to-PDF converter:
   - https://www.markdowntopdf.com/
   - https://md2pdf.netlify.app/
   - https://cloudconvert.com/md-to-pdf

2. Upload `API-Documentation.md`
3. Download the generated PDF

### Method 4: Using VS Code Extension

1. Install "Markdown PDF" extension in VS Code
2. Open `API-Documentation.md`
3. Right-click and select "Markdown PDF: Export (pdf)"

---

## Alternative Documentation Formats

### 1. **OpenAPI/Swagger Specification**

**What:** JSON/YAML file that defines your API in OpenAPI 3.0 format

**Advantages:**
- Industry standard
- Generate client SDKs automatically
- Import into Swagger Editor, Postman, Insomnia
- Auto-generate docs using Swagger UI

**How to Create:**
- FastAPI auto-generates this at `/openapi.json`
- Visit `http://localhost:8000/openapi.json` when server is running
- Save the JSON file

**Tools:**
- Swagger UI: https://swagger.io/tools/swagger-ui/
- ReDoc: https://redocly.com/redoc/
- Stoplight: https://stoplight.io/

### 2. **Interactive API Documentation (Built-in)**

FastAPI provides interactive docs automatically:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

**Advantages:**
- Automatically updated when code changes
- Test endpoints directly in browser
- No maintenance required

### 3. **API Blueprint**

**What:** Markdown-based API description format

**Advantages:**
- Human-readable
- Easy to write and maintain
- Generate HTML docs with Aglio

**Example:**
```markdown
FORMAT: 1A
HOST: http://localhost:8000

# Growth Tracker API

API for tracking personal growth metrics

## Health Check [/api/health/]

### Get Health Status [GET]

+ Response 200 (application/json)
    + Body
            {
                "status": "ok",
                "message": "Growth Tracker API running"
            }
```

### 4. **Docusaurus / GitBook**

**What:** Full documentation websites

**Advantages:**
- Beautiful, searchable documentation sites
- Version control for docs
- Support for multiple languages
- Great for public APIs

**Best For:**
- Public APIs
- Large projects
- Team collaboration

### 5. **ReadTheDocs**

**What:** Documentation hosting platform

**Advantages:**
- Free hosting
- Automatic builds from Git
- Versioning support
- Search functionality

**Setup:**
```bash
# Install Sphinx
pip install sphinx

# Initialize docs
sphinx-quickstart docs

# Build
sphinx-build -b html docs docs/_build
```

### 6. **API Mocking & Documentation Platforms**

**Postman:**
- Import collection
- Auto-generate documentation
- Host on Postman's public docs
- Share with team

**Stoplight:**
- Visual API designer
- Automated docs generation
- Mock servers

**Swagger Hub:**
- Host OpenAPI specs
- Collaborative editing
- Auto-generated docs

### 7. **Markdown + GitHub Pages**

**What:** Host markdown docs on GitHub

**Advantages:**
- Free hosting
- Version controlled
- Easy collaboration
- Automatic deployment

**Setup:**
1. Push markdown to GitHub repo
2. Enable GitHub Pages in settings
3. Choose theme
4. Docs available at `username.github.io/repo`

---

## Recommended Approach

### For Your Current Needs:

1. **PDF**: Print `API-Documentation.html` to PDF (easiest, immediate)
2. **Postman Collection**: Already created and documented
3. **FastAPI Built-in Docs**: Available at `/docs` and `/redoc`

### For Future Growth:

1. **Start with:** FastAPI's auto-generated OpenAPI docs
2. **Add:** Postman collection for team sharing
3. **Consider:** Docusaurus or GitBook if API becomes public
4. **Export:** PDF periodically for offline reference

---

## Quick Commands

```bash
# View HTML documentation
start API-Documentation.html  # Windows
open API-Documentation.html   # Mac
xdg-open API-Documentation.html  # Linux

# Get OpenAPI spec from running server
curl http://localhost:8000/openapi.json > openapi.json

# View interactive docs
# Start server then visit:
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

---

## Maintenance

- **Update frequency:** Update docs whenever endpoints change
- **Version control:** Keep docs in sync with API versions
- **Review:** Review documentation with each PR/commit
- **Automation:** Consider CI/CD pipeline to auto-generate docs

---

## Contact

For questions about the documentation or API:
- Check interactive docs at `/docs`
- Review this documentation
- Contact the development team
