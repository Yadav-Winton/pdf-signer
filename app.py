import io
import fitz  # PyMuPDF
import streamlit as st
from PIL import Image
from rembg import remove, new_session
import base64

st.set_page_config(page_title="Ashish Yadav - Pro PDF Signer", page_icon="✍️", layout="wide")

# --- Full-Screen Startup Animation & Professional Styling ---
st.markdown("""
    <style>
    @keyframes fadeOut {
        0% { opacity: 1; visibility: visible; }
        80% { opacity: 1; visibility: visible; }
        100% { opacity: 0; visibility: hidden; }
    }
    @keyframes pulseGlow {
        0% { transform: scale(0.95); text-shadow: 0 0 10px rgba(59, 130, 246, 0.5); }
        50% { transform: scale(1.05); text-shadow: 0 0 25px rgba(59, 130, 246, 0.8); }
        100% { transform: scale(0.95); text-shadow: 0 0 10px rgba(59, 130, 246, 0.5); }
    }
    .startup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: #0f172a;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 99999;
        animation: fadeOut 1.5s ease-in-out forwards;
    }
    .startup-logo {
        color: #ffffff;
        font-size: 38px;
        font-weight: 800;
        letter-spacing: 1px;
        animation: pulseGlow 1.2s infinite ease-in-out;
        font-family: sans-serif;
    }
    .startup-sub {
        color: #38bdf8;
        font-size: 16px;
        margin-top: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-family: sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        border-left: 5px solid #3b82f6;
        border-right: 5px solid #3b82f6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }
    .brand-title {
        color: #ffffff;
        font-size: 26px;
        font-weight: 700;
        margin: 0;
    }
    .brand-subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>

    <div class="startup-overlay">
        <div class="startup-logo">Ashish Yadav Codes</div>
        <div class="startup-sub">Initializing Secure Environment...</div>
    </div>

    <div class="main-header">
        <h1 class="brand-title">Ashish Yadav &bull; Pro PDF Signer</h1>
        <p class="brand-subtitle">Secure AI-Powered Document Signing Platform</p>
    </div>
""", unsafe_allow_html=True)

@st.cache_resource
def get_ai_session():
    return new_session("u2netp")

session = get_ai_session()

# --- SIDEBAR: Signature Management ---
st.sidebar.header("1. Signature Configuration")

if "signature_img" not in st.session_state:
    sig_file = st.sidebar.file_uploader("Upload Signature Image (PNG/JPG)", type=["png", "jpg", "jpeg"], key="sig_up")
    if sig_file is not None:
        input_image = Image.open(sig_file)
        with st.spinner("Processing background with AI..."):
            output_image = remove(input_image, session=session)
            st.session_state["signature_img"] = output_image.convert("RGBA")
        st.rerun()
else:
    st.sidebar.success("Signature loaded successfully.")
    st.sidebar.image(st.session_state["signature_img"], caption="Active Digital Signature", width=150)
    
    if st.sidebar.button("Remove / Change Signature"):
        del st.session_state["signature_img"]
        st.rerun()

# --- MAIN SECTION: PDF Upload & Drag-Drop Component ---
st.markdown("### 2. Document Workspace & Positioning")
pdf_file = st.file_uploader("Upload Target PDF Document", type=["pdf"], key="pdf_up")

