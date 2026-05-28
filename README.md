# 🏥 Multi-Agent ISAC Health Security System

A multi-agent AI system that analyses real wearable sensor data (10,299 rows) to detect security threats in Integrated Sensing and Communications (ISAC) healthcare applications — with a built-in chat interface to ask follow-up questions about the security analysis.

**GitHub Repository:** https://github.com/sravsperum1/isac-health-security

**Deployement:** https://youtu.be/Sks1ib0m258?si=mBcXohkZdEUgxRyF

---

## 📌 Project Overview

This project was built as a capstone for a Generative AI course, demonstrating how multiple specialised AI agents can work together in a sequential pipeline to solve a real-world data science problem in healthcare security.

The system ingests real UCI HAR dataset (accelerometer + gyroscope readings from 30 human subjects), runs it through four specialised agents, produces a structured JSON security report with data visualisations, and exposes everything through a Streamlit web app where users can chat with the agents about the findings.

---

## 🏗️ Architecture

**INPUT** → **AGENT 1** → **AGENT 2** → **AGENT 3** → **AGENT 4** → **OUTPUT**

---

### Input Layer
- **Dataset:** UCI HAR Dataset (10,299 rows)
- **Sensors:** Accelerometer (3-axis), Gyroscope (3-axis)
- **Subjects:** 30 human participants

⬇️

### Agent 1: SensorDataAnalyzer
- Noise detection and filtering
- Signal quality assessment (SNR, RSSI)
- Outlier detection in sensor readings
- **Output:** Sensor health report with anomaly percentages

⬇️

### Agent 2: SecurityThreatDetector
- Attack identification (spoofing, jamming, tampering)
- Threat scoring (0-100 scale)
- **Tools:** `detect_signal_anomaly()`, `calculate_threat_score()`
- **Output:** Threat scores and risk levels

⬇️

### Agent 3: ISACRiskAssessor
- Cross-domain vulnerability fusion
- Attack propagation path analysis
- Cascading risk identification
- **Output:** Integrated risk assessment

⬇️

### Agent 4: SecurityReportWriter
- Executive summary generation
- Risk prioritization (P0/P1/P2)
- JSON and text report export
- **Output:** Final security report

⬇️

### Output Layer
- 📊 4 Visualizations
- 📄 JSON Report
- 📝 Text Report
- 🖥️ Streamlit UI (6 Tabs)
---

## 🔄 Sequential Pipeline Flow
INPUT → AGENT 1 → AGENT 2 → AGENT 3 → AGENT 4 → OUTPUT

Each agent's output becomes the next agent's input.

---

## 🤖 The 4 Agents

| Agent | Focus | Key Functions |
|-------|-------|---------------|
| **SensorDataAnalyzer** | SENSING domain | Noise detection, signal quality, outlier detection |
| **SecurityThreatDetector** | COMMUNICATION domain | Attack identification, threat scoring, risk levels |
| **ISACRiskAssessor** | INTEGRATION domain | Cross-domain vulnerabilities, attack propagation |
| **SecurityReportWriter** | OUTPUT domain | Executive summary, recommendations, JSON export |

## 🔧 Custom Tools (Function Calling)

### Tool 1: `detect_signal_anomaly(snr_db, rssi_dbm, protocol)`
- **Purpose:** Detect jamming, interference, and signal degradation
- **Input:** SNR (dB), RSSI (dBm), Protocol
- **Output:** Anomaly flag, risk score, recommendation

### Tool 2: `calculate_threat_score(threat_type, encryption, attack_success)`
- **Purpose:** Calculate overall security threat score
- **Input:** Threat type, encryption method, attack success
- **Output:** Threat score (0-100), risk level, action required

## 🖥️ Streamlit UI (6 Tabs)

