import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure Gemini API
GEMINI_API_KEY = "YOUR-API-KEY"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')

# Streamlit UI
st.title("📝 OCR with Gemini (Accurate Extraction & Refinement)")

# Upload image
uploaded_file = st.file_uploader("Upload an image of handwritten text", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract & Refine Text"):
        with st.spinner("Extracting text..."):
            try:
                # Initial Extraction
                prompt_initial = [
                    image,
                    "You are an expert in extracting handwritten text from student answer scripts. Your task is to:\n\n"
                    "1. Accurately extract the handwritten text exactly as it is.\n"
                    "2. Carefully cross-check and correct only recognition errors (e.g., OCR mistakes).\n"
                    "3. Do not modify or clean up grammatical or factual errors.\n"
                    "4. If the student's script contains tables, diagrams, figures, or flowcharts, you must:\n"
                    "- Reproduce tables in plain text or markdown table format, ensuring blank cells remain blank.\n"
                    "- Recreate flowcharts using markdown-friendly formats (e.g., Mermaid).\n"
                    "- For diagrams, recreate using ASCII art if possible.\n\n"
                    "If the student's script contains any graphs (e.g., line graphs, bar charts, scatter plots with X and Y axes), recreate them using markdown-supported formats such as Mermaid.js or ASCII plots. Ensure the axes, labels, and plotted data points are captured accurately. If needed, describe the graph layout and its key data in words.\n\n"
                    "Your role is to capture the student's original input precisely, as this will be evaluated by a human. Maintain full fidelity to the original script.\n\n"
                    "Additionally, if there are any strikethrough texts, either preserve them with formatting (e.g., ~~strikethrough~~) or ignore them from the extraction."
                ]

                response_initial = model.generate_content(prompt_initial)
                extracted_text = response_initial.text

                # Refinement Pass
                prompt_refine = [
                    image,
                    f"Here is the initially extracted text:\n```\n{extracted_text}\n```\n"
                    "Now, carefully correct any OCR errors **without modifying spelling mistakes, grammar, or factual content**:\n"
                    "- Maintain markdown tables correctly aligned, ensuring blank cells remain blank.\n"
                    "- Fix incorrect characters or missing words but do not autofill empty spaces.\n"
                    "- Ensure strikethrough text is either preserved as `~~text~~` or removed based on the original formatting."
                ]

                response_refine = model.generate_content(prompt_refine)
                refined_text = response_refine.text

                # Display results
                st.subheader("✅ Final Extracted Text:")
                st.markdown(refined_text, unsafe_allow_html=True)
                st.code(refined_text, language="text")

                # Allow Download
                st.download_button("⬇️ Download Markdown", refined_text, file_name="extracted_text.md", mime="text/markdown")

            except Exception as e:
                st.error(f"Error: {e}")
