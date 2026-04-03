# 🔍 FactMind - AI-Powered Fact Checker

A sophisticated fact-checking system powered by CrewAI that uses multiple specialized AI agents to analyze claims and determine their authenticity.

## ✨ Features

- **Multi-Agent System**: 7 specialized AI agents working in sequence
- **Real-time Analysis**: Live web search and content analysis
- **Social Media Monitoring**: Tracks viral spread and misinformation patterns
- **Intelligent Validation**: Determines if statements contain factual claims
- **Streamlit Interface**: Clean, intuitive web UI with color-coded results
- **Comprehensive Analysis**: Detailed explanations and confidence scoring

## 🏗️ System Architecture

### Agent Pipeline
```
Input → Validator → Scraper → Claim Expert → Researcher → Analyst → Social Media → Verdict
```

1. **🔍 Validator**: Determines if input contains verifiable claims
2. **🌐 Scraper**: Extracts content from URLs and web sources
3. **🎯 Claim Expert**: Identifies specific checkable factual claims
4. **📚 Researcher**: Searches trusted sources for supporting evidence
5. **⚖️ Analyst**: Cross-references claims against found evidence
6. **📱 Social Media Analyst**: Analyzes viral patterns and spread
7. **📋 Verdict Agent**: Generates final verdict with detailed explanation

### Technology Stack
- **AI Framework**: CrewAI for multi-agent orchestration
- **Language Models**: OpenAI GPT-4o-mini, X.AI Grok-4-fast
- **Web Search**: Tavily API for real-time information retrieval
- **URL Analysis**: Exa API for citation extraction and verification
- **Frontend**: Streamlit for interactive web interface
- **Backend**: Python 3.8+

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- API keys for OpenAI, X.AI, and Tavily

### Installation

1. **Clone Repository**
```bash
git clone <your-repo-url>
cd Factcheck
```

2. **Setup Environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
Create `.env` file in root directory:
```env
OPENAI_API_KEY=your_openai_key_here
XAI_API_KEY=your_xai_key_here
TAVILY_API_KEY=your_tavily_key_here
EXA_API_KEY=your_exa_key_here
```

### Launch Application
```bash
streamlit run app.py
```
Access at: `http://localhost:8501`

## 📱 Usage

### Web Interface
1. Enter a claim in the text input
2. Click "🔍 Analyze Claim"
3. View color-coded verdict:
   - ✅ **Green**: Genuine/True
   - ❌ **Red**: Fake/False
   - ⚠️ **Yellow**: Misleading/Uncertain

### Programmatic Usage
```python
from crew import run_factcheck

result = run_factcheck("Your claim here", "text")
print(result)
```

## 📊 Output Structure

```json
{
  "verdict": "Genuine|Fake|Misleading",
  "explanation": "Detailed analysis of the claim...",
  "confidence_score": "0-100",
  "claims_analyzed": "Summary of specific claims checked"
}
```

## 📁 Project Structure

```
Factcheck/
├── crew/                      # Core AI system
│   ├── tools/                 # Agent tools
│   │   ├── __init__.py
│   │   ├── config.py          # API configurations
│   │   ├── validate_tool.py   # Claim validation
│   │   ├── search_tool.py     # Web search functionality
│   │   ├── scraper_tool.py    # Content extraction
│   │   └── social_media.py    # Social media analysis
│   ├── __init__.py
│   ├── agent.py               # AI agent definitions
│   ├── task.py                # Task workflows
│   └── crew_runner.py         # Main orchestration
├── app.py                     # Streamlit web interface
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                  # This file
```

## 🔧 Configuration

### Required API Keys

| Service | Purpose | Get Key |
|---------|---------|---------|
| OpenAI | GPT-4o-mini model access | [OpenAI Platform](https://platform.openai.com) |
| X.AI | Grok-4-fast model | [X.AI Console](https://console.x.ai) |
| Tavily | Web search API | [Tavily API](https://tavily.com) |
| Exa | URL citation & analysis | [Exa](https://exa.ai) |

### Trusted Sources
The system prioritizes information from:
- **News**: Reuters, AP News, BBC
- **Health**: WHO, CDC
- **Science**: Nature, academic journals
- **Fact-checking**: Snopes, PolitiFact, FactCheck.org
- **Reference**: Wikipedia

## 🎯 Example Analysis

**Input**: "The Earth is flat and NASA is hiding the truth"

**Output**:
- **Verdict**: ❌ Fake
- **Confidence**: 98%
- **Analysis**: "This claim contradicts overwhelming scientific evidence. The spherical nature of Earth has been established through multiple independent methods including satellite imagery, physics experiments, and astronomical observations..."

## ⚡ Performance Features

- **Parallel API Calls**: Social media searches (Twitter, Reddit, General) and URL HEAD checks run concurrently via `ThreadPoolExecutor`
- **LLM Response Cache**: SQLiteCache persists responses to disk — identical LLM inputs never hit the API twice
- **Claim Result Cache**: Repeated claims return instantly from an in-memory cache within the same session
- **Optimized Search**: Trusted-domain and general-web searches share a single `SearchTool` implementation
- **Reduced Token Usage**: Verdict agent receives only the essential context (research + analysis + social) instead of all 6 prior task outputs
- **Single Iteration**: Streamlined analysis pipeline

## 🛠️ Development

### Adding Custom Tools
1. Create new tool in `crew/tools/`
2. Import in `crew/tools/__init__.py`
3. Assign to relevant agent in `crew/agent.py`

### Modifying Agents
Edit `crew/agent.py` to customize:
- Agent roles and objectives
- Tool assignments
- LLM model selection
- Temperature settings

### Extending Tasks
Modify `crew/task.py` to adjust:
- Task descriptions
- Expected outputs
- Agent assignments
- Task dependencies

## 🔒 Privacy & Ethics

- No personal data storage
- API calls follow provider terms
- Transparent analysis process
- Open-source methodology

## 📈 Roadmap

- [ ] Multi-language support
- [ ] Image/video fact-checking


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: your-email@example.com

## 🙏 Acknowledgments

- [CrewAI](https://crewai.com) for the multi-agent framework
- [Streamlit](https://streamlit.io) for the web interface
- [Tavily](https://tavily.com) for search capabilities
- OpenAI and X.AI for language models

---

**Built with ❤️ for truth and transparency**

*"In a world of information overload, FactMind helps you separate fact from fiction."*
