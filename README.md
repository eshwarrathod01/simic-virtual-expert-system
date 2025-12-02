# Simic Virtual Expert System (SVES)

<div align="center">

🔬 **AI-Powered Technical Advisory for Advanced Energy Technologies**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Claude AI](https://img.shields.io/badge/Claude-Sonnet%204-purple.svg)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-Proprietary-green.svg)](#license)
[![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)](#changelog)

**[Live Demo](#installation) • [Documentation](#documentation) • [Multi-Agent Report](SVES_MULTI_AGENT_DEMONSTRATION.md) • [API Reference](#api-reference)**

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [What's New in v2.0](#-whats-new-in-v20)
- [Features](#-features)
- [Multi-Agent Architecture](#-multi-agent-architecture-v20)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Knowledge Domains](#-knowledge-domains)
- [Documentation](#-documentation)
- [Project Structure](#-project-structure)
- [Changelog](#-changelog)
- [Security](#-security--api-keys)
- [Contributing](#-contributing)
- [License](#-license)

---

## Overview

The **Simic Virtual Expert System (SVES)** is a sophisticated AI-powered platform designed for high-stakes technical decision-making in advanced energy technologies. Originally developed as a Phase I government proposal deliverable, SVES has evolved into a comprehensive **multi-agent laboratory simulator** capable of reasoning across complex domains:

| Domain | Description | Key Applications |
|--------|-------------|------------------|
| **RTCR** | Radical Thermochemical Chain Reactions | In-situ hydrogen generation from ultramafic rocks |
| **Cosmos X-9** | Supercritical Water Drilling | Enhanced ROP in crystalline formations |
| **SCWO** | Supercritical Water Oxidation | Waste treatment and resource recovery |

---

## 🆕 What's New in v2.0

### Multi-Agent Orchestration System

SVES v2.0 introduces a revolutionary **multi-agent architecture** where specialized AI agents collaborate to solve complex engineering problems:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SVES ORCHESTRATION LAYER                      │
│         (Task Decomposition, Dispatch, Synthesis)                │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   DRILLING    │    │     RTCR      │    │   MATERIALS   │
│     AGENT     │    │     AGENT     │    │     AGENT     │
│               │    │               │    │               │
│ • FLAC3D      │    │ • Cantera     │    │ • JMatPro     │
│ • OpenFOAM    │    │ • ODE Solvers │    │ • OLI Systems │
│ • Stress Mdls │    │ • Kinetics    │    │ • Corrosion DB│
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌───────────────┐
                    │    SAFETY     │
                    │     AGENT     │
                    │               │
                    │ • PRA Models  │
                    │ • Fault Trees │
                    │ • Risk Engine │
                    └───────────────┘
```

### Key Improvements

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Agent Architecture | Single AI | Multi-Agent (4 specialists) |
| Conflict Resolution | Manual | Automated inter-agent negotiation |
| Risk Assessment | Basic | Probabilistic Risk Analysis (PRA) |
| Simulation Tools | Code generation | Integrated FLAC3D, Cantera, JMatPro |
| Report Format | Text responses | Structured engineering reports |
| Safety Validation | Advisory | Mandatory agent approval |

---

## 🚀 Features

### Core Capabilities

- **🤖 Expert-Level AI Reasoning**: Powered by Anthropic's Claude Sonnet 4 with 200K token context
- **🔄 Multi-Agent Collaboration**: 4 specialized agents with conflict resolution
- **🌐 Interactive Web Interface**: Professional Streamlit-based UI
- **📊 Automated Experimental Design**: Generate complete RTCR protocols with safety assessments
- **⚙️ Drilling Scenario Analysis**: Real-time engineering calculations and risk ratings
- **📚 RAG-Simulated Knowledge Base**: 3 comprehensive technical documents

### Agent Capabilities

| Agent | Expertise | Simulation Tools |
|-------|-----------|------------------|
| **Drilling & Geomechanics** | HPHT drilling, rock mechanics, wellbore stability | FLAC3D, OpenFOAM, custom stress models |
| **RTCR Chemistry** | Supercritical water chemistry, radical kinetics, H₂ yield | Cantera, custom ODE solvers |
| **Materials & Corrosion** | High-temp metallurgy, alloy degradation | JMatPro, OLI Systems, corrosion databases |
| **Safety** | Risk assessment, fault-tree analysis | PRA models, rule-based engines |

---

## 🏗️ Multi-Agent Architecture (v2.0)

### How It Works

1. **Task Decomposition**: The Orchestrator breaks complex queries into specialized sub-tasks
2. **Agent Dispatch**: Sub-tasks are assigned to domain expert agents
3. **Parallel Analysis**: Agents run simulations and generate technical reports
4. **Conflict Detection**: Orchestrator identifies incompatibilities between agent recommendations
5. **Iterative Resolution**: Agents collaborate to find safe, effective solutions
6. **Synthesis**: Final plan integrates all agent insights with safety validation

### Example Workflow

```
User Query: "Design RTCR stimulation for granite at 4,500m depth"
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR: Decomposing into 4 sub-tasks...                   │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
┌───────────────────────┐                 ┌───────────────────────┐
│ DRILLING AGENT        │                 │ RTCR AGENT            │
│ ─────────────────────│                 │ ─────────────────────│
│ T: 165°C, P: 67 MPa  │                 │ Peak T: 720°C        │
│ Stress: σH=145 MPa   │                 │ H₂ Yield: 42 m³/ton  │
│ Risk: Shear failure  │                 │ Duration: 45 min     │
└───────────────────────┘                 └───────────────────────┘
        │                                           │
        └─────────────────────┬─────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ ⚠️ CONFLICT DETECTED: 720°C exceeds P-110 casing limit (538°C)  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ ITERATIVE RESOLUTION:                                           │
│ • RTCR Agent: Reduce reaction intensity → Peak T: 480°C         │
│ • Materials Agent: Recommend Inconel 825 liner                  │
│ • Safety Agent: Approve revised plan (Risk Score: 4/10)         │
└─────────────────────────────────────────────────────────────────┘
```

📄 **See full demonstration**: [SVES_MULTI_AGENT_DEMONSTRATION.md](SVES_MULTI_AGENT_DEMONSTRATION.md)

---

## 📋 Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend/UI** | Python 3.8+ with Streamlit | Web application framework |
| **AI Engine** | Anthropic Claude Sonnet 4 | Expert reasoning and code generation |
| **Scientific Computing** | NumPy | Numerical calculations |
| **Knowledge Base** | Context-injected documents | Domain expertise (200K tokens) |
| **Version Control** | Git/GitHub | Source code management |

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Quick Start

```bash
# Clone the repository
git clone https://github.com/eshwarrathod01/simic-virtual-expert-system.git
cd simic-virtual-expert-system

# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install streamlit anthropic numpy

# Run the application
streamlit run app.py
```

The app will automatically open at `http://localhost:8501`. Enter your Anthropic API key in the sidebar and start asking technical questions!

---

## 💡 Usage Examples

### Basic Queries

```
"Design an RTCR experiment for olivine at 450°C and 28 MPa"
"Analyze a drilling scenario at 3000m depth in granite with ROP of 12 m/hr"
"What are the main challenges with salt precipitation in SCWO?"
```

### Advanced Multi-Agent Queries (v2.0)

```
"Design a safe and effective RTCR stimulation plan for a granite reservoir 
at 4,500 meters depth. The primary goal is to maximize hydrogen yield while 
ensuring the integrity of a standard P-110 steel production casing."
```

This complex query triggers the full multi-agent workflow:
1. Drilling Agent assesses downhole conditions
2. RTCR Agent designs the chemical reaction
3. Materials Agent evaluates casing compatibility
4. Safety Agent validates the final plan

---

## 📚 Knowledge Domains

### RTCR (Radical Thermochemical Chain Reactions)

| Parameter | Value | Description |
|-----------|-------|-------------|
| Operating Temperature | >400°C | Supercritical regime |
| Operating Pressure | >25 MPa | Above critical point |
| Primary Reactant | Olivine (Mg,Fe)₂SiO₄ | Iron-bearing ultramafic rock |
| H₂ Production Target | >500 kg/day | Economic viability threshold |
| Cost Target | <$2.50/kg H₂ | Competitive with SMR |

**Key Reactions:**
```
Step 1: H₂O → OH• + H•                    (Initiation)
Step 2: Fe²⁺ + OH• → Fe³⁺ + OH⁻ + e⁻     (Iron Oxidation)
Step 3: 2H• + 2e⁻ → H₂ ↑                  (Hydrogen Production)
Step 4: H• + O₂ → OH• + O•                (Chain Branching)
```

### Cosmos X-9 Supercritical Drilling

| Parameter | Conventional | Cosmos X-9 |
|-----------|--------------|------------|
| ROP in Granite | 2-8 m/hr | 15-30 m/hr |
| Bit Life | 150-250 m | 400-600 m |
| Mud Viscosity | 30-80 cP | 0.05-0.08 cP |
| Operating Temp | <150°C | 400-550°C |

### SCWO (Supercritical Water Oxidation)

| Critical Parameter | Value |
|-------------------|-------|
| Critical Temperature | 647.1 K (373.95°C) |
| Critical Pressure | 22.064 MPa (3,200 psi) |
| Ion Product (Kw) | 10⁻²⁰ (vs 10⁻¹⁴ normal) |
| Destruction Efficiency | >99.99% |
| Residence Time | 30-120 seconds |

---

## 📁 Project Structure

```
simic-virtual-expert-system/
│
├── app.py                              # Main Streamlit application (550+ lines)
│   ├── load_knowledge_base()           # RAG-simulated knowledge system
│   ├── get_sves_response()             # AI Agent Core with Golden Prompt
│   ├── render_sidebar()                # Configuration UI
│   └── render_chat_interface()         # Chat UI with history
│
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore patterns
│
├── README.md                           # This documentation
├── PROJECT_DOCUMENTATION.md            # Complete technical specification
├── PROFESSIONAL_EMAIL.txt              # Shareable project summary
└── SVES_MULTI_AGENT_DEMONSTRATION.md   # v2.0 Multi-agent report (650+ lines)
```

---

## 📄 Documentation

| Document | Description | Lines |
|----------|-------------|-------|
| [README.md](README.md) | Project overview and setup guide | 300+ |
| [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) | Complete technical specification | 400+ |
| [SVES_MULTI_AGENT_DEMONSTRATION.md](SVES_MULTI_AGENT_DEMONSTRATION.md) | Multi-agent orchestration report | 650+ |
| [PROFESSIONAL_EMAIL.txt](PROFESSIONAL_EMAIL.txt) | Shareable project summary | 150+ |

---

## 📋 Changelog

### Version 2.0.0 (December 2025)

**🆕 New Features:**
- Multi-Agent Orchestration System with 4 specialized agents
- Conflict detection and resolution between agents
- Probabilistic Risk Assessment (PRA) integration
- Structured engineering report generation
- Iterative solution refinement workflow

**📊 New Agents:**
- Drilling & Geomechanics Agent (FLAC3D, OpenFOAM)
- RTCR Chemistry Agent (Cantera, ODE solvers)
- Materials & Corrosion Agent (JMatPro, OLI Systems)
- Safety Agent (PRA models, fault-tree analysis)

**📄 New Documentation:**
- `SVES_MULTI_AGENT_DEMONSTRATION.md` - Complete orchestration example
- Updated README with architecture diagrams
- Enhanced technical specifications

### Version 1.0.0 (November 2025)

**Initial Release:**
- Single-agent AI expert system
- Streamlit web interface
- 3-document knowledge base (SCWO, RTCR, Cosmos X-9)
- Code generation tools
- Golden Prompt architecture
- GitHub integration

---

## 🔒 Security & API Keys

⚠️ **Important**: Never commit your API key to version control!

| Security Feature | Implementation |
|-----------------|----------------|
| API Key Storage | Session-only (not persisted) |
| Key Input | Password-masked field |
| Git Protection | `.gitignore` excludes sensitive files |
| Production Recommendation | Environment variables or secret managers |

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Update documentation for new features
- Test with multiple query types before submitting

---

## 📞 Support & Contact

**Developer:** Eshwar Rathod  
**GitHub:** [@eshwarrathod01](https://github.com/eshwarrathod01)  
**Repository:** [simic-virtual-expert-system](https://github.com/eshwarrathod01/simic-virtual-expert-system)

For technical support:
- 📖 Review example queries in the sidebar
- 🔑 Verify API key is correctly entered
- 📦 Ensure all dependencies are installed
- 🌐 Check internet connectivity for API calls
- 🐛 Open an issue on GitHub for bugs

---

## 📄 License

Copyright © 2025 Simic Energy Services. All rights reserved.

This prototype is provided for demonstration and evaluation purposes.

---

<div align="center">

**Built with ❤️ for the future of clean energy**

🔬 RTCR • ⚡ Cosmos X-9 • 💧 SCWO

[![GitHub stars](https://img.shields.io/github/stars/eshwarrathod01/simic-virtual-expert-system?style=social)](https://github.com/eshwarrathod01/simic-virtual-expert-system)

</div>**Built with** ❤️ **for the future of clean energy**
