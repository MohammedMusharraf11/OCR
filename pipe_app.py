import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyBw9qlfSD4LBiZpAQEf0jaUCd70Z_fnkB8"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit UI
st.title("📝 OCR with Gemini (Refined Table Extraction)")

# Upload image
uploaded_file = st.file_uploader("Upload an image of handwritten text", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract & Refine Text"):
        with st.spinner("Extracting text..."):
            try:
                # First Pass: Initial Extraction
                prompt_initial = [
                    image,
                    "Extract handwritten text accurately while preserving tables in Markdown format:\n\n"
                    "- **Keep empty cells as blank (`|   |`) and DO NOT autofill.**\n"
                    "- If a cell is empty, return it as `-` or `N/A`, but do not guess content.\n"
                    "- Ensure tables are formatted correctly in Markdown (`| Col1 | Col2 |`).\n"
                    "- Do not modify grammar or content.\n"
                ]

                response_initial = model.generate_content(prompt_initial)
                extracted_text = response_initial.text

                # Second Pass: Auto-Refinement
                prompt_refine = [
                    image,
                    f"Here is the initially extracted text:\n```\n{extracted_text}\n```"
                    "Now, carefully correct any OCR errors **without autofilling empty cells**:\n"
                    "- **If a cell is empty, return it as `-` or leave it blank (`|   |`).**\n"
                    "- Ensure tables are properly aligned in Markdown.\n"
                    "- Fix incorrect characters or missing words but do not guess missing data."
                ]

                response_refine = model.generate_content(prompt_refine)
                refined_text = response_refine.text

                # Display results
                st.subheader("✅ Refined Output:")
                st.markdown(refined_text, unsafe_allow_html=True)
                st.code(refined_text, language="text")

                # Allow Download
                st.download_button("⬇️ Download Markdown", refined_text, file_name="refined_text.md", mime="text/markdown")

            except Exception as e:
                st.error(f"Error: {e}")
