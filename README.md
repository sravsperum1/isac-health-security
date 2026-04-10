\# 🏥 Multi-Agent ISAC Health Security System



A multi-agent AI system that analyses real wearable sensor data (10,299 rows) to detect security threats in Integrated Sensing and Communications (ISAC) healthcare applications — with a built-in chat interface to ask follow-up questions about the security analysis.



\*\*GitHub Repository:\*\* https://github.com/sravsperum1/isac-health-security



\---



\## 📌 Project Overview



This project was built as a capstone for a Generative AI course, demonstrating how multiple specialised AI agents can work together in a sequential pipeline to solve a real-world data science problem in healthcare security.



The system ingests real UCI HAR dataset (accelerometer + gyroscope readings from 30 human subjects), runs it through four specialised agents, produces a structured JSON security report with data visualisations, and exposes everything through a Streamlit web app where users can chat with the agents about the findings.



\---



\## 🏗️ Architecture

┌─────────────────────────────────────────────────────────────────────────────┐

│                              INPUT LAYER                                    │

│                                                                             │

│                    UCI HAR Dataset (10,299 rows)                           │

│              Accelerometer + Gyroscope readings from 30 subjects           │

│                    Activities: Walking, Sitting, Standing                  │

└─────────────────────────────────────────────────────────────────────────────┘

&#x20;                                     │

&#x20;                                     ▼

┌─────────────────────────────────────────────────────────────────────────────┐

│                         AGENT 1: SensorDataAnalyzer                        │

│                                                                             │

│  • Noise detection and filtering                                           │

│  • Signal quality assessment (SNR, RSSI)                                   │

│  • Outlier detection in sensor readings                                    │

│  • Data completeness verification                                          │

│  • Anomaly flagging (spikes, flatlines, irregular patterns)                │

│                                                                             │

│  OUTPUT: Sensor health report with anomaly percentages                     │

└─────────────────────────────────────────────────────────────────────────────┘

&#x20;                                     │

&#x20;                                     ▼

┌─────────────────────────────────────────────────────────────────────────────┐

│                       AGENT 2: SecurityThreatDetector                      │

│                                                                             │

│  • Attack type identification (spoofing, jamming, tampering)               │

│  • Quantitative threat scoring (0-100 scale)                               │

│  • Risk level classification (CRITICAL/HIGH/MEDIUM/LOW)                    │

│  • 🔧 FUNCTION CALLING TOOLS:                                              │

│    - detect\_signal\_anomaly(snr, rssi, protocol)                            │

│    - calculate\_threat\_score(threat, encryption, attack\_success)            │

│                                                                             │

│  OUTPUT: Threat scores and risk levels for each attack type                │

└─────────────────────────────────────────────────────────────────────────────┘

&#x20;                                     │

&#x20;                                     ▼

┌─────────────────────────────────────────────────────────────────────────────┐

│                         AGENT 3: ISACRiskAssessor                          │

│                                                                             │

│  • Cross-domain vulnerability fusion                                        │

│  • Attack propagation path analysis                                         │

│  • System vulnerability mapping                                             │

│  • Cascading risk identification                                            │

│  • Critical intersection point detection                                    │

│                                                                             │

│  OUTPUT: Integrated risk assessment (sensing + communication)              │

└─────────────────────────────────────────────────────────────────────────────┘

&#x20;                                     │

&#x20;                                     ▼

┌─────────────────────────────────────────────────────────────────────────────┐

│                        AGENT 4: SecurityReportWriter                       │

│                                                                             │

│  • Executive summary generation                                             │

│  • Risk prioritization (P0/P1/P2)                                           │

│  • Actionable recommendation formulation                                    │

│  • JSON structured report export                                            │

│  • Text report generation                                                   │

│                                                                             │

│  OUTPUT: Final security report + downloadable JSON + TXT                   │

└─────────────────────────────────────────────────────────────────────────────┘

