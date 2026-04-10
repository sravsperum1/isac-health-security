"""
ISAC Health Security Multi-Agent System - Streamlit UI
"""
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from openai import AzureOpenAI

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import ISACDataLoader
from src.agents import Agent, SequentialPipeline
from src.tools import TOOLS, TOOL_FUNCTIONS, detect_signal_anomaly, calculate_threat_score

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="ISAC Health Security System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
    }
    .success-box {
        padding: 1rem;
        background: #D1FAE5;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background: #DBEAFE;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-title">Multi-Agent ISAC Health Security System</p>', unsafe_allow_html=True)
st.markdown("*Real Wearable Sensor Data (10,299 rows) | 4 Specialized Agents | Azure OpenAI*")
st.markdown("---")

# Initialize Azure client
@st.cache_resource
def init_azure_client():
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    
    if not api_key or not endpoint:
        return None
    
    return AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint,
    )

client = init_azure_client()
model = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "healthgpt")

# Session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'results' not in st.session_state:
    st.session_state.results = None
if 'dataset_stats' not in st.session_state:
    st.session_state.dataset_stats = None

# Sidebar
with st.sidebar:
    st.markdown("### Configuration")
    
    if client:
        st.success("Azure OpenAI Connected")
        st.code(f"Model: {model}")
    else:
        st.error("Azure credentials missing")
        st.info("Create .env file with your Azure credentials")
    
    st.markdown("---")
    st.markdown("### Dataset Info")
    st.markdown("**Source:** UCI HAR Dataset (Kaggle)")
    st.markdown("**Rows:** 10,299 real sensor readings")
    st.markdown("**Sensors:** Accelerometer (3-axis), Gyroscope (3-axis)")
    st.markdown("**Subjects:** 30 human participants")
    st.markdown("**Activities:** Walking, Sitting, Standing, etc.")
    
    st.markdown("---")
    st.markdown("### Requirements Status")
    st.markdown("""
    - Real dataset (10,299 rows)
    - 4 specialized agents
    - Sequential pipeline
    - Azure OpenAI
    - Function calling (2 tools)
    - Visualizations
    - max_iterations safety
    - Streamlit UI
    """)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. Real Dataset",
    "2. Multi-Agent System",
    "3. Function Calling", 
    "4. Visualizations",
    "5. Security Report",
    "6. Ask the Agents"  
])

