import streamlit as st
import uuid

st.session_state.clear()


st.set_page_config(page_title="Inköpslista", layout="centered")

# -----------------------------
# Initiera data
# -----------------------------
if "kategorier" not in st.session_state:
    st.session_state.kategorier = {
        "Mejeri": [
            {"id": str(uuid.uuid4()), "name": "Mjölk"},
            {"id": str(uuid.uuid4()), "name": "Fil"},
            {"id": str(uuid.uuid4()), "name": "Matlagningsgrädde"},
            {"id": str(uuid.uuid4()), "name": "Smör"},
            {"id": str(uuid.uuid4()), "name": "Kefir"},
        ],
        "Frukt & Grönt": [
            {"id": str(uuid.uuid4()), "name": "Äpplen"},
            {"id": str(uuid.uuid4()), "name": "Bananer"},
            {"id": str(uuid.uuid4()), "name": "Tomater"},
            {"id": str(uuid.uuid4()), "name": "Gurka"},
            {"id": str(uuid.uuid4()), "name": "Lök"},
        ],
        "Skafferi": [
            {"id": str(uuid.uuid4()), "name": "Pasta"},
            {"id": str(uuid.uuid4()), "name": "Ris"},
            {"id": str(uuid.uuid4()), "name": "Kaffe"},
            {"id": str(uuid.uuid4()), "name": "Socker"},
            {"id": str(uuid.uuid4()), "name": "Mjöl"},
        ],
        "Kött": [
            {"id": str(uuid.uuid4()), "name": "Kycklingfilé"},
            {"id": str(uuid.uuid4()), "name": "Nötfärs"},
            {"id": str(uuid.uuid4()), "name": "Skinka"},
            {"id": str(uuid.uuid4()), "name": "Fläskfilé"},
        ],
        "Hygien": [
            {"id": str(uuid.uuid4()), "name": "Schampo"},
            {"id": str(uuid.uuid4()), "name": "Balsam"},
            {"id": str(uuid.uuid4()), "name": "Duschtvål"},
            {"id": str(uuid.uuid4()), "name": "Deo"},
        ],
        "Förbrukningsvaror": [
            {"id": str(uuid.uuid4()), "name": "Toapapper"},
            {"id": str(uuid.uuid4()), "name": "Diskmedel"},
            {"id": str(uuid.uuid4()), "name": "Tvättmedel"},
            {"id": str(uuid.uuid4()), "name": "Soppåsar"},
        ],
        "Godis": [
            {"id": str(uuid.uuid4()), "name": "Geisha"},
            {"id": str(uuid.uuid4()), "name": "Toffifee"},
            {"id": str(uuid.uuid4()), "name": "Chips"},
            {"id": str(uuid.uuid4()), "name": "Ostbågar"},
        ],
        "Djur": [
            {"id": str(uuid.uuid4()), "name": "Blötmat"},
            {"id": str(uuid.uuid4()), "name": "Torrfoder"},
            {"id": str(uuid.uuid4()), "name": "Kattgodis"},
            {"id": str(uuid.uuid4()), "name": "Strö"},
            {"id": str(uuid.uuid4()), "name": "Hö"},
            {"id": str(uuid.uuid4()), "name": "Grönsak till marsvin"},
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
    if st.checkbox(f" {item['name']}", key=f"done-{item['id']}"):
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
