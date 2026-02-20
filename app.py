import streamlit as st
import json

st.set_page_config(page_title="Inköpslista", layout="centered")

# -----------------------------------
# JavaScript för att läsa/skriva localStorage
# -----------------------------------
def js_localstorage_get(key):
    get_js = f"""
    <script>
        const value = window.localStorage.getItem("{key}");
        window.parent.postMessage({{"type": "FROM_JS", "value": value}}, "*");
    </script>
    """
    st.components.v1.html(get_js, height=0)

def js_localstorage_set(key, value):
    set_js = f"""
    <script>
        window.localStorage.setItem("{key}", JSON.stringify({json.dumps(value)}));
    </script>
    """
    st.components.v1.html(set_js, height=0)

# -----------------------------------
# Initiera standarddata
# -----------------------------------
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

# -----------------------------------
# Ladda sparad data från localStorage
# -----------------------------------
js_localstorage_get("inkopslista_v1")

event = st.experimental_get_query_params().get("event")

# -----------------------------------
# Funktion för att spara
# -----------------------------------
def save_state():
    js_localstorage_set("inkopslista_v1", {
        "kategorier": st.session_state.kategorier,
        "att_handla": st.session_state.att_handla,
        "ursprung": st.session_state.ursprung
    })

# -----------------------------------
# Funktioner för listlogik
# -----------------------------------
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

# -----------------------------------
# UI
# -----------------------------------
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
