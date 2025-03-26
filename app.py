import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyBw9qlfSD4LBiZpAQEf0jaUCd70Z_fnkB8"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')

# Streamlit UI
st.title("📝 OCR with Gemini (Markdown & Plain Text)")

uploaded_file = st.file_uploader("Upload an image of handwritten text", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text"):
        with st.spinner("Extracting text..."):
            try:
                prompt_parts = [
                    image,
                    "You are an expert in extracting handwritten text from student answer scripts. Your task is to:\n\n"
                    "1. Accurately extract the handwritten text exactly as it is.\n"
                    "2. Carefully cross-check and correct only recognition errors (e.g., OCR mistakes).\n"
                    "3. Do not modify or clean up grammatical or factual errors.\n"
                    "4. If the student's script contains tables, diagrams, figures, or flowcharts, you must:\n"
                    "- Reproduce tables in plain text or markdown table format.\n"
                    "- Recreate flowcharts using markdown-friendly formats (e.g., Mermaid).\n"
                    "- For diagrams, recreate using ASCII art if possible.\n\n"
                    "If the student's script contains any graphs (e.g., line graphs, bar charts, scatter plots with X and Y axes), recreate them using markdown-supported formats such as Mermaid.js or ASCII plots. Ensure the axes, labels, and plotted data points are captured accurately. If needed, describe the graph layout and its key data in words.\n\n"
                    "Your role is to capture the student's original input precisely, as this will be evaluated by a human. Maintain full fidelity to the original script."
                ]

                response = model.generate_content(prompt_parts)
                extracted_text = response.text

                if extracted_text:
                    st.subheader("📄 Rendered Markdown:")
                    st.markdown(extracted_text, unsafe_allow_html=True)

                    st.subheader("📝 Plain Extracted Text:")
                    st.code(extracted_text, language="text")

                    # Download as .md file
                    st.download_button("⬇️ Download Markdown", extracted_text, file_name="extracted_text.md", mime="text/markdown")
                else:
                    st.error("No text was extracted.")
            except Exception as e:
                st.error(f"Error: {e}")
