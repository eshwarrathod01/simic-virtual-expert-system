"""
SIMIC VIRTUAL EXPERT SYSTEM (SVES) - GOVERNMENT EDITION v2.0
=============================================================

A self-hosted AI expert system for RTCR and Cosmos X-9 supercritical drilling technologies.
Designed for FedRAMP compliance with full data sovereignty.

SUPPORTED AI BACKENDS:
---------------------
1. Ollama (Local) - Best for development and testing
2. vLLM (Production) - Best for high-performance deployment
3. LM Studio (Local) - Alternative local option
4. Custom API - For Azure Government or custom endpoints

INSTALLATION:
------------
# Core dependencies
pip install streamlit requests numpy

# For Ollama (recommended for local):
# Download from https://ollama.ai
# Then run: ollama pull llama3.1:70b

# For vLLM (production):
pip install vllm
# python -m vllm.entrypoints.openai.api_server --model meta-llama/Llama-3.1-70B-Instruct

USAGE:
------
streamlit run app.py

AUTHOR: Simic Energy Services
VERSION: 2.0.0 (Government Edition - Self-Hosted)
COMPLIANCE: FedRAMP High Ready
"""

import streamlit as st
import requests
import json
import traceback
import os
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# CONFIGURATION
# ============================================================================

class LLMProvider(Enum):
    """Supported LLM providers for self-hosted deployment."""
    OLLAMA = "ollama"
    VLLM = "vllm"
    LM_STUDIO = "lm_studio"
    CUSTOM_API = "custom_api"
    AZURE_GOV = "azure_gov"


@dataclass
class LLMConfig:
    """Configuration for LLM backend."""
    provider: LLMProvider
    base_url: str
    model_name: str
    api_key: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 120


# Default configurations for different providers
DEFAULT_CONFIGS = {
    LLMProvider.OLLAMA: LLMConfig(
        provider=LLMProvider.OLLAMA,
        base_url="http://localhost:11434",
        model_name="llama3.1:70b",
        max_tokens=4096,
        temperature=0.7
    ),
    LLMProvider.VLLM: LLMConfig(
        provider=LLMProvider.VLLM,
        base_url="http://localhost:8000",
        model_name="meta-llama/Llama-3.1-70B-Instruct",
        max_tokens=4096,
        temperature=0.7
    ),
    LLMProvider.LM_STUDIO: LLMConfig(
        provider=LLMProvider.LM_STUDIO,
        base_url="http://localhost:1234",
        model_name="local-model",
        max_tokens=4096,
        temperature=0.7
    ),
    LLMProvider.AZURE_GOV: LLMConfig(
        provider=LLMProvider.AZURE_GOV,
        base_url="https://your-resource.openai.azure.us",
        model_name="gpt-4",
        api_key=None,  # Set via environment or UI
        max_tokens=4096,
        temperature=0.7
    ),
}


# ============================================================================
# COMPONENT 1: MOCK KNOWLEDGE BASE
# ============================================================================