&#x20;                                     │

&#x20;                                     ▼

┌─────────────────────────────────────────────────────────────────────────────┐

│                              OUTPUT LAYER                                   │

│                                                                             │

│  📊 Visualizations    📄 JSON Report    📝 Text Report    💾 CSV Export     │

│                                                                             │

│  • Figure 1: Activity Distribution    • Executive Summary                   │

│  • Figure 2: Threat Distribution      • Key Findings                        │

│  • Figure 3: SNR by Threat Type       • P0/P1/P2 Recommendations           │

│  • Figure 4: Protocol Usage           • Conclusion                          │

│                                                                             │

│  🖥️ Streamlit UI (6 Tabs)                                                   │

│  • Dataset • Multi-Agent • Function Calling • Visuals • Report • Q\&A       │

└─────────────────────────────────────────────────────────────────────────────┘

\---

\## Sequential Pipeline Flow (Output Chaining)

┌─────────────────────────────────────────────────────────────────────────────┐

│                                                                             │

│   INPUT ───▶ AGENT 1 ───▶ AGENT 2 ───▶ AGENT 3 ───▶ AGENT 4 ───▶ OUTPUT   │

│                │            │            │            │                     │

│                ▼            ▼            ▼            ▼                     │

│            Output 1 ──▶ Input 2    Output 2 ──▶ Input 3    Output 3 ──▶ Input 4

│                                                                             │

│   Each agent's output becomes the next agent's input                        │

│                                                                             │

└─────────────────────────────────────────────────────────────────────────────┘

\---



\---



\## 🤖 The 4 Agents



┌─────────────────┬──────────────────────────────────────────────────────────┐

│     AGENT       │                      DESCRIPTION                         │

├─────────────────┼──────────────────────────────────────────────────────────┤

│ SensorData      │ Analyzes accelerometer and gyroscope patterns            │

│ Analyzer        │ Detects anomalies, noise, and signal quality issues      │

│                 │ Focus: SENSING domain only                               │

├─────────────────┼──────────────────────────────────────────────────────────┤

│ Security        │ Identifies spoofing, jamming, tampering attacks          │

│ Threat          │ Uses FUNCTION CALLING tools for scoring                  │

│ Detector        │ Focus: COMMUNICATION security domain                     │

├─────────────────┼──────────────────────────────────────────────────────────┤

│ ISAC Risk       │ Integrates sensing + communication analysis              │

│ Assessor        │ Identifies cross-domain vulnerabilities                  │

│                 │ Focus: INTEGRATION risks (the "I" in ISAC)               │

├─────────────────┼──────────────────────────────────────────────────────────┤

│ Security        │ Generates executive summary and recommendations          │

│ Report Writer   │ Exports JSON and text reports                            │

│                 │ Focus: ACTIONABLE OUTPUT for stakeholders                │

└─────────────────┴──────────────────────────────────────────────────────────┘



All agents inherit from a shared base `Agent` class that handles OpenAI function calling, tool dispatch, error handling, and `max\_iterations` safety guard.



\---



\## 🔧 Custom Tools (Function Calling)



┌─────────────────────────────────────────────────────────────────────────────┐

│                           TOOL 1: detect\_signal\_anomaly                    │

├─────────────────────────────────────────────────────────────────────────────┤

│  PURPOSE: Detect jamming, interference, and signal degradation             │

│                                                                             │

│  INPUT:                                                                     │

│    • snr\_db (float): Signal-to-noise ratio in dB                           │

│    • rssi\_dbm (float): Received signal strength in dBm                     │

│    • protocol (string): 5G-NR, 5G-mmWave, WiFi-6, LoRaWAN, NB-IoT          │

│                                                                             │

│  OUTPUT:                                                                    │

│    • is\_anomaly (bool): True/False                                          │

│    • anomaly\_type (string): JAMMING\_DETECTED, WEAK\_SIGNAL\_INTERFERENCE     │

