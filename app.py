"""
SIMIC VIRTUAL EXPERT SYSTEM (SVES) - PROTOTYPE
==============================================

A web-based AI expert system for RTCR and Cosmos X-9 supercritical drilling technologies.

INSTALLATION:
------------
pip install streamlit anthropic numpy

USAGE:
------
streamlit run app.py

Then enter your Anthropic API key in the sidebar and start asking questions.

AUTHOR: Simic Energy Services
VERSION: 1.0.0 (Phase I Prototype)
"""

import streamlit as st
import anthropic
import json
import traceback
from typing import Dict, List, Optional


# ============================================================================
# COMPONENT 1: MOCK KNOWLEDGE BASE
# ============================================================================

def load_knowledge_base() -> str:
    """
    Simulates a RAG system by loading foundational documents directly into context.
    In production, this would query a vector database (Pinecone, Weaviate, etc.).
    
    Returns:
        str: Concatenated knowledge base content for Claude's context window.
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
# COMPONENT 2: AI AGENT CORE
# ============================================================================

def get_sves_response(user_query: str, api_key: str, conversation_history: List[Dict] = None) -> str:
    """
    Core AI reasoning engine. Constructs the "Golden Prompt" and calls Claude API.
    
    Args:
        user_query: The user's question or request
        api_key: Anthropic API key
        conversation_history: Previous messages in the conversation
        
    Returns:
        str: Claude's expert response
        
    Raises:
        Exception: If API call fails or key is invalid
    """
    
    try:
        # Initialize Anthropic client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Load knowledge base
        knowledge_base = load_knowledge_base()
        
        # Construct the "Golden Prompt" system message
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

Example code structure:
```python
def design_rtcr_experiment(rock_type: str, target_temp: float, target_pressure: float) -> dict:
    \"\"\"Design RTCR experiment for specified conditions.\"\"\"
    import numpy as np
    import json
    
    # Your experimental design logic here
    # Calculate reactant ratios, safety margins, expected yields
    
    return {{
        'reactant_recipe': {{'component1': 'value1', 'component2': 'value2'}},
        'safety_precautions': {{'precaution1': 'description1'}},
        'expected_products': {{'product1': 'amount1'}}
    }}

# Execute the design
result = design_rtcr_experiment("olivine", 450.0, 28.0)
print(json.dumps(result, indent=2))
```

**Tool 2: analyze_drilling_scenario**
Purpose: Analyze drilling performance and provide engineering recommendations
Usage: When user asks about drilling problems, ROP optimization, or wellbore stability
Output: Generate a Python function that performs calculations and returns:
- analysis (quantitative assessment of the scenario)
- recommendation (specific engineering actions)
- risk_factors (identified hazards with severity ratings)

Example code structure:
```python
def analyze_drilling_scenario(depth: float, rock_type: str, rop: float, mud_temp: float) -> dict:
    \"\"\"Analyze drilling scenario and provide recommendations.\"\"\"
    import numpy as np
    import json
    
    # Your analysis logic here
    # Calculate thermal stress, cuttings transport efficiency, etc.
    
    return {{
        'analysis': {{'metric1': 'value1', 'metric2': 'value2'}},
        'recommendation': {{'action1': 'description1'}},
        'risk_factors': {{'risk1': 'severity1'}}
    }}

# Execute the analysis
result = analyze_drilling_scenario(3000.0, "granite", 12.0, 425.0)
print(json.dumps(result, indent=2))
```

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

        # Build message history
        if conversation_history is None:
            conversation_history = []
        
        # Add current user query
        messages = conversation_history + [
            {
                "role": "user",
                "content": user_query
            }
        ]
        
        # Call Claude API with extended context window
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            temperature=0.7,
            system=system_prompt,
            messages=messages
        )
        
        # Extract response text
        response_text = response.content[0].text
        
        return response_text
        
    except anthropic.AuthenticationError:
        raise Exception("Invalid API key. Please check your Anthropic API key and try again.")
    except anthropic.RateLimitError:
        raise Exception("Rate limit exceeded. Please wait a moment and try again.")
    except anthropic.APIConnectionError:
        raise Exception("Network error. Please check your internet connection.")
    except Exception as e:
        raise Exception(f"Error calling Claude API: {str(e)}\n\n{traceback.format_exc()}")


# ============================================================================
# COMPONENT 3: STREAMLIT USER INTERFACE
# ============================================================================

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""


def render_sidebar():
    """Render the sidebar with API key input and system information."""
    with st.sidebar:
        st.title("🔬 SVES Prototype")
        st.markdown("---")
        
        # API Key input
        st.subheader("Configuration")
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            value=st.session_state.api_key,
            help="Enter your Anthropic API key to enable AI responses"
        )
        st.session_state.api_key = api_key
        
        st.markdown("---")
        
        # System description
        st.subheader("About SVES")
        st.markdown("""
        The **Simic Virtual Expert System** is an AI-powered technical advisor for:
        
        - **RTCR Technology**: Radical Thermochemical Chain Reactions for in-situ hydrogen generation
        - **Cosmos X-9**: Supercritical water drilling systems
        - **SCWO Chemistry**: Supercritical Water Oxidation fundamentals
        
        **Capabilities:**
        - Answer technical questions with expert-level depth
        - Design experimental protocols
        - Analyze drilling scenarios
        - Perform engineering calculations
        - Generate safety assessments
        """)
        
        st.markdown("---")
        
        # Usage tips
        st.subheader("💡 Example Queries")
        st.markdown("""
        - "Design an RTCR experiment for olivine at 450°C and 28 MPa"
        - "Analyze a drilling scenario at 3000m depth in granite with ROP of 12 m/hr"
        - "What are the main challenges with salt precipitation in SCWO?"
        - "Calculate the thermal stress in a wellbore during Cosmos X-9 operations"
        """)
        
        st.markdown("---")
        st.caption("Simic Energy Services | Phase I Prototype v1.0.0")
        
        # Clear conversation button
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


def render_chat_interface():
    """Render the main chat interface."""
    st.title("Simic Virtual Expert System")
    st.markdown("*AI-Powered Technical Advisory for RTCR & Cosmos X-9 Technologies*")
    st.markdown("---")
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a technical question..."):
        # Check if API key is provided
        if not st.session_state.api_key:
            st.error("⚠️ Please enter your Anthropic API key in the sidebar to continue.")
            return
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🔬 Analyzing query and consulting knowledge base..."):
                try:
                    # Prepare conversation history for API (exclude system messages)
                    conversation_history = [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in st.session_state.messages[:-1]  # Exclude the current user message
                        if msg["role"] in ["user", "assistant"]
                    ]
                    
                    # Get response from AI agent
                    response = get_sves_response(
                        user_query=prompt,
                        api_key=st.session_state.api_key,
                        conversation_history=conversation_history
                    )
                    
                    # Display response
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_message = f"❌ **Error**: {str(e)}"
                    st.error(error_message)
                    # Don't add error to message history


# ============================================================================
# COMPONENT 4: MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    
    # Configure Streamlit page
    st.set_page_config(
        page_title="SVES - Simic Virtual Expert System",
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
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Render UI components
    render_sidebar()
    render_chat_interface()


if __name__ == "__main__":
    main()
