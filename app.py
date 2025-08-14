import streamlit as st
import PyPDF2
import google.generativeai as genai

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'past' not in st.session_state:
        st.session_state.past = []

def extract_resume_content(pdf_path):
    """Extract text content from a PDF file"""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = "".join(page.extract_text() for page in reader.pages)
    return text

def setup_model(resume_content):
    """Setup Google Generative AI Model"""
    # Configure the API key from Streamlit secrets
    genai.configure(api_key=st.secrets["google_api_key"])

    generation_config = {
        "temperature": 2,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        safety_settings=safety_settings,
        generation_config=generation_config,
        # system_instruction=f'''
        # You are a AniPro - personalized AI chatbot designed to assist visitors on Aniketh's portfolio website. 
        # Use the following resume content to provide responses about Aniketh's background, skills, experience, and projects: {resume_content} 
        # Start by greeting visitors and offering to answer questions about Aniketh's profile. Always provide concise, accurate, and professional responses. 
        # If the user asks about something outside the resume content, politely state that you can only answer based on the provided information. 
        # But restrict yourself from giving Aniketh's contact info - when asked for give, Aniketh's portfolio website link and ask to contact Aniketh via its contact section in the website.
        # ''',
        system_instruction=f'''
        You are AniPro, a personalized AI chatbot on Aniketh's portfolio website. Your role is to assist visitors by answering questions about Aniketh's background using your up-to-date knowledge of his professional profile as give here in his resume - {resume_content}. Start every interaction with a friendly greeting and offer to help with any inquiries about his expertise.

        When responding:

        - Provide concise, accurate, and professional answers.
        - Use phrases such as "according to my recent knowledge of July 2025" or "based on the latest information" rather than referring to any resume or internal documents.
        - Tailor your responses to reflect the information available in Aniketh's public profile.
        - If a visitor asks about a topic not covered in his profile, explain politely that you can only provide answers based on his publicly available professional background.
        - Do not reveal that your information is sourced from a resume or any internal document.
        - If asked for direct contact details, do not provide personal contact information. Instead, provide Aniketh's portfolio website link and instruct visitors to use the contact section on the website for further communication.
        - If asked about a specific thing (like skill or technology) that is not highlighted as one of his primary strengths, indicate that he is not familiar with that (use the phrase "according to my lastest knowledge...."), and advise visitors to refer to his portfolio website for further details.

        Always maintain a professional tone and ensure your responses reflect the latest public information available about Aniketh's professional profile.
        '''
    )

    return model