| Tab | Function |
|-----|----------|
| **1. Real Dataset** | Load and explore 10,299 sensor readings |
| **2. Multi-Agent System** | Run 4 agents sequentially |
| **3. Function Calling** | Test security tools manually |
| **4. Visualizations** | Generate 4 security charts |
| **5. Security Report** | View/download JSON report |
| **6. Ask the Agents** | Q&A chat interface |
---
## 🛡️ Safety Features (max_iterations Guard)

**Agent.run() with max_iterations=3**

- Iteration 1 → Try API call → Success? → Return output
- If fails → Wait 2 seconds
- Iteration 2 → Try API call → Success? → Return output  
- If fails → Wait 4 seconds
- Iteration 3 → Try API call → Success? → Return output
- If fails → Return error: "Max iterations exceeded"

*Prevents infinite loops and handles API failures gracefully.*

## 📊 Dataset

| Property | Value |
|----------|-------|
| **Source** | UCI HAR Dataset / Kaggle |
| **Kaggle Link** | https://www.kaggle.com/datasets/uciml/human-activity-recognition-with-smartphones |
| **Total Rows** | 10,299 |
| **Subjects** | 30 human participants (ages 19-48) |
| **Sensors** | Accelerometer (3-axis), Gyroscope (3-axis) |
| **Activities** | Walking, Walking Upstairs, Walking Downstairs, Sitting, Standing, Laying |

### Why this dataset for ISAC?

| Component | How Dataset Provides It |
|-----------|------------------------|
| **Sensing** | Real accelerometer + gyroscope readings from 30 human subjects |
| **Communication** | Added 5G/WiFi protocol labels (5G-NR, 5G-mmWave, WiFi-6, LoRaWAN, NB-IoT) |
| **Security** | Added threat labels (Spoofing, Jamming, Tampering, Eavesdropping) |
| **Health Monitoring** | Activity recognition directly relevant to healthcare |

---

## 🖥️ Streamlit App (6 Tabs)

| Tab | What it does |
|-----|--------------|
| **1. Real Dataset** | Load and explore UCI HAR dataset (10,299 rows) |
| **2. Multi-Agent System** | Run 4 agents sequentially with progress tracking |
| **3. Function Calling** | Test the 2 security tools manually |
| **4. Visualizations** | Generate 4 security charts |
| **5. Security Report** | View/download final security assessment |
| **6. Ask the Agents** | Q&A chat interface to ask questions about analysis |

---

## 📈 Results & Key Findings

### Quantitative Results

| Metric | Value |
|--------|-------|
| Attack Success Rate | ~30% |
| Average SNR | ~11.6 dB |
| Threat Rate | ~25% |
| Pipeline Time | ~30-40 seconds |
| Total Tokens | ~4,000 |

### Key Findings by Domain

| Domain | Top Issues |
|--------|------------|
| **Sensing** | Sensor Spoofing, Physical Tampering, Low SNR/RSSI |
| **Communication** | NB-IoT Vulnerabilities, Jamming Attacks, Off-Hours Weaknesses |
| **ISAC Integration** | Cross-Domain Vulnerabilities, Cascading Attack Vectors |

### Recommendations

| Priority | Timeframe | Actions |
|----------|-----------|---------|
| **P0** | 24 hours | Deploy emergency monitoring, patch NB-IoT, secure physical sensors |
| **P1** | 1 week | Enhance sensing algorithms, deploy cross-domain detection, off-hours audits |
| **P2** | 1 month | Implement hardened protocols, strengthen ISAC framework, risk assessments |

---

## 📊 Visualizations Generated

| Figure | Description | Key Insight |
|--------|-------------|-------------|
| **Figure 1** | Activity Distribution | Walking (26%), Sitting (15%), Standing (15%) |
| **Figure 2** | Threat Distribution | Normal (75%), Spoofing (8%), Tampering (7%) |
| **Figure 3** | SNR by Threat Type | Jamming reduces SNR to -4.9 dB (vs normal 12.8 dB) |
| **Figure 4** | Protocol Usage | 5G-NR (21%), 5G-mmWave (20%), WiFi-6 (20%) |