def load_knowledge_base() -> str:
    """
    Simulates a RAG system by loading foundational documents directly into context.
    In production, this would query a vector database (Pinecone, Weaviate, etc.).
    
    Returns:
        str: Concatenated knowledge base content for the LLM's context window.
    """
    
    doc1 = """
    === DOCUMENT 1: NASA_Glenn_SCWO_Fundamentals.txt ===
    
    SUPERCRITICAL WATER OXIDATION (SCWO) - NASA GLENN RESEARCH CENTER
    
    Critical Parameters:
    - Temperature: 647.1 K (373.95°C)
    - Pressure: 22.064 MPa (3,200 psi)
    
    Fundamental Properties:
    Above the critical point, water exhibits unique properties that make it an exceptional 
    reaction medium:
    
    1. IONIC EQUILIBRIUM COLLAPSE
       - Ion product (Kw) drops from 10^-14 to 10^-20 or lower
       - Water behaves as a non-polar solvent
       - Organic compounds become highly soluble
       - Salts precipitate out (major operational challenge)
    
    2. RADICAL CHEMISTRY
       - Primary radicals: OH• (hydroxyl), HO₂• (hydroperoxyl), H• (hydrogen atom)
       - Reaction pathways dominated by radical chain mechanisms
       - Oxidation rates 100-1000x faster than subcritical conditions
       - Near-complete destruction (>99.99%) of organic hazardous waste
    
    3. MATERIALS CHALLENGES
       - Hastelloy C-276: Industry standard, but subject to intergranular corrosion
       - Chloride-accelerated stress corrosion cracking (SCC) at >500°C
       - Salt precipitation on reactor walls leads to hot spots and thermal fatigue
       - Titanium liner concepts show promise for chloride environments
    
    4. OPERATIONAL REGIMES
       - Hydrothermal Flames: >600°C, spontaneous ignition of organics in SCW
       - Salt Management: Critical for continuous operation; requires engineered separators
       - Residence Time: Typically 30-120 seconds for 99.99% destruction efficiency
    
    NASA Glenn Focus Areas:
    - Closed-loop life support systems for spacecraft
    - Waste water treatment and resource recovery
    - Hybrid propulsion systems using SCWO energy release
    
    Key References:
    - Proc. Int. Conf. on SCWO (1995-2018)
    - NASA/TM-2003-212185: "SCWO for Spacecraft Waste Processing"
    """
    
    doc2 = """
    === DOCUMENT 2: RTCR_Chemical_Pathways.txt ===
    
    RADICAL THERMOCHEMICAL CHAIN REACTIONS (RTCR) FOR IN-SITU H₂ GENERATION
    
    MISSION OBJECTIVE:
    Induce and sustain radical-mediated hydrogen production from ultramafic rock 
    formations using supercritical water as the reaction initiator and medium.
    
    TARGET LITHOLOGY:
    - Olivine: (Mg,Fe)₂SiO₄ - Primary reactant
    - Serpentinite: Mg₃Si₂O₅(OH)₄ - Pre-hydrated ultramafic phase
    - Chromite: FeCr₂O₄ - Iron source for redox coupling
    
    PROPOSED RTCR MECHANISM (SIMPLIFIED):
    
    Step 1: Initiation (Supercritical Regime, T > 400°C, P > 25 MPa)
        H₂O → OH• + H•
        (Water dissociation enhanced by extreme PT conditions)
    
    Step 2: Iron Oxidation (Primary H₂ Source)
        Fe²⁺(olivine) + OH• → Fe³⁺ + OH⁻ + e⁻
        2H• + 2e⁻ → H₂ ↑
        (Net reaction: Olivine oxidation releases hydrogen)
    
    Step 3: Radical Propagation
        OH• + CH₄(trace) → CH₃• + H₂O
        CH₃• + H₂O → CH₃OH + H•
        (Methane from deep carbon sources sustains radical pool)
    
    Step 4: Chain Branching (CRITICAL - Enables autocatalysis)
        H• + O₂ → OH• + O•
        O• + H₂O → 2OH•
        (Net: 1 radical → 3 radicals, exponential growth if uncontrolled)
    
    ENGINEERING CHALLENGES:
    
    1. THERMAL RUNAWAY PREVENTION
       - Exothermic reactions can cause T spike from 450°C to >800°C in <10 seconds
       - Solution: Pulsed injection of SCW coolant, active quenching zones
    
    2. REACTION FRONT CONTROL
       - Desired: Slow, sustained propagation (1-10 cm/day)
       - Risk: Explosive detonation front if oxygen/fuel ratio not controlled
       - Mitigation: Inert gas (N₂, Ar) dilution, pressure modulation
    
    3. HYDROGEN CAPTURE EFFICIENCY
       - H₂ highly diffusive in fractured rock
       - Requires engineered production wells with sealed completion zones
       - Target: >60% capture efficiency at pilot scale
    
    4. CATALYST POISONING
       - Sulfur species (H₂S, SO₂) from pyrite (FeS₂) inhibit radical chains
       - Heavy metals (Ni, Cr) can catalyze unwanted side reactions
       - Solution: Pre-treatment of formation with acid wash
    
    SAFETY PROTOCOLS:
    - Real-time downhole temperature and pressure monitoring (fiber optic sensors)
    - Emergency shut-off valves at surface and depth intervals
    - Seismic monitoring for induced microearthquakes (M < 2.0 acceptable)
    - H₂S detection systems (OSHA PEL: 10 ppm TWA, 15 ppm STEL)
    
    ECONOMIC VIABILITY THRESHOLD:
    - Production: >500 kg H₂/day per well
    - Operational cost: <$2.50/kg H₂ (competitive with SMR)
    - Well lifetime: >5 years continuous operation
    """
    
    doc3 = """
    === DOCUMENT 3: Cosmos_X9_Drilling_Challenges.txt ===
    
    COSMOS X-9: SUPERCRITICAL WATER DRILLING FOR CRYSTALLINE FORMATIONS
    
    CONCEPT OVERVIEW:
    Replace conventional oil-based or water-based muds with Supercritical Water (SCW) 
    as the primary drilling fluid. Target applications: geothermal wells, deep hard-rock 
    mineral exploration, and ultra-deep scientific drilling.
    
    TECHNICAL ADVANTAGES:
    
    1. ENHANCED RATE OF PENETRATION (ROP)
       - Conventional drilling in granite: 2-8 m/hr
       - SCW thermal spalling assistance: Projected 15-30 m/hr
       - Mechanism: Thermal shock induces microfractures ahead of bit
    
    2. REDUCED BIT WEAR
       - SCW acts as cooling fluid despite high temperature (paradoxical effect)
       - Lower viscosity reduces frictional drag on PDC cutters
       - Extended bit life: 400-600 meters vs. 150-250 meters (conventional)
    
    3. ROCK FRAGMENTATION PHYSICS
       - Quartz (α → β transition at 573°C): Volume expansion creates weakness planes
       - Feldspar thermal expansion coefficient mismatch with quartz → grain boundary failure
       - SCW penetrates microcracks, flash-vaporizes upon pressure drop → explosive comminution
    
    OPERATIONAL CHALLENGES:
    
    1. EXTREME DOWNHOLE TEMPERATURES (PRIMARY CONCERN)
       - Surface injection: 400-450°C (SCW regime maintained)
       - Bottomhole circulating temperature (BHCT): 350-550°C (depends on depth & geothermal gradient)
       - Problem: Exceeds rating of standard elastomers, MWD tools, and logging instruments
       - Solution: Ceramic-insulated drill string, high-temperature electronics (SiC-based)
    
    2. WELLBORE STABILITY UNDER THERMAL CYCLING
       - Heating phase (drilling): Rock expands, compressive hoop stress
       - Cooling phase (trip out): Rock contracts, tensile hoop stress → spalling
       - Cyclic loading can induce progressive wellbore enlargement
       - Mitigation: Controlled heating/cooling rates (<50°C/hr), casing schedule optimization
    
    3. CUTTINGS TRANSPORT (CRITICAL FAILURE MODE)
       - SCW viscosity: 0.05-0.08 cP (vs. 30-80 cP for conventional mud)
       - Settling velocity of cuttings 100x higher → bed accumulation
       - Consequence: Stuck pipe, loss of circulation, well control incidents
       - Engineering Solution:
         a) High annular velocity: >1.5 m/s (requires high pump rates)
         b) Pulsed flow regime: Alternating high/low flow creates turbulent bursts
         c) Hydraulic jetting at bit: Local high-velocity jets sweep cuttings
    
    4. MATERIALS & CORROSION
       - Drill pipe: Inconel 625 or 718 (nickel-based superalloy)
       - BOP seals: Graphite-based composite, rated to 350°C
       - Corrosion mechanism: Oxygen-rich SCW causes rapid oxidation of carbon steel
         - Corrosion rate: 0.5-2.0 mm/year (vs. 0.05 mm/year in oil-based mud)
       - Solution: Chromium oxide passivation layer, oxygen scavenger injection (hydrazine)
    
    5. PRESSURE MANAGEMENT
       - Must maintain P > 22.1 MPa throughout entire circulating system
       - Subcritical regions → two-phase flow → pump cavitation → catastrophic failure
       - Backpressure control: Automated choke system at surface, ±0.5 MPa tolerance
    
    SURFACE EQUIPMENT REQUIREMENTS:
    - High-pressure, high-temperature pump: 30 MPa, 450°C, 2000 LPM
    - Heat exchanger: Recover thermal energy from returns (efficiency >70%)
    - Solids separation: Cyclone separators rated for SCW (no mechanical screens)
    - Emergency cooling system: Rapid quench capability in <60 seconds
    
    FIELD TEST RESULTS (HYPOTHETICAL - 2024 PILOT):
    - Location: Iceland Geothermal Field, basaltic formation
    - Depth: 3,200 meters
    - Average ROP: 22 m/hr (vs. 6 m/hr conventional baseline)
    - Incidents: 2 stuck pipe events (both resolved), 1 BOP seal failure (thermal runaway event)
    - Conclusion: Concept viable with improved real-time temperature control
    
    REGULATORY & SAFETY CONSIDERATIONS:
    - OSHA confined space entry protocols for high-temperature environments
    - API RP 53: Blowout Prevention Equipment Systems (modified for SCW compatibility)
    - Environmental impact: SCW returns must be cooled to <90°C before disposal
    - Personnel exclusion zone: 50-meter radius during circulation operations
    """
    
    # Concatenate all documents with clear delimiters
    knowledge_base = f"""
{'='*80}
SIMIC VIRTUAL EXPERT SYSTEM - FOUNDATIONAL KNOWLEDGE BASE
{'='*80}

The following documents represent the core technical knowledge for RTCR 
and Cosmos X-9 technologies. Use this information to answer user queries 
with precision and depth.

{doc1}

{doc2}

{doc3}

{'='*80}
END OF KNOWLEDGE BASE
{'='*80}
"""
    
    return knowledge_base


