from base64 import b64encode
import io

from PIL import Image, ImageOps
import requests
import streamlit as st
import numpy as np

api_token = st.secrets["CLOUDFLARE_API_TOKEN"]
account_id = st.secrets["CLOUDFLARE_ACCOUNT_ID"]

st.set_page_config(
    page_title="Imagen a Imagen",
    page_icon="pages/lib/icon.png"
)

" ## Imagen a imagen"
st.markdown("*Ajustando parametros del modelo para mejores resultados")
"""
---
"""

# Cargar la imagen
input_image = st.file_uploader("Sube una imagen")
if not input_image:
    st.stop()

img = Image.open(input_image)
img = ImageOps.contain(img, (600, 600))

# Crear una máscara blanca que cubra toda la imagen
masking_result = np.ones((img.height, img.width), dtype=np.uint8) * 255  # Máscara blanca

def image_to_int_array(image, format="PNG"):
    """Convertir la imagen a un array de enteros."""
    bytes = io.BytesIO()
    image.save(bytes, format=format)
    return list(bytes.getvalue())

with st.form("Prompt"):
    prompt = st.text_input(label="Describe las modificaciones que quieres")
    submitted = st.form_submit_button("Generar")
    if submitted:
        model = "@cf/runwayml/stable-diffusion-v1-5-img2img"
        image_array = image_to_int_array(img)

        # Crear la máscara a partir del masking_result
        mask_array = image_to_int_array(Image.fromarray(masking_result))

        with st.spinner("Generando..."):
            url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {api_token}",
                },
                json={"prompt": prompt, "image": image_array, "mask": mask_array, "strength": 0.65, "guidance": 15},
            )
            if response.ok:
                st.image(response.content, caption=prompt)
            else:
                st.warning(f"Error {response.status_code}")
                st.warning(response.reason)
                st.warning(response.text)
                st.code(image_array[:10])
                st.code(mask_array[:10])
