# Simic Virtual Expert System (SVES)

🔬 **AI-Powered Technical Advisory for Advanced Energy Technologies**

## Overview

The Simic Virtual Expert System (SVES) is a cutting-edge AI prototype designed to provide expert-level technical guidance for complex domains in supercritical chemistry and advanced drilling technologies. Built as a Phase I government proposal deliverable, this system demonstrates AI's capability to reason across:

- **RTCR Technology**: Radical Thermochemical Chain Reactions for in-situ hydrogen generation
- **Cosmos X-9**: Supercritical water drilling systems for crystalline formations
- **SCWO Chemistry**: Supercritical Water Oxidation fundamentals

## 🚀 Features

- **Expert-Level AI Reasoning**: Powered by Anthropic's Claude AI with a comprehensive technical knowledge base
- **Interactive Web Interface**: Built with Streamlit for intuitive user experience
- **Automated Experimental Design**: Generate detailed RTCR experimental protocols with safety assessments
- **Drilling Scenario Analysis**: Perform real-time engineering calculations and risk assessments
- **RAG-Simulated Knowledge Base**: Leverages Claude's 200K token context window for deep technical reasoning

## 📋 Technology Stack

- **Backend/UI**: Python 3 with Streamlit
- **AI Engine**: Anthropic Claude API (Sonnet 4)
- **Scientific Computing**: NumPy
- **Knowledge Representation**: Context-injected technical documents

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/simic-virtual-expert-system.git
   cd simic-virtual-expert-system
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit anthropic numpy
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - Enter your Anthropic API key in the sidebar
   - Start asking technical questions!

## 💡 Example Queries

Try asking SVES:

- "Design an RTCR experiment for olivine at 450°C and 28 MPa"
- "Analyze a drilling scenario at 3000m depth in granite with ROP of 12 m/hr"
- "What are the main challenges with salt precipitation in SCWO?"
- "Calculate the thermal stress in a wellbore during Cosmos X-9 operations"
- "Explain the radical chain mechanism in supercritical water"

## 🏗️ Architecture

### Four Core Components

1. **Mock Knowledge Base** (`load_knowledge_base()`)
   - NASA Glenn SCWO Fundamentals
   - RTCR Chemical Pathways
   - Cosmos X-9 Drilling Challenges

2. **AI Agent Core** (`get_sves_response()`)
   - Constructs the "Golden Prompt" for Claude
   - Manages conversation history
   - Handles API calls with robust error handling

3. **User Interface** (Streamlit components)
   - Professional sidebar with configuration
   - Chat interface with conversation history
   - Markdown rendering for formatted responses

4. **Tool System**
   - `design_rtcr_experiment`: Experimental protocol generator
   - `analyze_drilling_scenario`: Engineering analysis tool

## 📚 Knowledge Domains

### RTCR (Radical Thermochemical Chain Reactions)
- In-situ hydrogen generation from ultramafic rocks
- Supercritical water-mediated radical pathways
- Thermal runaway prevention and safety protocols

### Cosmos X-9 Supercritical Drilling
- Enhanced Rate of Penetration (ROP) in crystalline formations
- Thermal stress management and wellbore stability
- Cuttings transport in low-viscosity SCW environments

### SCWO (Supercritical Water Oxidation)
- Critical point chemistry (647 K, 22.1 MPa)
- Radical-mediated oxidation mechanisms
- Materials compatibility and corrosion management

## 🔒 Security & API Keys

⚠️ **Important**: Never commit your API key to version control!

- The application requires you to enter your Anthropic API key via the sidebar
- Keys are stored only in session state (not persisted)
- For production deployment, use environment variables or secure key management systems

## 🤝 Contributing

This is a prototype for demonstration purposes. For contributions or inquiries:

- Simic Energy Services
- Phase I Government Proposal Deliverable
- Version 1.0.0

## 📄 License

Copyright © 2025 Simic Energy Services. All rights reserved.

This prototype is provided for demonstration and evaluation purposes.

## 🔬 Technical Notes

### AI Prompt Engineering
The system uses a carefully crafted "Golden Prompt" that:
- Defines the AI's expert role and capabilities
- Injects the full knowledge base into context
- Specifies tool usage patterns with executable code examples
- Enforces safety-first response guidelines

### Scalability
In production, this prototype would be enhanced with:
- Vector database integration (Pinecone, Weaviate)
- User authentication and session management
- Response caching and optimization
- Multi-modal support (diagrams, equations)
- API rate limiting and cost monitoring

## 📞 Support

For technical questions or support:
- Review the example queries in the sidebar
- Check that your API key is correctly entered
- Ensure all dependencies are installed
- Verify internet connectivity for API calls

---

**Built with** ❤️ **for the future of clean energy**
