import streamlit as st
import pandas as pd
from weather_api import get_current_weather, get_city_coordinates

def determine_condition(temp, desc):
    d = desc.lower()
    if "rain" in d:           return "🌧️"
    if "snow" in d or temp<10: return "❄️"
    if temp>=25:              return "☀️"
    return "☁️"

st.set_page_config(page_title="Virtual Closet", page_icon="👗", layout="wide")

st.title("👗 Virtual Closet App")

# --- Inject updated CSS ---
st.markdown("""
<style>
.image-card {
    background-color: #FFFFFF;
    padding: 12px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
    margin-bottom: 16px;
}
.image-card img {
    border-radius: 6px;
    margin-bottom: 8px;
}
.image-card .caption {
    font-weight: 600;
    color: #333333;
}
</style>
""", unsafe_allow_html=True)

# --- Load DataFrame (never reassign df to a display call!) ---
df = pd.read_csv("closet_items.csv")

# Helper: display a DataFrame of items in a responsive grid
def display_grid(df_items, img_width=180):
    records = df_items.to_dict("records")
    for i in range(0, len(records), 3):
        row = records[i:i+3]
        cols = st.columns(len(row), gap="small")
        for col, item in zip(cols, row):
            # HTML card
            col.markdown(f"""
              <div class="image-card">
                <img src="{item['image_url']}" width="{img_width}">
                <div class="caption">{item['item_name']}</div>
              </div>
            """, unsafe_allow_html=True)

# Prepare selector lists
tops    = df[df.type=="Top"].item_name.tolist()
bottoms = df[df.type=="Bottom"].item_name.tolist()
dresses = df[df.type=="Dress"].item_name.tolist()
shoes   = df[df.type=="Shoes"].item_name.tolist()

# === Tabs ===
tab1, tab2, tab3 = st.tabs(["🗄️ My Closet", "🌦 Weather View", "🛍️ Build Outfit"])

# --- Tab 1: My Closet + Filters ---
with tab1:
    st.header("Browse & Filter Your Closet")
    f_type    = st.multiselect("Type",    options=df["type"].unique())
    f_style   = st.multiselect("Style",   options=df["style"].unique())
    f_weather = st.multiselect("Weather", options=df["weather"].unique())

    df1 = df.copy()
    if f_type:    df1 = df1[df1.type.isin(f_type)]
    if f_style:   df1 = df1[df1.style.isin(f_style)]
    if f_weather: df1 = df1[df1.weather.apply(lambda w: any(x in w for x in f_weather))]

    if df1.empty:
        st.write("No items match those filters.")
    else:
        display_grid(df1)

# --- Tab 2: Weather‑Adapted View ---
with tab2:
    st.header("Weather‑Adapted Suggestions")
    city = st.text_input("Enter City", "St. Gallen")
    if st.button("Show Weather‑Adapted Items"):
        lat, lon = get_city_coordinates(city)
        if lat is None:
            st.error("City not found")
        else:
            w = get_current_weather(lat, lon)
            if not w:
                st.error("Weather API error")
            else:
                temp = w["current"]["temp"]
                desc = w["current"]["weather"][0]["description"]
                cond = determine_condition(temp, desc)
                st.write(f"**{city}**: {temp}°C, {desc} → **{cond}**")

                df2 = df[df.weather.apply(lambda w: cond in w)]
                if df2.empty:
                    st.write("No items match this condition.")
                else:
                    display_grid(df2)

# --- Tab 3: Build Outfit (selectors left, vertical cards right) ---
with tab3:
    st.header("🛍️ Build Your Outfit")
    st.write("Pick a dress+shoes or top+bottom+shoes, then click **Show Outfit**.")

    # Create two columns: selectors on the left, display on the right
    col_sel, col_show = st.columns([1, 1], gap="medium")

    # Left column: selectors + button
    with col_sel:
        dress_choice  = st.selectbox("Dress (if using)",    [""] + dresses)
        top_choice    = st.selectbox("Top (if using)",      [""] + tops)
        bottom_choice = st.selectbox("Bottom (if using)",   [""] + bottoms)
        shoe_choice   = st.selectbox("Shoes (required)",     [""] + shoes)
        show = st.button("Show Outfit")

    # Right column: immediately render the outfit as a vertical stack
    with col_show:
        if show:
            # Determine which mode
            if dress_choice and shoe_choice and not (top_choice or bottom_choice):
                items = [dress_choice, shoe_choice]
            elif top_choice and bottom_choice and shoe_choice and not dress_choice:
                items = [top_choice, bottom_choice, shoe_choice]
            else:
                st.warning("Select either Dress+Shoes OR Top+Bottom+Shoes.")
                items = []

            # Render each selected piece as a small card (vertical)
            for name in items:
                item = df[df.item_name == name].iloc[0]
                st.markdown(f'''
                    <div class="image-card" style="max-width:150px; margin:0 auto 5px;">
                      <img src="{item.image_url}" width="150">
                      <div class="caption">{item.item_name}</div>
                    </div>
                ''', unsafe_allow_html=True)
        else:
            # placeholder so col_show always has top alignment
            col_show.empty()

# --- Sidebar: Add New Clothing Item Only ---
st.sidebar.header("➕ Add New Clothing Item")
with st.sidebar.form("add_item"):
    nm    = st.text_input("Item Name")
    tp    = st.selectbox("Type",    ["Top","Bottom","Dress","Shoes"])
    stl   = st.selectbox("Style",   ["Casual","Fancy"])
    wthr  = st.multiselect("Weather", ["❄️","☀️","☁️","🌧️"])
    img   = st.text_input("Image URL")
    if st.form_submit_button("Add Item"):
        if nm and tp and stl and wthr and img:
            pd.DataFrame([{
                "item_name": nm,
                "type":      tp,
                "style":     stl,
                "weather":   ",".join(wthr),
                "image_url": img
            }]).to_csv("closet_items.csv", mode="a", index=False, header=False)
            st.sidebar.success("Item added! Refresh to see it.")
        else:
            st.sidebar.error("Please fill in all fields.")
