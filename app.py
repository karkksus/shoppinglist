import streamlit as st
import json

st.set_page_config(page_title="Inköpslista", layout="centered")

# -----------------------------------
# JavaScript för att läsa/skriva localStorage
# -----------------------------------
def js_localstorage_get(key):
    js = f"""
    <script>
        const value = window.localStorage.getItem("{key}");
        window.parent.postMessage({{"type": "LOAD_DATA", "value": value}}, "*");
    </script>
    """
    st.components.v1.html(js, height=0)

def js_localstorage_set(key, value):
    js = f"""
    <script>
        window.localStorage.setItem("{key}", JSON.stringify({json.dumps(value)}));
    </script>
    """
    st.components.v1.html(js, height=0)

# -----------------------------------
# Initiera standarddata
# -----------------------------------
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.kategorier = {
        "Kylvaror": ["Mjölk", "Fil", "Grädde"],
        "Frukt & Grönt": ["Äpplen", "Bananer", "Tomater"],
        "Skafferi": ["Pasta", "Ris", "Kaffe"]
    }
    st.session_state.att_handla = []
    st.session_state.ursprung = {}

# -----------------------------------
# Ladda sparad data från localStorage
# -----------------------------------
js_localstorage_get("inkopslista_v1")

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

# -----------------------------
# Att handla först
# -----------------------------
st.header("Att handla")

if st.session_state.att_handla:
    vara_att_ta_bort = st.selectbox(
        "Markera som handlad:",
        st.session_state.att_handla,
        key="select_handlat"
    )

    if st.button("✔ Markera som handlad"):
        flytta_tillbaka(vara_att_ta_bort)
else:
    st.write("Inget att handla just nu.")

# -----------------------------
# Kategorier
# -----------------------------
st.header("Kategorier")

for kategori, varor in st.session_state.kategorier.items():
    with st.expander(kategori, expanded=True):

        if varor:
            vara_att_lagga_till = st.selectbox(
                f"Välj vara från {kategori}:",
                varor,
                key=f"select-{kategori}"
            )

            if st.button(f"➕ Lägg till {vara_att_lagga_till}", key=f"btn-{kategori}"):
                flytta_till_handla(vara_att_lagga_till, kategori)
        else:
            st.write("Inga varor kvar i denna kategori.")