if pdf_file is not None and "signature_img" in st.session_state:
    pdf_bytes = pdf_file.read()
    
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page_num = st.number_input("Select Target Page", min_value=1, max_value=len(doc), value=1)
    page = doc[page_num - 1]
    
    pix = page.get_pixmap(dpi=150)
    page_img = Image.open(io.BytesIO(pix.tobytes("png")))
    
    def img_to_b64(img):
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
        
    page_b64 = img_to_b64(page_img)
    sig_b64 = img_to_b64(st.session_state["signature_img"])
    pdf_b64 = base64.b64encode(pdf_bytes).decode()
    
    st.info("Drag and drop (or touch and drag on mobile) the signature box to your desired position on the document preview below.")

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <script src="https://unpkg.com/pdf-lib@1.4.0/dist/pdf-lib.min.js"></script>
    <style>
      #container {{
        position: relative;
        display: inline-block;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        user-select: none;
        max-width: 100%;
        background: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        touch-action: none;
      }}
      #pdf-page {{
        display: block;
        width: 100%;
        max-width: 750px;
        height: auto;
      }}
      #signature-box {{
        position: absolute;
        top: 100px;
        left: 100px;
        width: 150px;
        cursor: grab;
        border: 2px dashed #2563eb;
        background: rgba(37, 99, 235, 0.05);
        padding: 2px;
        border-radius: 4px;
        touch-action: none;
      }}
      #signature-box:active {{
        cursor: grabbing;
      }}
      #signature-box img {{
        width: 100%;
        display: block;
        pointer-events: none;
      }}
      .download-btn {{
        margin-top: 20px;
        background-color: #2563eb;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 15px;
        font-weight: 600;
        transition: background-color 0.2s;
      }}
      .download-btn:hover {{
        background-color: #1d4ed8;
      }}
    </style>
    </head>
    <body>

    <div id="container">
        <img src="data:image/png;base64,{page_b64}" id="pdf-page">
        <div id="signature-box">
            <img src="data:image/png;base64,{sig_b64}">
        </div>
    </div>
    <br>
    <button class="download-btn" onclick="downloadSignedPDF()">Download Signed Document</button>

    <script>
    const box = document.getElementById('signature-box');
    let isDragging = false;
    let startX, startY;

    // Mouse Events
    box.addEventListener('mousedown', (e) => {{
        isDragging = true;
        startX = e.clientX - box.offsetLeft;
        startY = e.clientY - box.offsetTop;
        e.preventDefault();
    }});

    document.addEventListener('mousemove', (e) => {{
        if (!isDragging) return;
        let newX = e.clientX - startX;
        let newY = e.clientY - startY;
        
        if(newX < 0) newX = 0;
        if(newY < 0) newY = 0;
        
        box.style.left = newX + 'px';
        box.style.top = newY + 'px';
    }});

    document.addEventListener('mouseup', () => {{
        isDragging = false;
    }});

    // Touch Events for Mobile / Tablets
    box.addEventListener('touchstart', (e) => {{
        isDragging = true;
        const touch = e.touches[0];
        startX = touch.clientX - box.offsetLeft;
        startY = touch.clientY - box.offsetTop;
        e.preventDefault();
    }}, {{ passive: false }});

    document.addEventListener('touchmove', (e) => {{
        if (!isDragging) return;
        const touch = e.touches[0];
        let newX = touch.clientX - startX;
        let newY = touch.clientY - startY;
        
        if(newX < 0) newX = 0;
        if(newY < 0) newY = 0;
        
        box.style.left = newX + 'px';
        box.style.top = newY + 'px';
        e.preventDefault();
    }}, {{ passive: false }});

    document.addEventListener('touchend', () => {{
        isDragging = false;
    }});

    async function downloadSignedPDF() {{
        try {{
            const pdfBase64 = "{pdf_b64}";
            const sigBase64 = "{sig_b64}";
            
            const pdfBytes = Uint8Array.from(atob(pdfBase64), c => c.charCodeAt(0));
            const pdfDoc = await PDFLib.PDFDocument.load(pdfBytes);
            
            const pngImageBytes = Uint8Array.from(atob(sigBase64), c => c.charCodeAt(0));
            const pngImage = await pdfDoc.embedPng(pngImageBytes);
            
            const pages = pdfDoc.getPages();
            const page = pages[{page_num - 1}];
            const {{ width, height }} = page.getSize();
            
            const imgElement = document.getElementById('pdf-page');
            const displayedWidth = imgElement.clientWidth;
            const displayedHeight = imgElement.clientHeight;
            
            const scaleX = width / displayedWidth;
            const scaleY = height / displayedHeight;
            
            const boxLeft = box.offsetLeft;
            const boxTop = box.offsetTop;
            const boxWidth = box.clientWidth;
            const boxHeight = box.clientHeight;
            
            const pdfX = boxLeft * scaleX;
            const pdfY = height - ((boxTop + boxHeight) * scaleY);
            const pdfWidth = boxWidth * scaleX;
            const pdfHeight = boxHeight * scaleY;
            
            page.drawImage(pngImage, {{
                x: pdfX,
                y: pdfY,
                width: pdfWidth,
                height: pdfHeight,
            }});
            
            const modifiedPdfBytes = await pdfDoc.save();
            
            const blob = new Blob([modifiedPdfBytes], {{ type: 'application/pdf' }});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = "Signed_{pdf_file.name}";
            link.click();
        }} catch (err) {{
            alert("Error: " + err.message);
        }}
    }}
    </script>
    </body>
    </html>
    """
    
    st.components.v1.html(html_code, height=750, scrolling=True)

elif pdf_file is not None and "signature_img" not in st.session_state:
    st.warning("Please upload and configure your signature in the sidebar first.")
