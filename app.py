import streamlit as st
from supabase import create_client, Client

# --- Supabase connection ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase: Client = create_client(url, key)
items = load_items()

# ============================================================
# 1. INKÖPSLISTA (överst)
# ============================================================

st.subheader("🛍️ Inköpslista")

shopping_items = [i for i in items if i.get("in_shopping_list")]

# CSS för att hålla knapp + text på samma rad även på mobil
st.markdown("""
<style>
.item-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 0;
}
.item-name {
    font-weight: bold;
    font-size: 1.1em;
}
.return-btn {
    background: none;
    border: none;
    font-size: 1.3em;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

if not shopping_items:
    st.write("Inget i inköpslistan just nu.")
else:
    for item in shopping_items:
        st.markdown(
            f"""
            <div class="item-row">
                <form action="" method="post">
                    <button name="back_{item['id']}" class="return-btn" type="submit">↩️</button>
                </form>
                <span class="item-name">{item['name']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Hantera klick
        if f"back_{item['id']}" in st.session_state:
            supabase.table("items").update({"in_shopping_list": False}).eq("id", item["id"]).execute()
            st.rerun()

st.markdown("---")


# ============================================================
# 2. KATEGORIER (under inköpslistan)
# ============================================================


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

