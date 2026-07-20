"""OSINT Orchestrator - Manages multiple integrations"""

from typing import Dict, List, Any
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class OSINTOrchestrator:
    """Orchestrates multiple OSINT integrations"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize orchestrator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.integrations = {}
        self.results = {}
        self.correlations = []
        self.risk_scores = {}

    def register_integration(self, name: str, integration):
        """Register an OSINT integration.
        
        Args:
            name: Integration name
            integration: Integration instance
        """
        if integration.enabled:
            self.integrations[name] = integration
            logger.info(f"Registered integration: {name}")
        else:
            logger.debug(f"Integration {name} is disabled")

    def search_concurrent(self, query: str, max_workers: int = 5) -> Dict[str, Any]:
        """Execute concurrent searches across all integrations.
        
        Args:
            query: Search query
            max_workers: Maximum concurrent threads
            
        Returns:
            Aggregated results from all integrations
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(integration.search, query): name 
                for name, integration in self.integrations.items()
            }
            
            for future in as_completed(futures):
                integration_name = futures[future]
                try:
                    result = future.result()
                    results[integration_name] = result
                    logger.info(f"[{integration_name}] Search completed")
                except Exception as e:
                    logger.error(f"[{integration_name}] Search failed: {str(e)}")
                    results[integration_name] = {'error': str(e)}
        
        self.results = results
        return results

    def correlate_accounts(self) -> List[Dict[str, Any]]:
        """Find correlations between accounts across platforms.
        
        Returns:
            List of correlated accounts
        """
        correlations = []
        accounts_by_platform = {}
        
        # Collect all accounts
        for integration_name, result in self.results.items():
            accounts = result.get('accounts', [])
            for account in accounts:
                platform = account.get('platform', integration_name)
                if platform not in accounts_by_platform:
                    accounts_by_platform[platform] = []
                accounts_by_platform[platform].append(account)
        
        # Find correlations
        platforms = list(accounts_by_platform.keys())
        for i, platform1 in enumerate(platforms):
            for platform2 in platforms[i+1:]:
                accounts1 = accounts_by_platform[platform1]
                accounts2 = accounts_by_platform[platform2]
                
                for acc1 in accounts1:
                    for acc2 in accounts2:
                        correlation = self._calculate_correlation(acc1, acc2)
                        if correlation['confidence'] > 0.7:
                            correlations.append({
                                'account_1': f"{platform1}/{acc1.get('username', 'unknown')}",
                                'account_2': f"{platform2}/{acc2.get('username', 'unknown')}",
                                'confidence': correlation['confidence'],
                                'correlation_type': correlation['type']
                            })
        
        self.correlations = correlations
        return correlations

    def _calculate_correlation(self, acc1: Dict, acc2: Dict) -> Dict[str, Any]:
        """Calculate correlation between two accounts."""
        correlation_score = 0.0
        correlation_type = 'unknown'
        
        # Username match
        if acc1.get('username') == acc2.get('username'):
            correlation_score = 0.95
            correlation_type = 'username_match'
        
        # Email match
        elif acc1.get('email') == acc2.get('email'):
            correlation_score = 0.85
            correlation_type = 'email_match'
        
        # Display name similarity
        elif acc1.get('display_name') == acc2.get('display_name'):
            correlation_score = 0.75
            correlation_type = 'display_name_match'
        
        return {
            'confidence': correlation_score,
            'type': correlation_type
        }

    def calculate_risk_scores(self) -> Dict[str, float]:
        """Calculate risk scores for findings.
        
        Returns:
            Risk scores by platform
        """
        risk_scores = {}
        
        for integration_name, result in self.results.items():
            accounts = result.get('accounts', [])
            breaches = result.get('breaches', [])
            
            # Base score
            score = 0.0
            
            # Account found = risk increase
            if accounts:
                score += 0.3
            
            # Verified account = higher risk
            for account in accounts:
                if account.get('verified'):
                    score += 0.2
            
            # Breaches = high risk
            if breaches:
                score += 0.4 * len(breaches)
            
            # Normalize score to 0-10
            score = min(score * 10, 10.0)
            risk_scores[integration_name] = score
        
        self.risk_scores = risk_scores
        return risk_scores

    def generate_report(self, username: str, format: str = 'json') -> str:
        """Generate comprehensive OSINT report.
        
        Args:
            username: Target username
            format: Report format (json, csv, html)
            
        Returns:
            Formatted report
        """
        report = {
            'username': username,
            'search_date': datetime.now().isoformat(),
            'integrations_used': list(self.integrations.keys()),
            'results': self.results,
            'correlations': self.correlations,
            'risk_scores': self.risk_scores,
            'summary': {
                'total_accounts_found': sum(
                    len(r.get('accounts', [])) for r in self.results.values()
                ),
                'total_breaches': sum(
                    len(r.get('breaches', [])) for r in self.results.values()
                ),
                'total_correlations': len(self.correlations),
                'average_risk_score': sum(self.risk_scores.values()) / len(self.risk_scores) if self.risk_scores else 0
            }
        }
        
        if format == 'json':
            return json.dumps(report, indent=2)
        elif format == 'csv':
            return self._format_csv(report)
        elif format == 'html':
            return self._format_html(report)
        else:
            return json.dumps(report, indent=2)

    def _format_csv(self, report: Dict) -> str:
        """Format report as CSV."""
        lines = [
            'Integration,Accounts Found,Breaches,Risk Score',
        ]
        for integration, risk_score in self.risk_scores.items():
            result = self.results.get(integration, {})
            accounts = len(result.get('accounts', []))
            breaches = len(result.get('breaches', []))
            lines.append(f'{integration},{accounts},{breaches},{risk_score:.2f}')
        return '\n'.join(lines)

    def _format_html(self, report: Dict) -> str:
        """Format report as HTML."""
        html = f"""
        <html>
        <head><title>OSINT Report - {report['username']}</title></head>
        <body>
        <h1>OSINT Intelligence Report</h1>
        <p><strong>Username:</strong> {report['username']}</p>
        <p><strong>Date:</strong> {report['search_date']}</p>
        <h2>Summary</h2>
        <ul>
        <li>Total Accounts Found: {report['summary']['total_accounts_found']}</li>
        <li>Total Breaches: {report['summary']['total_breaches']}</li>
        <li>Correlations: {report['summary']['total_correlations']}</li>
        </ul>
        </body>
        </html>
        """
        return html

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all findings.
        
        Returns:
            Summary dictionary
        """
        total_accounts = sum(
            len(r.get('accounts', [])) for r in self.results.values()
        )
        total_integrations = len(self.integrations)
        successful_integrations = len([r for r in self.results.values() if 'error' not in r])
        
        return {
            'total_integrations': total_integrations,
            'successful_integrations': successful_integrations,
            'total_accounts_found': total_accounts,
            'total_correlations': len(self.correlations),
            'avg_risk_score': sum(self.risk_scores.values()) / len(self.risk_scores) if self.risk_scores else 0
        }