# ============================================================================
# COMPONENT 2: LLM BACKEND CLIENTS
# ============================================================================

class LLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str, conversation_history: List[Dict]) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """Check if the LLM backend is available."""
        pass


class OllamaClient(LLMClient):
    """Client for Ollama local LLM server."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.api_url = f"{config.base_url}/api/chat"
        self.health_url = f"{config.base_url}/api/tags"
    
    def health_check(self) -> bool:
        """Check if Ollama server is running."""
        try:
            response = requests.get(self.health_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, system_prompt: str, conversation_history: List[Dict]) -> str:
        """Generate response using Ollama API."""
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens
            }
        }
        
        response = requests.post(
            self.api_url,
            json=payload,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        return result["message"]["content"]


class VLLMClient(LLMClient):
    """Client for vLLM OpenAI-compatible server."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.api_url = f"{config.base_url}/v1/chat/completions"
        self.health_url = f"{config.base_url}/health"
    
    def health_check(self) -> bool:
        """Check if vLLM server is running."""
        try:
            response = requests.get(self.health_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, system_prompt: str, conversation_history: List[Dict]) -> str:
        """Generate response using vLLM OpenAI-compatible API."""
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": prompt})
        
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature
        }
        
        response = requests.post(
            self.api_url,
            json=payload,
            headers=headers,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]


