# SVES Copilot Instructions

## Architecture Overview

This is a **single-file Streamlit application** (`app.py`, ~916 lines) implementing the Simic Virtual Expert System (SVES) - an AI-powered technical advisor for advanced energy technologies (RTCR, Cosmos X-9 drilling, SCWO).

### Component Structure in `app.py`

1. **Configuration Layer** (lines 47-100): `LLMProvider` enum, `LLMConfig` dataclass, `DEFAULT_CONFIGS` dict
2. **Knowledge Base** (lines 102-320): `load_knowledge_base()` - simulates RAG with embedded technical documents
3. **LLM Clients** (lines 322-545): Abstract `LLMClient` + implementations: `OllamaClient`, `VLLMClient`, `LMStudioClient`, `AzureGovClient`
4. **AI Agent Core** (lines 550-650): `build_system_prompt()`, `get_sves_response()` - the "Golden Prompt" architecture
5. **Streamlit UI** (lines 655-916): `render_sidebar()`, `render_chat_interface()`, `main()`

### LLM Backend Pattern

All LLM clients follow an OpenAI-compatible chat interface:
```python
def generate(self, prompt: str, system_prompt: str, conversation_history: List[Dict]) -> str:
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": prompt})
```

Use `create_llm_client(config: LLMConfig)` factory function to instantiate clients.

## Key Patterns

### Knowledge Base Injection
The `load_knowledge_base()` function returns concatenated technical documents embedded directly into the system prompt. This simulates RAG without a vector database:
- Document 1: NASA SCWO fundamentals
- Document 2: RTCR chemical pathways  
- Document 3: Cosmos X-9 drilling challenges

### Session State Management
Streamlit session state holds:
- `st.session_state.messages` - conversation history
- `st.session_state.llm_config` - current `LLMConfig`
- `st.session_state.llm_client` - instantiated `LLMClient`

### Error Handling Pattern
```python
try:
    response = llm_client.generate(...)
except requests.exceptions.ConnectionError:
    raise Exception("Cannot connect to LLM server...")
except requests.exceptions.Timeout:
    raise Exception("LLM request timed out...")
```

## Development Workflow

### Running the Application
```bash
# Ensure Ollama is running with llama3.1:70b model
ollama serve
ollama pull llama3.1:70b

# Run the Streamlit app
streamlit run app.py
```

Default URL: `http://localhost:8501`

### Dependencies
Core: `streamlit>=1.28.0`, `requests>=2.31.0`, `numpy>=1.24.0`

### Adding a New LLM Provider
1. Add enum value to `LLMProvider`
2. Add default config to `DEFAULT_CONFIGS`
3. Create new client class inheriting from `LLMClient`
4. Register in `create_llm_client()` factory
5. Handle provider-specific UI in `render_sidebar()`

## Code Conventions

- **Type hints**: All functions use type annotations
- **Docstrings**: Triple-quoted docstrings on all public functions
- **Constants**: Uppercase with underscores (`DEFAULT_CONFIGS`, `LLMProvider`)
- **Data classes**: Use `@dataclass` for configuration objects
- **ABC pattern**: Abstract base class for extensible clients

## Domain Context

When modifying prompts or knowledge base, understand these technical domains:
- **RTCR**: Radical Thermochemical Chain Reactions for hydrogen generation from ultramafic rocks
- **Cosmos X-9**: Supercritical water drilling (400-550°C, >22.1 MPa)
- **SCWO**: Supercritical Water Oxidation (critical point: 647K, 22.064 MPa)

Critical parameters to preserve in technical content:
- Operating conditions: >400°C, >25 MPa for RTCR
- H₂ production target: >500 kg/day, <$2.50/kg
- Drilling ROP improvement: 15-30 m/hr vs 2-8 m/hr conventional

## File Organization

```
app.py                           # Entire application (single file)
requirements.txt                 # Minimal dependencies
PROJECT_DOCUMENTATION.md         # Technical specification
SVES_MULTI_AGENT_DEMONSTRATION.md # Multi-agent workflow examples
README.md                        # User-facing documentation
```

## Testing Queries

Validate changes with these example prompts:
- "Design an RTCR experiment for olivine at 450°C and 28 MPa"
- "Analyze a drilling scenario at 3000m depth in granite with ROP of 12 m/hr"
- "What are the main challenges with salt precipitation in SCWO?"
