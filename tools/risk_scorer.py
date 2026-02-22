#!/usr/bin/env python3
"""
Jurisdiction Risk Scorer

Score transaction and customer risk based on Turkey-specific
AML factors and the Turkey-Russia-Iran corridor analysis.
"""

import argparse
import json
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class RiskLevel(Enum):
    """Risk level classifications."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


class CountryRisk(Enum):
    """Country risk classifications for AML purposes."""
    PROHIBITED = "prohibited"      # OFAC comprehensive sanctions
    HIGH_RISK = "high_risk"        # FATF high-risk, partial sanctions
    ELEVATED = "elevated"          # Significant AML concerns
    STANDARD = "standard"          # Normal risk
    LOW = "low"                    # Low-risk jurisdictions


@dataclass
class RiskScore:
    """Result of risk scoring."""
    overall_level: RiskLevel
    score: int  # 0-100
    country_risk: CountryRisk
    factors: List[str]
    recommendations: List[str]
    edd_required: bool
    block_recommended: bool


class TurkeyCorridorRiskScorer:
    """
    Risk scorer specialized for Turkey and the Turkey-Russia-Iran
    sanctions evasion corridor.
    
    Based on:
    - FATF country risk assessments
    - OFAC designations and guidance
    - Turkey-specific AML patterns
    - Iran/Russia sanctions evasion indicators
    """
    
    # Country risk classifications
    COUNTRY_RISK = {
        # Prohibited/Comprehensive Sanctions
        "IR": CountryRisk.PROHIBITED,   # Iran
        "KP": CountryRisk.PROHIBITED,   # North Korea
        "SY": CountryRisk.PROHIBITED,   # Syria
        "CU": CountryRisk.PROHIBITED,   # Cuba (limited)
        
        # High Risk (FATF + Partial Sanctions)
        "RU": CountryRisk.HIGH_RISK,    # Russia
        "BY": CountryRisk.HIGH_RISK,    # Belarus
        "MM": CountryRisk.HIGH_RISK,    # Myanmar
        "VE": CountryRisk.HIGH_RISK,    # Venezuela
        "YE": CountryRisk.HIGH_RISK,    # Yemen
        
        # FATF Grey List / Elevated
        "AE": CountryRisk.ELEVATED,     # UAE (high crypto activity)
        "PK": CountryRisk.ELEVATED,     # Pakistan
        "NG": CountryRisk.ELEVATED,     # Nigeria
        "PH": CountryRisk.ELEVATED,     # Philippines
        
        # Turkey - Special handling
        "TR": CountryRisk.STANDARD,     # Turkey itself
        
        # Standard Risk (most countries)
        # ... default to STANDARD
        
        # Low Risk
        "US": CountryRisk.LOW,
        "GB": CountryRisk.LOW,
        "DE": CountryRisk.LOW,
        "FR": CountryRisk.LOW,
        "JP": CountryRisk.LOW,
        "SG": CountryRisk.LOW,
        "CH": CountryRisk.LOW,
    }
    
    # High-risk crypto types
    HIGH_RISK_CRYPTO = {
        "XMR": 40,   # Monero - privacy coin
        "ZEC": 30,   # Zcash - shielded transactions
        "DASH": 25,  # Dash - mixing features
        "USDT": 15,  # Tether - commonly used in evasion
    }
    
    # Risk weights
    RISK_WEIGHTS = {
        "prohibited_country": 100,
        "high_risk_country": 50,
        "elevated_country": 25,
        "large_amount": 20,
        "privacy_coin": 40,
        "new_relationship": 15,
        "complex_structure": 20,
        "rapid_movement": 25,
        "no_economic_purpose": 30,
        "turkey_corridor": 35,
    }
    
    def __init__(self):
        """Initialize the risk scorer."""
        pass
    
    def get_country_risk(self, country_code: str) -> CountryRisk:
        """Get risk classification for a country."""
        return self.COUNTRY_RISK.get(
            country_code.upper(),
            CountryRisk.STANDARD
        )
    
    def score_transaction(
        self,
        from_country: str,
        to_country: str,
        amount_usd: float,
        crypto_type: str = "BTC",
        is_new_customer: bool = False,
        days_since_deposit: int = 30,
        has_economic_purpose: bool = True,
    ) -> RiskScore:
        """
        Score a transaction for risk.
        
        Args:
            from_country: Source country code (ISO 3166-1 alpha-2)
            to_country: Destination country code
            amount_usd: Transaction amount in USD
            crypto_type: Cryptocurrency type
            is_new_customer: Whether customer is new (<30 days)
            days_since_deposit: Days since funds were deposited
            has_economic_purpose: Whether transaction has clear purpose
            
        Returns:
            RiskScore with assessment
        """
        score = 0
        factors = []
        recommendations = []
        edd_required = False
        block_recommended = False
        
        # Assess country risk
        from_risk = self.get_country_risk(from_country)
        to_risk = self.get_country_risk(to_country)
        
        # Higher of the two country risks
        country_risk = from_risk if from_risk.value < to_risk.value else to_risk
        
        # Country risk scoring
        if country_risk == CountryRisk.PROHIBITED:
            score += self.RISK_WEIGHTS["prohibited_country"]
            factors.append(f"⛔ PROHIBITED: Transaction involves sanctioned jurisdiction ({from_country}/{to_country})")
            recommendations.append("BLOCK: Transaction involves comprehensively sanctioned jurisdiction")
            block_recommended = True
            edd_required = True
        
        elif country_risk == CountryRisk.HIGH_RISK:
            score += self.RISK_WEIGHTS["high_risk_country"]
            factors.append(f"🔴 HIGH RISK: Transaction involves high-risk jurisdiction ({from_country}/{to_country})")
            recommendations.append("Enhanced due diligence required")
            recommendations.append("Verify source and destination of funds")
            edd_required = True
        
        elif country_risk == CountryRisk.ELEVATED:
            score += self.RISK_WEIGHTS["elevated_country"]
            factors.append(f"🟠 ELEVATED: Transaction involves elevated-risk jurisdiction ({from_country}/{to_country})")
            recommendations.append("Additional monitoring recommended")
        
        # Turkey corridor check (Turkey + Iran/Russia)
        corridor_countries = {"TR", "IR", "RU", "AE", "BY"}
        if from_country.upper() in corridor_countries and to_country.upper() in corridor_countries:
            if {from_country.upper(), to_country.upper()} & {"IR", "RU"}:
                score += self.RISK_WEIGHTS["turkey_corridor"]
                factors.append("🚨 CORRIDOR ALERT: Transaction pattern matches Turkey-Iran-Russia sanctions evasion corridor")
                recommendations.append("Manual review required - corridor transaction")
                edd_required = True
        
        # Crypto type risk
        if crypto_type.upper() in self.HIGH_RISK_CRYPTO:
            crypto_score = self.HIGH_RISK_CRYPTO[crypto_type.upper()]
            score += crypto_score
            factors.append(f"💰 HIGH-RISK CRYPTO: {crypto_type} has elevated privacy/evasion risk")
            if crypto_type.upper() == "XMR":
                recommendations.append("Monero transactions cannot be traced - extra caution required")
        
        # Amount risk
        if amount_usd >= 100000:
            score += self.RISK_WEIGHTS["large_amount"]
            factors.append(f"💵 LARGE AMOUNT: ${amount_usd:,.0f} exceeds $100,000 threshold")
            edd_required = True
        elif amount_usd >= 10000:
            score += self.RISK_WEIGHTS["large_amount"] // 2
            factors.append(f"💵 SIGNIFICANT AMOUNT: ${amount_usd:,.0f}")
        
        # New customer risk
        if is_new_customer:
            score += self.RISK_WEIGHTS["new_relationship"]
            factors.append("👤 NEW CUSTOMER: Relationship less than 30 days")
            recommendations.append("Verify customer identity and source of funds")
        
        # Rapid movement risk
        if days_since_deposit < 3:
            score += self.RISK_WEIGHTS["rapid_movement"]
            factors.append(f"⚡ RAPID MOVEMENT: Funds withdrawn {days_since_deposit} days after deposit")
            recommendations.append("Review for potential layering activity")
        
        # Economic purpose
        if not has_economic_purpose:
            score += self.RISK_WEIGHTS["no_economic_purpose"]
            factors.append("❓ NO CLEAR PURPOSE: Transaction lacks apparent economic rationale")
            recommendations.append("Request documentation of transaction purpose")
        
        # Determine overall risk level
        if score >= 80 or block_recommended:
            overall_level = RiskLevel.CRITICAL
        elif score >= 50:
            overall_level = RiskLevel.HIGH
        elif score >= 30:
            overall_level = RiskLevel.MEDIUM
        elif score >= 15:
            overall_level = RiskLevel.LOW
        else:
            overall_level = RiskLevel.MINIMAL
        
        # Add general recommendations based on level
        if overall_level in (RiskLevel.CRITICAL, RiskLevel.HIGH):
            if "Manual review" not in str(recommendations):
                recommendations.append("Manual compliance review recommended before processing")
        
        return RiskScore(
            overall_level=overall_level,
            score=min(score, 100),
            country_risk=country_risk,
            factors=factors,
            recommendations=recommendations,
            edd_required=edd_required,
            block_recommended=block_recommended,
        )


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Score transaction risk for Turkey corridor"
    )
    parser.add_argument("--from-country", "-f", type=str, required=True, help="Source country code")
    parser.add_argument("--to-country", "-t", type=str, required=True, help="Destination country code")
    parser.add_argument("--amount", "-a", type=float, required=True, help="Amount in USD")
    parser.add_argument("--crypto", "-c", type=str, default="BTC", help="Crypto type (default: BTC)")
    parser.add_argument("--new-customer", action="store_true", help="Is new customer")
    parser.add_argument("--days-since-deposit", type=int, default=30, help="Days since deposit")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    scorer = TurkeyCorridorRiskScorer()
    result = scorer.score_transaction(
        from_country=args.from_country,
        to_country=args.to_country,
        amount_usd=args.amount,
        crypto_type=args.crypto,
        is_new_customer=args.new_customer,
        days_since_deposit=args.days_since_deposit,
    )
    
    if args.json:
        output = {
            "overall_level": result.overall_level.value,
            "score": result.score,
            "country_risk": result.country_risk.value,
            "factors": result.factors,
            "recommendations": result.recommendations,
            "edd_required": result.edd_required,
            "block_recommended": result.block_recommended,
        }
        print(json.dumps(output, indent=2))
    else:
        level_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢",
            "minimal": "⚪",
        }
        
        print(f"\n{'='*60}")
        print("Turkey Corridor Risk Assessment")
        print(f"{'='*60}")
        print(f"Transaction: {args.from_country} → {args.to_country}")
        print(f"Amount: ${args.amount:,.2f} USD ({args.crypto})")
        print(f"{'='*60}")
        print(f"Risk Level: {level_emoji[result.overall_level.value]} {result.overall_level.value.upper()}")
        print(f"Risk Score: {result.score}/100")
        print(f"Country Risk: {result.country_risk.value}")
        print(f"EDD Required: {'✅ YES' if result.edd_required else '❌ NO'}")
        print(f"Block Recommended: {'🛑 YES' if result.block_recommended else '❌ NO'}")
        
        if result.factors:
            print(f"\n📋 Risk Factors:")
            for factor in result.factors:
                print(f"  {factor}")
        
        if result.recommendations:
            print(f"\n💡 Recommendations:")
            for rec in result.recommendations:
                print(f"  • {rec}")
        
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