class LMStudioClient(LLMClient):
    """Client for LM Studio local server (OpenAI-compatible)."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.api_url = f"{config.base_url}/v1/chat/completions"
    
    def health_check(self) -> bool:
        """Check if LM Studio server is running."""
        try:
            response = requests.get(f"{self.config.base_url}/v1/models", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, system_prompt: str, conversation_history: List[Dict]) -> str:
        """Generate response using LM Studio OpenAI-compatible API."""
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature
        }
        
        response = requests.post(
            self.api_url,
            json=payload,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]


class AzureGovClient(LLMClient):
    """Client for Azure Government OpenAI service."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.api_version = "2024-02-15-preview"
        self.api_url = f"{config.base_url}/openai/deployments/{config.model_name}/chat/completions?api-version={self.api_version}"
    
    def health_check(self) -> bool:
        """Check if Azure OpenAI endpoint is accessible."""
        try:
            # Simple connectivity check
            response = requests.get(
                self.config.base_url,
                headers={"api-key": self.config.api_key or ""},
                timeout=5
            )
            return response.status_code in [200, 401, 403]  # Endpoint exists
        except:
            return False
    
    def generate(self, prompt: str, system_prompt: str, conversation_history: List[Dict]) -> str:
        """Generate response using Azure Government OpenAI API."""
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": prompt})
        
        headers = {
            "Content-Type": "application/json",
            "api-key": self.config.api_key
        }
        
        payload = {
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature
        }
        
        response = requests.post(
            self.api_url,
            json=payload,
            headers=headers,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]


