import json
import os
import sys
import subprocess
from jinja2 import Template

# Ensure Playwright dependencies are set up
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Playwright is not installed. Installing it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    from playwright.sync_api import sync_playwright

def install_playwright_browser():
    """Ensure the headless Chromium browser is installed."""
    try:
        # Check if browser is available
        with sync_playwright() as p:
            p.chromium.launch()
    except Exception as e:
        print("Playwright Chromium browser not found. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("Chromium browser installed successfully!")

def generate_menu_pdf(json_path='menu.json', template_path='menu_template.html', output_pdf='fumo33_A3_menu.pdf'):
    """Read menu data, render HTML template, and write to high-quality print PDF."""
    print("Step 1: Reading Fumo 33 menu database...")
    if not os.path.exists(json_path):
        print(f"Error: Database file '{json_path}' not found!")
        return False
        
    with open(json_path, 'r', encoding='utf-8') as f:
        menu_data = json.load(f)

    print("Step 2: Loading A3 HTML print layout template...")
    if not os.path.exists(template_path):
        print(f"Error: Template file '{template_path}' not found!")
        return False

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    print("Step 3: Rendering data into HTML template via Jinja2...")
    template = Template(template_content)
    rendered_html = template.render(data=menu_data)

    # Write temporary rendered HTML file to disk so Playwright can read it local-file style
    temp_html_path = os.path.abspath('temp_menu_render.html')
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

    print("Step 4: Launching headless browser to print vector A3 PDF...")
    install_playwright_browser()
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Load the temporary HTML file
            file_url = f"file:///{temp_html_path.replace(os.sep, '/')}"
            page.goto(file_url)
            
            # CRITICAL: Wait for external Google Fonts to load and network to be completely idle
            page.wait_for_load_state("networkidle")
            
            # Print to PDF using @page CSS size rules (A3 portrait, margins, color accuracy)
            page.pdf(
                path=output_pdf,
                prefer_css_page_size=True,
                print_background=True
            )
            browser.close()
            
        print(f"Success! A3 Print-ready menu generated: '{output_pdf}'")
        return True
        
    except Exception as e:
        print(f"Failed to generate PDF: {e}")
        return False
        
    finally:
        # Clean up temporary HTML file
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)

if __name__ == '__main__':
    generate_menu_pdf()
