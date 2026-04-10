"""
Function Calling Tools for ISAC Security Analysis
2 custom tools for threat detection and risk assessment
"""

def detect_signal_anomaly(snr_db: float, rssi_dbm: float, protocol: str) -> dict:
    """
    Tool 1: Detect anomalies in wireless signals
    Identifies jamming, interference, and signal degradation
    """
    is_anomaly = False
    anomaly_type = None
    risk_score = 0
    
    # Jamming detection
    if snr_db < 5:
        is_anomaly = True
        anomaly_type = "JAMMING_DETECTED"
        risk_score += 50
    elif rssi_dbm < -85:
        is_anomaly = True
        anomaly_type = "WEAK_SIGNAL_INTERFERENCE"
        risk_score += 30
    
    # Protocol-specific checks
    if protocol in ['LoRaWAN', 'NB-IoT'] and snr_db < 10:
        is_anomaly = True
        anomaly_type = "PROTOCOL_VULNERABILITY"
        risk_score += 20
    
    risk_level = "HIGH" if risk_score > 50 else "MEDIUM" if risk_score > 20 else "LOW"
    
    return {
        "is_anomaly": is_anomaly,
        "anomaly_type": anomaly_type,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "recommendation": "Increase transmission power and enable encryption" if is_anomaly else "Normal operation"
    }


def calculate_threat_score(threat_type: str, encryption: str, attack_success: bool) -> dict:
    """
    Tool 2: Calculate overall security threat score
    Evaluates risk based on threat type, encryption, and attack success
    """
    base_scores = {
        'Spoofing': 80,
        'Data_Tampering': 85,
        'Jamming': 70,
        'Eavesdropping': 75,
        'Normal': 10
    }
    
    encryption_boost = {
        'AES-256-GCM': -30,
        'ChaCha20-Poly1305': -25,
        'Lightweight-Crypto': -10,
        'None': 20
    }
    
    score = base_scores.get(threat_type, 50)
    score += encryption_boost.get(encryption, 0)
    
    if attack_success:
        score += 30
    
    score = max(0, min(100, score))
    
    if score > 70:
        level = "CRITICAL"
        action = "Immediate intervention required"
    elif score > 40:
        level = "HIGH"
        action = "Priority security review needed"
    elif score > 20:
        level = "MEDIUM"
        action = "Monitor and plan upgrades"
    else:
        level = "LOW"
        action = "Maintain current security posture"
    
    return {
        "threat_score": score,
        "risk_level": level,
        "recommended_action": action,
        "requires_immediate_action": score > 70
    }


# Tool definitions for Azure OpenAI function calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "detect_signal_anomaly",
            "description": "Detect anomalies in wireless signals including jamming and interference",
            "parameters": {
                "type": "object",
                "properties": {
                    "snr_db": {"type": "number", "description": "Signal-to-noise ratio in dB"},
                    "rssi_dbm": {"type": "number", "description": "Received signal strength in dBm"},
                    "protocol": {"type": "string", "description": "Communication protocol (5G-NR, WiFi-6, LoRaWAN, NB-IoT)"}
                },
                "required": ["snr_db", "rssi_dbm", "protocol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_threat_score",
            "description": "Calculate overall security threat score for ISAC system",
            "parameters": {
                "type": "object",
                "properties": {
                    "threat_type": {"type": "string", "description": "Type of security threat detected"},
                    "encryption": {"type": "string", "description": "Encryption method used"},
                    "attack_success": {"type": "boolean", "description": "Whether attack was successful"}
                },
                "required": ["threat_type", "encryption", "attack_success"]
            }
        }
    }
]

TOOL_FUNCTIONS = {
    "detect_signal_anomaly": detect_signal_anomaly,
    "calculate_threat_score": calculate_threat_score,
}