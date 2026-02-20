import streamlit as st
from supabase import create_client, Client

# --- Supabase connection ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase: Client = create_client(url, key)

st.title("🛒 Inköpslista")

# --- Load categories ---
def load_categories():
    data = supabase.table("categories").select("*").execute()
    return sorted(data.data, key=lambda x: x["name"])

categories = load_categories()

# Find the "Handla" category
handla_cat = next((c for c in categories if c["name"].lower() == "handla"), None)

# --- Load items ---
def load_items():
    data = supabase.table("items").select("*").execute()
    return data.data

items = load_items()

# --- HANDLA (always shown first) ---
st.subheader("🛍️ Handla")

if handla_cat:
    handla_items = [i for i in items if i["category_id"] == handla_cat["id"]]
    for item in handla_items:
        col1, col2 = st.columns([4, 1])
        col1.write(item["name"])
        if col2.button("❌", key=item["id"]):
            supabase.table("items").delete().eq("id", item["id"]).execute()
            st.rerun()

st.markdown("---")

# --- OTHER CATEGORIES ---
st.subheader("📦 Kategorier")

for cat in categories:
    if cat["name"].lower() == "handla":
        continue  # skip handla here

    st.write(f"**{cat['name']}**")

    # Small clickable square to move item to Handla
    if st.button("⬜ Flytta till Handla", key=f"move_{cat['id']}"):
        # Move ALL items in this category to Handla
        supabase.table("items").update({"category_id": handla_cat["id"]}).eq("category_id", cat["id"]).execute()
        st.rerun()

    # Show items in this category
    cat_items = [i for i in items if i["category_id"] == cat["id"]]
    for item in cat_items:
        st.write(f"- {item['name']}")

    st.markdown("---")

# --- ADD NEW ITEM ---
st.subheader("➕ Lägg till vara")

item_name = st.text_input("Vara")

category_names = [c["name"] for c in categories if c["name"].lower() != "handla"]
category_choice = st.selectbox("Kategori", category_names)

if st.button("Lägg till"):
    if item_name.strip():
        category_id = next(c["id"] for c in categories if c["name"] == category_choice)
        supabase.table("items").insert({"name": item_name, "category_id": category_id}).execute()
        st.success(f"'{item_name}' lades till i {category_choice}")
        st.rerun()
