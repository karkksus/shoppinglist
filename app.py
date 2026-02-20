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

# --- Load items ---
def load_items():
    data = supabase.table("items").select("*").execute()
    return data.data

items = load_items()

# ============================================================
# 1. INKÖPSLISTA (överst)
# ============================================================

shopping_items = [i for i in items if i.get("in_shopping_list")]

if not shopping_items:
    st.write("Inget i inköpslistan just nu.")
else:
    for item in shopping_items:
        col1, col2 = st.columns([4, 1])
        col1.write(f"**{item['name']}**")
        if col2.button("↩️", key=f"back_{item['id']}"):
            supabase.table("items").update({"in_shopping_list": False}).eq("id", item["id"]).execute()
            st.rerun()

st.markdown("---")

# ============================================================
# 2. KATEGORIER (under inköpslistan)
# ============================================================

st.subheader("📦 Kategorier")

for cat in categories:
    st.write(f"### {cat['name']}")

    cat_items = [i for i in items if i["category_id"] == cat["id"] and not i.get("in_shopping_list")]

    if not cat_items:
        st.write("_Tom kategori_")
    else:
        for item in cat_items:
            # Klickbar rad: kategori först, sedan vara
            if st.button(item["name"], key=f"move_{item['id']}"):
                supabase.table("items").update({"in_shopping_list": True}).eq("id", item["id"]).execute()
                st.rerun()

    st.markdown("---")

# ============================================================
# 3. LÄGG TILL VARA (längst ner)
# ============================================================
st.subheader("➕ Lägg till vara")

category_names = [c["name"] for c in categories]
category_choice = st.selectbox("Kategori", category_names)

item_name = st.text_input("Vara")

if st.button("Lägg till"):
    if item_name.strip():
        category_id = next(c["id"] for c in categories if c["name"] == category_choice)
        supabase.table("items").insert({
            "name": item_name,
            "category_id": category_id,
            "in_shopping_list": False
        }).execute()
        st.success(f"'{item_name}' lades till i {category_choice}")
        st.rerun()

