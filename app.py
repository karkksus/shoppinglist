import streamlit as st

st.set_page_config(page_title="Inköpslista", layout="centered")

# -----------------------------
# Data
# -----------------------------
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


def flytta_till_handla(vara, kategori):
    if vara not in st.session_state.att_handla:
        st.session_state.kategorier[kategori].remove(vara)
        st.session_state.att_handla.append(vara)
        st.session_state.ursprung[vara] = kategori


def flytta_tillbaka(vara):
    kategori = st.session_state.ursprung.get(vara)
    if kategori:
        st.session_state.att_handla.remove(vara)
        st.session_state.kategorier[kategori].append(vara)


st.title("🛒 Inköpslista")

# -----------------------------
# Att handla först
# -----------------------------
st.header("Att handla")

for vara in st.session_state.att_handla:
    if st.checkbox(f"Handlat: {vara}", key=f"handlat-{vara}"):
        flytta_tillbaka(vara)

# -----------------------------
# Kategorier
# -----------------------------
st.header("Kategorier")

for kategori, varor in st.session_state.kategorier.items():
    with st.expander(kategori, expanded=True):
        for vara in varor:
            if st.checkbox(vara, key=f"{kategori}-{vara}"):
                flytta_till_handla(vara, kategori)
