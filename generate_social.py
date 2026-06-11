import os
import sys
import subprocess
import tempfile
from pathlib import Path
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
    flag_file = os.path.join(tempfile.gettempdir(), "playwright_installed.flag")
    if os.path.exists(flag_file):
        return
        
    try:
        # Check if browser is available
        with sync_playwright() as p:
            p.chromium.launch()
        # Create flag file
        with open(flag_file, "w") as f:
            f.write("installed")
    except Exception:
        print("Playwright Chromium browser not found. Installing it now...")
        try:
            # Run the silent install command using the active python executable
            subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Create flag file
            with open(flag_file, "w") as f:
                f.write("installed")
            print("Chromium browser installed successfully!")
        except Exception as e:
            # Fallback to standard command-line call if sys.executable fails
            try:
                subprocess.run(["playwright", "install", "chromium"], check=True)
                with open(flag_file, "w") as f:
                    f.write("installed")
                print("Chromium browser installed successfully via fallback!")
            except Exception as inner_e:
                raise RuntimeError(f"Playwright auto-installation failed: {str(e)} | Inner: {str(inner_e)}")

# HTML & CSS Template for Social Media Posts
SOCIAL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <!-- Import brand typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: 'Outfit', sans-serif;
      background-color: #111111;
      color: #FAF7F0;
    }

    /* Background food image */
    .bg-image {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      z-index: 1;
    }

    /* Dynamic gradient overlay to ensure text contrast */
    .gradient-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 2;
      background: {{ gradient_style }};
    }

    /* Elegant gold double border matching brand style */
    .border-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 3;
      padding: {{ border_padding }};
      box-sizing: border-box;
    }

    .border-inner {
      width: 100%;
      height: 100%;
      border: {{ border_style_rule }};
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: {{ content_padding }};
      box-sizing: border-box;
    }

    /* Branding elements */
    .brand-header {
      text-align: center;
      width: 100%;
    }

    .brand-name {
      font-family: 'Cinzel', serif;
      font-size: {{ brand_size }};
      font-weight: 900;
      letter-spacing: 4px;
      color: #F2C94C; /* Gold */
      margin-bottom: 2px;
      text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    .brand-tagline {
      font-size: {{ tagline_size }};
      font-weight: 500;
      letter-spacing: 5px;
      text-transform: uppercase;
      color: #D4AF37;
      text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    /* Middle element space */
    .middle-space {
      flex-grow: 1;
    }

    /* Content details block */
    .content-block {
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 15px;
      z-index: 4;
    }

    /* Custom promotional badges */
    .promo-badge {
      align-self: {{ align_self }};
      background-color: rgba(212, 175, 55, 0.15);
      border: 1px solid #D4AF37;
      color: #F2C94C;
      font-family: 'Outfit', sans-serif;
      font-size: {{ badge_size }};
      font-weight: 700;
      text-transform: uppercase;
      padding: 6px 16px;
      border-radius: 50px;
      letter-spacing: 1.5px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.3);
      width: fit-content;
    }

    /* Dish layout info */
    .dish-info {
      text-align: {{ text_align }};
    }

    .dish-title-row {
      display: flex;
      flex-direction: {{ title_row_direction }};
      justify-content: {{ title_row_justify }};
      align-items: baseline;
      gap: 15px;
      margin-bottom: 8px;
    }

    .dish-name {
      font-family: 'Cinzel', serif;
      font-size: {{ dish_size }};
      font-weight: 700;
      color: #FAF7F0;
      text-shadow: 0 2px 5px rgba(0,0,0,0.6);
      line-height: 1.15;
    }

    .dish-price {
      font-family: 'Cinzel', serif;
      font-size: {{ price_size }};
      font-weight: 700;
      color: #F2C94C;
      text-shadow: 0 2px 5px rgba(0,0,0,0.6);
      white-space: nowrap;
    }

    .dish-description {
      font-size: {{ desc_size }};
      font-weight: 300;
      color: #C0C0C0;
      line-height: 1.4;
      text-shadow: 0 2px 4px rgba(0,0,0,0.5);
      max-width: {{ max_width_desc }};
      margin: {{ margin_desc }};
    }

    /* Footer info */
    .footer {
      text-align: center;
      width: 100%;
      border-top: 1px dashed rgba(212, 175, 55, 0.3);
      padding-top: 10px;
      margin-top: 10px;
    }

    .footer-text {
      font-size: {{ footer_size }};
      color: #A0A0A0;
      letter-spacing: 2px;
      text-transform: uppercase;
      text-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }
    
    /* Layout styles specifically for landscape */
    {% if format_name == 'landscape' %}
    .border-inner {
      flex-direction: row;
      align-items: center;
    }
    .left-pane {
      width: 45%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      z-index: 4;
    }
    .right-spacer {
      width: 55%;
      height: 100%;
    }
    {% endif %}
  </style>
</head>
<body>
  
  <img class="bg-image" src="{{ image_url }}" alt="Background food">
  <div class="gradient-overlay"></div>
  
  <div class="border-container">
    <div class="border-inner">
      {% if format_name == 'landscape' %}
        <div class="left-pane">
          <!-- Logo top left -->
          <div>
            <div class="brand-name" style="text-align: left; font-size: 24px;">FUMO 33</div>
            <div class="brand-tagline" style="text-align: left; font-size: 10px;">Woodfired Kitchen</div>
          </div>
          
          <!-- Dish details middle left -->
          <div class="content-block" style="gap: 10px;">
            {% if badge_text %}
              <div class="promo-badge">{{ badge_text }}</div>
            {% endif %}
            <div class="dish-info">
              <div class="dish-title-row">
                <div class="dish-name">{{ dish_name }}</div>
                <div class="dish-price">£{{ price }}</div>
              </div>
              <div class="dish-description" style="text-align: left; max-width: 100%;">{{ description }}</div>
            </div>
          </div>
          
          <!-- CTA bottom left -->
          <div class="footer" style="border-top: 1px solid rgba(212, 175, 55, 0.3); padding-top: 8px; text-align: left; margin: 0;">
            <div class="footer-text" style="text-align: left; font-size: 10px;">📍 Ryde, IOW • fumo33.co.uk</div>
          </div>
        </div>
        <div class="right-spacer"></div>
      {% else %}
        <!-- Logo top center -->
        <div class="brand-header">
          <div class="brand-name">FUMO 33</div>
          <div class="brand-tagline">Woodfired Kitchen & Bar</div>
        </div>
        
        <div class="middle-space"></div>
        
        <!-- Dish Details bottom center -->
        <div class="content-block">
          {% if badge_text %}
            <div class="promo-badge">{{ badge_text }}</div>
          {% endif %}
          
          <div class="dish-info">
            <div class="dish-title-row">
              <div class="dish-name">{{ dish_name }}</div>
              <div class="dish-price">£{{ price }}</div>
            </div>
            {% if description %}
              <div class="dish-description">{{ description }}</div>
            {% endif %}
          </div>
          
          <div class="footer">
            <div class="footer-text">📍 Ryde, Isle of Wight • fumo33.co.uk</div>
          </div>
        </div>
      {% endif %}
    </div>
  </div>

</body>
</html>
"""

def generate_social_post(image_path, format_name, dish_name, description, price, badge_text, overlay_opacity=0.6, border_style="double", output_path="social_post.png"):
    """
    Renders the Fumo 33 branded HTML and uses Playwright to capture a screenshot of the specified size.
    Formats:
      - square (1080 x 1080)
      - vertical (1080 x 1920)
      - landscape (1200 x 630)
    """
    print(f"Generating social post for '{dish_name}' in format '{format_name}'...")
    
    # Configure dimensions
    if format_name == "square":
        width, height = 1080, 1080
        border_padding = "25px"
        content_padding = "40px"
        brand_size = "44px"
        tagline_size = "13px"
        align_self = "center"
        badge_size = "13px"
        text_align = "center"
        title_row_direction = "column"
        title_row_justify = "center"
        dish_size = "48px"
        price_size = "36px"
        desc_size = "20px"
        max_width_desc = "80%"
        margin_desc = "0 auto"
        footer_size = "12px"
        gradient_style = f"linear-gradient(to top, rgba(17,17,17,{overlay_opacity + 0.2}) 0%, rgba(17,17,17,{overlay_opacity}) 50%, rgba(17,17,17,0) 100%)"
    elif format_name == "vertical":
        width, height = 1080, 1920
        border_padding = "35px"
        content_padding = "60px"
        brand_size = "56px"
        tagline_size = "16px"
        align_self = "center"
        badge_size = "15px"
        text_align = "center"
        title_row_direction = "column"
        title_row_justify = "center"
        dish_size = "58px"
        price_size = "44px"
        desc_size = "22px"
        max_width_desc = "85%"
        margin_desc = "0 auto"
        footer_size = "13px"
        gradient_style = f"linear-gradient(to top, rgba(17,17,17,{overlay_opacity + 0.25}) 0%, rgba(17,17,17,{overlay_opacity + 0.1}) 40%, rgba(17,17,17,0) 100%)"
    elif format_name == "landscape":
        width, height = 1200, 630
        border_padding = "20px"
        content_padding = "30px"
        brand_size = "28px"
        tagline_size = "10px"
        align_self = "flex-start"
        badge_size = "11px"
        text_align = "left"
        title_row_direction = "row"
        title_row_justify = "space-between"
        dish_size = "36px"
        price_size = "30px"
        desc_size = "16px"
        max_width_desc = "100%"
        margin_desc = "0"
        footer_size = "11px"
        # Linear left-to-right gradient overlay for text legibility
        gradient_style = f"linear-gradient(to right, rgba(17,17,17,{overlay_opacity + 0.25}) 0%, rgba(17,17,17,{overlay_opacity}) 40%, rgba(17,17,17,0) 80%)"
    else:
        raise ValueError(f"Unknown format: {format_name}")

    # Set up border rule
    if border_style == "double":
        border_style_rule = "3px double #D4AF37"
    elif border_style == "solid":
        border_style_rule = "1.5px solid #D4AF37"
    else:
        border_style_rule = "none"

    # Convert absolute image path to file URI for Playwright
    image_url = Path(image_path).resolve().as_uri()

    # Compile Template using Jinja2
    template = Template(SOCIAL_TEMPLATE)
    rendered_html = template.render(
        format_name=format_name,
        image_url=image_url,
        gradient_style=gradient_style,
        border_padding=border_padding,
        content_padding=content_padding,
        border_style_rule=border_style_rule,
        brand_size=brand_size,
        tagline_size=tagline_size,
        align_self=align_self,
        badge_size=badge_size,
        text_align=text_align,
        title_row_direction=title_row_direction,
        title_row_justify=title_row_justify,
        dish_size=dish_size,
        price_size=price_size,
        desc_size=desc_size,
        max_width_desc=max_width_desc,
        margin_desc=margin_desc,
        footer_size=footer_size,
        dish_name=dish_name,
        description=description,
        price=price,
        badge_text=badge_text
    )

    # Write temporary file
    temp_html_path = os.path.abspath('temp_social_render.html')
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

    # Compile using Playwright Chromium
    install_playwright_browser()
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_viewport_size({"width": width, "height": height})
            
            # Go to the local page
            file_url = f"file:///{temp_html_path.replace(os.sep, '/')}"
            page.goto(file_url)
            
            # Wait for network idle to ensure fonts and image are fully loaded
            page.wait_for_load_state("networkidle")
            
            # Take screenshot and save to output path
            page.screenshot(path=output_path, type="png")
            browser.close()
            
        print(f"Social post graphic compiled successfully at: {output_path}")
        return True
        
    except Exception as e:
        print(f"Failed to generate social post graphic: {e}")
        return False
        
    finally:
        # Clean up temporary HTML file
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)

def generate_automated_caption(tone, name, price, description, badge):
    """
    Generates structured, platform-ready social captions based on user input.
    """
    # 1. Clean the Badge
    badge_clean = f"[{badge.upper()}]" if (badge and str(badge).strip()) else "[NEW DISH ALERT]"
    
    # 2. Clean the Name (avoid double "our" grammar bug)
    if name and str(name).strip():
        name_clean = str(name).strip()
    else:
        name_clean = "our newest creation"
        
    # 3. Clean the Price (safely handle currency formatting)
    if price and str(price).strip():
        price_val = str(price).strip()
        # Remove any stray currency symbols to prevent double formatting
        if price_val.startswith("£"):
            price_val = price_val[1:]
        try:
            # Check if it's a valid float
            price_clean = f"for only £{float(price_val):.2f}"
        except ValueError:
            price_clean = f"for only £{price_val}"
    else:
        price_clean = "today"

    # 4. Clean the Description
    desc_clean = f"\n\n{description}\n" if (description and str(description).strip()) else ""

    # 5. Normalize Tone string for strict comparison
    tone_normalized = str(tone).strip().lower()

    # Determine which template to output
    if "hype" in tone_normalized or "energetic" in tone_normalized:
        return f"""🔥 {badge_clean} 🔥

Weekend plans? Sorted. Say hello to {"our" if "our" not in name_clean.lower() else ""} mouth-watering {name_clean}! 🤤{desc_clean}
Indulge {price_clean} at Fumo 33. This is the ultimate fuel to kickstart your weekend. 

Tables are filling fast—don't miss out. 

📍 33 Union Street, Ryde
🔗 Reserve your space: fumo33.co.uk

#Fumo33 #Ryde #IsleOfWight #IOWFood #SovereignDining #SupportLocal #IOW"""

    elif "elegant" in tone_normalized or "sophisticated" in tone_normalized:
        return f"""✨ {badge_clean} ✨

Introducing your new favorite: the {name_clean}. 

Crafted with precision, cooked over wood fire, and designed to deliver a refined dining experience.{desc_clean}
Available {price_clean} at Fumo 33. Pairing recommendation available from our sommelier.

Experience the art of local gastronomy.

📍 33 Union Street, Ryde
🔗 Bookings & Menu: fumo33.co.uk

#Fumo33 #Ryde #IsleOfWight #SovereignDining #BoutiqueEats #ResponsibleGastronomy"""

    else:  # Local / Community Focus
        return f"""⚓ {badge_clean} • SUPPORT LOCAL ⚓

We are proud to introduce our {name_clean}, built entirely on a foundation of sovereign Island sourcing.{desc_clean}
By using hand-pressed local beef, fresh vegetables, and regional bakes, we ensure that every single pound spent at Fumo 33 remains within our circular Island economy. 

Enjoy this local masterpiece {price_clean}.

📍 33 Union Street, Ryde
🔗 Support our high street: fumo33.co.uk

#Fumo33 #Ryde #IsleOfWight #SovereignDining #SupportLocal #KeepItLocal #IOWEconomy"""

if __name__ == '__main__':

    # Simple test run if executed directly
    test_img = os.path.abspath("food_images/20260521_122755.jpg")
    if os.path.exists(test_img):
        generate_social_post(
            image_path=test_img,
            format_name="square",
            dish_name="Test Woodfired Pizza",
            description="Classic mozzarella with local basil fresh out of our stone oven.",
            price="14.50",
            badge_text="Weekend Special",
            output_path="test_social_post.png"
        )
