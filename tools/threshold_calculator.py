#!/usr/bin/env python3
"""
MASAK Threshold Calculator

Calculate reporting thresholds and compliance requirements
for cryptocurrency transactions in Turkey.
"""

import argparse
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
import json


class TransactionType(Enum):
    """Transaction types for threshold calculation."""
    WIRE_TRANSFER = "wire_transfer"
    CASH = "cash"
    CRYPTO_DEPOSIT = "crypto_deposit"
    CRYPTO_WITHDRAWAL = "crypto_withdrawal"
    CRYPTO_TRANSFER = "crypto_transfer"
    FIAT_DEPOSIT = "fiat_deposit"
    FIAT_WITHDRAWAL = "fiat_withdrawal"


@dataclass
class ThresholdResult:
    """Result of threshold calculation."""
    transaction_type: TransactionType
    amount_try: float
    amount_usd: float
    requires_reporting: bool
    reporting_type: str
    travel_rule_applies: bool
    edd_required: bool
    notes: list


class MASAKThresholdCalculator:
    """
    Calculator for MASAK AML reporting thresholds.
    
    Based on:
    - Law No. 5549
    - MASAK General Communiqué No. 5
    - Circular No. 29 (June 2025)
    """
    
    # Thresholds in TRY (as of 2025)
    THRESHOLDS = {
        "wire_transfer_reporting": 75_000,
        "cash_reporting": 100_000,
        "travel_rule": 15_000,
        "edd_trigger": 500_000,
        "large_crypto": 75_000,
    }
    
    # Approximate USD/TRY rate (volatile - update as needed)
    USD_TRY_RATE = 34.0  # As of Feb 2026
    
    def __init__(self, usd_try_rate: Optional[float] = None):
        """Initialize calculator with optional exchange rate."""
        if usd_try_rate:
            self.USD_TRY_RATE = usd_try_rate
    
    def calculate(
        self,
        transaction_type: TransactionType,
        amount_try: Optional[float] = None,
        amount_usd: Optional[float] = None,
    ) -> ThresholdResult:
        """
        Calculate threshold requirements for a transaction.
        
        Args:
            transaction_type: Type of transaction
            amount_try: Amount in Turkish Lira
            amount_usd: Amount in US Dollars (converted if TRY not provided)
            
        Returns:
            ThresholdResult with compliance requirements
        """
        # Convert amounts
        if amount_try is None and amount_usd is not None:
            amount_try = amount_usd * self.USD_TRY_RATE
        elif amount_try is not None and amount_usd is None:
            amount_usd = amount_try / self.USD_TRY_RATE
        elif amount_try is None and amount_usd is None:
            raise ValueError("Either amount_try or amount_usd must be provided")
        
        # Determine reporting requirements
        requires_reporting = False
        reporting_type = "None"
        travel_rule_applies = False
        edd_required = False
        notes = []
        
        # Check thresholds based on transaction type
        if transaction_type in (
            TransactionType.WIRE_TRANSFER,
            TransactionType.FIAT_DEPOSIT,
            TransactionType.FIAT_WITHDRAWAL,
        ):
            if amount_try >= self.THRESHOLDS["wire_transfer_reporting"]:
                requires_reporting = True
                reporting_type = "Large Transaction Report (same day)"
                notes.append(f"Exceeds wire transfer threshold of {self.THRESHOLDS['wire_transfer_reporting']:,} TRY")
        
        elif transaction_type == TransactionType.CASH:
            if amount_try >= self.THRESHOLDS["cash_reporting"]:
                requires_reporting = True
                reporting_type = "Cash Transaction Report (same day)"
                notes.append(f"Exceeds cash threshold of {self.THRESHOLDS['cash_reporting']:,} TRY")
        
        elif transaction_type in (
            TransactionType.CRYPTO_DEPOSIT,
            TransactionType.CRYPTO_WITHDRAWAL,
            TransactionType.CRYPTO_TRANSFER,
        ):
            if amount_try >= self.THRESHOLDS["large_crypto"]:
                requires_reporting = True
                reporting_type = "Large Transaction Report (same day)"
                notes.append(f"Exceeds crypto threshold of {self.THRESHOLDS['large_crypto']:,} TRY")
        
        # Travel Rule check
        if amount_try >= self.THRESHOLDS["travel_rule"]:
            travel_rule_applies = True
            notes.append(f"Travel Rule applies (≥{self.THRESHOLDS['travel_rule']:,} TRY)")
            notes.append("Must collect/transmit originator and beneficiary information")
        
        # EDD check
        if amount_try >= self.THRESHOLDS["edd_trigger"]:
            edd_required = True
            notes.append(f"Enhanced Due Diligence required (≥{self.THRESHOLDS['edd_trigger']:,} TRY)")
            notes.append("Additional source of funds verification needed")
        
        # Circular No. 29 notes for crypto
        if transaction_type == TransactionType.CRYPTO_WITHDRAWAL:
            notes.append("Per Circular No. 29: Withdrawal delays may apply for first-time or high-risk withdrawals")
        
        return ThresholdResult(
            transaction_type=transaction_type,
            amount_try=amount_try,
            amount_usd=amount_usd,
            requires_reporting=requires_reporting,
            reporting_type=reporting_type,
            travel_rule_applies=travel_rule_applies,
            edd_required=edd_required,
            notes=notes,
        )
    
    def calculate_cumulative(
        self,
        transactions: list,
        period_days: int = 1,
    ) -> ThresholdResult:
        """
        Calculate thresholds for cumulative transactions.
        
        MASAK requires cumulative analysis for structuring detection.
        """
        total_try = sum(t.get("amount_try", 0) for t in transactions)
        total_usd = total_try / self.USD_TRY_RATE
        
        # Use most common transaction type, default to crypto_transfer
        tx_types = [t.get("type") for t in transactions]
        most_common = max(set(tx_types), key=tx_types.count) if tx_types else "crypto_transfer"
        
        try:
            tx_type = TransactionType(most_common)
        except ValueError:
            tx_type = TransactionType.CRYPTO_TRANSFER
        
        result = self.calculate(tx_type, amount_try=total_try)
        
        # Add structuring warning
        if len(transactions) > 1:
            avg_amount = total_try / len(transactions)
            for threshold_name, threshold_value in self.THRESHOLDS.items():
                if 0.8 * threshold_value <= avg_amount < threshold_value:
                    result.notes.append(
                        f"⚠️ STRUCTURING ALERT: Average transaction ({avg_amount:,.0f} TRY) "
                        f"is just below {threshold_name} threshold ({threshold_value:,} TRY)"
                    )
        
        return result


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate MASAK AML reporting thresholds"
    )
    parser.add_argument(
        "--transaction-type", "-t",
        type=str,
        choices=[t.value for t in TransactionType],
        required=True,
        help="Type of transaction"
    )
    parser.add_argument(
        "--amount", "-a",
        type=float,
        required=True,
        help="Transaction amount"
    )
    parser.add_argument(
        "--currency", "-c",
        type=str,
        choices=["TRY", "USD"],
        default="TRY",
        help="Currency (default: TRY)"
    )
    parser.add_argument(
        "--rate", "-r",
        type=float,
        default=None,
        help="USD/TRY exchange rate (default: 34.0)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    calculator = MASAKThresholdCalculator(usd_try_rate=args.rate)
    
    amount_try = args.amount if args.currency == "TRY" else None
    amount_usd = args.amount if args.currency == "USD" else None
    
    result = calculator.calculate(
        TransactionType(args.transaction_type),
        amount_try=amount_try,
        amount_usd=amount_usd,
    )
    
    if args.json:
        output = {
            "transaction_type": result.transaction_type.value,
            "amount_try": result.amount_try,
            "amount_usd": result.amount_usd,
            "requires_reporting": result.requires_reporting,
            "reporting_type": result.reporting_type,
            "travel_rule_applies": result.travel_rule_applies,
            "edd_required": result.edd_required,
            "notes": result.notes,
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\n{'='*60}")
        print("MASAK Threshold Analysis")
        print(f"{'='*60}")
        print(f"Transaction Type: {result.transaction_type.value}")
        print(f"Amount: {result.amount_try:,.2f} TRY (~${result.amount_usd:,.2f} USD)")
        print(f"{'='*60}")
        print(f"Reporting Required: {'✅ YES' if result.requires_reporting else '❌ NO'}")
        if result.requires_reporting:
            print(f"  Report Type: {result.reporting_type}")
        print(f"Travel Rule Applies: {'✅ YES' if result.travel_rule_applies else '❌ NO'}")
        print(f"EDD Required: {'✅ YES' if result.edd_required else '❌ NO'}")
        
        if result.notes:
            print(f"\n📝 Notes:")
            for note in result.notes:
                print(f"  • {note}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
