import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configure Gemini API
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit UI
st.title("📝 OCR with Gemini")

uploaded_file = st.file_uploader("Upload an image of handwritten text", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text"):
        with st.spinner("Extracting text..."):
            try:
                prompt_parts = [
                    image,
                    "You are an expert in extracting handwritten text from student answer scripts. Your task is to:\n\n"
                    "Accurately extract the handwritten text as it is.\n\n"
                    "Carefully cross-check and correct only recognition errors (e.g., OCR mistakes), ensuring the extracted text exactly matches what the student wrote.\n\n"
                    "Do not add, remove, or modify any content, formatting, or phrasing, even if the student's writing contains grammatical, spelling, or factual errors.\n\n"
                    "Your role is to capture the student's original input precisely, as this text will be evaluated later by a human. Maintain full fidelity to the original script."
                ]

                response = model.generate_content(prompt_parts)
                extracted_text = response.text

                if extracted_text:
                    st.subheader("📄 Extracted Text:")
                    st.code(extracted_text, language="text")

                    # Copy to clipboard functionality (works in Streamlit cloud or browser)
                    st.download_button("📋 Copy Text", extracted_text, file_name="extracted_text.txt", mime="text/plain")
                else:
                    st.error("No text was extracted.")
            except Exception as e:
                st.error(f"Error: {e}")
