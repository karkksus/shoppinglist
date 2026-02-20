import streamlit as st
from supabase import create_client, Client

# --- Supabase connection ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase: Client = create_client(url, key)

st.title("🛒 Inköpslista")

# --- Load categories from database ---
@st.cache_data
def load_categories():
    data = supabase.table("categories").select("*").execute()
    return sorted(data.data, key=lambda x: x["name"])

categories = load_categories()

# --- Load items ---
def load_items():
    data = supabase.table("items").select("id, name, category_id").execute()
    return data.data

items = load_items()

# --- Add new item ---
st.subheader("Lägg till vara")

item_name = st.text_input("Vara")
category_names = [c["name"] for c in categories]
category_choice = st.selectbox("Kategori", category_names)

if st.button("Lägg till"):
    if item_name.strip():
        category_id = next(c["id"] for c in categories if c["name"] == category_choice)
        supabase.table("items").insert({"name": item_name, "category_id": category_id}).execute()
        st.success(f"'{item_name}' lades till i {category_choice}")
        st.rerun()

# --- Show items grouped by category ---
st.subheader("Varor per kategori")

for cat in categories:
    cat_items = [i for i in items if i["category_id"] == cat["id"]]

    if cat_items:
        with st.expander(cat["name"]):
            for item in cat_items:
                col1, col2 = st.columns([4, 1])
                col1.write(item["name"])
                if col2.button("❌", key=item["id"]):
                    supabase.table("items").delete().eq("id", item["id"]).execute()
                    st.rerun()
