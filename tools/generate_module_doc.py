import os
import sys
import subprocess
import time
import markdown

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>__DOC_TITLE__</title>
<style>
    @page {
        size: A4;
        margin: 18mm 16mm 20mm 16mm;
    }
    
    body {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        color: #1e293b;
        line-height: 1.65;
        font-size: 10.5pt;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }

    /* Print Header & Footer */
    .doc-header {
        border-bottom: 2px solid #0284c7;
        padding-bottom: 8px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .doc-header-title {
        font-size: 9pt;
        font-weight: 700;
        color: #0284c7;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .doc-header-sub {
        font-size: 8.5pt;
        color: #64748b;
    }

    /* Title & Headers */
    h1 {
        color: #0f172a;
        font-size: 21pt;
        font-weight: 800;
        border-bottom: 2px solid #0284c7;
        padding-bottom: 10px;
        margin-top: 0;
        margin-bottom: 16px;
        letter-spacing: -0.3px;
    }

    h2 {
        color: #0369a1;
        font-size: 14.5pt;
        font-weight: 700;
        border-bottom: 1.5px solid #e2e8f0;
        padding-bottom: 6px;
        margin-top: 26px;
        margin-bottom: 12px;
        page-break-after: avoid;
    }

    h3 {
        color: #0f172a;
        font-size: 12pt;
        font-weight: 700;
        margin-top: 18px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }

    h4 {
        color: #334155;
        font-size: 11pt;
        font-weight: 600;
        margin-top: 14px;
        margin-bottom: 6px;
    }

    p {
        margin-top: 0;
        margin-bottom: 11px;
        text-align: justify;
    }

    /* Table of Contents (TOC) Container */
    .toc {
        background-color: #f8fafc;
        border: 1.5px solid #cbd5e1;
        border-radius: 8px;
        padding: 16px 22px;
        margin: 18px 0 26px 0;
        page-break-after: always;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    .toc h2 {
        color: #0f172a;
        font-size: 13.5pt;
        margin-top: 0;
        margin-bottom: 12px;
        border-bottom: 2px solid #0284c7;
        padding-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .toc ul {
        list-style-type: none;
        padding-left: 0;
        margin: 0;
    }

    .toc li {
        margin-bottom: 7px;
        font-size: 10pt;
        line-height: 1.45;
        border-bottom: 1px dashed #e2e8f0;
        padding-bottom: 4px;
    }

    .toc li a {
        text-decoration: none;
        color: #0369a1;
        font-weight: 600;
    }

    .toc li a:hover {
        text-decoration: underline;
    }

    /* Executive Callouts / Plain English Explanations */
    blockquote {
        margin: 14px 0;
        padding: 12px 18px;
        background-color: #f0fdf4;
        border-left: 4.5px solid #16a34a;
        color: #14532d;
        border-radius: 4px;
        font-size: 10pt;
        page-break-inside: avoid;
    }

    blockquote strong {
        color: #15803d;
    }

    /* Panel Defense Rapid-Answer Card */
    .defense-card {
        margin: 16px 0;
        padding: 14px 18px;
        background-color: #f5f3ff;
        border: 1px solid #ddd6fe;
        border-left: 5px solid #6366f1;
        border-radius: 6px;
        color: #312e81;
        page-break-inside: avoid;
    }

    .defense-card strong {
        color: #4338ca;
        font-size: 10.5pt;
    }

    /* Formula & Math Card */
    .formula-card {
        margin: 14px 0;
        padding: 12px 18px;
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #0284c7;
        border-radius: 6px;
        color: #0f172a;
        page-break-inside: avoid;
    }

    .formula-card strong {
        color: #0369a1;
    }

    /* Warning / Alert Callouts */
    .alert-box {
        margin: 14px 0;
        padding: 12px 16px;
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        border-left: 4.5px solid #dc2626;
        color: #991b1b;
        border-radius: 4px;
        page-break-inside: avoid;
        font-size: 10pt;
    }

    /* Technical Note Callouts */
    .note-box {
        margin: 14px 0;
        padding: 12px 16px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4.5px solid #64748b;
        color: #334155;
        border-radius: 4px;
        page-break-inside: avoid;
        font-size: 10pt;
    }

    /* Code & Formulas */
    code {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 9pt;
        background-color: #f1f5f9;
        color: #0f172a;
        padding: 2px 5px;
        border-radius: 3px;
        border: 1px solid #e2e8f0;
    }

    pre {
        background-color: #0f172a;
        color: #f8fafc;
        padding: 12px 16px;
        border-radius: 6px;
        overflow-x: auto;
        font-size: 8.5pt;
        line-height: 1.45;
        margin: 14px 0;
        page-break-inside: avoid;
    }

    pre code {
        background-color: transparent;
        color: #f8fafc;
        padding: 0;
        border: none;
        font-size: 8.5pt;
    }

    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        font-size: 9.5pt;
        page-break-inside: avoid;
    }

    th {
        background-color: #f1f5f9;
        color: #0f172a;
        font-weight: 700;
        text-align: left;
        padding: 8px 10px;
        border: 1px solid #cbd5e1;
    }

    td {
        padding: 7px 10px;
        border: 1px solid #e2e8f0;
        vertical-align: top;
    }

    tr:nth-child(even) {
        background-color: #f8fafc;
    }

    /* Lists */
    ul, ol {
        margin-top: 0;
        margin-bottom: 12px;
        padding-left: 22px;
    }

    li {
        margin-bottom: 5px;
    }

    /* Badges & Pills */
    .badge {
        display: inline-block;
        padding: 2px 7px;
        font-size: 8pt;
        font-weight: 700;
        border-radius: 10px;
        background-color: #e0f2fe;
        color: #0369a1;
        margin-right: 4px;
        text-transform: uppercase;
    }

    .badge-red {
        background-color: #fee2e2;
        color: #b91c1c;
    }

    .badge-green {
        background-color: #dcfce7;
        color: #15803d;
    }

    .badge-purple {
        background-color: #f3e8ff;
        color: #7e22ce;
    }

    /* Page Breaks */
    .page-break {
        page-break-before: always;
        break-before: page;
    }

    /* Running Footer */
    .doc-footer {
        margin-top: 30px;
        padding-top: 10px;
        border-top: 1px solid #cbd5e1;
        font-size: 8.5pt;
        color: #94a3b8;
        display: flex;
        justify-content: space-between;
    }
</style>
</head>
<body>
<div class="doc-header">
    <div class="doc-header-title">BioMechAI — Technical Engineering & Biomechanical Reference</div>
    <div class="doc-header-sub">Official Defense Specification Manual</div>
</div>
__DOC_BODY__
<div class="doc-footer">
    <div>BioMechAI Autonomous Biomechanical AI System</div>
    <div>Official Defense Reference Document</div>
</div>
</body>
</html>
"""

def md_to_pdf(md_path, pdf_path=None):
    if not os.path.exists(md_path):
        print(f"Error: {md_path} does not exist.")
        return False

    if pdf_path is None:
        pdf_path = os.path.splitext(md_path)[0] + ".pdf"

    md_text = None
    for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
        try:
            with open(md_path, "r", encoding=enc) as f:
                md_text = f.read()
            break
        except UnicodeDecodeError:
            continue
    if md_text is None:
        print(f"Error: Unable to decode {md_path} with supported encodings.")
        return False

    # Convert Markdown to HTML
    html_content = markdown.markdown(
        md_text,
        extensions=[
            "extra",
            "tables",
            "fenced_code",
            "codehilite",
            "toc",
            "nl2br",
            "sane_lists"
        ]
    )

    # Derive document title from first header or filename
    title = os.path.splitext(os.path.basename(md_path))[0].replace("_", " ").title()
    full_html = HTML_TEMPLATE.replace("__DOC_TITLE__", title).replace("__DOC_BODY__", html_content)

    temp_html_path = os.path.splitext(md_path)[0] + "_temp.html"
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    # Path to Microsoft Edge
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    edge_exe = next((p for p in edge_paths if os.path.exists(p)), None)

    if not edge_exe:
        print("Error: Microsoft Edge executable not found.")
        return False

    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        temp_html_path
    ]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        time.sleep(1.5)
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            print(f"Successfully generated PDF: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
            if os.path.exists(temp_html_path):
                os.remove(temp_html_path)
            return True
        else:
            print(f"Failed to generate PDF. Returncode: {proc.returncode}")
            return False
    except Exception as e:
        print(f"Exception during PDF generation: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_module_doc.py <path_to_markdown_file>")
        sys.exit(1)
    md_to_pdf(sys.argv[1])