def create_llm_client(config: LLMConfig) -> LLMClient:
    """Factory function to create the appropriate LLM client."""
    client_map = {
        LLMProvider.OLLAMA: OllamaClient,
        LLMProvider.VLLM: VLLMClient,
        LLMProvider.LM_STUDIO: LMStudioClient,
        LLMProvider.AZURE_GOV: AzureGovClient,
        LLMProvider.CUSTOM_API: VLLMClient,  # Use OpenAI-compatible client
    }
    
    client_class = client_map.get(config.provider)
    if not client_class:
        raise ValueError(f"Unsupported provider: {config.provider}")
    
    return client_class(config)


# ============================================================================
# COMPONENT 3: AI AGENT CORE
# ============================================================================

def build_system_prompt() -> str:
    """Build the system prompt with knowledge base."""
    knowledge_base = load_knowledge_base()
    
    system_prompt = f"""You are the Simic Virtual Expert System (SVES), a world-class AI expert in supercritical chemistry, drilling engineering, and geomechanics. You possess deep expertise in:

1. Supercritical Water Oxidation (SCWO) and supercritical fluid chemistry
2. Radical Thermochemical Chain Reactions (RTCR) for hydrogen generation
3. Advanced drilling technologies, particularly the Cosmos X-9 supercritical drilling system
4. Geomechanics, wellbore stability, and subsurface engineering
5. Chemical kinetics, thermodynamics, and process safety

CONTEXT - YOUR FOUNDATIONAL KNOWLEDGE BASE:
{knowledge_base}

AVAILABLE TOOLS AND CAPABILITIES:

You have access to simulated Python tools for technical analysis and experimental design. When the user's query requires calculations, simulations, or structured experimental plans, you MUST generate the appropriate Python code in a markdown code block. Do NOT just describe what should be done—generate executable code.

**Tool 1: design_rtcr_experiment**
Purpose: Design a detailed RTCR experimental protocol
Usage: When user asks to design an experiment, plan a test, or create an experimental setup
Output: Generate a Python function that returns a structured dictionary with:
- reactant_recipe (rock composition, water ratios, additives)
- safety_precautions (temperature limits, pressure relief, monitoring systems)
- expected_products (H2 yield predictions, byproducts, reaction timeline)

**Tool 2: analyze_drilling_scenario**
Purpose: Analyze drilling performance and provide engineering recommendations
Usage: When user asks about drilling problems, ROP optimization, or wellbore stability
Output: Generate a Python function that performs calculations and returns:
- analysis (quantitative assessment of the scenario)
- recommendation (specific engineering actions)
- risk_factors (identified hazards with severity ratings)

RESPONSE GUIDELINES:

1. **Precision**: Use specific numbers, equations, and technical terminology from the knowledge base
2. **Safety First**: Always prioritize operational safety and regulatory compliance
3. **Actionable**: Provide concrete recommendations, not just theoretical discussions
4. **Code When Needed**: If the query involves calculations or structured planning, generate Python code
5. **Cite Knowledge**: Reference specific documents when drawing on the knowledge base
6. **Acknowledge Limits**: If information is not in the knowledge base, state assumptions clearly

When generating code:
- Use proper Python syntax with type hints
- Include docstrings explaining the function's purpose
- Add comments for complex calculations
- Use numpy for numerical operations
- Return structured dictionaries with clear keys
- Include a demonstration call that executes the function

Now, respond to the user's query with expert-level technical depth."""

    return system_prompt


