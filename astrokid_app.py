import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import time

# Load environment variables
load_dotenv('api.env')

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    st.error("Please set your GEMINI_API_KEY in the api.env file")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# Astronomy keywords for topic detection
ASTRONOMY_KEYWORDS = [
    "planet", "sun", "star", "galaxy", "black hole", "universe", "solar system",
    "space", "orbit", "moon", "comet", "meteor", "astronaut", "NASA", "cosmos",
    "Milky Way", "gravity", "big bang", "telescope", "astronomy", "nebula", 
    "dark matter", "aliens", "Mars", "Jupiter", "Neptune", "Mercury", "Earth", 
    "Saturn", "Venus", "Uranus", "Pluto", "asteroid", "meteorite", "constellation",
    "supernova", "pulsar", "quasar", "exoplanet", "satellite", "space station",
    "rover", "spacecraft", "launch", "rocket", "space shuttle", "ISS", "Hubble",
    "telescope", "observatory", "planetarium", "astronomer", "astrophysics",
    "cosmology", "stellar", "lunar", "solar", "celestial", "interstellar",
    "extraterrestrial", "space exploration", "space mission", "space travel"
]

def is_astronomy_question(question):
    """Check if the question is related to astronomy"""
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in ASTRONOMY_KEYWORDS)

def web_search(query, max_results=3):
    """Perform web search for astronomy-related information"""
    try:
        with DDGS() as ddgs:
            # Add "astronomy" to the search query to ensure relevant results
            search_query = f"{query} astronomy space science"
            results = ddgs.text(search_query, max_results=max_results)
            return [r["body"] for r in results]
    except Exception as e:
        st.warning(f"Web search failed: {str(e)}")
        return []

def extract_text_from_url(url):
    """Extract text content from a URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:1000]  # Limit to first 1000 characters
    except Exception as e:
        return f"Could not extract content from {url}: {str(e)}"

def get_gemini_response(question, web_context=""):
    """Get response from Gemini AI"""
    try:
        # Configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create the prompt
        prompt = f"""You are AstroKid, a friendly and knowledgeable astronomy expert who explains complex space concepts to children aged 6-12 in simple, engaging terms.

Your mission is to:
1. Explain astronomy concepts in child-friendly language
2. Use simple analogies and examples kids can relate to
3. Make learning about space fun and exciting
4. Only answer questions about astronomy, space, and related topics
5. If asked about non-astronomy topics, politely redirect to astronomy

Here's some additional information from the web to help you answer:
{web_context}

Question: {question}

Please provide a clear, engaging, and educational response suitable for children:"""

        # Generate response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Sorry, I'm having trouble thinking about space right now. Error: {str(e)}"

def main():
    # Page configuration
    st.set_page_config(
        page_title="AstroKid - Your Space Teacher",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .astronomy-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .response-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🚀 AstroKid</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your friendly space teacher who makes astronomy fun and easy to understand!</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🌟 About AstroKid")
        st.markdown("""
        AstroKid is your personal astronomy teacher! 
        
        **What I can help you with:**
        - Planets and solar system
        - Stars and galaxies
        - Space exploration
        - Astronauts and missions
        - And much more!
        
        **Just ask me anything about space!** 🌌
        """)
        
        st.header("🎯 Quick Questions")
        quick_questions = [
            "What is a black hole?",
            "How do planets orbit the sun?",
            "What is the biggest planet?",
            "How do astronauts live in space?",
            "What is a shooting star?",
            "How big is the universe?"
        ]
        
        for question in quick_questions:
            if st.button(question, key=f"quick_{question}"):
                st.session_state.user_question = question
    
    # Main content area
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Input area
        st.markdown('<div class="astronomy-box">', unsafe_allow_html=True)
        user_question = st.text_input(
            "Ask me anything about space! 🌟",
            placeholder="e.g., What is a black hole? How do planets orbit the sun?",
            key="user_input"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Check if question was submitted
        if st.button("🚀 Ask AstroKid!", type="primary") or 'user_question' in st.session_state:
            if 'user_question' in st.session_state:
                user_question = st.session_state.user_question
                del st.session_state.user_question
            
            if user_question:
                # Check if it's an astronomy question
                if not is_astronomy_question(user_question):
                    st.error("🚫 Oops! I'm AstroKid, your space teacher! I can only answer questions about astronomy and space. Try asking me about planets, stars, galaxies, or space exploration!")
                else:
                    # Show loading
                    with st.spinner("🔍 Searching the cosmos for answers..."):
                        # Get web context
                        web_results = web_search(user_question)
                        web_context = "\n".join(web_results) if web_results else ""
                        
                        # Get AI response
                        response = get_gemini_response(user_question, web_context)
                    
                    # Display response
                    st.markdown('<div class="response-box">', unsafe_allow_html=True)
                    st.markdown("### 🌟 AstroKid's Answer:")
                    st.markdown(response)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Show web sources if available
                    if web_results:
                        with st.expander("📚 Sources from the web"):
                            for i, result in enumerate(web_results[:3], 1):
                                st.markdown(f"**Source {i}:**")
                                st.markdown(result[:300] + "..." if len(result) > 300 else result)
                                st.divider()
                    
                    # Follow-up suggestions
                    st.markdown("### 💫 Want to know more?")
                    follow_up_questions = [
                        "Tell me more about this!",
                        "Can you explain this in simpler terms?",
                        "What are some fun facts about this?",
                        "How does this relate to other space things?"
                    ]
                    
                    cols = st.columns(2)
                    for i, follow_up in enumerate(follow_up_questions):
                        if cols[i % 2].button(follow_up, key=f"follow_{i}"):
                            # Generate a follow-up response
                            follow_up_prompt = f"Based on your previous answer about '{user_question}', {follow_up.lower()}"
                            with st.spinner("Thinking..."):
                                follow_up_response = get_gemini_response(follow_up_prompt, web_context)
                            
                            st.markdown('<div class="response-box">', unsafe_allow_html=True)
                            st.markdown("### 🌟 AstroKid's Follow-up:")
                            st.markdown(follow_up_response)
                            st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Please ask me a question about space! 🌌")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        Made with ❤️ by AstroKid | Powered by Gemini AI | 
        <a href="https://github.com/yourusername/astrokid" target="_blank">GitHub</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
