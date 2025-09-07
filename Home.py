import time
import requests
import random
import streamlit as st
import numpy as np
from PIL import Image, ImageOps

import utils
import plotly.figure_factory as ff

st.set_page_config(
    page_title="Free Streamlit Theme Generator - Create Beautiful Custom Themes Instantly",
    page_icon="images/theme.png",   # relative path
    layout="wide"
)
st.title("Streamlit Theme Generator: Build Stunning App Themes in One Click")
st.write("Design and preview custom Streamlit themes with ease. Use our free theme generator to create professional color palettes, apply light or dark modes, and download ready-to-use config.toml files for your apps. Perfect for developers, data scientists, and Streamlit enthusiasts.")
st.divider()
utils.local_css("local_styles.css")

# Init state. This is only run whenever a new session starts (i.e. each time a new
# browser tab is opened).
if not st.session_state:
    st.session_state.primaryColor = "#f63366"
    st.session_state.backgroundColor = "#FFFFFF"
    st.session_state.secondaryBackgroundColor = "#f0f2f6"
    st.session_state.textColor = "#262730"
    st.session_state.is_dark_theme = False
    st.session_state.first_time = True

# Show header.
header_img = st.empty()
header_img.image(
    "images/woman-artist-light-skin-tone.png",  # relative path
    width=100,
) 

col1, col2 = st.columns([0.35, 0.65])
with col1:
    new_theme_clicked = st.button("🔄 Generate new theme")
with col2:
    theme_type = st.radio("theme type", ["Light theme", "Dark theme"])
# Shortcut
state = st.session_state

spinner = st.empty()
if not state.first_time:
    "---"
    "Done! Scroll down to see your new theme"

dark_checked = st.checkbox("Use dark themes")  # "Black is beautiful" or "Make it dark"

"---"

quote = st.container()

# Show current theme colors.
locked = []
columns = st.columns(4)
labels = ["backgroundColor", "secondaryBackgroundColor", "primaryColor", "textColor"]
for column, label in zip(columns, labels):
    c = column.color_picker(
        label.rstrip("Color").replace("B", " b").capitalize(),
        state[label],
        key="color_picker" + label,
    )
    st.write(c)
    st.text_input("c", state[label], key="test" + label)
    img = Image.new("RGB", (100, 50), st.session_state[label])
    img = ImageOps.expand(img, border=1, fill="black")
    column.image(img, width=150)
    column.markdown(
        f"<small>{label.rstrip('Color').replace('B', ' b').capitalize()}</small>",
        unsafe_allow_html=True,
    )
    lock_value = column.radio("lock value", ["Locked", "Unlocked"], index=1, key="lock-" + label)
    locked.append(lock_value == "Locked")

def apply_theme_from_session_state():
    """Retrieve theme from session state and apply it to streamlit config."""
    if st.config.get_option("theme.primaryColor") != st.session_state.primaryColor:
        st.config.set_option("theme.primaryColor", st.session_state.primaryColor)
        st.config.set_option("theme.backgroundColor", st.session_state.backgroundColor)
        st.config.set_option(
            "theme.secondaryBackgroundColor", st.session_state.secondaryBackgroundColor
        )
        st.config.set_option("theme.textColor", st.session_state.textColor)
        st.rerun()

def generate_new_theme():
    """Retrieve new theme from colormind, store in state, and apply to app."""
    if any(locked):
        input_list = ["N", "N", "N", "N", "N"]
        if locked[0]:
            if st.session_state.is_dark_theme:
                input_list[4] = utils.hex2rgb(st.session_state.backgroundColor)
            else:
                input_list[0] = utils.hex2rgb(st.session_state.backgroundColor)
        if locked[1]:
            if st.session_state.is_dark_theme:
                input_list[3] = utils.hex2rgb(st.session_state.secondaryBackgroundColor)
            else:
                input_list[1] = utils.hex2rgb(st.session_state.secondaryBackgroundColor)
        if locked[2]:
            input_list[2] = utils.hex2rgb(st.session_state.primaryColor)
        if locked[3]:
            if st.session_state.is_dark_theme:
                input_list[0] = utils.hex2rgb(st.session_state.textColor)
            else:
                input_list[4] = utils.hex2rgb(st.session_state.textColor)
        res = requests.get(
            "http://colormind.io/api/", json={"input": input_list, "model": "ui"}
        )
    else:
        res = requests.get("http://colormind.io/api/", json={"model": "ui"})

    rgb_colors = res.json()["result"]
    hex_colors = [utils.rgb2hex(*rgb) for rgb in res.json()["result"]]

    if theme_type == "Light theme":
        st.session_state.primaryColor = hex_colors[2]
        st.session_state.backgroundColor = hex_colors[0]
        st.session_state.secondaryBackgroundColor = hex_colors[1]
        st.session_state.textColor = hex_colors[4]
        st.session_state.is_dark_theme = False
    else:
        st.session_state.primaryColor = hex_colors[2]
        st.session_state.backgroundColor = hex_colors[4]
        st.session_state.secondaryBackgroundColor = hex_colors[3]
        st.session_state.textColor = hex_colors[0]
        st.session_state.is_dark_theme = True