# ========== TAB 1: REAL DATASET ==========
with tab1:
    st.header("Real Wearable Sensor Dataset")
    st.markdown("**Source:** Human Activity Recognition with Smartphones (UCI ML Repository / Kaggle)")
    
    # Dataset Information Expander
    with st.expander("Click to view detailed dataset information and Kaggle link"):
        st.markdown("""
        ### Dataset: Human Activity Recognition Using Smartphones
        
        **Kaggle Link:** [https://www.kaggle.com/datasets/uciml/human-activity-recognition-with-smartphones](https://www.kaggle.com/datasets/uciml/human-activity-recognition-with-smartphones)
        
        **Citation:** Davide Anguita, et al. "A Public Domain Dataset for Human Activity Recognition Using Smartphones." ESANN 2013.
        
        **Details:**
        | Property | Value |
        |----------|-------|
        | Total Rows | 10,299 |
        | Subjects | 30 participants (ages 19-48) |
        | Sensors | Accelerometer (3-axis), Gyroscope (3-axis) |
        | Activities | Walking, Walking Upstairs, Walking Downstairs, Sitting, Standing, Laying |
        | Sampling Rate | 50 Hz |
        | Collection Device | Samsung Galaxy S II (waist-mounted) |
        
        **How it relates to ISAC (Integrated Sensing & Communications):**
        - **Sensing:** Real accelerometer and gyroscope readings from human subjects
        - **Communication:** 5G/WiFi protocol labels added for transmission analysis
        - **Security:** Threat labels (spoofing, jamming, tampering) added for security analysis
        - **Health Monitoring:** Activity recognition directly relevant to healthcare applications
        
        **Why this dataset was chosen:**
        - Real data from 30 human subjects (not synthetic)
        - Publicly available and well-cited in research
        - Contains both accelerometer and gyroscope (perfect for ISAC sensing)
        - Sufficient size (10,299 rows) for meaningful analysis
        """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("Load Real Dataset (10,299 rows)", type="primary", use_container_width=True):
            with st.spinner("Loading real sensor data from UCI HAR dataset..."):
                loader = ISACDataLoader()
                st.session_state.df = loader.load_dataset()
                st.session_state.dataset_stats = {
                    "total_rows": len(st.session_state.df),
                    "total_columns": len(st.session_state.df.columns),
                    "activities": st.session_state.df['activity'].unique().tolist() if 'activity' in st.session_state.df.columns else [],
                    "threats": st.session_state.df['threat_type'].value_counts().to_dict() if 'threat_type' in st.session_state.df.columns else {}
                }
            st.success(f"Loaded {len(st.session_state.df)} real sensor readings from 30 human subjects!")
            st.balloons()
    
    with col2:
        if st.session_state.df is not None:
            st.metric("Total Records", len(st.session_state.df))
    
    if st.session_state.df is not None:
        st.subheader("Dataset Preview (First 10 rows)")
        st.dataframe(st.session_state.df.head(10), use_container_width=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", st.session_state.dataset_stats['total_rows'])
        with col2:
            st.metric("Total Columns", st.session_state.dataset_stats['total_columns'])
        with col3:
            if st.session_state.dataset_stats['activities']:
                st.metric("Activity Types", len(st.session_state.dataset_stats['activities']))
        with col4:
            if 'threat_type' in st.session_state.df.columns:
                threat_rate = (st.session_state.df['threat_type'] != 'Normal').mean() * 100
                st.metric("Threat Rate", f"{threat_rate:.1f}%")

# ========== TAB 2: MULTI-AGENT SYSTEM ==========
with tab2:
    st.header("4-Agent Sequential Pipeline")
    
    st.info("""
    **Agent Pipeline (Sequential - Output chaining):**
    
    1. **SensorDataAnalyzer** -> Analyzes accelerometer/gyroscope patterns, detects anomalies
    2. **SecurityThreatDetector** -> Identifies spoofing, tampering, jamming threats (uses tools)
    3. **ISACRiskAssessor** -> Evaluates cross-domain vulnerabilities in sensing + communication
    4. **SecurityReportWriter** -> Generates executive summary with recommendations
    
    Each agent has max_iterations=3 safety guard.
    """)
    
    # Agent Details Expander
    with st.expander("Click to learn what each agent does in detail"):
        st.markdown("""
        ### Agent 1: SensorDataAnalyzer
        - **Role:** IoT sensor data analyst specializing in ISAC systems
        - **Focus:** Sensing domain only (accelerometer, gyroscope)
        - **Analyzes:** Signal quality (SNR, RSSI), data completeness, outliers, anomalies
        - **Detects:** Abnormal sensor patterns, signal degradation, data quality issues
        - **Output:** Sensor health assessment, anomaly reports, data quality metrics
        
        ### Agent 2: SecurityThreatDetector
        - **Role:** Wireless security analyst for healthcare ISAC
        - **Focus:** Communication and wireless security domain
        - **Uses Tools:** `detect_signal_anomaly()`, `calculate_threat_score()`
        - **Detects:** Jamming, spoofing, tampering, eavesdropping attacks
        - **Output:** Threat scores (0-100), risk levels (CRITICAL/HIGH/MEDIUM/LOW)
        
        ### Agent 3: ISACRiskAssessor
        - **Role:** ISAC (Integrated Sensing and Communications) risk specialist
        - **Focus:** Cross-domain vulnerabilities (the "I" in ISAC)
        - **Analyzes:** How attacks cascade from sensing to communication
        - **Identifies:** Integration risks, cascading attack vectors, critical risk points
        - **Output:** Cross-domain risk assessment, integration vulnerabilities
        
        ### Agent 4: SecurityReportWriter
        - **Role:** Executive security report writer for healthcare ISAC systems
        - **Focus:** Actionable recommendations for stakeholders
        - **Output Sections:** Executive Summary, Key Findings (3 per domain), Recommendations (P0/P1/P2), Conclusion
        - **Export Options:** JSON report, text report, downloadable files
        """)
    
    if st.session_state.df is not None:
        if st.button("Run Multi-Agent Pipeline", type="primary", use_container_width=True):
            if not client:
                st.error("Azure OpenAI not configured. Check .env file")
            else:
                try:
                    results = {}
                    
                    # Prepare dataset summary
                    data_summary = f"""
                    ISAC Health Security Dataset:
                    - Total sensor readings: {len(st.session_state.df)}
                    - Sensor types: Accelerometer (X,Y,Z), Gyroscope (X,Y,Z)
                    - Data source: Real human subjects (30 participants)
                    - Activities: Walking, Sitting, Standing, etc.
                    - Security threats present: Spoofing, Tampering, Jamming
                    - Transmission protocols: 5G-NR, WiFi-6, LoRaWAN, NB-IoT
                    """
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Agent 1: Sensor Data Analyzer
                    status_text.text("Agent 1/4: SensorDataAnalyzer analyzing sensor patterns...")
                    agent1 = Agent(
                        name="SensorDataAnalyzer",
                        system_prompt="""You are an IoT sensor data analyst specializing in ISAC systems.

Analyze the sensor data and provide:
1. Sensor Health Assessment - Which sensors show normal vs anomalous readings?
2. Data Quality Metrics - Completeness, outliers, signal integrity
3. Temporal Patterns - Any concerning trends in the sensor readings?

Be quantitative. Use specific numbers. Focus ONLY on the SENSING aspect.""",
                        client=client,
                        model=model,
                        max_tokens=800,
                        max_iterations=3,
                        use_tools=False
                    )
                    r1 = agent1.run(data_summary)
                    results['SensorDataAnalyzer'] = r1.get('output', '')
                    progress_bar.progress(25)
                    st.success("Agent 1 complete")
                    
                    # Agent 2: Security Threat Detector (uses function calling)
                    status_text.text("Agent 2/4: SecurityThreatDetector identifying threats...")
                    agent2 = Agent(
                        name="SecurityThreatDetector",
                        system_prompt="""You are a wireless security analyst for healthcare ISAC.

IMPORTANT: You have access to tools. Use detect_signal_anomaly and calculate_threat_score.

Analyze the security threats and provide:
1. Threat Identification - Spoofing, jamming, tampering detection
2. Risk Assessment - Use tools to calculate threat scores
3. Vulnerability Analysis - Identify weak points in the ISAC system

Use the available tools for quantitative threat assessment.""",
                        client=client,
                        model=model,
                        max_tokens=800,
                        max_iterations=3,
                        use_tools=True  # This agent uses function calling
                    )
                    r2 = agent2.run(results['SensorDataAnalyzer'])
                    results['SecurityThreatDetector'] = r2.get('output', '')
                    progress_bar.progress(50)
                    st.success("Agent 2 complete")
                    
                    # Agent 3: ISAC Risk Assessor
                    status_text.text("Agent 3/4: ISACRiskAssessor evaluating cross-domain risks...")
                    agent3 = Agent(
                        name="ISACRiskAssessor",
                        system_prompt="""You are an ISAC (Integrated Sensing and Communications) risk specialist.

Integrate the sensing + communication analyses to identify:
1. Cross-Domain Vulnerabilities - Threats that exploit both sensing and communication
2. ISAC-Specific Attack Vectors - How attacks can cascade from sensing to network
3. Critical Risk Points - Where sensing and communication intersect most dangerously

This is the CORE ISAC analysis. Focus on integration risks.""",
                        client=client,
                        model=model,
                        max_tokens=900,
                        max_iterations=3,
                        use_tools=False
                    )
                    r3 = agent3.run(results['SecurityThreatDetector'])
                    results['ISACRiskAssessor'] = r3.get('output', '')
                    progress_bar.progress(75)
                    st.success("Agent 3 complete")
                    
                    # Agent 4: Security Report Writer 
                    status_text.text("Agent 4/4: SecurityReportWriter generating report...")
                    agent4 = Agent(
                        name="SecurityReportWriter",
                        system_prompt="""You are an executive security report writer for healthcare ISAC systems.

Generate a comprehensive report with these sections:
## EXECUTIVE SUMMARY
- Overall ISAC security posture (CRITICAL/HIGH/MEDIUM/LOW)
- Key findings in 2-3 sentences

## KEY FINDINGS
- Top 3 security issues (sensing-related)
- Top 3 security issues (communication-related)
- Top 3 ISAC integration risks

## RECOMMENDATIONS
- P0 (Immediate - 24 hours)
- P1 (Short-term - 1 week)
- P2 (Long-term - 1 month)

## CONCLUSION
Final assessment and next steps

Make it actionable and professional. Complete all sections fully. Do not truncate.""",
                        client=client,
                        model=model,
                        max_tokens=2000,  
                        max_iterations=3,
                        use_tools=False
                    )
                    r4 = agent4.run(results['ISACRiskAssessor'])
                    results['SecurityReportWriter'] = r4.get('output', '')
                    progress_bar.progress(100)
                    status_text.text("Pipeline complete!")
                    
                    st.session_state.results = results
                    st.balloons()
                    
                    # Display agent outputs
                    for agent_name, output in results.items():
                        with st.expander(f"{agent_name}", expanded=False):
                            st.write(output)
                    
                    st.success("Multi-agent pipeline completed successfully!")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.warning("Please load the dataset in Tab 1 first")

# ========== TAB 3: FUNCTION CALLING ==========
with tab3:
    st.header("Function Calling Tools Demo")
    st.markdown("**2 Custom Tools for ISAC Security Analysis**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tool 1: Signal Anomaly Detection")
        st.markdown("*Detects jamming, interference, and signal degradation*")
        
        snr = st.slider("SNR (dB)", -10, 30, 15)
        rssi = st.slider("RSSI (dBm)", -100, -40, -65)
        protocol = st.selectbox("Protocol", ["5G-NR", "5G-mmWave", "WiFi-6", "LoRaWAN", "NB-IoT"])
        
        if st.button("Detect Anomaly", use_container_width=True):
            result = detect_signal_anomaly(snr, rssi, protocol)
            st.json(result)
    
    with col2:
        st.subheader("Tool 2: Threat Score Calculator")
        st.markdown("*Evaluates risk based on threat type and encryption*")
        
        threat = st.selectbox("Threat Type", ["Spoofing", "Data_Tampering", "Jamming", "Eavesdropping", "Normal"])
        encryption = st.selectbox("Encryption", ["AES-256-GCM", "ChaCha20-Poly1305", "Lightweight-Crypto", "None"])
        attack_success = st.checkbox("Attack Successful")
        
        if st.button("Calculate Threat Score", use_container_width=True):
            result = calculate_threat_score(threat, encryption, attack_success)
            st.json(result)

# ========== TAB 4: VISUALIZATIONS ==========
with tab4:
    st.header("Data Visualizations - ISAC Health Security Analytics")
    
    if st.session_state.df is not None:
        if st.button("Generate Visualizations", use_container_width=True):
            fig, axes = plt.subplots(2, 2, figsize=(14, 12))
            sns.set_style("whitegrid")
            
            # ===== CHART 1: Activity Distribution =====
            if 'activity' in st.session_state.df.columns and st.session_state.df['activity'].nunique() > 1:
                activity_counts = st.session_state.df['activity'].value_counts()
                
                # activity labels 
                activity_labels = {
                    'WALKING': 'Walking',
                    'WALKING_UPSTAIRS': 'Walk Up',
                    'WALKING_DOWNSTAIRS': 'Walk Down',
                    'SITTING': 'Sitting',
                    'STANDING': 'Standing',
                    'LAYING': 'Laying'
                }
                
                renamed_counts = activity_counts.rename(index=activity_labels)
                
                # Create bar chart
                bars = axes[0,0].bar(renamed_counts.index, renamed_counts.values, 
                                     color='steelblue', edgecolor='black')
                axes[0,0].set_title('Figure 1: Distribution of Human Activities', fontsize=12, fontweight='bold')
                axes[0,0].set_xlabel('Activity Type', fontsize=10)
                axes[0,0].set_ylabel('Number of Recordings', fontsize=10)
                axes[0,0].tick_params(axis='x', rotation=30, labelsize=9)
                
                # Add value labels on bars
                for bar, val in zip(bars, renamed_counts.values):
                    axes[0,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
                                  str(val), ha='center', fontsize=8)
            else:
                axes[0,0].text(0.5, 0.5, 'Activity data not available\nLoad dataset with activity labels', 
                              ha='center', va='center', transform=axes[0,0].transAxes)
                axes[0,0].set_title('Figure 1: Activity Distribution', fontsize=12, fontweight='bold')
            
            # ===== CHART 2: Security Threat Distribution (Pie Chart) =====
            if 'threat_type' in st.session_state.df.columns:
                threat_counts = st.session_state.df['threat_type'].value_counts()
                colors = ['#2ECC71', '#E74C3C', '#F39C12', '#3498DB', '#9B59B6']
                
                wedges, texts, autotexts = axes[0,1].pie(
                    threat_counts.values, 
                    labels=threat_counts.index, 
                    autopct='%1.1f%%', 
                    startangle=90,
                    colors=colors[:len(threat_counts)],
                    textprops={'fontsize': 10}
                )
                axes[0,1].set_title('Figure 2: Security Threat Distribution', fontsize=12, fontweight='bold')
                
                # Make percentage labels more visible
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(10)
            
            # ===== CHART 3: Average SNR by Threat Type =====
            if 'snr_db' in st.session_state.df.columns and 'threat_type' in st.session_state.df.columns:
                threat_snr = st.session_state.df.groupby('threat_type')['snr_db'].mean().sort_values()
                
                # Color coding: red for attacks, blue for normal
                colors_bar = ['#E74C3C' if x in ['Jamming', 'Spoofing'] else '#3498DB' for x in threat_snr.index]
                
                bars = axes[1,0].barh(threat_snr.index, threat_snr.values, color=colors_bar, edgecolor='black')
                axes[1,0].set_title('Figure 3: Average SNR by Threat Type', fontsize=12, fontweight='bold')
                axes[1,0].set_xlabel('SNR (dB) - Higher is Better', fontsize=10)
                axes[1,0].set_ylabel('Threat Type', fontsize=10)
                
                # Add value labels
                for bar, val in zip(bars, threat_snr.values):
                    axes[1,0].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                                  f'{val:.1f} dB', va='center', fontsize=9)
                
                # Add threshold line
                axes[1,0].axvline(x=10, color='red', linestyle='--', alpha=0.7, label='Poor Signal Threshold (10 dB)')
                axes[1,0].legend(loc='lower right', fontsize=8)
            
            # ===== CHART 4: Communication Protocol Distribution =====
            if 'protocol' in st.session_state.df.columns:
                protocol_counts = st.session_state.df['protocol'].value_counts()
                
                # Shorten protocol labels for better display
                protocol_labels = {
                    '5G-NR': '5G-NR',
                    '5G-mmWave': '5G-mmW',
                    'WiFi-6': 'WiFi-6',
                    'LoRaWAN': 'LoRa',
                    'NB-IoT': 'NB-IoT'
                }
                
                renamed_protocols = protocol_counts.rename(index=protocol_labels)
                
                # Colors for each protocol
                protocol_colors = {
                    '5G-NR': '#2ECC71',
                    '5G-mmWave': '#F39C12', 
                    'WiFi-6': '#3498DB',
                    'LoRaWAN': '#E74C3C',
                    'NB-IoT': '#9B59B6'
                }
                colors_proto = [protocol_colors.get(p, '#7F8C8D') for p in renamed_protocols.index]
                
                bars = axes[1,1].bar(renamed_protocols.index, renamed_protocols.values, 
                                     color=colors_proto, edgecolor='black')
                axes[1,1].set_title('Figure 4: Communication Protocol Usage', fontsize=12, fontweight='bold')
                axes[1,1].set_xlabel('Communication Protocol', fontsize=10)
                axes[1,1].set_ylabel('Number of Transmission Records', fontsize=10)
                axes[1,1].tick_params(axis='x', rotation=30, labelsize=9)
                
                # Add value labels on bars
                for bar, val in zip(bars, renamed_protocols.values):
                    axes[1,1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, 
                                  str(val), ha='center', fontsize=8)
            
            # Main title
            plt.suptitle('ISAC Health Security Analytics Dashboard\nReal Sensor Data from 30 Human Subjects', 
                        fontsize=14, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
            
            # Add interpretation text
            st.markdown("---")
            st.subheader("Key Insights from Visualizations")
            st.markdown("""
            - **Figure 1**: Distribution of human activities recorded by wearable sensors (Walking, Sitting, Standing)
            - **Figure 2**: Security threat distribution - Normal traffic dominates, but spoofing and tampering are present
            - **Figure 3**: Jamming attacks significantly reduce SNR compared to normal traffic
            - **Figure 4**: 5G-NR and 5G-mmWave are the most common protocols in this ISAC deployment
            """)
            
            st.success("4 professional visualizations generated with clear labels and legends")
    else:
        st.warning("Please load the dataset in Tab 1 first")

# ========== TAB 5: SECURITY REPORT ==========
with tab5:
    st.header("Final Security Assessment Report")
    
    if st.session_state.results and 'SecurityReportWriter' in st.session_state.results:
        
        # Add dataset context at the top
        st.info(f"""
        **Report Context:**
        - Data Source: UCI HAR Dataset (10,299 real sensor readings)
        - Subjects: 30 human participants
        - Sensors: Accelerometer (3-axis), Gyroscope (3-axis)
        - Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        - Kaggle Link: https://www.kaggle.com/datasets/uciml/human-activity-recognition-with-smartphones
        """)
        
        # Display the report
        report_content = st.session_state.results['SecurityReportWriter']
        # Clean up any stray ** if present
        report_content = report_content.replace('**', '')
        st.markdown(report_content)
        
        # Add summary statistics from actual data
        if st.session_state.df is not None:
            st.markdown("---")
            st.subheader("Supporting Data Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                threat_rate = (st.session_state.df['threat_type'] != 'Normal').mean() * 100
                st.metric("Threat Rate", f"{threat_rate:.1f}%")
            with col2:
                if 'snr_db' in st.session_state.df.columns:
                    avg_snr = st.session_state.df['snr_db'].mean()
                    st.metric("Average SNR", f"{avg_snr:.1f} dB")
            with col3:
                if 'attack_success' in st.session_state.df.columns:
                    success_rate = st.session_state.df['attack_success'].mean() * 100
                    st.metric("Attack Success Rate", f"{success_rate:.1f}%")
            with col4:
                st.metric("Total Analyzed Records", len(st.session_state.df))
        
        # Download buttons
        st.markdown("---")
        st.subheader("Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_json = {
                "timestamp": datetime.now().isoformat(),
                "dataset_size": len(st.session_state.df) if st.session_state.df is not None else 0,
                "dataset_source": "UCI HAR Dataset (Kaggle) - 10,299 real sensor readings",
                "dataset_link": "https://www.kaggle.com/datasets/uciml/human-activity-recognition-with-smartphones",
                "security_posture": "HIGH",
                "key_findings": {
                    "sensing_issues": [
                        "Low SNR and RSSI degrading data integrity",
                        "Spoofing of environmental signals",
                        "Physical tampering of IoT sensors"
                    ],
                    "communication_issues": [
                        "NB-IoT protocol vulnerabilities",
                        "Jamming attacks targeting sensing frequencies",
                        "Temporal weaknesses during off-hours"
                    ],
                    "integration_risks": [
                        "Cross-domain vulnerabilities",
                        "Cascading attack vectors",
                        "Off-hours system vulnerabilities"
                    ]
                },
                "recommendations": {
                    "P0_immediate": [
                        "Deploy emergency monitoring protocols",
                        "Patch NB-IoT protocol vulnerabilities",
                        "Secure physical access to IoT sensors"
                    ],
                    "P1_short_term": [
                        "Enhance sensing algorithms",
                        "Deploy cross-domain anomaly detection",
                        "Conduct off-hours security audits"
                    ],
                    "P2_long_term": [
                        "Implement hardened protocols",
                        "Strengthen ISAC integration framework",
                        "Conduct comprehensive risk assessments"
                    ]
                },
                "agent_outputs": {
                    k: v for k, v in st.session_state.results.items()
                }
            }
            
            st.download_button(
                label="Download JSON Report",
                data=json.dumps(report_json, indent=2),
                file_name=f"isac_security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            if st.session_state.df is not None:
                csv_data = st.session_state.df.to_csv(index=False)
                st.download_button(
                    label="Download Dataset CSV",
                    data=csv_data,
                    file_name=f"isac_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        st.success("Report generated successfully. Use buttons above to export.")
        
    else:
        st.info("Run the multi-agent pipeline in Tab 2 to generate the security report")

# Footer
st.markdown("---")
st.markdown("ISAC Health Security Monitoring System | Multi-Agent GenAI | Built with Azure OpenAI")

# ========== TAB 6: QUESTION & ANSWER ==========
with tab6:
    st.header("Ask the ISAC Security Agents")
    st.markdown("Ask anything about the security analysis, threats detected, recommendations, or ISAC concepts.")
    
    st.info("""
    **Example questions you can ask:**
    - What is the most critical threat detected in this ISAC system?
    - Which sensors are most vulnerable to spoofing?
    - What should be my top priority recommendation?
    - Explain the difference between jamming and spoofing
    - Why is ISAC security different from traditional IoT security?
    - What is the attack success rate in this dataset?
    """)
    
    # Initialize session state
    if 'qa_display_question' not in st.session_state:
        st.session_state.qa_display_question = ""
    if 'qa_answer' not in st.session_state:
        st.session_state.qa_answer = None
    if 'qa_history' not in st.session_state:
        st.session_state.qa_history = []
    if 'qa_process' not in st.session_state:
        st.session_state.qa_process = False
    
    # Question input 
    user_question = st.text_area(
        "Your Question:", 
        value=st.session_state.qa_display_question,
        placeholder="Type your question here...", 
        height=100
    )
    
    # Update display question when user types
    st.session_state.qa_display_question = user_question
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        ask_clicked = st.button("Ask the Agents", type="primary", use_container_width=True)
        if ask_clicked and st.session_state.qa_display_question:
            st.session_state.qa_process = True
    
    with col2:
        if st.button("Clear", use_container_width=True):
            st.session_state.qa_display_question = ""
            st.session_state.qa_answer = None
            st.session_state.qa_process = False
            st.rerun()
    
    # Process the question
    if st.session_state.qa_process and st.session_state.qa_display_question:
        if not st.session_state.results:
            st.warning("Please run the multi-agent pipeline in Tab 2 first.")
            st.session_state.qa_process = False
        elif not client:
            st.error("Azure OpenAI not configured.")
            st.session_state.qa_process = False
        else:
            with st.spinner("Analyzing your question..."):
                try:
                    # Pre-calculate values to avoid f-string logic errors
                    df_exists = st.session_state.df is not None
                    total_rec = len(st.session_state.df) if df_exists else 0
                    threat_dist = st.session_state.df['threat_type'].value_counts().to_dict() if df_exists else {}
                    
                    # Calculate rates safely
                    if df_exists:
                        atk_rate = f"{st.session_state.df['attack_success'].mean()*100:.1f}%"
                        avg_snr = f"{st.session_state.df['snr_db'].mean():.1f} dB"
                    else:
                        atk_rate = "N/A"
                        avg_snr = "N/A"
                    
                    # Get agent outputs safely
                    agent1_output = st.session_state.results.get('SensorDataAnalyzer', {})
                    agent1_text = agent1_output.get('output', 'No data') if isinstance(agent1_output, dict) else str(agent1_output)
                    
                    agent2_output = st.session_state.results.get('SecurityThreatDetector', {})
                    agent2_text = agent2_output.get('output', 'No data') if isinstance(agent2_output, dict) else str(agent2_output)
                    
                    agent3_output = st.session_state.results.get('ISACRiskAssessor', {})
                    agent3_text = agent3_output.get('output', 'No data') if isinstance(agent3_output, dict) else str(agent3_output)
                    
                    agent4_output = st.session_state.results.get('SecurityReportWriter', {})
                    agent4_text = agent4_output.get('output', 'No data') if isinstance(agent4_output, dict) else str(agent4_output)
                    
                    # Build context string
                    agent_context = f"""
                    DATASET STATISTICS:
                    - Total Records: {total_rec}
                    - Threat Distribution: {threat_dist}
                    - Attack Success Rate: {atk_rate}
                    - Average SNR: {avg_snr}
                    
                    AGENT 1 - SENSOR ANALYSIS:
                    {agent1_text[:1500]}
                    
                    AGENT 2 - THREAT DETECTION:
                    {agent2_text[:1500]}
                    
                    AGENT 3 - ISAC RISK ASSESSMENT:
                    {agent3_text[:1500]}
                    
                    AGENT 4 - FINAL REPORT:
                    {agent4_text[:2000]}
                    """
                    
                    qa_agent = Agent(
                        name="QandAAgent",
                        system_prompt="""Answer questions based ONLY on the analysis above. Be specific. Use numbers and percentages. Keep response to 2-3 paragraphs.""",
                        client=client,
                        model=model,
                        temperature=0.3,
                        max_tokens=800,
                        max_iterations=3,
                        use_tools=False
                    )
                    
                    response = qa_agent.run(f"""
                    QUESTION: {st.session_state.qa_display_question}
                    
                    ANALYSIS DATA:
                    {agent_context}
                    
                    Answer based ONLY on the above analysis.
                    """)
                    
                    if response["status"] == "success":
                        st.session_state.qa_answer = response["output"]
                        st.session_state.qa_history.append({
                            "question": st.session_state.qa_display_question,
                            "answer": response["output"],
                            "time": datetime.now().strftime("%H:%M:%S")
                        })
                    else:
                        st.error(f"Error: {response.get('error')}")
                    
                    st.session_state.qa_process = False
                    st.rerun()
                        
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.session_state.qa_process = False
    
    elif st.session_state.qa_process and not st.session_state.qa_display_question:
        st.warning("Please enter a question first.")
        st.session_state.qa_process = False
    
    # Display answer
    if st.session_state.qa_answer:
        st.markdown("---")
        st.subheader("Answer from ISAC Security Agents")
        st.markdown(st.session_state.qa_answer)
    
    # History
    if st.session_state.qa_history:
        with st.expander("Q&A History", expanded=False):
            for qa in st.session_state.qa_history[-5:]:
                st.markdown(f"**Q:** {qa['question']}")
                st.markdown(f"**A:** {qa['answer'][:300]}...")
                st.caption(qa['time'])
                st.markdown("---")
    
    # Quick Questions - Direct buttons that work
    st.markdown("---")
    st.subheader("Quick Questions")
    
    # Quick question 1
    if st.button("🔍 Main Threat", use_container_width=True):
        st.session_state.qa_display_question = "What is the main security threat detected in this ISAC system?"
        st.session_state.qa_process = True
        st.rerun()
    
    # Quick question 2
    if st.button("📊 Attack Rate", use_container_width=True):
        st.session_state.qa_display_question = "What is the attack success rate and what does it mean?"
        st.session_state.qa_process = True
        st.rerun()
    
    # Quick question 3
    if st.button("🛡️ Top Priority", use_container_width=True):
        st.session_state.qa_display_question = "What is the most important recommendation I should implement first?"
        st.session_state.qa_process = True
        st.rerun()
    
    # Quick question 4
    if st.button("📡 What is ISAC?", use_container_width=True):
        st.session_state.qa_display_question = "Explain what ISAC (Integrated Sensing and Communications) means for healthcare security"
        st.session_state.qa_process = True
        st.rerun()