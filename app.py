import streamlit as st
import requests
import base64
from PIL import Image
import io
from datetime import datetime

st.set_page_config(page_title="AI Image Generator", layout="wide")

# Custom CSS
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px;
        color: white;
        text-align: center;
        margin: -40px -20px 30px -20px;
        border-radius: 0 0 20px 20px;
    }
    
    .main-header h1 {
        font-size: 3em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.1em;
        opacity: 0.95;
    }
    
    .upload-section {
        background: white;
        border: 3px dashed #667eea;
        border-radius: 15px;
        padding: 40px 20px;
        text-align: center;
        margin: 20px 0;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #764ba2;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.2);
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 15px 0;
        color: #155724;
        font-weight: 500;
    }
    
    .error-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 15px 0;
        color: #721c24;
        font-weight: 500;
    }
    
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left: 5px solid #0c5460;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 15px 0;
        color: #0c5460;
    }
    
    .image-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .button-group {
        display: flex;
        gap: 10px;
        margin-top: 20px;
    }
    
    .control-section {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .section-title {
        color: #667eea;
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
    }
    
    .download-btn {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none;
        margin: 10px 5px 10px 0;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .image-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .image-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .image-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .image-card img {
        width: 100%;
        height: 280px;
        object-fit: cover;
        display: block;
    }
    
    .image-card-footer {
        padding: 15px;
        text-align: center;
    }
    
    .comparison-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin: 20px 0;
    }
    
    @media (max-width: 768px) {
        .comparison-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎨 AI Image Generator</h1>
    <p>Upload an image + write a prompt to generate AI variations</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []

# Download button function
def get_download_link(img_url, filename="generated.png"):
    """Create download link for image"""
    try:
        img_data = requests.get(img_url).content
        b64 = base64.b64encode(img_data).decode()
        return f'<a href="data:file/png;base64,{b64}" download="{filename}" class="download-btn">⬇️ Download</a>'
    except:
        return ""

# API call function
def generate_from_image(prompt, size, api_key_override=None):
    """Generate images using the API"""
    url = "https://ai-text-to-image-generator-flux-free-api.p.rapidapi.com/aaaaaaaaaaaaaaaaaiimagegenerator/quick.php"
    
    payload = {
        "prompt": prompt,
        "style_id": 4,
        "size": size
    }
    
    headers = {
        "x-rapidapi-key": api_key_override or "233ac05831msh4aa6d3d9d37c03cp12fb72jsn620bfec6f4bc",
        "x-rapidapi-host": "ai-text-to-image-generator-flux-free-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Main UI
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown('<div class="control-section"><div class="section-title">📤 Upload Image</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png", "webp", "bmp"],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        
        st.markdown(f"""
        <div style='background: #f0f4ff; padding: 10px; border-radius: 8px; margin: 10px 0;'>
            <p style='margin: 5px 0;'><strong>📊 Image Info:</strong></p>
            <p style='margin: 3px 0; font-size: 0.9em;'>Size: {img.size[0]} × {img.size[1]} px</p>
            <p style='margin: 3px 0; font-size: 0.9em;'>Format: {img.format}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="border: 1px solid #ddd; border-radius: 10px; overflow: hidden; margin: 15px 0;">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="upload-section">
            <p style="font-size: 3em; margin-bottom: 10px;">📁</p>
            <p style="font-size: 1.1em; color: #667eea; font-weight: bold;">Drag & drop or click to upload</p>
            <p style="color: #999; margin-top: 10px;">JPG, PNG, WebP, or BMP • Any size</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="control-section"><div class="section-title">✍️ Describe Changes</div>', unsafe_allow_html=True)
    
    prompt = st.text_area(
        "What do you want to change or create?",
        placeholder="e.g., 'Make it in cyberpunk style with neon lights' or 'Turn this into a watercolor painting' or 'Add a galaxy background'",
        height=150,
        label_visibility="collapsed"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="control-section"><div class="section-title">⚙️ Settings</div>', unsafe_allow_html=True)
    
    output_size = st.radio(
        "Output Size",
        ["1-1 (Square)", "16-9 (Landscape)", "9-16 (Portrait)"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    size_map = {
        "1-1 (Square)": "1-1",
        "16-9 (Landscape)": "16-9",
        "9-16 (Portrait)": "9-16"
    }
    
    num_images = st.slider(
        "Number of variations",
        min_value=1,
        max_value=4,
        value=1,
        label_visibility="collapsed"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Generate button
st.markdown("")
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    generate_btn = st.button(
        "✨ Generate Image",
        use_container_width=True,
        disabled=not (uploaded_file and prompt)
    )

if generate_btn:
    if not uploaded_file:
        st.markdown('<div class="error-box">❌ Please upload an image first</div>', unsafe_allow_html=True)
    elif not prompt:
        st.markdown('<div class="error-box">❌ Please describe what you want to change</div>', unsafe_allow_html=True)
    else:
        with st.spinner("🔄 Generating variations... This may take a moment"):
            try:
                # Create enhanced prompt combining image context with user request
                enhanced_prompt = f"Transform this image: {prompt}"
                
                size_key = size_map[output_size]
                data = generate_from_image(enhanced_prompt, size_key)
                
                if "result" in data and "data" in data["result"] and "results" in data["result"]["data"]:
                    results = data["result"]["data"]["results"]
                    
                    st.markdown('<div class="success-box">✅ Generation complete! Here are your variations:</div>', unsafe_allow_html=True)
                    
                    # Store in session
                    st.session_state.generated_images = results
                    
                    # Display images in grid
                    st.markdown('<div class="image-grid">', unsafe_allow_html=True)
                    
                    for idx, img_result in enumerate(results):
                        st.markdown(f"""
                        <div class="image-card">
                            <img src="{img_result['origin']}" alt="Generated image {idx+1}">
                            <div class="image-card-footer">
                                <p style="margin: 0; font-weight: bold; color: #667eea;">Variation {idx+1}</p>
                                {get_download_link(img_result['origin'], f'generated_{datetime.now().strftime("%Y%m%d_%H%M%S")}_{idx+1}.png')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download all button
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.info(f"💡 Generated {len(results)} variation(s). Click download buttons above to save individual images.")
                
                else:
                    st.markdown(f'<div class="error-box">❌ Error: {data.get("message", "Generation failed")}</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)

# Tips section
st.markdown("---")

with st.expander("💡 Tips for best results"):
    st.markdown("""
    ### Image Upload Tips:
    - **Clear subject**: Upload images with a clear, recognizable subject
    - **Good lighting**: Well-lit images work better than dark ones
    - **Supported formats**: JPG, PNG, WebP, BMP
    - **Any size**: Resolution doesn't matter - we'll adapt it
    
    ### Prompt Tips:
    - **Be specific**: "Add a sunset background with warm orange tones" works better than "make it better"
    - **Style descriptions**: "In oil painting style", "cyberpunk neon aesthetic", "watercolor"
    - **Detail level**: Include details about lighting, mood, colors, composition
    - **Action/change**: "Transform into", "Change the background to", "Add elements like"
    - **Examples**:
        - "Transform into a cyberpunk character with neon colors and futuristic outfit"
        - "Make it a watercolor painting with soft pastel colors"
        - "Change the background to a starry night sky with galaxy colors"
        - "Add a dramatic sunset in the background with golden lighting"
    
    ### Output Sizes:
    - **1-1 (Square)**: Perfect for social media thumbnails and profile pictures
    - **16-9 (Landscape)**: Great for banners and wallpapers
    - **9-16 (Portrait)**: Ideal for mobile wallpapers and stories
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #999;'>
    <p>🚀 Powered by advanced AI image generation</p>
    <p>Transform your images with AI • Unlimited variations • Instant generation</p>
</div>
""", unsafe_allow_html=True)