│    • risk\_score (int): 0-100                                                │

│    • risk\_level (string): HIGH/MEDIUM/LOW                                   │

│    • recommendation (string): Actionable advice                            │

└─────────────────────────────────────────────────────────────────────────────┘



┌─────────────────────────────────────────────────────────────────────────────┐

│                         TOOL 2: calculate\_threat\_score                     │

├─────────────────────────────────────────────────────────────────────────────┤

│  PURPOSE: Calculate overall security threat score                          │

│                                                                             │

│  INPUT:                                                                     │

│    • threat\_type (string): Spoofing, Jamming, Tampering, Eavesdropping     │

│    • encryption (string): AES-256-GCM, ChaCha20-Poly1305, None             │

│    • attack\_success (bool): True/False                                      │

│                                                                             │

│  OUTPUT:                                                                    │

│    • threat\_score (int): 0-100                                              │

│    • risk\_level (string): CRITICAL/HIGH/MEDIUM/LOW                          │

│    • recommended\_action (string): What to do                                │

│    • requires\_immediate\_action (bool): True/False                           │

└─────────────────────────────────────────────────────────────────────────────┘



```

\## Streamlit UI Tabs (6 Tabs)



┌─────────────────────────────────────────────────────────────────────────────┐

│                                                                             │

│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐

│  │  Tab 1   │ │  Tab 2   │ │  Tab 3   │ │  Tab 4   │ │  Tab 5   │ │  Tab 6   │

│  │ Dataset  │ │  Agents  │ │  Tools   │ │   Viz    │ │  Report  │ │   Q\&A    │

│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘

│       │           │           │           │           │           │

│       ▼           ▼           ▼           ▼           ▼           ▼

│  Load 10,299  Run 4       Test 2      Generate    View JSON   Ask questions

│  rows        agents       tools       4 charts    report      to agents

│                                                                             │

└─────────────────────────────────────────────────────────────────────────────┘

\---



\## Safety Features (max\_iterations Guard)

┌─────────────────────────────────────────────────────────────────────────────┐

│                                                                             │

│   Agent.run() with max\_iterations=3                                        │

│                                                                             │

│   ┌─────────────────────────────────────────────────────────────────────┐   │

│   │  Iteration 1 ──▶ Try API call ──▶ Success? ──▶ Return output        │   │

│   │       │                                                              │   │

│   │       ▼ (if fails)                                                   │   │

│   │  Wait 2 seconds (exponential backoff)                                │   │

│   │       │                                                              │   │

│   │       ▼                                                              │   │

│   │  Iteration 2 ──▶ Try API call ──▶ Success? ──▶ Return output        │   │

│   │       │                                                              │   │

│   │       ▼ (if fails)                                                   │   │

│   │  Wait 4 seconds                                                      │   │

│   │       │                                                              │   │

│   │       ▼                                                              │   │

│   │  Iteration 3 ──▶ Try API call ──▶ Success? ──▶ Return output        │   │

│   │       │                                                              │   │

│   │       ▼ (if fails)                                                   │   │

│   │  Return error: "Max iterations exceeded"                             │   │

│   └─────────────────────────────────────────────────────────────────────┘   │

│                                                                             │

│   Prevents infinite loops and handles API failures gracefully              │

│                                                                             │

└─────────────────────────────────────────────────────────────────────────────┘

\## 📊 Dataset



| Property | Value |

|----------|-------|

| \*\*Source\*\* | UCI HAR Dataset / Kaggle |

| \*\*Kaggle Link\*\* | https://www.kaggle.com/datasets/uciml/human-activity-recognition-with-smartphones |

| \*\*Total Rows\*\* | 10,299 |

| \*\*Subjects\*\* | 30 human participants (ages 19-48) |

| \*\*Sensors\*\* | Accelerometer (3-axis), Gyroscope (3-axis) |

| \*\*Activities\*\* | Walking, Walking Upstairs, Walking Downstairs, Sitting, Standing, Laying |



\### Why this dataset for ISAC?



| Component | How Dataset Provides It |

|-----------|------------------------|

| \*\*Sensing\*\* | Real accelerometer + gyroscope readings from 30 human subjects |

| \*\*Communication\*\* | Added 5G/WiFi protocol labels (5G-NR, 5G-mmWave, WiFi-6, LoRaWAN, NB-IoT) |

| \*\*Security\*\* | Added threat labels (Spoofing, Jamming, Tampering, Eavesdropping) |

| \*\*Health Monitoring\*\* | Activity recognition directly relevant to healthcare |



\---



\## 🖥️ Streamlit App (6 Tabs)



| Tab | What it does |

|-----|--------------|

| \*\*1. Real Dataset\*\* | Load and explore UCI HAR dataset (10,299 rows) |

| \*\*2. Multi-Agent System\*\* | Run 4 agents sequentially with progress tracking |

| \*\*3. Function Calling\*\* | Test the 2 security tools manually |

| \*\*4. Visualizations\*\* | Generate 4 security charts |

| \*\*5. Security Report\*\* | View/download final security assessment |

| \*\*6. Ask the Agents\*\* | Q\&A chat interface to ask questions about analysis |



\---



\## 📈 Results \& Key Findings



\### Quantitative Results



| Metric | Value |

|--------|-------|

| Attack Success Rate | \~30% |

| Average SNR | \~11.6 dB |

| Threat Rate | \~25% |

| Pipeline Time | \~30-40 seconds |

| Total Tokens | \~4,000 |



\### Key Findings by Domain



| Domain | Top Issues |

|--------|------------|

| \*\*Sensing\*\* | Sensor Spoofing, Physical Tampering, Low SNR/RSSI |

| \*\*Communication\*\* | NB-IoT Vulnerabilities, Jamming Attacks, Off-Hours Weaknesses |

| \*\*ISAC Integration\*\* | Cross-Domain Vulnerabilities, Cascading Attack Vectors |



\### Recommendations



| Priority | Timeframe | Actions |

|----------|-----------|---------|

| \*\*P0\*\* | 24 hours | Deploy emergency monitoring, patch NB-IoT, secure physical sensors |

| \*\*P1\*\* | 1 week | Enhance sensing algorithms, deploy cross-domain detection, off-hours audits |

| \*\*P2\*\* | 1 month | Implement hardened protocols, strengthen ISAC framework, risk assessments |



\---



\## 📊 Visualizations Generated



| Figure | Description | Key Insight |

|--------|-------------|-------------|

| \*\*Figure 1\*\* | Activity Distribution | Walking (26%), Sitting (15%), Standing (15%) |

| \*\*Figure 2\*\* | Threat Distribution | Normal (75%), Spoofing (8%), Tampering (7%) |

| \*\*Figure 3\*\* | SNR by Threat Type | Jamming reduces SNR to -4.9 dB (vs normal 12.8 dB) |

| \*\*Figure 4\*\* | Protocol Usage | 5G-NR (21%), 5G-mmWave (20%), WiFi-6 (20%) |



\---



\## 🛡️ Safety Features



| Feature | Implementation | Why |

|---------|----------------|-----|

| \*\*max\_iterations=3\*\* | Each agent retries up to 3 times | Prevents infinite loops |

| \*\*Exponential Backoff\*\* | Wait 1s, 2s, 4s between retries | Handles API rate limits |

| \*\*Try/Except Blocks\*\* | Graceful error handling | App doesn't crash on errors |

| \*\*Token Tracking\*\* | Monitors API usage | Cost control |

| \*\*.gitignore\*\* | Excludes .env, .venv | Protects API keys |



\---



\## ✅ Requirements Checklist



| Requirement | Status | Evidence |

|-------------|--------|----------|

| Real dataset (500+ rows) | ✅ | 10,299 rows - UCI HAR Dataset |

| 3+ specialized agents | ✅ | 4 agents with unique system prompts |

| Multi-agent pattern | ✅ | Sequential pipeline (output chaining) |

| Azure OpenAI | ✅ | AzureOpenAI client with GPT-4o |

| Function calling (2+ tools) | ✅ | detect\_signal\_anomaly, calculate\_threat\_score |

| Structured output + viz | ✅ | JSON report + 4 matplotlib/seaborn charts |

| Safety guardrails | ✅ | max\_iterations=3, exponential backoff |

| Streamlit UI (Bonus) | ✅ | Full web interface with 6 tabs |



\---



\## 🚀 How to Run



\### Prerequisites

\- Python 3.11 or higher

\- Azure OpenAI account with GPT-4o deployment



\### Step 1: Clone Repository

```bash

