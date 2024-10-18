from base64 import b64encode
import io

from PIL import Image, ImageOps
import requests
import streamlit as st
from streamlit_drawable_canvas import st_canvas

api_token = st.secrets["CLOUDFLARE_API_TOKEN"]
account_id = st.secrets["CLOUDFLARE_ACCOUNT_ID"]

st.set_page_config(
    page_title="Editar Imagen",
    page_icon="pages/lib/icon.png"
)

" ## Editar imagen"
"""
---
"""

image_upload = st.file_uploader("Sube una imagen")

if not image_upload:
    st.stop()

img = Image.open(image_upload)
img = ImageOps.contain(img, (600, 600))
masking_result = st_canvas(width=img.width, height=img.height, background_image=img)

def image_to_int_array(image, format="PNG"):
    """Current Workers AI REST API consumes an array of unsigned 8 bit integers"""
    bytes = io.BytesIO()
    image.save(bytes, format=format)
    return list(bytes.getvalue())

if masking_result.image_data is not None:
    # st.image(masking_result.image_data, caption="Your masking")
    with st.form("Prompt"):
        prompt = st.text_input(label="Que te gustaría reemplazar de esta imagen?")
        submitted = st.form_submit_button("Generar")
        if submitted:
            model = "@cf/runwayml/stable-diffusion-v1-5-inpainting"
            image_array = image_to_int_array(img)
            # Reverse the order / Boolean array to mark the bits
            mask = masking_result.image_data[:, :, -1] > 0
            mask_image = Image.fromarray(mask)
            mask_array = image_to_int_array(mask_image)
            with st.spinner("Generando..."):
                url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
                response = requests.post(
                    url,
                    headers={
                        "Authorization": f"Bearer {api_token}",
                    },
                    json={"prompt": prompt, "image": image_array, "mask": mask_array},
                )
                if response.ok:
                    st.image(response.content, caption=prompt)
                else:
                    st.warning(f"Error {response.status_code}")
                    st.warning(response.reason)
                    st.warning(response.text)
                    f"Image Array is {len(image_array)} entries, first 10:"
                    st.code(image_array[:10])
                    f"Mask Array is {len(mask_array)} entries, first 10:"
                    st.code(mask_array[:10])