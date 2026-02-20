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

# ============================================================
# 1. INKÖPSLISTA (överst)
# ============================================================

st.subheader("🛍️ Inköpslista")

shopping_items = [i for i in items if i.get("in_shopping_list")]

if not shopping_items:
    st.write("Inget i inköpslistan just nu.")
else:
    for item in shopping_items:
        # En knapp per rad: symbol + varans namn
        if st.button(f"↩️ {item['name']}", key=f"back_{item['id']}"):
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
            # Klickbar vara (utan kategori framför)
            if st.button(item["name"], key=f"move_{item['id']}"):
                supabase.table("items").update({"in_shopping_list": True}).eq("id", item["id"]).execute()
                st.rerun()

    st.markdown("---")

# ============================================================
# 3. LÄGG TILL VARA (längst ner)
# ============================================================

st.subheader("➕ Lägg till vara")

# Initiera flagga
if "clear_new_item" not in st.session_state:
    st.session_state.clear_new_item = False

# Om vi ska tömma fältet efter rerun
if st.session_state.clear_new_item:
    st.session_state.new_item_name = ""
    st.session_state.clear_new_item = False

# Kategori först
category_names = [c["name"] for c in categories]
category_choice = st.selectbox("Kategori", category_names)

# Textfältet
item_name = st.text_input("Vara", key="new_item_name")

if st.button("Lägg till"):
    if item_name.strip():
        category_id = next(c["id"] for c in categories if c["name"] == category_choice)

        supabase.table("items").insert({
            "name": item_name,
            "category_id": category_id,
            "in_shopping_list": False
        }).execute()

        # ⭐ Sätt flagga att tömma fältet efter rerun
        st.session_state.clear_new_item = True

        st.experimental_rerun()


        # ⭐ Viktigt: gör en ren omstart av appen
        st.experimental_rerun()



