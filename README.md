# AniPro – Personalized AI Chatbot for your (Aniketh's) Portfolio

AniPro 2.0 is a **Streamlit-powered AI chatbot** that uses **Google's Gemini API** to provide professional, concise, and engaging answers about your professional profile. It reads directly from a PDF version of your resume and is designed to integrate seamlessly into your portfolio website for an interactive visitor experience.

---

## ✨ Features

- **Interactive Chat Interface** – Real-time Q&A via Streamlit's `st.chat_message` & `st.chat_input`.
- **Resume-Based AI Responses** – Extracts and uses resume content for accurate answers.
- **Google Gemini API** – Powered by `gemini-2.5-flash` for quick, contextual replies.
- **Persistent Session Memory** – Maintains conversation flow during a session.
- **Professional & Polite Tone** – Always starts with a friendly greeting and stays on-topic.
- **Custom Safety Filters** – Configured to avoid sharing sensitive or inappropriate information.
- **Portfolio Integration** – Redirects visitors to the portfolio site for contact.

---

## 🛠️ Tech Stack

- [Python](https://www.python.org/) - Programming Language
- [Streamlit](https://streamlit.io/) – Web UI framework
- [PyPDF2](https://pypi.org/project/PyPDF2/) – PDF parsing
- [Google Generative AI Python SDK](https://ai.google.dev/) – Gemini AI responses

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/AniPro-2.0.git
cd AniPro-2.0
```

### 2️⃣ Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Key - Create a {.streamlit/secrets.toml} file in the project root

```bash
google_api_key = "YOUR_GOOGLE_API_KEY"
```

### 5️⃣ Replace data.pdf with your custom resume (rename your resume into data.pdf) in the root.

### 6️⃣ Run the application

```bash
streamlit run app.py
```

---

## 📌 Usage Instructions

- When you open the app in your browser, you’ll see a friendly greeting.
- Ask any questions about your's career, skills, certifications, or projects.
- Out-of-scope or unrelated questions will be politely declined.
- For direct communication, you’ll be directed to the portfolio website (you can reset the link to your portfolio website in the app.py code file).

---

## 🔒 Limitations

- Does not share personal contact details directly.
- Can only respond based on publicly available professional information.
- Cannot answer questions outside of the professional scope.