git clone https://github.com/sravsperum1/isac-health-security.git

cd isac-health-security

```



\### Step 2: Download Dataset

Download from Kaggle: https://www.kaggle.com/datasets/uciml/human-activity-recognition-with-smartphones

Place `train.csv` and `test.csv` in the `data/` folder.



\### Step 3: Create Virtual Environment

```bash

python -m venv .venv

.venv\\Scripts\\activate  # Windows

source .venv/bin/activate  # Mac/Linux

```



\### Step 4: Install Dependencies

```bash

pip install -r requirements.txt

```



\### Step 5: Configure Azure OpenAI

```bash

cp .env.example .env

\# Edit .env with your Azure credentials

```



\### Step 6: Run the App

```bash

streamlit run app/app.py

```



\### Step 7: Open Browser

Navigate to `http://localhost:8501`



\---



\## 📁 Project Structure



```

isac-health-security/

│

├── app/

│   └── app.py                 # Main Streamlit application (6 tabs)

│

├── src/

│   ├── \_\_init\_\_.py

│   ├── agents.py              # Agent classes with max\_iterations=3 safety

│   ├── tools.py               # Function calling tools (2 tools)

│   └── data\_loader.py         # Dataset loader for UCI HAR data

│

├── data/

│   ├── train.csv              # Training data (7,352 rows)

│   └── test.csv               # Test data (2,947 rows)

│

├── outputs/

│   └── isac\_security\_report\_\*.json

│

├── visuals/

│   └── visual.png

│

├── .env.example               # Environment template (NO real keys)

├── .gitignore                 # Git ignore rules

├── requirements.txt           # Python dependencies

└── README.md                  # This file

```



