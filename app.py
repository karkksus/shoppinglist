import streamlit as st
import uuid

st.set_page_config(page_title="Inköpslista", layout="centered")

# -----------------------------
# Initiera data
# -----------------------------
if "kategorier" not in st.session_state:
    st.session_state.kategorier = {
        "Kylvaror": [
            {"id": str(uuid.uuid4()), "name": "Mjölk"},
            {"id": str(uuid.uuid4()), "name": "Fil"},
            {"id": str(uuid.uuid4()), "name": "Grädde"},
        ],
        "Frukt & Grönt": [
            {"id": str(uuid.uuid4()), "name": "Äpplen"},
            {"id": str(uuid.uuid4()), "name": "Bananer"},
            {"id": str(uuid.uuid4()), "name": "Tomater"},
        ],
        "Skafferi": [
            {"id": str(uuid.uuid4()), "name": "Pasta"},
            {"id": str(uuid.uuid4()), "name": "Ris"},
            {"id": str(uuid.uuid4()), "name": "Kaffe"},
        ],
    }

if "att_handla" not in st.session_state:
    st.session_state.att_handla = []

if "ursprung" not in st.session_state:
    st.session_state.ursprung = {}


# -----------------------------
# Funktioner
# -----------------------------
def flytta_till_handla(item, kategori):
    st.session_state.kategorier[kategori] = [
        v for v in st.session_state.kategorier[kategori] if v["id"] != item["id"]
    ]
    st.session_state.att_handla.append(item)
    st.session_state.ursprung[item["id"]] = kategori


def flytta_tillbaka(item):
    kategori = st.session_state.ursprung.get(item["id"])
    st.session_state.att_handla = [
        v for v in st.session_state.att_handla if v["id"] != item["id"]
    ]
    st.session_state.kategorier[kategori].append(item)


# -----------------------------
# UI
# -----------------------------
st.title("🛒 Inköpslista")

# -----------------------------
# Att handla först
# -----------------------------
st.header("Att handla")

for item in st.session_state.att_handla:
    if st.checkbox(f"Handlat: {item['name']}", key=f"done-{item['id']}"):
        flytta_tillbaka(item)

# -----------------------------
# Kategorier
# -----------------------------
st.header("Kategorier")

for kategori, varor in st.session_state.kategorier.items():
    with st.expander(kategori, expanded=True):
        for item in varor:
            if st.checkbox(item["name"], key=item["id"]):
                flytta_till_handla(item, kategori)
