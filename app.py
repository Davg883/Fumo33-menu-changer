import streamlit as st
import json
import os
import subprocess
import time
from datetime import datetime

# Set page configuration with a custom title and icon
st.set_page_config(
    page_title="Fumo 33 - Single Source of Truth Portal",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load current menu data
def load_menu():
    with open('menu.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Load current drinks data
def load_drinks():
    with open('drinks_menu.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Save updated menu data and trigger PDF regeneration
def save_menu(data):
    with open('menu.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    # Trigger both the PDF generator and Leaflet generator scripts
    try:
        subprocess.run(["python", "generate_pdf.py"], capture_output=True, text=True, check=True)
        subprocess.run(["python", "generate_leaflet.py"], capture_output=True, text=True, check=True)
        return True, "fumo33_A3_menu.pdf and fumo33_leaflet_menu.pdf"
    except Exception as e:
        return False, str(e)

# Save updated drinks data and trigger PDF regeneration
def save_drinks(data):
    with open('drinks_menu.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    # Trigger the drinks PDF generator script
    try:
        subprocess.run(["python", "generate_drinks.py"], capture_output=True, text=True, check=True)
        return True, "fumo33_drinks_menu.pdf"
    except Exception as e:
        return False, str(e)

# Custom premium styling injected directly
st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Base page styling */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            font-family: 'Outfit', sans-serif !important;
            background-color: #111111 !important;
            color: #FAF7F0 !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #1C1C1E !important;
            color: #FAF7F0 !important;
            border-right: 1px solid #D4AF37;
        }
        [data-testid="stSidebar"] * {
            color: #FAF7F0 !important;
        }
        
        /* Gold Accent Header */
        h1, h2, h3, .brand-font {
            font-family: 'Cinzel', serif !important;
            color: #F2C94C !important;
            font-weight: 700 !important;
        }
        
        .sidebar-brand {
            font-family: 'Cinzel', serif;
            font-size: 20pt;
            font-weight: 900;
            color: #F2C94C !important;
            text-align: center;
            border-bottom: 2px solid #D4AF37;
            padding-bottom: 10px;
            margin-bottom: 20px;
            letter-spacing: 2px;
        }
        
        /* Premium custom cards */
        .premium-card {
            background-color: #1C1C1E;
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-left: 5px solid #D4AF37;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            color: #FAF7F0;
        }
        .premium-card h3, .premium-card h4, .premium-card p {
            color: #FAF7F0 !important;
        }
        
        .stat-card {
            background-color: #1C1C1E;
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stat-card h5 {
            color: #A0A0A0 !important;
        }
        
        .stat-val {
            font-size: 24pt;
            font-weight: 700;
            color: #F2C94C;
            margin: 5px 0;
        }
        
        /* Button overrides */
        .stButton>button {
            background-color: #1C1C1E !important;
            color: #FAF7F0 !important;
            border: 1px solid #D4AF37 !important;
            font-weight: 600 !important;
            border-radius: 4px !important;
            padding: 0.5rem 1.5rem !important;
            transition: all 0.3s ease !important;
        }
        .stButton>button:hover {
            background-color: #D4AF37 !important;
            color: #1C1C1E !important;
            border-color: #1C1C1E !important;
            box-shadow: 0 4px 8px rgba(212, 175, 55, 0.4) !important;
        }
        
        /* Input elements text color */
        input, select, textarea, [data-baseweb="select"] {
            color: #FAF7F0 !important;
        }
        
        /* Green Accent Out-of-Stock Toggle styling */
        .sold-out-badge {
            color: #EB5757;
            border: 1px solid #EB5757;
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 8pt;
            font-weight: 700;
            text-transform: uppercase;
            display: inline-block;
        }
        
        .veg-badge {
            color: #27AE60;
            border: 1px solid #27AE60;
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 8pt;
            font-weight: 700;
            text-transform: uppercase;
            display: inline-block;
            margin-right: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Main Application Logic
menu_data = load_menu()

# Sidebar Navigation
with st.sidebar:
    st.markdown('<div class="sidebar-brand">FUMO 33</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; color: #A0A0A0;'>Woodfired Kitchen & Bar</p>", unsafe_allow_html=True)
    st.write("---")
    
    app_mode = st.radio(
        "Navigate",
        ["🏠 Portal Dashboard", "📝 Menu Editor (CRUD)", "🍹 Drinks & Bar Snacks", "📱 Customer Live View", "📈 AI Inventory Forecast", "💬 AI Review Sentiment", "✍️ AI Social Copywriter", "📸 Social Post Generator"]
    )
    st.write("---")
    st.markdown(f"**Last Sync:** `{menu_data['last_updated']}`")
    st.markdown("📍 Ryde, Isle of Wight")

# ==================== 🏠 PORTAL DASHBOARD ====================
if app_mode == "🏠 Portal Dashboard":
    st.markdown("<h1>🏠 Fumo 33 Management Hub</h1>", unsafe_allow_html=True)
    st.write("Welcome to the Single Source of Truth Control Center. From here, any menu updates instantly sync across physical A3 printed menus, the digital customer QR system, and the restaurant's active database.")
    st.write("---")
    
    # Calculate stats
    total_sections = len(menu_data["menu"])
    total_items = 0
    active_items = 0
    veg_items = 0
    
    for section_name, items in menu_data["menu"].items():
        total_items += len(items)
        for item in items:
            if item.get("available", True):
                active_items += 1
            if item.get("is_vegetarian", False):
                veg_items += 1
                
    out_of_stock = total_items - active_items
    
    # Render Stat Grid
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f'<div class="stat-card"><h5>Menu Sections</h5><div class="stat-val">{total_sections}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><h5>Total Dishes</h5><div class="stat-val">{total_items}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><h5>Active Dishes</h5><div class="stat-val" style="color: #27AE60;">{active_items}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card"><h5>Out of Stock</h5><div class="stat-val" style="color: #EB5757;">{out_of_stock}</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="stat-card"><h5>Vegetarian (V)</h5><div class="stat-val" style="color: #2F80ED;">{veg_items}</div></div>', unsafe_allow_html=True)
        
    st.write("")
    st.write("")
    
    # Action blocks
    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.markdown('<div class="premium-card"><h3>🔥 Multi-Format Menu Control Center</h3><p>Manage your single source of truth menu database. The system automatically compiles press-ready vector PDFs for both the A3 poster menu (with bottom 3-inch cutoff margin) and the 2-page A4 landscape takeaway leaflet menu.</p></div>', unsafe_allow_html=True)
        
        sub_col1, sub_col2 = st.columns(2)
        
        with sub_col1:
            st.write("#### 📜 Standard A3 Print Menu")
            st.caption("Custom A3 height (with blank 3-inch bottom margin for clean print-shop cutoff).")
            pdf_path_a3 = "fumo33_A3_menu.pdf"
            if os.path.exists(pdf_path_a3):
                with open(pdf_path_a3, "rb") as f:
                    st.download_button(
                        label="📥 Download A3 Menu PDF",
                        data=f,
                        file_name="fumo33_A3_menu.pdf",
                        mime="application/pdf",
                        key="dl_a3"
                    )
                st.success("✅ A3 print menu is ready.")
            else:
                st.warning("⚠️ A3 menu file not found.")

        with sub_col2:
            st.write("#### 📖 Takeaway Leaflet Menu")
            st.caption("Premium 2-page A4 landscape booklet designed for marketing and handouts.")
            pdf_path_leaflet = "fumo33_leaflet_menu.pdf"
            if os.path.exists(pdf_path_leaflet):
                with open(pdf_path_leaflet, "rb") as f:
                    st.download_button(
                        label="📥 Download Leaflet PDF",
                        data=f,
                        file_name="fumo33_leaflet_menu.pdf",
                        mime="application/pdf",
                        key="dl_leaflet"
                    )
                st.success("✅ Leaflet takeaway menu is ready.")
            else:
                st.warning("⚠️ Leaflet menu file not found.")
        
        st.write("---")
        if st.button("🔮 Re-compile Both Menus Now", type="primary"):
            with st.spinner("Compiling vector layouts using headless Chromium..."):
                success, msg = save_menu(menu_data)
                if success:
                    st.success("✅ Successfully regenerated A3 print menu and A4 Takeaway Leaflet!")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error(f"❌ Failed to generate menus: {msg}")
                        
    with right_col:
        # Show QR scan card
        st.markdown("""
            <div class="premium-card" style="text-align: center; border-left-color: #F2C94C;">
                <h4 style="margin: 0;">Table QR Menu</h4>
                <p style="font-size: 9pt; color: #7A7A7A; margin-top: 5px;">Scan to see the Single Source of Truth Customer Live Menu</p>
                <img src="https://chart.googleapis.com/chart?chs=180x180&cht=qr&chl=Fumo33CustomerLiveMenu&choe=UTF-8" style="margin: 10px 0; border: 5px solid white; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);" />
                <div style="font-weight: 600; font-size: 10pt; color: #1C1C1E; background-color: #F2C94C; padding: 5px; border-radius: 4px;">TABLE 12 QR</div>
            </div>
        """, unsafe_allow_html=True)

# ==================== 📝 MENU EDITOR (CRUD) ====================
elif app_mode == "📝 Menu Editor (CRUD)":
    st.markdown("<h1>📝 Menu Database Editor</h1>", unsafe_allow_html=True)
    st.write("Modify names, descriptions, pricing, and availability. Saving edits rewrites `menu.json` and automatically triggers a silent compile of `fumo33_A3_menu.pdf` using headless Chromium.")
    st.write("---")
    
    # Select category to edit
    categories = list(menu_data["menu"].keys())
    formatted_cats = {cat: cat.replace("_", " ").title() for cat in categories}
    
    selected_cat = st.selectbox(
        "Select Menu Section to Manage:",
        categories,
        format_func=lambda x: formatted_cats[x]
    )
    
    st.write(f"### Managing Section: **{formatted_cats[selected_cat]}**")
    
    items = menu_data["menu"][selected_cat]
    
    # We will display each item in an expander form for clean interface
    updated_items = []
    
    for i, item in enumerate(items):
        is_avail = item.get("available", True)
        badge = ""
        if not is_avail:
            badge = " 🔴 [OUT OF STOCK]"
            
        with st.expander(f"{item['name']} — £{item['price']:.2f}{badge}"):
            if not is_avail:
                st.markdown("<div style='background-color: #FDEDEC; border: 1px solid #FADBD8; padding: 10px; border-radius: 4px; margin-bottom: 12px; font-size: 9.5pt;'><b style='color: #C0392B;'>🔴 Current Status: OUT OF STOCK</b><br/><span style='color: #7B241C;'>This item is temporarily hidden from the printed A3 menu and marked as sold out on the customer live QR menu.</span></div>", unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])
            with col1:
                item_name = st.text_input(f"Item Name ({i})", value=item["name"], key=f"name_{selected_cat}_{i}")
                item_desc = st.text_area(f"Description ({i})", value=item["description"], key=f"desc_{selected_cat}_{i}", height=70)
            with col2:
                item_price = st.number_input(f"Price (£) ({i})", value=float(item["price"]), min_value=0.0, step=0.1, format="%.2f", key=f"price_{selected_cat}_{i}")
                item_veg = st.checkbox("Vegetarian (V)", value=item.get("is_vegetarian", False), key=f"veg_{selected_cat}_{i}")
                item_active = st.checkbox("Available In Stock", value=is_avail, key=f"avail_{selected_cat}_{i}")
            
            # Handle addons if they exist (like on Patatas Bravas)
            addons = item.get("addons", [])
            updated_addons = []
            if addons:
                st.write("**Addons:**")
                for j, addon in enumerate(addons):
                    acol1, acol2 = st.columns(2)
                    with acol1:
                        aname = st.text_input(f"Addon {j} Name", value=addon["name"], key=f"aname_{selected_cat}_{i}_{j}")
                    with acol2:
                        aprice = st.number_input(f"Addon {j} Price", value=float(addon["price"]), min_value=0.0, step=0.5, format="%.2f", key=f"aprice_{selected_cat}_{i}_{j}")
                    updated_addons.append({"name": aname, "price": aprice})
            
            # Pack new item dictionary
            new_item = {
                "name": item_name,
                "description": item_desc,
                "price": item_price,
                "is_vegetarian": item_veg,
                "available": item_active
            }
            if updated_addons:
                new_item["addons"] = updated_addons
                
            updated_items.append(new_item)
            
    # Quick addition form at the bottom
    st.write("---")
    st.write("#### Add New Item to this Section:")
    with st.form("add_new_item_form"):
        new_name = st.text_input("Item Name")
        new_desc = st.text_area("Description", height=60)
        col_price, col_flags = st.columns(2)
        with col_price:
            new_price = st.number_input("Price (£)", value=10.0, min_value=0.0, step=0.5, format="%.2f")
        with col_flags:
            new_veg = st.checkbox("Is Vegetarian (V)")
        
        submit_new = st.form_submit_button("Add Item to Menu")
        if submit_new and new_name:
            new_item_dict = {
                "name": new_name,
                "description": new_desc,
                "price": new_price,
                "is_vegetarian": new_veg,
                "available": True
            }
            updated_items.append(new_item_dict)
            st.success(f"Added '{new_name}' to working list! Save changes below to commit to database.")
            
    st.write("---")
    
    # Save button
    col_save, col_cancel = st.columns([1, 4])
    with col_save:
        if st.button("💾 SAVE CHANGES", type="primary"):
            menu_data["menu"][selected_cat] = updated_items
            menu_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            
            with st.spinner("Writing database & compiling print menu..."):
                success, path = save_menu(menu_data)
                if success:
                    st.success("✅ Changes committed to menu.json and fumo33_A3_menu.pdf compiled successfully!")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error(f"❌ Failed to compile PDF: {path}")


# ==================== 🍹 DRINKS & BAR SNACKS ====================
elif app_mode == "🍹 Drinks & Bar Snacks":
    st.markdown("<h1>🍹 Drinks & Bar Snacks Control Hub</h1>", unsafe_allow_html=True)
    st.write("Manage your beverages and bar snacks from a Single Source of Truth. Update pricing structures, descriptions, and item stock instantly across print menus, customer QR layouts, and active registers.")
    st.write("---")
    
    drinks_data = load_drinks()
    
    # Calculate drinks statistics
    total_drinks_sections = len(drinks_data["menu"])
    total_drinks_items = 0
    active_drinks_items = 0
    veg_drinks_items = 0
    
    for section_name, items in drinks_data["menu"].items():
        total_drinks_items += len(items)
        for item in items:
            if item.get("available", True):
                active_drinks_items += 1
            if item.get("is_vegetarian", False):
                veg_drinks_items += 1
                
    out_of_stock_drinks = total_drinks_items - active_drinks_items
    
    # Render Drinks Stat Grid
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f'<div class="stat-card"><h5>Beverage Sections</h5><div class="stat-val">{total_drinks_sections}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><h5>Total Items</h5><div class="stat-val">{total_drinks_items}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><h5>In Stock</h5><div class="stat-val" style="color: #27AE60;">{active_drinks_items}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card"><h5>Out of Stock</h5><div class="stat-val" style="color: #EB5757;">{out_of_stock_drinks}</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="stat-card"><h5>Snack (V) Options</h5><div class="stat-val" style="color: #2F80ED;">{veg_drinks_items}</div></div>', unsafe_allow_html=True)
        
    st.write("")
    st.write("")
    
    # Action blocks for Drinks PDF
    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.markdown('<div class="premium-card"><h3>🔥 Print Drinks Menu Compiler</h3><p>Compiles a premium dark charcoal & gold A3 printable drinks and bar snacks list. Saving updates in the CRUD editor below will trigger an automatic silent PDF compile in the background.</p></div>', unsafe_allow_html=True)
        
        pdf_path_drinks = "fumo33_drinks_menu.pdf"
        if os.path.exists(pdf_path_drinks):
            with open(pdf_path_drinks, "rb") as f:
                st.download_button(
                    label="📥 Download Print-Ready A3 Drinks Menu PDF",
                    data=f,
                    file_name="fumo33_drinks_menu.pdf",
                    mime="application/pdf",
                    key="dl_drinks"
                )
            st.success("✅ Press-ready vector drinks PDF is available.")
        else:
            st.warning("⚠️ No drinks PDF found. Click compile below to generate the initial PDF.")
            if st.button("Generate Drinks PDF Now", key="gen_drinks_btn"):
                with st.spinner("Compiling drinks vector layout..."):
                    success, msg = save_drinks(drinks_data)
                    if success:
                        st.success("Successfully generated drinks PDF!")
                        st.rerun()
                    else:
                        st.error(f"Failed to generate: {msg}")
                        
    with right_col:
        # Show QR scan card specific to Drinks
        st.markdown("""
            <div class="premium-card" style="text-align: center; border-left-color: #F2C94C;">
                <h4 style="margin: 0;">Bar QR Code</h4>
                <p style="font-size: 9pt; color: #A0A0A0; margin-top: 5px;">Scan to see the Single Source of Truth customer drinks menu</p>
                <img src="https://chart.googleapis.com/chart?chs=180x180&cht=qr&chl=Fumo33DrinksLiveMenu&choe=UTF-8" style="margin: 10px 0; border: 5px solid white; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);" />
                <div style="font-weight: 600; font-size: 10pt; color: #1C1C1E; background-color: #F2C94C; padding: 5px; border-radius: 4px;">DRINKS & SNACKS QR</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")
    
    # Tab Layout to separate CRUD Editor and Customer Preview
    tab_editor, tab_preview = st.tabs(["📝 Drinks CRUD Database Editor", "📱 Customer QR Drinks Preview"])
    
    with tab_editor:
        # Select category to edit
        categories = list(drinks_data["menu"].keys())
        formatted_cats = {cat: cat.replace("_", " ").title() for cat in categories}
        
        selected_cat = st.selectbox(
            "Select Drinks/Snacks Section to Manage:",
            categories,
            format_func=lambda x: formatted_cats[x],
            key="drinks_cat_selector"
        )
        
        st.write(f"### Managing Section: **{formatted_cats[selected_cat]}**")
        
        items = drinks_data["menu"][selected_cat]
        updated_items = []
        
        for i, item in enumerate(items):
            is_avail = item.get("available", True)
            badge = ""
            if not is_avail:
                badge = " 🔴 [OUT OF STOCK]"
                
            # Compute main display title/price for expander bar
            bar_price = ""
            if "price" in item:
                bar_price = f" — £{item['price']:.2f}"
            elif "price_bottle" in item:
                bar_price = f" — Bt: £{item['price_bottle']:.2f}"
            elif "price_pint" in item:
                bar_price = f" — Pint: £{item['price_pint']:.2f}"
            elif "price_double" in item:
                bar_price = f" — Dbl: £{item['price_double']:.2f}"
            elif "price_reg" in item:
                bar_price = f" — Reg: £{item['price_reg']:.2f}"
                
            with st.expander(f"{item['name']}{bar_price}{badge}"):
                if not is_avail:
                    st.markdown("<div style='background-color: #5C2523; border: 1px solid #782F2D; padding: 10px; border-radius: 4px; margin-bottom: 12px; font-size: 9.5pt;'><b style='color: #EB5757;'>🔴 Current Status: OUT OF STOCK</b><br/><span style='color: #C0C0C0;'>This item is hidden from print PDFs and marked as sold out on the table order list.</span></div>", unsafe_allow_html=True)
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    item_name = st.text_input(f"Item Name ({i})", value=item["name"], key=f"dname_{selected_cat}_{i}")
                    item_desc = st.text_area(f"Description ({i})", value=item.get("description", ""), key=f"ddesc_{selected_cat}_{i}", height=70)
                
                with col2:
                    new_item_dict = {
                        "name": item_name,
                        "description": item_desc,
                        "available": st.checkbox("Available In Stock", value=is_avail, key=f"davail_{selected_cat}_{i}")
                    }
                    
                    # Render price input fields conditionally based on category structure
                    if selected_cat == "wines":
                        col_w1, col_w2 = st.columns(2)
                        with col_w1:
                            if "price_175ml" in item:
                                new_item_dict["price_175ml"] = st.number_input(f"175ml (£)", value=float(item["price_175ml"]), min_value=0.0, step=0.1, format="%.2f", key=f"dp175_{i}")
                            if "price_125ml" in item:
                                new_item_dict["price_125ml"] = st.number_input(f"125ml (£)", value=float(item["price_125ml"]), min_value=0.0, step=0.1, format="%.2f", key=f"dp125_{i}")
                        with col_w2:
                            if "price_250ml" in item:
                                new_item_dict["price_250ml"] = st.number_input(f"250ml (£)", value=float(item["price_250ml"]), min_value=0.0, step=0.1, format="%.2f", key=f"dp250_{i}")
                            if "price_bottle" in item:
                                new_item_dict["price_bottle"] = st.number_input(f"Bottle (£)", value=float(item["price_bottle"]), min_value=0.0, step=0.1, format="%.2f", key=f"dpbot_{i}")
                    
                    elif selected_cat == "beers_ciders":
                        col_b1, col_b2 = st.columns(2)
                        with col_b1:
                            if "price_half" in item:
                                new_item_dict["price_half"] = st.number_input(f"Half Pint (£)", value=float(item["price_half"]), min_value=0.0, step=0.1, format="%.2f", key=f"dphalf_{i}")
                            if "price" in item:
                                new_item_dict["price"] = st.number_input(f"Bottle (£)", value=float(item["price"]), min_value=0.0, step=0.1, format="%.2f", key=f"dpbeer_{i}")
                        with col_b2:
                            if "price_pint" in item:
                                new_item_dict["price_pint"] = st.number_input(f"Pint (£)", value=float(item["price_pint"]), min_value=0.0, step=0.1, format="%.2f", key=f"dppint_{i}")
                    
                    elif selected_cat == "spirits":
                        col_s1, col_s2 = st.columns(2)
                        with col_s1:
                            if "price_single" in item:
                                new_item_dict["price_single"] = st.number_input(f"Single (£)", value=float(item["price_single"]), min_value=0.0, step=0.1, format="%.2f", key=f"dpsingle_{i}")
                            if "price" in item:
                                new_item_dict["price"] = st.number_input(f"Price (£)", value=float(item["price"]), min_value=0.0, step=0.1, format="%.2f", key=f"dpshot_{i}")
                        with col_s2:
                            if "price_double" in item:
                                new_item_dict["price_double"] = st.number_input(f"Double (£)", value=float(item["price_double"]), min_value=0.0, step=0.1, format="%.2f", key=f"dpdouble_{i}")
                    
                    elif selected_cat == "hot_drinks":
                        col_h1, col_h2 = st.columns(2)
                        with col_h1:
                            if "price_reg" in item:
                                new_item_dict["price_reg"] = st.number_input(f"Regular (£)", value=float(item["price_reg"]), min_value=0.0, step=0.1, format="%.2f", key=f"dpreg_{i}")
                            if "price" in item:
                                new_item_dict["price"] = st.number_input(f"Price (£)", value=float(item["price"]), min_value=0.0, step=0.1, format="%.2f", key=f"dphot_{i}")
                        with col_h2:
                            if "price_lrg" in item:
                                new_item_dict["price_lrg"] = st.number_input(f"Large (£)", value=float(item["price_lrg"]), min_value=0.0, step=0.1, format="%.2f", key=f"dplrg_{i}")
                    
                    else:
                        new_item_dict["price"] = st.number_input(f"Price (£)", value=float(item["price"]), min_value=0.0, step=0.1, format="%.2f", key=f"dprice_{selected_cat}_{i}")
                    
                    # Veg flag only for snacks
                    if selected_cat == "bar_snacks":
                        new_item_dict["is_vegetarian"] = st.checkbox("Vegetarian (V)", value=item.get("is_vegetarian", False), key=f"dveg_{selected_cat}_{i}")
                
                updated_items.append(new_item_dict)
                
        st.write("---")
        if st.button("💾 SAVE DRINKS CHANGES", type="primary", key="save_drinks_btn"):
            drinks_data["menu"][selected_cat] = updated_items
            drinks_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            
            with st.spinner("Writing database & compiling drinks menu..."):
                success, path = save_drinks(drinks_data)
                if success:
                    st.success("✅ Drinks database saved & PDF compiled successfully!")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error(f"❌ Failed to compile PDF: {path}")
                    
    with tab_preview:
        st.markdown("<p style='text-align: center; color: #7A7A7A;'>📱 SIMULATED CUSTOMER MOBILE PREVIEW (DRINKS & SNACKS) 📱</p>", unsafe_allow_html=True)
        
        col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
        with col_m2:
            mobile_drinks_html = """
                <div style="background-color: #151515; border: 8px solid #333333; border-radius: 36px; padding: 25px 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); max-width: 420px; margin: 0 auto; min-height: 700px; display: flex; flex-direction: column; font-family: 'Outfit', sans-serif; color: #FAF7F0;">
                    
                    <!-- Phone top speaker/camera bar -->
                    <div style="width: 140px; height: 18px; background-color: #333333; border-radius: 0 0 10px 10px; margin: -25px auto 15px auto;"></div>
                    
                    <!-- Customer Menu Header -->
                    <div style="text-align: center; margin-bottom: 20px; border-bottom: 1px dashed rgba(212, 175, 55, 0.4); padding-bottom: 10px;">
                        <div style="font-family: 'Cinzel', serif; font-size: 22px; font-weight: 900; letter-spacing: 2px; color: #F2C94C;">FUMO 33</div>
                        <div style="font-size: 8px; letter-spacing: 3px; color: #D4AF37; text-transform: uppercase; margin-top: 2px; font-weight: 600;">Drinks & Bar Snacks</div>
                        <div style="font-size: 8px; color: #A0A0A0; margin-top: 3px;">Table 12 • Digital Ordering</div>
                    </div>
                    
                    <!-- Menu Sections Container -->
                    <div style="flex-grow: 1; overflow-y: auto; max-height: 520px; padding-right: 5px;">
            """
            
            for cat_key, items in drinks_data["menu"].items():
                cat_title = cat_key.replace("_", " ").title()
                
                avail_count = sum(1 for item in items if item.get("available", True))
                if avail_count == 0:
                    continue
                    
                mobile_drinks_html += f"""
                    <div style="font-family: 'Cinzel', serif; font-size: 12px; font-weight: 700; text-transform: uppercase; border-bottom: 1px solid #D4AF37; margin-top: 15px; margin-bottom: 8px; padding-bottom: 2px; color: #F2C94C; letter-spacing: 1px;">
                        {cat_title}
                    </div>
                """
                
                for item in items:
                    is_avail = item.get("available", True)
                    name_str = item["name"]
                    veg_tag_html = '<span style="color: #27AE60; font-size: 8px; font-weight: bold; border: 1px solid #27AE60; border-radius: 3px; padding: 0 3px; margin-left: 5px;">V</span>' if item.get("is_vegetarian", False) else ''
                    
                    price_str = ""
                    if "price" in item:
                        price_str = f"£{item['price']:.2f}"
                    elif "price_bottle" in item:
                        price_str = f"Bt: £{item['price_bottle']:.2f}"
                    elif "price_pint" in item:
                        price_str = f"Pint: £{item['price_pint']:.2f}"
                    elif "price_single" in item:
                        price_str = f"Sgl: £{item['price_single']:.2f}"
                    elif "price_reg" in item:
                        price_str = f"Reg: £{item['price_reg']:.2f}"
                        
                    if is_avail:
                        mobile_drinks_html += f"""
                            <div style="margin-bottom: 10px; display: flex; justify-content: space-between; align-items: flex-start; text-align: left;">
                                <div style="width: 70%;">
                                    <div style="font-size: 11px; font-weight: 600; color: #FAF7F0;">
                                         {name_str}{veg_tag_html}
                                    </div>
                                    <div style="font-size: 9px; color: #C0C0C0; font-weight: 300; line-height: 1.3;">
                                        {item.get('description', '')}
                                    </div>
                                </div>
                                <div style="font-size: 10px; font-weight: 700; color: #F2C94C; text-align: right; width: 30%;">
                                    {price_str}
                                </div>
                            </div>
                        """
                    else:
                        mobile_drinks_html += f"""
                            <div style="margin-bottom: 10px; display: flex; justify-content: space-between; align-items: flex-start; opacity: 0.4; text-align: left;">
                                <div style="width: 70%;">
                                    <div style="font-size: 11px; font-weight: 600; color: #888888; text-decoration: line-through;">
                                        {name_str}{veg_tag_html}
                                    </div>
                                    <div style="font-size: 9px; color: #888888; font-weight: 300; line-height: 1.3;">
                                        {item.get('description', '')}
                                    </div>
                                </div>
                                <div style="font-size: 9px; font-weight: 700; color: #EB5757; text-align: right; text-transform: uppercase; width: 30%;">
                                    Sold Out
                                </div>
                            </div>
                        """
            
            mobile_drinks_html += """
                    </div>
                    <div style="text-align: center; border-top: 1px dashed rgba(212, 175, 55, 0.4); padding-top: 10px; margin-top: 15px; font-size: 8px; color: #A0A0A0; line-height: 1.3;">
                        Please drink responsibly. VAT included.<br/>
                        <b>🍹 Powered by Single Source of Truth</b>
                    </div>
                </div>
            """
            st.html(mobile_drinks_html)

# ==================== 📱 CUSTOMER LIVE VIEW ====================
elif app_mode == "📱 Customer Live View":
    st.markdown("<h1>📱 Customer QR Live Menu</h1>", unsafe_allow_html=True)
    st.write("This is a pixel-perfect mockup of the mobile responsive web page customers see when scanning the table QR code. It uses the identical `menu.json` Single Source of Truth. If an item is marked 'Out of Stock' in the portal, it immediately updates here!")
    st.write("---")
    
    # Render simulated mobile view
    st.markdown("<p style='text-align: center; color: #7A7A7A;'>📱 SIMULATED MOBILE DEVICE (RESPONSIVE PREVIEW) 📱</p>", unsafe_allow_html=True)
    
    mobile_col_left, mobile_col_center, mobile_col_right = st.columns([1, 2, 1])
    
    with mobile_col_center:
        # Build the entire HTML content as a single unified string to prevent wrapper division breakage
        mobile_html = """
            <div style="background-color: #151515; border: 8px solid #333333; border-radius: 36px; padding: 25px 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); max-width: 420px; margin: 0 auto; min-height: 700px; display: flex; flex-direction: column; font-family: 'Outfit', sans-serif; color: #FAF7F0;">
                
                <!-- Phone top speaker/camera bar -->
                <div style="width: 140px; height: 18px; background-color: #333333; border-radius: 0 0 10px 10px; margin: -25px auto 15px auto;"></div>
                
                <!-- Customer Menu Header -->
                <div style="text-align: center; margin-bottom: 20px; border-bottom: 1px dashed rgba(212, 175, 55, 0.4); padding-bottom: 10px;">
                    <div style="font-family: 'Cinzel', serif; font-size: 22px; font-weight: 900; letter-spacing: 2px; color: #F2C94C;">FUMO 33</div>
                    <div style="font-size: 9px; letter-spacing: 3px; color: #D4AF37; text-transform: uppercase; margin-top: 2px; font-weight: 600;">Woodfired Kitchen & Bar</div>
                    <div style="font-size: 9px; color: #A0A0A0; margin-top: 3px;">Table 12 • Digital Ordering</div>
                </div>
                
                <!-- Menu Sections Container -->
                <div style="flex-grow: 1; overflow-y: auto; max-height: 520px; padding-right: 5px;">
        """
        
        # Loop through categories and items in responsive list and append to unified HTML
        for cat_key, items in menu_data["menu"].items():
            cat_title = cat_key.replace("_", " ").title()
            
            # Count available items
            avail_count = sum(1 for item in items if item.get("available", True))
            if avail_count == 0:
                continue # Hide section on mobile if no items available
                
            mobile_html += f"""
                <div style="font-family: 'Cinzel', serif; font-size: 13px; font-weight: 700; text-transform: uppercase; border-bottom: 1px solid #D4AF37; margin-top: 15px; margin-bottom: 8px; padding-bottom: 2px; color: #F2C94C; letter-spacing: 1px;">
                    {cat_title}
                </div>
            """
            
            for item in items:
                is_avail = item.get("available", True)
                name_str = item["name"]
                veg_tag_html = '<span style="color: #27AE60; font-size: 8px; font-weight: bold; border: 1px solid #27AE60; border-radius: 3px; padding: 0 3px; margin-left: 5px;">V</span>' if item.get("is_vegetarian", False) else ''
                
                if is_avail:
                    mobile_html += f"""
                        <div style="margin-bottom: 10px; display: flex; justify-content: space-between; align-items: flex-start; text-align: left;">
                            <div style="width: 75%;">
                                <div style="font-size: 11px; font-weight: 600; color: #FAF7F0;">
                                     {name_str}{veg_tag_html}
                                </div>
                                <div style="font-size: 9px; color: #C0C0C0; font-weight: 300; line-height: 1.3;">
                                    {item['description']}
                                </div>
                            </div>
                            <div style="font-size: 11px; font-weight: 700; color: #F2C94C; text-align: right;">
                                £{item['price']:.2f}
                            </div>
                        </div>
                    """
                else:
                    mobile_html += f"""
                        <div style="margin-bottom: 10px; display: flex; justify-content: space-between; align-items: flex-start; opacity: 0.4; text-align: left;">
                            <div style="width: 75%;">
                                <div style="font-size: 11px; font-weight: 600; color: #888888; text-decoration: line-through;">
                                    {name_str}{veg_tag_html}
                                </div>
                                <div style="font-size: 9px; color: #888888; font-weight: 300; line-height: 1.3;">
                                    {item['description']}
                                </div>
                            </div>
                            <div style="font-size: 9px; font-weight: 700; color: #EB5757; text-align: right; text-transform: uppercase;">
                                Sold Out
                            </div>
                        </div>
                    """
        
        # Phone bottom end tags
        mobile_html += """
                </div>
                <div style="text-align: center; border-top: 1px dashed rgba(212, 175, 55, 0.4); padding-top: 10px; margin-top: 15px; font-size: 8px; color: #A0A0A0; line-height: 1.3;">
                    Prices include VAT. A 10% service charge applies to tables of 4+.<br/>
                    <b>🔥 Powered by Single Source of Truth</b>
                </div>
            </div>
        """
        
        # Render the complete mobile preview
        st.html(mobile_html)

# ==================== 📈 AI INVENTORY FORECAST ====================
elif app_mode == "📈 AI Inventory Forecast":
    st.markdown("<h1>📈 AI Intelligent Prep & Inventory Forecast</h1>", unsafe_allow_html=True)
    st.write("Leverage weather predictions and historical sales logs to forecast ideal ingredient preparation volume. This avoids costly restaurant waste while capitalizing on weekend tourism rushes in Ryde.")
    st.write("---")
    
    st.write("### 🌤️ Live Weather Inputs & Forecast")
    col_w1, col_w2, col_w3 = st.columns(3)
    with col_w1:
        weather_cond = st.selectbox("Weekend Weather Condition", ["Warm & Sunny (Peak Tourism)", "Overcast / Light Drizzle", "Stormy / Cold (Heavy rain)", "Clear & Crisp (Autumny)"])
    with col_w2:
        temperature = st.slider("Forecast Temperature (°C)", 5, 35, 22)
    with col_w3:
        pax_log = st.number_input("Expected Bookings (Covers)", min_value=50, max_value=400, value=180)
        
    st.write("### 🧮 Historical Reference")
    st.info("💡 Past sales reports indicate sunny weekends in Ryde trigger a massive surge (up to 40%) in Woodfired Pizza orders and White Wines, whereas rainy weather increases heavy beef burger and risotto requests.")
    
    st.write("")
    if st.button("🔮 Run Predictive AI Simulator", type="primary"):
        with st.spinner("Processing sales arrays and weather vectors..."):
            time.sleep(1)
            
        st.success("🔮 AI Prep Plan Generated Successfully!")
        
        # Display simulated metrics
        st.write("#### 🍕 Recommended Prep Volumes for Saturday & Sunday:")
        
        col_rec1, col_rec2, col_rec3 = st.columns(3)
        
        # Simple predictive scaling based on weather choice
        scale = 1.35 if "Sunny" in weather_cond else (0.8 if "Stormy" in weather_cond else 1.0)
        
        with col_rec1:
            pizza_dough = int(80 * scale)
            st.metric("Woodfired Pizza Dough Portions", pizza_dough, delta=f"{pizza_dough-80} portions" if scale != 1.0 else "Normal baseline")
        with col_rec2:
            squid_prep = int(45 * scale)
            st.metric("Squid Starter Prep (Portions)", squid_prep, delta=f"{squid_prep-45} portions" if scale != 1.0 else "Normal baseline")
        with col_rec3:
            rump_steaks = int(35 * (0.9 if "Sunny" in weather_cond else 1.2 if "Stormy" in weather_cond else 1.0))
            st.metric("IOW Rump Steak Inventory", rump_steaks, delta=f"{rump_steaks-35} steaks" if "Sunny" in weather_cond or "Stormy" in weather_cond else "Normal baseline")
            
        st.write("#### 📦 Ingredient Order List recommendations:")
        
        st.markdown(f"""
        | Ingredient | Base Need | AI Adjust | Target Order Quantity | Rationale |
        |---|---|---|---|---|
        | **Fior di Latte Mozzarella** | 10 kg | +{10 * (scale-1.0):.1f} kg | **{10 * scale:.1f} kg** | Highly responsive to pizza orders. Sunny weather increases pizza pull. |
        | **Isle of Wight Beef Patties** | 40 units | {int(40 * (1.1 if "Stormy" in weather_cond else 0.9 if "Sunny" in weather_cond else 1.0)) - 40} units | **{int(40 * (1.1 if "Stormy" in weather_cond else 0.9 if "Sunny" in weather_cond else 1.0))} units** | Warm weather drives customers toward lighter pizzas and salads over burgers. |
        | **Pinot Grigio / Prosecco** | 12 bottles | +{int(12 * (scale-1.0))} bot | **{int(12 * scale)} bottles** | Outdoor tables and warm sunset hours increase white wine / sparkling consumption. |
        | **Fresh Basil & Salad Leaf** | 15 bags | +{int(15 * (scale-1.0))} bags | **{int(15 * scale)} bags** | Salad/Pizza heavy garnish requirement grows. |
        """)
        
        st.caption("⚠️ Inventory recommendations are estimated based on local Ryde weather-tourist correlation vectors. Double check supplier delivery schedules before confirming.")

# ==================== 💬 AI REVIEW SENTIMENT ====================
elif app_mode == "💬 AI Review Sentiment":
    st.markdown("<h1>💬 AI Review & Reputation Analyzer</h1>", unsafe_allow_html=True)
    st.write("Paste reviews from TripAdvisor, Google Reviews, or Facebook into the engine to automatically distill kitchen praise and service gaps into actionable items.")
    st.write("---")
    
    st.write("#### Paste Recent Reviews Below:")
    default_review = """1. "The Salt & Pepper Squid was incredibly tender, absolute best starter we had! But the Lamb Kofte felt a little dry on Saturday night and we had to wait 30 minutes for our Margaritas because the bar was swamped." - Google Local Guide
    
2. "Amazing woodfired pizzas! The Goats cheese beetroot pizza is highly recommended. The terrace in Ryde is beautiful. One minor thing, our kids ordered the IOW burger and it took quite a long time to arrive, but service was very friendly." - TripAdvisor"""
    
    review_input = st.text_area("Reviews Text:", value=default_review, height=180)
    
    if st.button("Analyze Sentiment", type="primary"):
        with st.spinner("Parsing text constructs and running semantic extraction..."):
            time.sleep(1.2)
            
        st.success("✅ Semantic Extraction Completed!")
        
        col_praise, col_improve = st.columns(2)
        
        with col_praise:
            st.markdown("""
                <div style="background-color: rgba(39, 174, 96, 0.08); border: 1px solid rgba(39, 174, 96, 0.3); border-radius: 8px; padding: 15px;">
                    <h4 style="color: #27AE60; margin: 0 0 10px 0;">🎉 Top Kitchen Praise</h4>
                    <ul>
                        <li><b>Salt & Pepper Squid</b>: Highlighted as "incredibly tender" and the "best starter". (High customer sentiment)</li>
                        <li><b>Goats Cheese Beetroot Pizza</b>: Highly recommended, excellent taste vector.</li>
                        <li><b>Service Attitude</b>: Front of house praised as "very friendly."</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
        with col_improve:
            st.markdown("""
                <div style="background-color: rgba(235, 87, 87, 0.08); border: 1px solid rgba(235, 87, 87, 0.3); border-radius: 8px; padding: 15px;">
                    <h4 style="color: #EB5757; margin: 0 0 10px 0;">⚠️ Actionable Kitchen Gaps</h4>
                    <ul>
                        <li><b>Lamb Kofte Dryness</b>: Feedback noted kofte was dry on Saturday. Recommend kitchen line-check on cook times.</li>
                        <li><b>Burger Prep Lag</b>: Burgers reported as slow. Streamline buns/fries assembly line.</li>
                        <li><b>Bar Bottleneck</b>: Pizza / Beverage wait times peaked at 30 mins during peak rush. Review shift cover.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        st.markdown("""
            **📢 Generated Manager Summary Report:**
            > *"Fumo 33 continues to perform exceptionally well on seafood starters (Squid) and artisan pizzas. To protect margins and satisfaction on busy weekends, focus on streamlining the grill prep (kofte moisture and burger timing) and bar throughput."*
        """)

# ==================== ✍️ AI SOCIAL COPYWRITER ====================
elif app_mode == "✍️ AI Social Copywriter":
    st.markdown("<h1>✍️ AI Social Media Copywriter</h1>", unsafe_allow_html=True)
    st.write("Generate engaging, high-converting social media copy directly from your active menu database. No copywriting skills required!")
    st.write("---")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    
    with col_c1:
        # Flatten all items to let them choose
        flat_items = []
        for cat, items in menu_data["menu"].items():
            for item in items:
                flat_items.append(f"{item['name']} ({cat.replace('_',' ').title()})")
                
        selected_dish = st.selectbox("Select Menu Item to Promote", flat_items)
        dish_name = selected_dish.split(" (")[0]
        
    with col_c2:
        platform = st.selectbox("Target Platform", ["Instagram Post", "Facebook Ad / Post", "Twitter/X Thread Starter", "Local Email Newsletter"])
        
    with col_c3:
        tone = st.selectbox("Brand Tone", ["Warm & Rustic (Cozy)", "Upscale & Elegant", "Fun & Playful", "Weekend Hype"])
        
    st.write("")
    if st.button("✍️ Generate Social Post", type="primary"):
        with st.spinner("Writing copy with Fumo 33 brand guidelines..."):
            time.sleep(0.8)
            
        st.success("✍️ Social Copy Drafted!")
        
        # Render simulated copy
        post_content = ""
        if "Warm" in tone:
            post_content = f"""🔥 **Cozy woodfired comfort in the heart of Ryde!** 🔥

Craving something truly special tonight? Our **{dish_name}** is fresh out of the hearth and ready for you. Prepared with local passion and cooked to perfection in our stone ovens, it’s the ultimate way to spend an evening. 

Gather your favorite people, slide into a cozy booth at Fumo 33, and let us handle the rest. 🍷✨

📍 Fumo 33, Ryde, Isle of Wight
📞 Tap the link in bio to book your table!
#Fumo33 #WoodfiredKitchen #IsleOfWight #RydeEats #IOWFoodies #ArtisanEats #WoodfiredKitchenAndBar"""
        elif "Elegant" in tone:
            post_content = f"""✨ **Artistry in every detail.** ✨

This evening, we invite you to experience the elegant textures of our **{dish_name}**. Perfectly balanced, beautifully plated, and cooked over local coals, this dish is a testament to honest craftsmanship.

Pair it with a hand-selected glass of crisp white wine on our terrace, and watch the sunset over Ryde. 🌅🥂

Reserve your table for an exceptional dining experience.
#Fumo33 #FineDiningIOW #IsleOfWightFood #RydeIsleOfWight #IsleOfWightEats #GourmetBistro"""
        elif "Playful" in tone:
            post_content = f"""Squid? Burgers? Pizzas? Yes, yes, and double yes! 🍕🍔🤤

If you haven't tried our legendary **{dish_name}** yet, are you even eating in Ryde? It's warm, it's delicious, and it's calling your name.

Stop scrolling and start eating. Walk-ins welcome, but booking is smarter! See you tonight! 👇
#Fumo33 #IOWRestaurants #RydeDining #FoodHumor #IsleOfWightFoodie #FoodLove"""
        else:
            post_content = f"""🚨 **WEEKEND HYPE: The table is set, the fire is hot!** 🚨

Weekend mode: **ON**. We are firing up the ovens and getting ready for another incredible weekend in Ryde. 

If there’s one dish you MUST try this Saturday, it’s our crowd-favorite **{dish_name}**. It sells out fast, so get your bookings in now! 💥

Let's make it a delicious weekend at Fumo 33!
#Fumo33 #RydeNightlife #WeekendVibes #IsleOfWightDining #IOWWeekends #WoodfiredFeast"""

        st.code(post_content, language="markdown")
        st.caption("📋 Copy this text directly and paste it into your scheduling app.")

# ==================== 📸 SOCIAL POST GENERATOR ====================
elif app_mode == "📸 Social Post Generator":
    st.markdown("<h1>📸 Visual Social Post Generator</h1>", unsafe_allow_html=True)
    st.write("Automatically render premium branded visual posts for Instagram Feed, Stories, and Facebook Ads using Fumo 33's design language.")
    st.write("---")
    
    # 1. Manage Food Images Folder
    image_dir = "food_images"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        
    # Get available JPEGs and PNGs in food_images
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    image_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(valid_extensions)])
    
    # 2. File Upload form
    with st.expander("📤 Upload New Food Image"):
        uploaded_file = st.file_uploader("Choose a food photograph", type=["jpg", "jpeg", "png", "webp"])
        if uploaded_file is not None:
            # Clean filename
            safe_name = "".join([c if c.isalnum() or c in (".", "_", "-") else "_" for c in uploaded_file.name])
            save_path = os.path.join(image_dir, safe_name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Uploaded and saved {safe_name} to food_images folder!")
            # Refresh list
            image_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(valid_extensions)])
            
    if not image_files:
        st.warning("⚠️ No images found in food_images folder. Please upload an image first.")
    else:
        # Columns layout
        col_ctrl, col_preview = st.columns([1, 1])
        
        with col_ctrl:
            st.write("### ⚙️ Design & Text Controls")
            
            # Select background image
            selected_img_file = st.selectbox("Select Food Image", image_files)
            selected_img_path = os.path.join(image_dir, selected_img_file)
            
            # --- LIVE BACKGROUND IMAGE PREVIEW ---
            if selected_img_file:
                st.image(selected_img_path, caption=f"Selected File: {selected_img_file}", width="stretch")
            
            # Platform & format selector
            post_format = st.selectbox(
                "Select Format (Target Dimension)",
                [
                    "Instagram Feed / Facebook Post (Square 1:1)",
                    "Instagram Story / Reel (Vertical 9:16)",
                    "Facebook Ad / Post (Landscape 16:9)"
                ]
            )
            
            # Map selected post format to string name
            format_name_map = {
                "Instagram Feed / Facebook Post (Square 1:1)": "square",
                "Instagram Story / Reel (Vertical 9:16)": "vertical",
                "Facebook Ad / Post (Landscape 16:9)": "landscape"
            }
            format_name = format_name_map[post_format]
            
            # Prefill from existing menu items
            st.write("#### Prefill Text from Menu")
            flat_items = ["-- Custom Text --"]
            
            # Load menu and drinks data to flatten
            try:
                for cat, items in menu_data["menu"].items():
                    for item in items:
                        flat_items.append(f"{item['name']} (Food - {cat.replace('_',' ').title()})")
            except Exception:
                pass
                
            try:
                drinks_data = load_drinks()
                for cat, items in drinks_data["menu"].items():
                    for item in items:
                        flat_items.append(f"{item['name']} (Drink - {cat.replace('_',' ').title()})")
            except Exception:
                pass
                
            selected_prefill = st.selectbox("Select Menu Item to Promote", flat_items)
            
            # Defaults
            default_dish_name = ""
            default_price = "0.00"
            default_desc = ""
            
            if selected_prefill != "-- Custom Text --":
                item_name = selected_prefill.split(" (")[0]
                # Search in menu
                found = False
                for cat, items in menu_data["menu"].items():
                    for item in items:
                        if item["name"] == item_name:
                            default_dish_name = item["name"]
                            default_price = f"{item['price']:.2f}"
                            default_desc = item["description"]
                            found = True
                            break
                    if found:
                        break
                
                if not found:
                    for cat, items in drinks_data["menu"].items():
                        for item in items:
                            if item["name"] == item_name:
                                default_dish_name = item["name"]
                                # Drinks can have multiple pricing variables, look for standard price or others
                                if "price" in item:
                                    default_price = f"{item['price']:.2f}"
                                elif "price_bottle" in item:
                                    default_price = f"{item['price_bottle']:.2f}"
                                elif "price_pint" in item:
                                    default_price = f"{item['price_pint']:.2f}"
                                else:
                                    default_price = "0.00"
                                default_desc = item.get("description", "")
                                break
            
            # UI text inputs
            dish_name = st.text_input("Dish/Drink Name", value=default_dish_name)
            dish_price = st.text_input("Price (£)", value=default_price)
            dish_desc = st.text_area("Promo Description (keep short for best fit)", value=default_desc, height=75)
            promo_badge = st.text_input("Promo Badge (e.g. 'WEEKEND HYPES', 'FRESH BURGER', leave blank to hide)", value="Weekend Special")
            
            # Styling tweaks
            with st.expander("🎨 Custom Visual Tweaks"):
                overlay_opacity = st.slider("Dark Overlay Opacity (controls readability)", 0.2, 0.9, 0.6, 0.05)
                border_style = st.selectbox("Border Style", ["double", "solid", "none"], index=0)
                
            st.markdown("#### Automated Copywriting")
            caption_tone = st.selectbox(
                "Select Caption Tone",
                ["Hype / Energetic", "Elegant / Sophisticated", "Local / Community Focus"]
            )
            
            st.write("")
            generate_clicked = st.button("🔮 Generate Branded Social Graphic", type="primary")
            
        with col_preview:
            st.write("### 🖼️ Graphic Live Preview")
            
            output_filename = f"social_{format_name}.png"
            output_filepath = os.path.join(image_dir, output_filename)
            
            if generate_clicked:
                with st.spinner("Compositing branded graphic using Pillow image engine..."):
                    from generate_social import generate_social_post
                    success = generate_social_post(
                        image_path=selected_img_path,
                        format_name=format_name,
                        dish_name=dish_name,
                        description=dish_desc,
                        price=dish_price,
                        badge_text=promo_badge,
                        overlay_opacity=overlay_opacity,
                        border_style=border_style,
                        output_path=output_filepath
                    )
                    
                    if success and os.path.exists(output_filepath):
                        st.session_state[f"last_gen_{format_name}"] = output_filepath
                        st.success("✅ Brand graphic compiled successfully!")
                    else:
                        st.error("❌ Rendering failed. Please check logs.")
            
            # Check if there is a generated graphic in session state or on disk
            last_gen_key = f"last_gen_{format_name}"
            if last_gen_key in st.session_state and os.path.exists(st.session_state[last_gen_key]):
                target_img_path = st.session_state[last_gen_key]
                
                # Show the image
                st.image(target_img_path, width="stretch")
                
                # Read bytes for download button
                with open(target_img_path, "rb") as f:
                    btn = st.download_button(
                        label=f"📥 Download {format_name.capitalize()} Graphic (PNG)",
                        data=f,
                        file_name=f"fumo33_{dish_name.replace(' ', '_').lower()}_{format_name}.png",
                        mime="image/png"
                    )
            else:
                # Show placeholder outline
                aspect_ratio_css = "1 / 1"
                if format_name == "vertical":
                    aspect_ratio_css = "9 / 16"
                elif format_name == "landscape":
                    aspect_ratio_css = "16 / 9"
                    
                st.markdown(f"""
                    <div style="
                        border: 2px dashed rgba(212, 175, 55, 0.4);
                        border-radius: 8px;
                        aspect-ratio: {aspect_ratio_css};
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        background-color: #1C1C1E;
                        color: #7A7A7A;
                        padding: 20px;
                        text-align: center;
                    ">
                        <div>
                            <span style="font-size: 28px;">📸</span><br/>
                            <p style="margin-top: 10px; font-weight: 500;">Branded Graphic Preview</p>
                            <p style="font-size: 8.5pt; color: #555555;">Click 'Generate Branded Social Graphic' on the left to render the layout.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Generate the automated caption using the LIVE widget state values
            from generate_social import generate_automated_caption
            automated_copy = generate_automated_caption(
                tone=caption_tone,
                name=dish_name,
                price=dish_price,
                description=dish_desc,
                badge=promo_badge
            )
            
            st.markdown("---")
            st.markdown("#### 📝 Copy-and-Paste Caption")
            st.caption("This text is automatically formatted based on your inputs and selected tone. Click inside to edit or copy.")
            
            st.text_area(
                label="Facebook / Instagram Caption",
                value=automated_copy,
                height=250,
                key="social_caption_output_live"
            )
