![CI](https://github.com/sonmez-lab/turkey-crypto-aml-framework/workflows/CI/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![GitHub stars](https://img.shields.io/github/stars/sonmez-lab/turkey-crypto-aml-framework?style=social)
![GitHub issues](https://img.shields.io/github/issues/sonmez-lab/turkey-crypto-aml-framework)

# Turkey Crypto AML Framework

## 👤 Author

**Osman Sonmez**

Blockchain Security Researcher | Smart Contract Auditor | Attorney at Law

Specializing in cryptocurrency compliance, blockchain law, smart contract security, and regulatory technology. Founder of Sonmez Partners Law Firm (Turkey) and Sonmez Consulting (USA).

- 🌐 Website: [osmansonmez.com](https://osmansonmez.com)
- 💼 LinkedIn: [linkedin.com/in/sonmezosman](https://www.linkedin.com/in/sonmezosman)
- 🐙 GitHub: [github.com/sonmez-lab](https://github.com/sonmez-lab)

**Focus Areas:** Blockchain Security | AML/CFT Compliance | Smart Contract Auditing | Cryptocurrency Law | OFAC Sanctions | DeFi Regulations | Token Classifications | Travel Rule | FATF Compliance

---



[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MASAK Compliant](https://img.shields.io/badge/MASAK-Compliant-green.svg)](https://masak.hmb.gov.tr/)

**Comprehensive Turkish cryptocurrency Anti-Money Laundering (AML) compliance framework, including MASAK reporting requirements, CMB licensing rules, and FATF compliance analysis.**

## 🎯 Purpose

Turkey represents a critical nexus in the global crypto ecosystem, particularly for the Turkey-Russia-Iran sanctions evasion corridor. This framework provides:

- **MASAK compliance tools** for Turkish CASPs (Crypto Asset Service Providers)
- **CMB licensing requirement analysis** under Turkey's July 2024 crypto law
- **Travel Rule implementation guidance** (February 2025 MASAK requirements)
- **Comparative analysis** with US, EU (MiCA), and FATF standards
- **Risk scoring** for Turkey-connected transactions

## 🏛️ Regulatory Context

### Law No. 7518 (July 2024)
Turkey's comprehensive crypto asset law established:
- CMB (Capital Markets Board) as the primary regulator
- Licensing requirements for CASPs
- Customer protection mandates
- AML/CFT obligations

### MASAK (Financial Crimes Investigation Board)
- Turkey's Financial Intelligence Unit
- Circular No. 29 (June 2025) - Withdrawal delays, stablecoin limits
- Travel Rule implementation (February 2025)
- Suspicious Transaction Reporting (STR) requirements

### FATF Status
- Removed from grey list: June 2024
- 5th round mutual evaluation: Ongoing
- Enhanced monitoring: None currently

## 📋 Features

### Documentation
- Complete Turkish crypto law analysis (Law No. 7518)
- MASAK AML/CFT requirements for CASPs
- CMB licensing process and requirements
- Travel Rule compliance checklist
- Iran/Russia sanctions risk factors

### Analysis Tools
- MASAK reporting threshold calculator
- Jurisdiction risk scoring
- US-Turkey-EU regulatory comparison
- FATF compliance gap analysis

### Risk Assessment
- Transaction monitoring rules for Turkey corridor
- Red flag indicators for sanctions evasion
- Customer due diligence requirements
- Enhanced due diligence triggers

## 📁 Project Structure

```
turkey-crypto-aml-framework/
├── docs/
│   ├── law-7518-analysis.md          # Crypto law deep dive
│   ├── masak-requirements.md          # MASAK AML/CFT guide
│   ├── cmb-licensing.md               # CMB CASP licensing
│   ├── travel-rule.md                 # Travel Rule implementation
│   ├── fatf-compliance.md             # FATF standards analysis
│   └── sanctions-evasion-patterns.md  # Iran/Russia corridor
├── analysis/
│   ├── us-turkey-comparison.md        # US vs Turkey AML
│   ├── eu-mica-comparison.md          # EU MiCA vs Turkey
│   ├── fatf-gap-analysis.md           # FATF compliance gaps
│   └── corridor-risk-factors.md       # Turkey-Iran-Russia risks
├── tools/
│   ├── threshold_calculator.py        # MASAK thresholds
│   ├── risk_scorer.py                 # Jurisdiction risk
│   └── compliance_checker.py          # Compliance verification
├── templates/
│   ├── str_template.md                # STR report template
│   ├── cdd_checklist.md               # CDD checklist
│   └── edd_triggers.md                # EDD trigger list
├── data/
│   ├── turkey_casp_list.json          # Licensed CASPs
│   └── masak_thresholds.json          # Reporting thresholds
└── README.md
```

## 🚀 Quick Start

### Requirements Analysis

```bash
# Check compliance requirements for a CASP
python tools/compliance_checker.py --casp-type exchange --customers 10000

# Calculate MASAK reporting thresholds
python tools/threshold_calculator.py --transaction-type withdrawal --amount 150000
```

### Risk Scoring

```bash
# Score jurisdiction risk for a transaction
python tools/risk_scorer.py --from-country TR --to-country RU --amount 50000 --crypto USDT
```

## 📊 Key Thresholds (as of 2025)

| Transaction Type | Threshold (TRY) | USD Equivalent* |
|------------------|-----------------|-----------------|
| Wire Transfer Reporting | 75,000 | ~$2,200 |
| Cash Transaction Reporting | 100,000 | ~$2,900 |
| Crypto Withdrawal Delay | Per Circular 29 | Varies |
| Travel Rule Application | 15,000 | ~$440 |

*USD equivalents approximate due to TRY volatility

## 🔗 Key Regulatory Sources

- [MASAK Official](https://masak.hmb.gov.tr/)
- [CMB Crypto Regulations](https://www.spk.gov.tr/)
- [Law No. 7518 Text](https://www.mevzuat.gov.tr/)
- [FATF Turkey Reports](https://www.fatf-gafi.org/countries/turkey)

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## ⚠️ Disclaimer

This framework is for informational purposes only and does not constitute legal advice. Consult with qualified legal counsel for specific compliance requirements.


## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🔗 Related Projects

- [ofac-crypto-screener](../ofac-crypto-screener) - OFAC sanctions screening
- [iran-sanctions-crypto-monitor](../iran-sanctions-crypto-monitor) - Iran crypto monitoring
- [russia-sanctions-tracker](../russia-sanctions-tracker) - Russia sanctions tracking