if new_theme_clicked:
    st.balloons()
    if st.session_state.first_time:
        st.session_state.first_time = False
    wait_texts = [
        "🎨 Mixing some magic colors...",
        "🌈 Catching rainbows...",
        "🖌️ Splashing colors around...",
        "🐿️ Making happy little accidents...",
        "🌲 Choosing the perfect palette...",
        "☀️ Lighting up your theme..."
    ]
    with st.spinner(random.choice(wait_texts)):
        time.sleep(2)
        st.success("Done! Your shiny new theme is ready! Scroll down to enjoy")
    generate_new_theme()

apply_theme_from_session_state()

st.write("---")

st.write("""
To use this theme in your app, just create a file *.streamlit/config.toml* in your app's 
root directory and add the following code:
""")

config = utils.CONFIG_TEMPLATE.format(
    st.session_state.primaryColor,
    st.session_state.backgroundColor,
    st.session_state.secondaryBackgroundColor,
    st.session_state.textColor,
)
st.code(config)

mode = st.radio("App mode", ["Normal", "Cute 🐿️"], key="mode")
if mode == "Cute 🐿️":
    header_img.image("images/bob.jpg", width=100)
    header_text.write(
        """
        # The Joy of Streamlitting 🐿️

        Welcome back, friend!  

        Today, let's sprinkle some fun colors into this little Streamlit app.  
        Hit the button, enjoy the magic, and remember:  
        *There are no mistakes – only happy little accidents!*

        Have fun, and happy streamlitting!
        """
    )
    st.write("And now scroll up ☝️")

    bob_quotes = [
        '🌈 *"If we all painted the same way, life would be so boring."*',
        '☀️ *"True joy comes from sharing your colors with others."*',
        '🌲 *"Friends are precious—just like trees need their forest."*',
        '🌚 *"A little darkness is needed to make the light shine."*',
        '👩‍🎨 *"An artist lives in all of us."*',
        '☁️ *"Let\'s make fluffy clouds that float and play."*',
        '🖌️ *"Every day is a great day to create."*',
        '🦄 *"Your way is the right way."*',
        '🕊️ *"Create calm, peaceful spaces for everyone."*',
        '👣 *"You never know what you can do until you try."*',
    ]
    block_methods = [st.error, st.warning, st.info, st.success]
    with quote:
        random.choice(block_methods)(random.choice(bob_quotes))
        st.write("---")

st.write("---")

def draw_all(key, plot=False):
    st.write(
        """
        ## Play with Widgets 🎈
        
        These widgets don’t actually do much—but look how colorful they are! 👀  

        ```python
        streamlit = "cool"
        theming = "fantastic"
        both = "💥"
        ```
        """
    )

    st.checkbox("Is this cool or what?", key=key + "check")
    st.radio(
        "How many balloons? 🎈",
        ["1 balloon 🎈", "2 balloons 🎈🎈", "3 balloons 🎈🎈🎈"],
        key=key + "radio",
    )
    st.button("🤡 Click me", key=key + "button")

    if plot:
        st.write("Oh look, a plot:")
        x1 = np.random.randn(200) - 2
        x2 = np.random.randn(200)
        x3 = np.random.randn(200) + 2

        hist_data = [x1, x2, x3]
        group_labels = ["Group 1", "Group 2", "Group 3"]

        fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.1, 0.25, 0.5])
        st.plotly_chart(fig, use_container_width=True)

    st.file_uploader("You can now upload with style", key=key + "file_uploader")
    st.slider(
        "From 10 to 11, how awesome are themes?",
        min_value=10,
        max_value=11,
        key=key + "slider",
    )
    st.select_slider("Pick a number", [1, 2, 3], key=key)
    st.number_input("So many numbers", key=key + "number")
    st.text_area("A little writing space for you :)", key=key + "text")
    st.selectbox(
        "My favorite thing in the world is…",
        ["Streamlit", "Theming", "Balloons 🎈"],
        key=key + "select",
    )
    st.multiselect("Pick a number", [1, 2, 3], key=key + "multiselect")
    st.color_picker("Colors, colors, colors", key=key + "colorpicker")
    with st.expander("Expand me!"):
        st.write("Hey! Nothing much here, just a surprise 👀")
    st.write("---")
    st.write("That's our colorful journey for today!")
    st.progress(0.99)
    if plot:
        st.write("And here's some data and plots")
        st.json({"data": [1, 2, 3, 4]})
        st.dataframe({"data": [1, 2, 3, 4]})
        st.table({"data": [1, 2, 3, 4]})
        st.line_chart({"data": [1, 2, 3, 4]})
    st.write("The End!")

draw_all("main", plot=True)

with st.sidebar:
    draw_all("sidebar")
