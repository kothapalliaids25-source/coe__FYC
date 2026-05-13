import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import numpy as np
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Document Scanner", layout="centered")

st.title("📄 Document Scanner")
st.write("Upload a document image, convert it to black & white, and download as PDF.")

uploaded_file = st.file_uploader(
    "Upload Document Image",
    type=["png", "jpg", "jpeg"]
)

def process_document(image):
    # Convert to grayscale
    gray = ImageOps.grayscale(image)

    # Increase contrast
    gray = ImageOps.autocontrast(gray)

    # Sharpen image
    gray = gray.filter(ImageFilter.SHARPEN)

    # Convert to numpy array
    img_array = np.array(gray)

    # Threshold for black & white effect
    threshold = 150
    bw_array = np.where(img_array > threshold, 255, 0).astype(np.uint8)

    # Convert back to image
    bw_image = Image.fromarray(bw_array)

    return bw_image

def image_to_pdf(image, pdf_path):
    temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    image.save(temp_img.name)

    pdf = FPDF()
    pdf.add_page()

    # Fit image to A4
    pdf.image(temp_img.name, x=10, y=10, w=190)

    pdf.output(pdf_path)

    temp_img.close()
    os.unlink(temp_img.name)

if uploaded_file:
    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to Scan PDF"):
        with st.spinner("Processing document..."):

            processed_image = process_document(image)

            st.subheader("Scanned Black & White Image")
            st.image(processed_image, use_container_width=True)

            # Save PDF
            pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            image_to_pdf(processed_image, pdf_file.name)

            with open(pdf_file.name, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name="scanned_document.pdf",
                mime="application/pdf"
            )

            os.unlink(pdf_file.name)