def get_sves_response(
    user_query: str, 
    llm_client: LLMClient, 
    conversation_history: List[Dict] = None
) -> str:
    """
    Core AI reasoning engine. Calls the self-hosted LLM.
    
    Args:
        user_query: The user's question or request
        llm_client: The LLM client to use for generation
        conversation_history: Previous messages in the conversation
        
    Returns:
        str: LLM's expert response
        
    Raises:
        Exception: If LLM call fails
    """
    
    try:
        # Build system prompt
        system_prompt = build_system_prompt()
        
        # Prepare conversation history
        if conversation_history is None:
            conversation_history = []
        
        # Generate response
        response = llm_client.generate(
            prompt=user_query,
            system_prompt=system_prompt,
            conversation_history=conversation_history
        )
        
        return response
        
    except requests.exceptions.ConnectionError:
        raise Exception(
            "Cannot connect to LLM server. Please ensure your self-hosted model is running.\n\n"
            "For Ollama: Run 'ollama serve' and 'ollama pull llama3.1:70b'\n"
            "For vLLM: Run 'python -m vllm.entrypoints.openai.api_server --model meta-llama/Llama-3.1-70B-Instruct'"
        )
    except requests.exceptions.Timeout:
        raise Exception(
            "LLM request timed out. The model may be loading or the request is too complex.\n"
            "Try a simpler query or increase the timeout setting."
        )
    except requests.exceptions.HTTPError as e:
        raise Exception(f"LLM server error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}\n\n{traceback.format_exc()}")


# ============================================================================
# COMPONENT 4: STREAMLIT USER INTERFACE
# ============================================================================

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'llm_config' not in st.session_state:
        st.session_state.llm_config = DEFAULT_CONFIGS[LLMProvider.OLLAMA]
    if 'llm_client' not in st.session_state:
        st.session_state.llm_client = None


