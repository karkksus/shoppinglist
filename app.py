from streamlit_browser_storage import BrowserStorage

storage = BrowserStorage(key="inkopslista_v1")

import streamlit as st
from streamlit_browser_storage import BrowserStorage

st.set_page_config(page_title="Inköpslista", layout="centered")

storage = BrowserStorage(key="inkopslista_v1")

# -----------------------------
# Ladda sparad data
# -----------------------------
saved = storage.get()

if saved:
    st.session_state.kategorier = saved.get("kategorier", {})
    st.session_state.att_handla = saved.get("att_handla", [])
    st.session_state.ursprung = saved.get("ursprung", {})
else:
    if "kategorier" not in st.session_state:
        st.session_state.kategorier = {
            "Kylvaror": ["Mjölk", "Fil", "Grädde"],
            "Frukt & Grönt": ["Äpplen", "Bananer", "Tomater"],
            "Skafferi": ["Pasta", "Ris", "Kaffe"]
        }

    if "att_handla" not in st.session_state:
        st.session_state.att_handla = []

    if "ursprung" not in st.session_state:
        st.session_state.ursprung = {}

# -----------------------------
# Funktioner
# -----------------------------
def save_state():
    storage.set({
        "kategorier": st.session_state.kategorier,
        "att_handla": st.session_state.att_handla,
        "ursprung": st.session_state.ursprung
    })

def flytta_till_handla(vara, kategori):
    if vara not in st.session_state.att_handla:
        st.session_state.kategorier[kategori].remove(vara)
        st.session_state.att_handla.append(vara)
        st.session_state.ursprung[vara] = kategori
        save_state()

def flytta_tillbaka(vara):
    kategori = st.session_state.ursprung.get(vara)
    if kategori:
        st.session_state.att_handla.remove(vara)
        st.session_state.kategorier[kategori].append(vara)
        save_state()

# -----------------------------
# UI
# -----------------------------
st.title("🛒 Inköpslista")

# Att handla först
st.header("Att handla")

for vara in st.session_state.att_handla:
    if st.checkbox(f"Handlat: {vara}", key=f"handlat-{vara}"):
        flytta_tillbaka(vara)

# Kategorier
st.header("Kategorier")

for kategori, varor in st.session_state.kategorier.items():
    with st.expander(kategori, expanded=True):
        for vara in varor:
            if st.checkbox(vara, key=f"{kategori}-{vara}"):
                flytta_till_handla(vara, kategori)
