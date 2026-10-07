import subprocess
import os
import time

html_path = r'c:\Machine learning\frontend\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make tab-predict active
mod_content = content.replace('id="tab-home" class="tab-pane active"', 'id="tab-home" class="tab-pane"')
mod_content = mod_content.replace('id="tab-predict" class="tab-pane"', 'id="tab-predict" class="tab-pane active"')
mod_content = mod_content.replace('<button class="nav-tab active" data-tab="tab-home"', '<button class="nav-tab" data-tab="tab-home"')
mod_content = mod_content.replace('<button class="nav-tab" data-tab="tab-predict"', '<button class="nav-tab active" data-tab="tab-predict"')

tmp_html = r'c:\Machine learning\frontend\temp_predict_view.html'
with open(tmp_html, 'w', encoding='utf-8') as f:
    f.write(mod_content)

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
out_file = r'c:\Machine learning\plots\website_predictor_screenshot.png'
cmd = [
    chrome,
    '--headless=new',
    '--disable-gpu',
    f'--screenshot={out_file}',
    '--window-size=1280,950',
    '--virtual-time-budget=4000',
    'http://127.0.0.1:5000/temp_predict_view.html'
]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
if os.path.exists(tmp_html):
    os.remove(tmp_html)

print('Predictor Screenshot exists:', os.path.exists(out_file))
if os.path.exists(out_file):
    print('Size:', os.path.getsize(out_file))