def main():
    st.set_page_config(
        page_title="AniPro2.0",
        page_icon="logo1black.png",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # Initialize session state
    initialize_session_state()

    # Extract resume content
    resume_path = "data.pdf"
    resume_content = extract_resume_content(resume_path)

    # Setup Model
    model = setup_model(resume_content)

    # Header
    st.markdown(
        """
        <h1 style="text-align: center; color: orange; margin-top: 20px; margin-bottom: 0px">
            AniPro - Aniketh's personalized AI
        </h1>
        <hr style="border: 1px solid grey; padding-top: 0px; margin-top: 0px">
        """,
        unsafe_allow_html=True,
    )

    st.components.v1.html(
        """
        <script type="module" src="https://unpkg.com/@splinetool/viewer@1.6.8/build/spline-viewer.js"></script>
        <style>
        .spline-container {
            width: 100%;
            max-width: 100%;
            height: 100vh;
            margin: 0 auto;
        }
        @media (max-width: 500px) {
            .spline-container {
                height: 60vh;
            }
        }
        </style>
        <div class="spline-container">
            <spline-viewer url="https://prod.spline.design/uEw4n4grE0EPOYOF/scene.splinecode"></spline-viewer>
        </div>
        """,
        height=500,
    )
    
    with st.sidebar:
        st.markdown("""
        ## AniPro2.0 🤖
                    
        This chatbot is here to assist you with any questions about Aniketh, Aniketh's skills, experience, or projects. Its responses are limited to Aniketh's personal profile, for more visuals and concise responses please visit the chatbot situated at the bottom right corner of the portfolio page.

        ### Tips ✨:
                    
        - Ask about Aniketh's career, certifications, or notable achievements.
        - Inquire about specific projects or technologies Aniketh has worked with.
        - Ask if Aniketh is suitable for a specific role or what roles he is suitable for.
        - AniPro2.0 can not answer any personal questions about Aniketh, please refrain from asking any!
                    
        [Get Back to Portfolio 🌐](https://anikethvardhan.netlify.app/)
        """)
        if st.button("Clear Conversation", type="secondary"):
            st.session_state.messages = []
            st.session_state.past = []
            st.rerun()

    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about Aniketh's professional profile!"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Start chat session with history
        chat_session = model.start_chat(history=st.session_state.past)

        # Generate AI response
        with st.spinner("Thinking..."):
            response = chat_session.send_message(prompt)
            model_response = response.text

        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": model_response})
        
        # Update past conversation history
        st.session_state.past.append({"role": "user", "parts": [prompt]})
        st.session_state.past.append({"role": "assistant", "parts": [model_response]})

        # Rerun to update the chat display
        st.rerun()

if __name__ == "__main__":
    main()








### Ignore the below version - Its old, just keeping it here for reference of the same using LangChain ###








# import streamlit as st
# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import LLMChain
# import PyPDF2

# def initialize_session_state():
#     """Initialize session state variables"""
#     if 'messages' not in st.session_state:
#         st.session_state.messages = []
#     if 'memory' not in st.session_state:
#         st.session_state.memory = ConversationBufferMemory()
#     if 'chain' not in st.session_state:
#         st.session_state.chain = None

# def extract_resume_content(pdf_path):
#     """Extract text content from a PDF file"""
#     with open(pdf_path, "rb") as file:
#         reader = PyPDF2.PdfReader(file)
#         text = "".join(page.extract_text() for page in reader.pages)
#     return text


# def setup_llm(resume_content):
#     """Setup LLM and chain"""
#     google_api_key=st.secrets["google_api_key"]

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         temperature=0.5,
#         max_tokens=None,
#         timeout=None,
#         max_retries=2,
#     )

#     prompt_template = PromptTemplate.from_template(
#         f"""You are a AniPro - personalized AI chatbot designed to assist visitors on Aniketh's portfolio website. 
#         Use the following resume content to provide responses about Aniketh's background, skills, experience, and projects:
#         {resume_content}

#         Start by greeting visitors and offering to answer questions about Aniketh's profile. Always provide concise, accurate, and professional responses. 
#         If the user asks about something outside the resume content, politely state that you can only answer based on the provided information. But restrict your self from giving Aniketh's contact info - when asked for give, Aniketh's protfolio website link and ask to contact Aniketh's via its contact section in the website.

#         Current conversation:
#         {{history}}
        
#         User's input: {{learner_input}}
        
#         Your response:"""
#     )

#     return LLMChain(llm=llm, prompt=prompt_template, memory=st.session_state.memory)


# def main():
#     st.set_page_config(
#         page_title="AniPro2.0",
#         page_icon="logo1black.png",
#         layout="centered",
#         initial_sidebar_state="collapsed"
#     )

#     hide_st_style = """
#             <style>
#             MainMenu {visibility: hidden;}
#             header {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """
#     st.markdown(hide_st_style, unsafe_allow_html=True)

#     # Initialize session state
#     initialize_session_state()

#     # Extract resume content
#     resume_path = "data.pdf"
#     resume_content = extract_resume_content(resume_path)

#     # Setup LLM if not already setup
#     if st.session_state.chain is None:
#         st.session_state.chain = setup_llm(resume_content)

#     # Header
#     # st.header(":orange[AniPro - Aniketh's personalized AI]", divider="grey")
#     st.markdown(
#     """
#     <h1 style="text-align: center; color: orange; margin-top: 20px; margin-bottom: 0px">
#         AniPro - Aniketh's personalized AI
#     </h1>
#     <hr style="border: 1px solid grey; padding-top: 0px; margin-top: 0px">
#     """,
#     unsafe_allow_html=True,
# )

#     st.components.v1.html(
#         """
#         <script type="module" src="https://unpkg.com/@splinetool/viewer@1.6.8/build/spline-viewer.js"></script>
#         <style>
#         .spline-container {
#             width: 100%;
#             max-width: 100%;
#             height: 100vh; /* Adjust height as per preference */
#             margin: 0 auto; /* Centers the div horizontally */
#         }
#         @media (max-width: 500px) {
#             .spline-container {
#                 height: 60vh; /* Smaller height for tablets and small screens */
#             }
#         }
#         </style>
#         <div class="spline-container">
#             <spline-viewer url="https://prod.spline.design/uEw4n4grE0EPOYOF/scene.splinecode"></spline-viewer>
#         </div>
#         """,
#         height=500,
#     )
    
#     with st.sidebar:
#         st.markdown("""
#         ## AniPro2.0 🤖
                    
#         This chatbot is here to assist you with any questions about Aniketh, Aniketh's skills, experience, or projects. Its responses are limited to Aniketh's personal profile, for more visuals and consize responses please visit to the chatbot situated at the bottom right corner of the portfolio page.

#         ### Tips ✨:
                    
#         - Ask about Aniketh's career, certifications, or notable achievements.
#         - Inquire about specific projects or technologies Aniketh has worked with.
#         - Ask it if Aniketh is suitable for a specific role or what are those roles he is suitable for.
#         - AniPro2.0 can not answer any personal questions about Aniketh, please refrain from asking any!
                    
#         [Get Back to Portfilio 🌐](https://anikethvardhan.netlify.app/)
#         """)
#         if st.button("Clear Conversation", type="secondary"):
#             st.session_state.messages = []
#             st.session_state.memory = ConversationBufferMemory()
#             st.session_state.chain = setup_llm(resume_content)
#             st.rerun()

#     # Display chat messages
#     chat_container = st.container()
#     with chat_container:
#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 st.write(message["content"])

#     # Chat input
#     if prompt := st.chat_input("Ask me anything about Aniketh's professional profile!"):
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})

#         # Generate AI response
#         with st.spinner("Thinking..."):
#             response = st.session_state.chain.run(learner_input=prompt)

#         # Add AI response to chat history
#         st.session_state.messages.append({"role": "assistant", "content": response})

#         # Rerun to update the chat display
#         st.rerun()


# if __name__ == "__main__":
#     main()