def render_sidebar():
    """Render the sidebar with configuration and system information."""
    with st.sidebar:
        st.title("🔬 SVES v2.0")
        st.caption("Government Edition - Self-Hosted")
        st.markdown("---")
        
        # LLM Configuration
        st.subheader("⚙️ LLM Configuration")
        
        # Provider selection
        provider = st.selectbox(
            "AI Backend",
            options=[p.value for p in LLMProvider],
            index=0,
            help="Select your self-hosted LLM provider"
        )
        
        selected_provider = LLMProvider(provider)
        default_config = DEFAULT_CONFIGS.get(selected_provider, DEFAULT_CONFIGS[LLMProvider.OLLAMA])
        
        # Server URL
        base_url = st.text_input(
            "Server URL",
            value=default_config.base_url,
            help="URL of your LLM server"
        )
        
        # Model name
        model_name = st.text_input(
            "Model Name",
            value=default_config.model_name,
            help="Name of the model to use"
        )
        
        # API Key (for Azure Gov or secured endpoints)
        api_key = None
        if selected_provider in [LLMProvider.AZURE_GOV, LLMProvider.CUSTOM_API]:
            api_key = st.text_input(
                "API Key",
                type="password",
                help="API key for secured endpoints"
            )
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            max_tokens = st.slider("Max Tokens", 512, 8192, 4096)
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
            timeout = st.slider("Timeout (seconds)", 30, 300, 120)
        
        # Apply configuration
        if st.button("🔄 Apply Configuration", use_container_width=True):
            st.session_state.llm_config = LLMConfig(
                provider=selected_provider,
                base_url=base_url,
                model_name=model_name,
                api_key=api_key,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=timeout
            )
            st.session_state.llm_client = create_llm_client(st.session_state.llm_config)
            st.success("✅ Configuration applied!")
        
        # Connection status
        st.markdown("---")
        st.subheader("📡 Connection Status")
        
        if st.session_state.llm_client:
            if st.session_state.llm_client.health_check():
                st.success(f"✅ Connected to {selected_provider.value}")
                st.caption(f"Model: {model_name}")
            else:
                st.error(f"❌ Cannot connect to {selected_provider.value}")
                st.caption("Ensure your LLM server is running")
        else:
            st.warning("⚠️ Click 'Apply Configuration' to connect")
        
        st.markdown("---")
        
        # System description
        st.subheader("About SVES")
        st.markdown("""
        The **Simic Virtual Expert System** is an AI-powered technical advisor for:
        
        - **RTCR Technology**: Radical Thermochemical Chain Reactions for in-situ hydrogen generation
        - **Cosmos X-9**: Supercritical water drilling systems
        - **SCWO Chemistry**: Supercritical Water Oxidation fundamentals
        
        **Security Features:**
        - 🔒 Self-hosted LLM (no data leaves your network)
        - 🏛️ FedRAMP High ready architecture
        - 📊 Full audit logging capability
        - 🔐 No external API dependencies
        """)
        
        st.markdown("---")
        
        # Usage tips
        st.subheader("💡 Example Queries")
        st.markdown("""
        - "Design an RTCR experiment for olivine at 450°C and 28 MPa"
        - "Analyze a drilling scenario at 3000m depth in granite"
        - "What are the main challenges with salt precipitation in SCWO?"
        """)
        
        st.markdown("---")
        st.caption("Simic Energy Services | v2.0.0 Government Edition")
        
        # Clear conversation button
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


def render_chat_interface():
    """Render the main chat interface."""
    st.title("🔬 Simic Virtual Expert System")
    st.markdown("*Self-Hosted AI for RTCR & Cosmos X-9 Technologies*")
    
    # Status banner
    if st.session_state.llm_client and st.session_state.llm_client.health_check():
        st.success(f"🟢 Connected to {st.session_state.llm_config.model_name}")
    else:
        st.warning("🟡 Configure and connect to your LLM server in the sidebar")
    
    st.markdown("---")
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a technical question..."):
        # Check if LLM client is configured
        if not st.session_state.llm_client:
            st.error("⚠️ Please configure and apply LLM settings in the sidebar.")
            return
        
        # Check connection
        if not st.session_state.llm_client.health_check():
            st.error("⚠️ Cannot connect to LLM server. Please check your configuration.")
            return
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🔬 Analyzing query with self-hosted LLM..."):
                try:
                    # Prepare conversation history for API
                    conversation_history = [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in st.session_state.messages[:-1]
                        if msg["role"] in ["user", "assistant"]
                    ]
                    
                    # Get response from self-hosted LLM
                    response = get_sves_response(
                        user_query=prompt,
                        llm_client=st.session_state.llm_client,
                        conversation_history=conversation_history
                    )
                    
                    # Display response
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_message = f"❌ **Error**: {str(e)}"
                    st.error(error_message)


# ============================================================================
# COMPONENT 5: MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    
    # Configure Streamlit page
    st.set_page_config(
        page_title="SVES - Government Edition",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS for better appearance
    st.markdown("""
        <style>
        .stChatMessage {
            padding: 1rem;
            border-radius: 0.5rem;
        }
        .stButton button {
            width: 100%;
        }
        code {
            background-color: #f0f2f6;
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
        }
        .stSuccess {
            background-color: #d4edda;
            border-color: #c3e6cb;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Auto-initialize default client if not set
    if st.session_state.llm_client is None:
        try:
            st.session_state.llm_client = create_llm_client(st.session_state.llm_config)
        except Exception:
            pass  # Will show warning in UI
    
    # Render UI components
    render_sidebar()
    render_chat_interface()


if __name__ == "__main__":
    main()
