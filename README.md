# 🚀 AstroKid - Your Space Teacher

AstroKid is an AI-powered astronomy teacher that explains complex space concepts to children in simple, engaging terms. Built with Streamlit and powered by Google's Gemini AI, it provides interactive, educational responses about astronomy and space exploration.

##  Features

- **Child-Friendly Explanations**: Complex astronomy concepts explained in simple terms for children aged 6-12
- **Web-Enhanced Knowledge**: Uses web search to provide up-to-date information
- **Interactive Interface**: Beautiful Streamlit UI with quick question buttons
- **Topic Detection**: Automatically detects if questions are astronomy-related
- **Follow-up Questions**: Suggests related questions to encourage deeper learning
- **Source Attribution**: Shows web sources for transparency

## Docker
**To facilitate dependency installation, the project is available on Docker at the following address:**
 ```bash
https://hub.docker.com/layers/amii765/astrokid/latest/images/sha256:309ff2ac8bec6dbc6e76f9242ff5f9a5b9a5470c6ecf5ab99495dbc3434ad035?uuid=B74B4A4B-7420-4176-B10A-27960C2020BE
   ```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Astrokid
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API keys**:
   - Edit the `api.env` file and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   To get a Gemini API key:
   1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   2. Create a new API key
   3. Copy and paste it into the `api.env` file

##  Running the Application

1. **Start the Streamlit app**:
   ```bash
   streamlit run astrokid_app.py
   ```

2. **Open your browser** and go to the URL shown in the terminal (usually `http://localhost:8501`)

3. **Start asking questions** about space! 🌌

##  Example Questions

Try asking AstroKid about:
- "What is a black hole?"
- "How do planets orbit the sun?"
- "What is the biggest planet?"
- "How do astronauts live in space?"
- "What is a shooting star?"
- "How big is the universe?"
- "What are constellations?"
- "How do rockets work?"

## 🏗️ Project Structure

```
Astrokid/
├── astrokid_app.py      # Main Streamlit application
├── requirements.txt     # Python dependencies
├── api.env             # API keys (create this file)
├── README.md           # This file

## 🔧 How It Works

1. **Question Input**: Users type astronomy questions in the Streamlit interface
2. **Topic Detection**: The app checks if the question is astronomy-related using keyword matching
3. **Web Search**: If it's an astronomy question, the app searches the web for relevant information
4. **AI Processing**: Gemini AI processes the question with web context to generate child-friendly responses
5. **Response Display**: The answer is displayed with follow-up suggestions and source attribution

##  Customization

You can customize AstroKid by:

- **Adding more keywords**: Edit the `ASTRONOMY_KEYWORDS` list in `astrokid_app.py`
- **Changing the prompt**: Modify the prompt in the `get_gemini_response()` function
- **Styling**: Update the CSS in the `main()` function
- **Quick questions**: Add more example questions in the sidebar

## 🚫 Limitations

- Only answers astronomy and space-related questions
- Requires internet connection for web search functionality
- API rate limits may apply depending on your Gemini plan

## 🤝 Contributing

Feel free to contribute to AstroKid by:
- Adding more astronomy keywords
- Improving the prompt engineering
- Enhancing the UI/UX
- Adding new features like image generation or interactive elements

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Google Gemini AI for providing the AI capabilities
- Streamlit for the beautiful web interface
- DuckDuckGo for web search functionality
- The astronomy community for inspiring this educational tool

---

**Made with ❤️ for young space explorers everywhere!** 🌟
