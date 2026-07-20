"""Risk Scoring and Assessment"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class RiskScorer:
    """Calculate risk scores for OSINT findings"""

    def __init__(self):
        """Initialize risk scorer."""
        self.scores = {}

    def calculate_account_risk(self, account: Dict[str, Any]) -> float:
        """Calculate risk score for a single account (0-10).
        
        Args:
            account: Account dictionary
            
        Returns:
            Risk score (0.0-10.0)
        """
        score = 0.0
        
        # Account found
        if account.get('found'):
            score += 1.0
        
        # Account verified
        if account.get('verified'):
            score += 2.0
        
        # High follower count indicates public profile
        followers = account.get('followers', 0)
        if followers > 10000:
            score += 1.5
        elif followers > 1000:
            score += 1.0
        elif followers > 100:
            score += 0.5
        
        # Public/private status
        if not account.get('private', False):
            score += 1.0
        
        # Normalize to 0-10 scale
        return min(score, 10.0)

    def calculate_email_risk(self, email_data: Dict[str, Any]) -> float:
        """Calculate risk score for email findings (0-10).
        
        Args:
            email_data: Email data dictionary
            
        Returns:
            Risk score (0.0-10.0)
        """
        score = 0.0
        
        # Breach count
        breaches = len(email_data.get('breaches', []))
        score += min(breaches * 2, 5.0)
        
        # Password leaked
        if email_data.get('password_leaked'):
            score += 2.0
        
        # Used in multiple sites
        sites = len(email_data.get('verified_sites', []))
        score += min(sites * 0.5, 3.0)
        
        return min(score, 10.0)

    def calculate_infrastructure_risk(self, infra_data: Dict[str, Any]) -> float:
        """Calculate risk score for infrastructure findings (0-10).
        
        Args:
            infra_data: Infrastructure data dictionary
            
        Returns:
            Risk score (0.0-10.0)
        """
        score = 0.0
        
        # Subdomains found
        subdomains = len(infra_data.get('subdomains', []))
        score += min(subdomains * 0.5, 3.0)
        
        # Vulnerabilities
        vulns = len(infra_data.get('vulnerabilities', []))
        score += min(vulns * 1.5, 5.0)
        
        # DNS issues
        if infra_data.get('dns_issues'):
            score += 1.0
        
        return min(score, 10.0)

    def calculate_overall_risk(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall risk assessment.
        
        Args:
            results: Complete results dictionary from orchestrator
            
        Returns:
            Risk assessment summary
        """
        account_risks = []
        email_risk = 0.0
        infra_risk = 0.0
        
        # Calculate individual risks
        for integration, result in results.items():
            if 'accounts' in result:
                for account in result['accounts']:
                    risk = self.calculate_account_risk(account)
                    account_risks.append(risk)
            
            if 'breaches' in result and result['breaches']:
                email_risk = max(email_risk, self.calculate_email_risk(result))
            
            if 'vulnerabilities' in result:
                infra_risk = max(infra_risk, self.calculate_infrastructure_risk(result))
        
        # Calculate average
        avg_account_risk = sum(account_risks) / len(account_risks) if account_risks else 0
        overall_risk = (avg_account_risk + email_risk + infra_risk) / 3
        
        # Determine risk level
        if overall_risk >= 7:
            risk_level = 'critical'
        elif overall_risk >= 5:
            risk_level = 'high'
        elif overall_risk >= 3:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'overall_score': round(overall_risk, 2),
            'risk_level': risk_level,
            'account_risk': round(avg_account_risk, 2),
            'email_risk': round(email_risk, 2),
            'infrastructure_risk': round(infra_risk, 2),
            'recommendations': self._generate_recommendations(risk_level)
        }

    def _generate_recommendations(self, risk_level: str) -> List[str]:
        """Generate recommendations based on risk level."""
        recommendations = {
            'critical': [
                'Immediate action required',
                'Review all compromised accounts',
                'Consider password reset across all platforms',
                'Enable two-factor authentication',
                'Monitor for further exposure'
            ],
            'high': [
                'Review exposed accounts',
                'Strengthen authentication methods',
                'Check email for breach notifications',
                'Update privacy settings on public profiles'
            ],
            'medium': [
                'Review privacy settings',
                'Consider limiting account visibility',
                'Monitor social media activity'
            ],
            'low': [
                'Continue standard security practices',
                'Regular monitoring recommended'
            ]
        }
        return recommendations.get(risk_level, [])
