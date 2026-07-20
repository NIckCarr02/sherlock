"""Report Generation"""

from typing import Dict, List, Any
import json
from datetime import datetime
import csv
import io


class ReportGenerator:
    """Generate comprehensive OSINT reports"""

    def __init__(self):
        """Initialize report generator."""
        self.report = {}

    def generate_json_report(self, username: str, results: Dict[str, Any], 
                            correlations: List[Dict], risk_assessment: Dict) -> str:
        """Generate JSON format report.
        
        Args:
            username: Target username
            results: Results from orchestrator
            correlations: Correlated accounts
            risk_assessment: Risk scores
            
        Returns:
            JSON formatted report
        """
        report = {
            'username': username,
            'search_date': datetime.now().isoformat(),
            'results': results,
            'correlations': correlations,
            'risk_assessment': risk_assessment,
            'summary': self._generate_summary(results, correlations, risk_assessment)
        }
        return json.dumps(report, indent=2)

    def generate_csv_report(self, username: str, results: Dict[str, Any]) -> str:
        """Generate CSV format report.
        
        Args:
            username: Target username
            results: Results from orchestrator
            
        Returns:
            CSV formatted report
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Integration', 'Accounts Found', 'Breaches', 'Domains', 'Emails'])
        
        # Data rows
        for integration, result in results.items():
            accounts = len(result.get('accounts', []))
            breaches = len(result.get('breaches', []))
            domains = len(result.get('domains', []))
            emails = len(result.get('emails', []))
            
            writer.writerow([integration, accounts, breaches, domains, emails])
        
        return output.getvalue()

    def generate_html_report(self, username: str, results: Dict[str, Any],
                            risk_assessment: Dict, correlations: List[Dict]) -> str:
        """Generate HTML format report.
        
        Args:
            username: Target username
            results: Results from orchestrator
            risk_assessment: Risk scores
            correlations: Correlated accounts
            
        Returns:
            HTML formatted report
        """
        summary = self._generate_summary(results, correlations, risk_assessment)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>OSINT Report - {username}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
        .risk-critical {{ color: #d32f2f; }}
        .risk-high {{ color: #f57c00; }}
        .risk-medium {{ color: #fbc02d; }}
        .risk-low {{ color: #388e3c; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
    </style>
</head>
<body>
    <h1>OSINT Intelligence Report</h1>
    <div class="summary">
        <h2>Target: {username}</h2>
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Total Accounts Found:</strong> {summary['total_accounts_found']}</p>
        <p><strong>Total Breaches:</strong> {summary['total_breaches']}</p>
        <p><strong>Correlations:</strong> {summary['total_correlations']}</p>
        <p class="risk-{risk_assessment.get('risk_level', 'low')}">
            <strong>Risk Level: {risk_assessment.get('risk_level', 'Unknown').upper()}</strong>
        </p>
    </div>
    
    <h2>Detailed Findings</h2>
    <table>
        <tr>
            <th>Integration</th>
            <th>Accounts</th>
            <th>Breaches</th>
            <th>Domains</th>
        </tr>
"""
        
        for integration, result in results.items():
            accounts = len(result.get('accounts', []))
            breaches = len(result.get('breaches', []))
            domains = len(result.get('domains', []))
            html += f"<tr><td>{integration}</td><td>{accounts}</td><td>{breaches}</td><td>{domains}</td></tr>"
        
        html += """
    </table>
</body>
</html>
        """
        
        return html

    def _generate_summary(self, results: Dict, correlations: List, 
                         risk_assessment: Dict) -> Dict[str, Any]:
        """Generate summary statistics."""
        total_accounts = sum(len(r.get('accounts', [])) for r in results.values())
        total_breaches = sum(len(r.get('breaches', [])) for r in results.values())
        total_domains = sum(len(r.get('domains', [])) for r in results.values())
        
        return {
            'total_accounts_found': total_accounts,
            'total_breaches': total_breaches,
            'total_domains': total_domains,
            'total_correlations': len(correlations),
            'risk_assessment': risk_assessment
        }
