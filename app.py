import streamlit as st
import requests
import base64

st.set_page_config(page_title="Text-to-Image Generator", layout="wide")
st.title("🎨 Text-to-Image Generator")

# --- User Inputs ---
prompt = st.text_area("Enter your prompt", "Iron Man and Spider-Man in futuristic armor")
size = st.radio("Choose Image Size", ["1-1", "9-16", "16-9"])

# --- Function to make download button ---
def download_button(img_url, filename="generated.png"):
    img_data = requests.get(img_url).content
    b64 = base64.b64encode(img_data).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="{filename}">⬇️ Download</a>'
    return href

# --- Generate Images ---
if st.button("Generate Image"):
    with st.spinner("Generating image..."):
        url = "https://ai-text-to-image-generator-flux-free-api.p.rapidapi.com/aaaaaaaaaaaaaaaaaiimagegenerator/quick.php"

        payload = {
            "prompt": prompt,
            "style_id": 4,
            "size": size
        }
        headers = {
            "x-rapidapi-key": "233ac05831msh4aa6d3d9d37c03cp12fb72jsn620bfec6f4bc",
            "x-rapidapi-host": "ai-text-to-image-generator-flux-free-api.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        try:
            results = data["result"]["data"]["results"]
            for img in results:
                st.image(img["origin"], caption=f"Generated Image #{img['index']}", use_container_width=True)

                # Add download button under each image
                st.markdown(download_button(img["origin"], f"image_{img['index']}.png"), unsafe_allow_html=True)

            st.success("✅ Done! You got multiple images with download buttons.")
        except Exception as e:
            st.error(f"⚠️ No image URL found in response. Error: {e}")
