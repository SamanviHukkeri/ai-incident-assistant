"""
Incident Reporter Module
Generates formatted incident summaries and reports
"""

from typing import Dict, List
from datetime import datetime
import json


class IncidentReporter:
    """Generate incident reports and summaries"""
    
    def generate_summary(self, analysis: Dict) -> str:
        """
        Generate a formatted incident summary
        
        Args:
            analysis: Analysis results from AI analyzer
            
        Returns:
            Formatted markdown summary
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        summary = f"""# Incident Report
**Generated:** {timestamp}

## 🔍 Root Cause Analysis
{analysis.get('root_cause', 'Unknown')}

**Severity:** `{analysis.get('severity', 'MEDIUM')}`
**Confidence:** `{analysis.get('confidence', 'MEDIUM')}`

## 🔧 Suggested Fixes
"""
        
        fixes = analysis.get('suggested_fixes', [])
        for i, fix in enumerate(fixes, 1):
            summary += f"{i}. {fix}\n"
        
        summary += "\n## 🎯 Affected APIs\n"
        affected_apis = analysis.get('affected_apis', [])
        if affected_apis:
            for api in affected_apis:
                summary += f"- `{api}`\n"
        else:
            summary += "- No specific APIs identified\n"
        
        summary += "\n## ✅ Additional Checks\n"
        checks = analysis.get('additional_checks', [])
        if checks:
            for check in checks:
                summary += f"- [ ] {check}\n"
        
        # Add AI error if present (fallback mode)
        if 'ai_error' in analysis:
            summary += f"\n---\n*Note: AI analysis unavailable. Using fallback analysis.*\n"
        
        return summary
    
    def generate_alert_message(self, analysis: Dict) -> str:
        """
        Generate a concise alert message for notifications
        
        Args:
            analysis: Analysis results
            
        Returns:
            Short alert message
        """
        severity = analysis.get('severity', 'MEDIUM')
        root_cause = analysis.get('root_cause', 'Unknown issue')
        affected_apis = analysis.get('affected_apis', [])
        
        emoji = {
            'CRITICAL': '🚨',
            'HIGH': '⚠️',
            'MEDIUM': '⚡',
            'LOW': 'ℹ️'
        }.get(severity, '⚡')
        
        message = f"{emoji} **{severity} Incident Detected**\n\n"
        message += f"**Issue:** {root_cause[:100]}\n"
        
        if affected_apis:
            message += f"**Affected APIs:** {', '.join(affected_apis[:3])}"
            if len(affected_apis) > 3:
                message += f" (+{len(affected_apis) - 3} more)"
        
        return message
    
    def generate_json_report(self, analysis: Dict, parsed_logs: List[Dict] = None) -> str:
        """
        Generate JSON format report
        
        Args:
            analysis: Analysis results
            parsed_logs: Optional parsed log entries
            
        Returns:
            JSON string
        """
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'analysis': analysis,
            'metadata': {
                'total_errors': len(parsed_logs) if parsed_logs else 0,
                'log_types': list(set(log.get('log_type') for log in parsed_logs)) if parsed_logs else []
            }
        }
        
        return json.dumps(report, indent=2)
    
    def generate_email_body(self, analysis: Dict) -> str:
        """
        Generate email-friendly incident report
        
        Args:
            analysis: Analysis results
            
        Returns:
            HTML email body
        """
        severity_color = {
            'CRITICAL': '#dc3545',
            'HIGH': '#fd7e14',
            'MEDIUM': '#ffc107',
            'LOW': '#28a745'
        }.get(analysis.get('severity', 'MEDIUM'), '#ffc107')
        
        html = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .header {{ background-color: {severity_color}; color: white; padding: 20px; }}
        .content {{ padding: 20px; }}
        .section {{ margin-bottom: 20px; }}
        .api-list {{ background-color: #f8f9fa; padding: 10px; border-left: 3px solid {severity_color}; }}
        .fix-item {{ margin: 10px 0; padding: 10px; background-color: #e9ecef; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Incident Alert - {analysis.get('severity', 'MEDIUM')} Severity</h1>
        <p>Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}</p>
    </div>
    
    <div class="content">
        <div class="section">
            <h2>Root Cause</h2>
            <p>{analysis.get('root_cause', 'Unknown')}</p>
        </div>
        
        <div class="section">
            <h2>Suggested Fixes</h2>
"""
        
        for i, fix in enumerate(analysis.get('suggested_fixes', []), 1):
            html += f'            <div class="fix-item">{i}. {fix}</div>\n'
        
        html += """        </div>
        
        <div class="section">
            <h2>Affected APIs</h2>
            <div class="api-list">
"""
        
        affected_apis = analysis.get('affected_apis', [])
        if affected_apis:
            for api in affected_apis:
                html += f'                <div>• {api}</div>\n'
        else:
            html += '                <div>No specific APIs identified</div>\n'
        
        html += """            </div>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_slack_message(self, analysis: Dict) -> Dict:
        """
        Generate Slack-formatted message
        
        Args:
            analysis: Analysis results
            
        Returns:
            Slack message payload
        """
        severity = analysis.get('severity', 'MEDIUM')
        color = {
            'CRITICAL': 'danger',
            'HIGH': 'warning',
            'MEDIUM': 'warning',
            'LOW': 'good'
        }.get(severity, 'warning')
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 {severity} Incident Detected"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Root Cause:*\n{analysis.get('root_cause', 'Unknown')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Severity:*\n{severity}"
                    }
                ]
            }
        ]
        
        # Add affected APIs
        affected_apis = analysis.get('affected_apis', [])
        if affected_apis:
            api_text = "\n".join([f"• `{api}`" for api in affected_apis[:5]])
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Affected APIs:*\n{api_text}"
                }
            })
        
        # Add suggested fixes
        fixes = analysis.get('suggested_fixes', [])
        if fixes:
            fix_text = "\n".join([f"{i}. {fix}" for i, fix in enumerate(fixes[:3], 1)])
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Suggested Fixes:*\n{fix_text}"
                }
            })
        
        return {
            "blocks": blocks,
            "attachments": [
                {
                    "color": color,
                    "text": "Incident requires immediate attention"
                }
            ]
        }

# Made with Bob
