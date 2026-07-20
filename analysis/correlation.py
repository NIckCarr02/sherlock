"""Account Correlation Analysis"""

from typing import Dict, List, Any
import logging
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class AccountCorrelator:
    """Correlate accounts across multiple platforms"""

    def __init__(self, threshold: float = 0.7):
        """
        Initialize correlator.
        
        Args:
            threshold: Correlation confidence threshold (0.0-1.0)
        """
        self.threshold = threshold
        self.correlations = []

    def correlate(self, accounts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find correlations between accounts.
        
        Args:
            accounts: List of account dictionaries
            
        Returns:
            List of correlated accounts
        """
        correlations = []
        
        for i, acc1 in enumerate(accounts):
            for acc2 in accounts[i+1:]:
                score = self._calculate_similarity(acc1, acc2)
                
                if score >= self.threshold:
                    correlations.append({
                        'account_1': self._format_account(acc1),
                        'account_2': self._format_account(acc2),
                        'confidence': score,
                        'type': self._determine_correlation_type(acc1, acc2)
                    })
        
        self.correlations = correlations
        return correlations

    def _calculate_similarity(self, acc1: Dict, acc2: Dict) -> float:
        """Calculate similarity between two accounts."""
        username1 = acc1.get('username', '').lower()
        username2 = acc2.get('username', '').lower()
        
        # Exact match
        if username1 == username2:
            return 0.95
        
        # Sequence matching
        ratio = SequenceMatcher(None, username1, username2).ratio()
        
        # Email match
        if acc1.get('email') == acc2.get('email') and acc1.get('email'):
            ratio = max(ratio, 0.85)
        
        return ratio

    def _determine_correlation_type(self, acc1: Dict, acc2: Dict) -> str:
        """Determine type of correlation."""
        if acc1.get('username') == acc2.get('username'):
            return 'username_match'
        elif acc1.get('email') == acc2.get('email'):
            return 'email_match'
        elif acc1.get('display_name') == acc2.get('display_name'):
            return 'display_name_match'
        else:
            return 'similar_username'

    def _format_account(self, account: Dict) -> str:
        """Format account for display."""
        platform = account.get('platform', 'unknown')
        username = account.get('username', 'unknown')
        return f"{platform}/{username}"

    def get_correlations(self) -> List[Dict[str, Any]]:
        """Get all correlations."""
        return self.correlations
