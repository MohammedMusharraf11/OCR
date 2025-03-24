
# 📝 OCR with Gemini AI

This is a simple Streamlit application that extracts handwritten text from images using Google's Gemini API.

---

## 🚀 Features
- Upload an image of handwritten text (e.g., student answer scripts).
- Accurately extract handwritten text using Gemini's advanced OCR capabilities.
- Download the extracted text.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/MohammedMusharraf11/OCR.git
cd OCR
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

### 3. Configure Your API Key
- Open `app.py` and locate the following line:
  ```python
  GEMINI_API_KEY = "YOU-API-KEY"
  ```
- Replace `"YOU-API-KEY"` with your actual Gemini API key.

### Get your API key here:  
👉 [Google AI Studio - API Key](https://aistudio.google.com/app/apikey)

---

### 4. Run the Streamlit App
```bash
python -m streamlit run app.py
```

---

## 📄 Example
- Upload an image like a handwritten answer sheet.
- Click **"Extract Text"** to get precise OCR results.
- Download the extracted text with one click.