\---



\## 📦 Dependencies



```txt

streamlit>=1.35.0

openai>=1.52.0

python-dotenv>=1.0.0

pandas>=2.2.0

numpy>=1.26.0

matplotlib>=3.8.0

seaborn>=0.13.0

requests>=2.31.0

```



\---



\## 📝 Author



\*\*Sravs\*\* - GenAI Foundations Course (Weeks 22-23)



GitHub: https://github.com/sravsperum1



\---



\## 🔗 Important Links



| Link | URL |

|------|-----|

| \*\*GitHub Repository\*\* | https://github.com/sravsperum1/isac-health-security |

| \*\*Dataset (Kaggle)\*\* | https://www.kaggle.com/datasets/uciml/human-activity-recognition-with-smartphones |

| \*\*Azure OpenAI Docs\*\* | https://learn.microsoft.com/en-us/azure/ai-services/openai/ |



\---



\## 🙏 Acknowledgments



\- \*\*UCI Machine Learning Repository\*\* for the Human Activity Recognition dataset

\- \*\*Kaggle\*\* for hosting and providing easy access to the dataset

\- \*\*Azure OpenAI\*\* for GPT-4o access

\- \*\*Streamlit\*\* for the web framework



\---



\*\*Built with:\*\* Python, Azure OpenAI GPT-4o, Streamlit, Pandas, Matplotlib, Seaborn



\---



