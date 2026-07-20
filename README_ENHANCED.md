# 🔍 Sherlock Enhanced: Multi-Tool OSINT Framework

[![Sherlock Project](https://img.shields.io/badge/Base-Sherlock%20Project-blue?logo=github)](https://github.com/sherlock-project/sherlock)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-red)](#license)

**Hunt down social media accounts by username across 400+ networks AND integrate with 15+ professional OSINT tools for comprehensive reconnaissance.**

This enhanced version of Sherlock extends the original project with a unified framework for integrating multiple OSINT tools, providing advanced analysis, correlation, risk scoring, and professional reporting.

## 🚀 What's New in Enhanced Sherlock

### 🔗 Multi-Tool Integration Framework
Connect and orchestrate 15+ popular OSINT tools:

- **Email Intelligence**: theHarvester, holehe, h8mail
- **Social Media OSINT**: GHunt, Twint, Osintgram, Instaloader
- **Infrastructure Mapping**: OneForAll, DNSTwist, SpiderFoot, Photon
- **Advanced Scanning**: BBOT, Raccoon
- **Tracking & Analysis**: Maigret, Trape
- **AI-Powered**: Robin

### 📊 Advanced Analysis
- **Account Correlation**: Link accounts across platforms
- **Risk Scoring**: Calculate exposure risk on 0-10 scale
- **Breach Detection**: Check for data leaks and compromises
- **Pattern Analysis**: Identify connected profiles

### 📈 Professional Reporting
- **Multiple Formats**: JSON, CSV, HTML, PDF
- **Executive Summaries**: High-level findings overview
- **Risk Assessments**: Detailed vulnerability analysis
- **Recommendations**: Actionable security guidance

### 🤖 AI-Powered Features
- Dark web monitoring integration
- Automated threat intelligence
- Pattern recognition
- Correlation analysis

## 📋 Features

### Core Sherlock Features
✅ Hunt usernames across 400+ social networks  
✅ Support for multiple output formats  
✅ Proxy and TOR support  
✅ Custom site filtering  
✅ Bulk username search  

### Enhanced Features
✅ **15+ Tool Integrations** for comprehensive OSINT  
✅ **Concurrent Scanning** with ThreadPoolExecutor  
✅ **Account Correlation** across platforms  
✅ **Risk Assessment** and scoring  
✅ **Data Enrichment** from multiple sources  
✅ **Unified Reporting** in multiple formats  
✅ **Configuration Management** via YAML  
✅ **Modular Architecture** for easy extension  

## 🔧 Installation

### Requirements
- Python 3.8+
- pip or uv
- 512MB+ RAM recommended

### Quick Install

```bash
# Clone the repository
git clone https://github.com/NIckCarr02/sherlock.git
cd sherlock

# Install base Sherlock
pip install sherlock-project

# Install enhanced features
pip install -r requirements_enhanced.txt
```

### Docker

```bash
docker run -it --rm sherlock/sherlock enhanced username
```

## 💻 Usage

### Basic Sherlock (Original)
```bash
# Search for username
sherlock username

# Search multiple usernames
sherlock user1 user2 user3

# Save results to file
sherlock --output results.txt username

# CSV export
sherlock --csv username

# HTML report
sherlock --html username
```

### Enhanced OSINT

```bash
# Run all integrations
python sherlock_osint_main.py username

# Email intelligence
python sherlock_osint_main.py john@example.com --type email

# Infrastructure scan
python sherlock_osint_main.py example.com --type domain

# Generate JSON report
python sherlock_osint_main.py username --output json

# Generate HTML report
python sherlock_osint_main.py username --output html

# Verbose output
python sherlock_osint_main.py username --verbose
```

## ⚙️ Configuration

Edit `config/sherlock_osint_config.yaml` to customize integrations:

```yaml
integrations:
  enabled:
    - sherlock
    - maigret
    - theharvester
    - ghunt
    - bbot
    
  sherlock:
    enabled: true
    timeout: 60
    
  maigret:
    enabled: true
    limit: 100
    
  ghunt:
    enabled: false
    api_key: "your_api_key"

reporting:
  format: [json, csv, html]
  include_risk_scores: true
  include_correlations: true

analysis:
  correlation_threshold: 0.7
  max_concurrent_workers: 5
```

## 📊 Output Examples

### JSON Report Structure
```json
{
  "username": "techuser",
  "search_date": "2024-07-20T15:30:00",
  "results": {
    "sherlock": {
      "accounts": [
        {
          "platform": "github",
          "username": "techuser",
          "url": "https://github.com/techuser",
          "verified": true
        }
      ]
    }
  },
  "correlations": [
    {
      "account_1": "github/techuser",
      "account_2": "twitter/techuser",
      "confidence": 0.95,
      "correlation_type": "username_match"
    }
  ],
  "risk_assessment": {
    "overall_score": 6.5,
    "risk_level": "high",
    "recommendations": [
      "Review exposed accounts",
      "Strengthen authentication methods"
    ]
  }
}
```

## 🎯 Integration Details

### Email Intelligence
- Harvest emails and subdomains
- Verify email usage across platforms
- Check password breach databases

### Social Media OSINT
- Google account reconnaissance
- Twitter/X profile analysis
- Instagram account investigation

### Infrastructure Mapping
- Subdomain enumeration
- Domain permutation detection
- Attack surface mapping

### Advanced Scanning
- Recursive network scanning
- Vulnerability detection
- Port and service enumeration

## 📈 Risk Scoring System

| Score | Level | Status |
|-------|-------|--------|
| 0-2 | 🟢 Low | Minimal exposure |
| 3-5 | 🟡 Medium | Moderate risk |
| 6-7 | 🟠 High | Significant exposure |
| 8-10 | 🔴 Critical | Immediate action required |

## 🔐 Security & Ethics

### Responsible Use ⚠️
- Only analyze accounts with explicit permission
- Follow all applicable laws and regulations
- Respect privacy and data protection regulations
- Document findings with proper timestamps
- Never store sensitive data unnecessarily

## 📚 Documentation

- **[OSINT_INTEGRATIONS.md](OSINT_INTEGRATIONS.md)** - Integration details
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Usage examples

## 📄 License

MIT License © 2024 NIckCarr02

Original Sherlock Project © Siddharth Dushantha

## 🔗 Links

- **Original Project**: [Sherlock Project](https://github.com/sherlock-project/sherlock)
- **GitHub**: [NIckCarr02/sherlock](https://github.com/NIckCarr02/sherlock)

---

**Made with ❤️ for OSINT Researchers & Security Professionals**
