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

st.subheader("🛍️ Inköpslista")

shopping_items = [i for i in items if i.get("in_shopping_list")]

# CSS som tvingar knapp + text på samma rad även på mobil
st.markdown("""
<style>
.item-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: 12px;
    padding: 6px 0;
}
.item-text {
    font-weight: bold;
    font-size: 1.1em;
}
</style>
""", unsafe_allow_html=True)

if not shopping_items:
    st.write("Inget i inköpslistan just nu.")
else:
    for item in shopping_items:

        row = st.container()  # håller ihop raden

        with row:
            # Gör en rad med flexbox
            st.markdown("<div class='item-row'>", unsafe_allow_html=True)

            # Knapp (Streamlit kan inte ligga i HTML, så vi lägger den separat)
            btn_col, text_col = st.columns([1, 8])

            with btn_col:
                if st.button("↩️", key=f"back_{item['id']}"):
                    supabase.table("items").update({"in_shopping_list": False}).eq("id", item["id"]).execute()
                    st.rerun()

            with text_col:
                st.markdown(f"<span class='item-text'>{item['name']}</span>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

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

# Kategori först
category_names = [c["name"] for c in categories]
category_choice = st.selectbox("Kategori", category_names)

# Vara sen
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