---

## 🛡️ Safety Features

| Feature | Implementation | Why |
|---------|----------------|-----|
| **max_iterations=3** | Each agent retries up to 3 times | Prevents infinite loops |
| **Exponential Backoff** | Wait 1s, 2s, 4s between retries | Handles API rate limits |
| **Try/Except Blocks** | Graceful error handling | App doesn't crash on errors |
| **Token Tracking** | Monitors API usage | Cost control |
| **.gitignore** | Excludes .env, .venv | Protects API keys |

---

## ✅ Requirements Checklist

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Real dataset (500+ rows) | ✅ | 10,299 rows - UCI HAR Dataset |
| 3+ specialized agents | ✅ | 4 agents with unique system prompts |
| Multi-agent pattern | ✅ | Sequential pipeline (output chaining) |
| Azure OpenAI | ✅ | AzureOpenAI client with GPT-4o |
| Function calling (2+ tools) | ✅ | detect_signal_anomaly, calculate_threat_score |
| Structured output + viz | ✅ | JSON report + 4 matplotlib/seaborn charts |
| Safety guardrails | ✅ | max_iterations=3, exponential backoff |
| Streamlit UI (Bonus) | ✅ | Full web interface with 6 tabs |

---

## 🚀 How to Run

### Prerequisites
- Python 3.11 or higher
- Azure OpenAI account with GPT-4o deployment

### Step 1: Clone Repository
```bash
git clone https://github.com/sravsperum1/isac-health-security.git
cd isac-health-security
Step 2: Download Dataset
Download from Kaggle: https://www.kaggle.com/datasets/uciml/human-activity-recognition-with-smartphones
Place train.csv and test.csv in the data/ folder.

Step 3: Create Virtual Environment
bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
Step 4: Install Dependencies
bash
pip install -r requirements.txt
Step 5: Configure Azure OpenAI
bash
cp .env.example .env
# Edit .env with your Azure credentials
Step 6: Run the App
bash
streamlit run app/app.py
Step 7: Open Browser
Navigate to http://localhost:8501

📁 Project Structure
text
isac-health-security/
│
├── app/
│   └── app.py                 # Main Streamlit application (6 tabs)
│
├── src/
│   ├── __init__.py
│   ├── agents.py              # Agent classes with max_iterations=3 safety
│   ├── tools.py               # Function calling tools (2 tools)
│   └── data_loader.py         # Dataset loader for UCI HAR data
│
├── data/
│   ├── train.csv              # Training data (7,352 rows)
│   └── test.csv               # Test data (2,947 rows)
│
├── outputs/
│   └── isac_security_report_*.json
│
├── visuals/
│   └── visual.png
│
├── .env.example               # Environment template (NO real keys)
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
└── README.md                  # This file
📦 Dependencies
txt
streamlit>=1.35.0
openai>=1.52.0
python-dotenv>=1.0.0
pandas>=2.2.0
numpy>=1.26.0
matplotlib>=3.8.0
seaborn>=0.13.0
requests>=2.31.0
📝 Author
Sravs - GenAI Foundations Course (Weeks 22-23)

GitHub: https://github.com/sravsperum1

🔗 Important Links
Link	URL
GitHub Repository	https://github.com/sravsperum1/isac-health-security
Dataset (Kaggle)	https://www.kaggle.com/datasets/uciml/human-activity-recognition-with-smartphones
Azure OpenAI Docs	https://learn.microsoft.com/en-us/azure/ai-services/openai/
🙏 Acknowledgments
UCI Machine Learning Repository for the Human Activity Recognition dataset

Kaggle for hosting and providing easy access to the dataset

Azure OpenAI for GPT-4o access

Streamlit for the web framework

Built with: Python, Azure OpenAI GPT-4o, Streamlit, Pandas, Matplotlib, Seaborn
