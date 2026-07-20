# Enhanced Usage Guide

## Quick Start with Multi-Tool OSINT

### Basic Usage

```bash
# Install enhanced Sherlock
pip install -r requirements_enhanced.txt

# Basic search (original Sherlock)
sherlock username

# Enhanced OSINT with integrations
sherlock --enhanced username
```

### Advanced Features

```bash
# Email intelligence scanning
sherlock --email-intel email@example.com

# Infrastructure reconnaissance
sherlock --infra-scan domain.com

# Social media deep dive
sherlock --social-media username

# Generate comprehensive report
sherlock --report html username

# Dark web checking
sherlock --dark-web username

# AI-powered analysis
sherlock --ai-analysis username
```

## Configuration

Edit `config/integrations.yaml` to enable/disable specific tools:

```yaml
integrations:
  enabled:
    - sherlock          # Core username search
    - maigret           # Multi-site account finder
    - theharvester      # Email/subdomain harvesting
    - ghunt             # Google account OSINT
    - twint             # Twitter scraping
    - osintgram         # Instagram analysis
    - oneforall         # Subdomain enumeration
    - bbot              # Recursive scanning
```

## Output Formats

- **JSON**: Full machine-readable results
- **CSV**: Spreadsheet-compatible format
- **PDF**: Professional report (requires additional setup)
- **HTML**: Interactive web report

## Integration Status

| Tool | Status | Type |
|------|--------|------|
| Sherlock | ✅ Core | Username Search |
| Maigret | 🔧 Integration | Cross-Site Account |
| theHarvester | 🔧 Integration | Email/Subdomain |
| holehe | 🔧 Integration | Email Verification |
| GHunt | 🔧 Integration | Google OSINT |
| Twint | 🔧 Integration | Twitter Scraping |
| Osintgram | 🔧 Integration | Instagram OSINT |
| OneForAll | 🔧 Integration | Subdomain Enum |
| DNSTwist | 🔧 Integration | Typosquatting |
| SpiderFoot | 🔧 Integration | Attack Surface |
| BBOT | 🔧 Integration | Recursive Scanner |
| Raccoon | 🔧 Integration | Recon Scanner |
| Robin | 🔧 Integration | Dark Web AI |

## Example Workflows

### Complete Target Assessment

```bash
sherlock --enhanced --report html --correlate john_doe
```

This will:
1. Search across all enabled integrations
2. Correlate accounts on different platforms
3. Calculate risk scores
4. Generate HTML report

### Email-Focused Investigation

```bash
sherlock --email-intel john@example.com --report csv
```

This will:
1. Run email intelligence modules
2. Check for breaches
3. Verify email usage across platforms
4. Export as CSV

### Infrastructure Mapping

```bash
sherlock --infra-scan example.com --report json
```

This will:
1. Enumerate subdomains
2. Detect typosquatting
3. Map attack surface
4. Export as JSON

## Risk Scoring

Risk scores are calculated based on:

- **Account Visibility**: Public/verified accounts = higher risk
- **Follower Count**: Large following = higher exposure
- **Breach History**: Past breaches significantly increase risk
- **Data Exposure**: Email leaks, password breaches
- **Infrastructure Issues**: Open ports, vulnerable services

## Responsible Use

⚠️ **Important**: 
- Use only on accounts you own or have explicit permission to analyze
- Follow all applicable laws and regulations
- Respect privacy and ethical guidelines
- Document all findings with timestamps
- Never store sensitive personal data unnecessarily

## Support & Contributing

- GitHub Issues: Report bugs and request features
- Documentation: Full API docs in `/docs`
- Contributing: See CONTRIBUTING.md

---

*Last Updated: July 2024*
