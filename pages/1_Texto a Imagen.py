import requests
import streamlit as st

account_id = st.secrets["CLOUDFLARE_ACCOUNT_ID"]
api_token = st.secrets["CLOUDFLARE_API_TOKEN"]

st.set_page_config(
    page_title="Texto a Imagen",
    page_icon="pages/lib/icon.png"
)

" ## Texto a Imagen"
"""
---
"""

with st.form("text_to_image"):
    # All models at https://developers.cloudflare.com/workers-ai/models/
    model = st.selectbox(
        "Elige un modelo",
        options=(
            "@cf/lykon/dreamshaper-8-lcm",
            "@cf/black-forest-labs/flux-1-schnell",
            "@cf/bytedance/stable-diffusion-xl-lightning",
            "@cf/stabilityai/stable-diffusion-xl-base-1.0",
        ),
    )
    prompt = st.text_area("Prompt")
    submitted = st.form_submit_button("Generar")
    if submitted:
        headers = {
            "Authorization": f"Bearer {api_token}",
        }
        with st.spinner("Generating..."):
            url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
            response = requests.post(
                url,
                headers=headers,
                json={"prompt": prompt},
            )
            st.image(response.content, caption=prompt)        