import subprocess
import os
import re
import json

md_path = 'c:/Machine learning/Research_Paper_Residential_Energy_Prediction.md'
html_path = 'c:/Machine learning/paper_printable.html'
pdf_path = 'c:/Machine learning/Research_Paper_Residential_Energy_Prediction.pdf'

with open(md_path, 'r', encoding='utf-8') as f:
    md_text = f.read()

# Fix image paths to file:///
def fix_img(m):
    alt = m.group(1)
    path = m.group(2).replace('\\', '/')
    return f'![{alt}](file:///{path})'

md_text_fixed = re.sub(r'!\[(.*?)\]\((.*?)\)', fix_img, md_text)
json_repr = json.dumps(md_text_fixed)

template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Research Paper - Residential Energy Consumption</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    @page {
      size: A4;
      margin: 18mm 15mm 18mm 15mm;
    }
    body {
      font-family: 'Times New Roman', Times, serif;
      color: #111;
      line-height: 1.5;
      font-size: 10.5pt;
      margin: 0;
      padding: 0;
    }
    h1 {
      font-size: 17pt;
      text-align: center;
      margin-bottom: 0.5rem;
      font-weight: bold;
    }
    h2 {
      font-size: 12.5pt;
      border-bottom: 1px solid #333;
      padding-bottom: 2px;
      margin-top: 1.4rem;
      margin-bottom: 0.4rem;
      font-weight: bold;
    }
    h3 {
      font-size: 11pt;
      margin-top: 1rem;
      margin-bottom: 0.3rem;
      font-weight: bold;
    }
    p {
      text-align: justify;
      margin-bottom: 0.7rem;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0;
      font-size: 9pt;
      page-break-inside: avoid;
    }
    th, td {
      border: 1px solid #444;
      padding: 4px 7px;
      text-align: left;
    }
    th {
      background-color: #f2f2f2;
      font-weight: bold;
    }
    img {
      max-width: 85%;
      display: block;
      margin: 1rem auto;
      page-break-inside: avoid;
    }
    ol, ul {
      margin-left: 2em;
      margin-bottom: 0.7rem;
    }
  </style>
</head>
<body>
  <div id="content"></div>
  <script>
    const rawMd = """ + json_repr + """;
    document.getElementById('content').innerHTML = marked.parse(rawMd);
  </script>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(template)

print(f"Generated {html_path}")

# Run Chrome headless to print to PDF
import tempfile
user_data = os.path.join(tempfile.gettempdir(), 'chrome_pdf_paper_tmp')
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
uri = 'file:///' + os.path.abspath(html_path).replace('\\', '/')

cmd = [
    chrome_path,
    '--headless=new',
    '--disable-gpu',
    f'--user-data-dir={user_data}',
    '--no-pdf-header-footer',
    f'--print-to-pdf={pdf_path}',
    uri
]

print("Compiling PDF with Chrome headless...")
res = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
print("Returncode:", res.returncode)
if os.path.exists(pdf_path):
    print(f"SUCCESS! PDF created at {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
else:
    print("PDF generation failed:", res.stderr)

