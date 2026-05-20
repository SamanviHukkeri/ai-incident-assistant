"""
Demo Test Script
Demonstrates the AI Incident Resolution Assistant functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from log_parser import LogParser
from incident_reporter import IncidentReporter


def test_log_parsing():
    """Test log parsing with demo example"""
    print("=" * 60)
    print("TEST 1: Log Parsing")
    print("=" * 60)
    
    # Read demo log file
    log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'demo_example.log')
    with open(log_file, 'r') as f:
        log_content = f.read()
    
    print("\n📄 Input Log Content:")
    print("-" * 60)
    print(log_content[:300] + "...")
    
    # Parse logs
    parser = LogParser()
    parsed_logs = parser.parse(log_content, 'demo_example.log')
    
    print("\n✅ Parsed Log Entries:")
    print("-" * 60)
    for i, entry in enumerate(parsed_logs[:3], 1):
        print(f"\nEntry {i}:")
        print(f"  Type: {entry.get('log_type')}")
        print(f"  Timestamp: {entry.get('timestamp')}")
        print(f"  Status Code: {entry.get('status_code')}")
        print(f"  API: {entry.get('api_endpoint')}")
        print(f"  Error: {entry.get('error_message')[:80]}...")
    
    # Analyze patterns
    patterns = parser.analyze_patterns(parsed_logs)
    print("\n📊 Pattern Analysis:")
    print("-" * 60)
    print(f"  Total Errors: {patterns.get('total_errors')}")
    print(f"  Status Codes: {patterns.get('status_codes')}")
    print(f"  Affected APIs: {patterns.get('affected_apis')}")
    print(f"  Timeout Errors: {patterns.get('timeout_errors')}")
    print(f"  Connection Errors: {patterns.get('connection_errors')}")
    
    return parsed_logs


def test_fallback_analysis(parsed_logs):
    """Test fallback analysis (without AI)"""
    print("\n" + "=" * 60)
    print("TEST 2: Fallback Analysis (Pattern-Based)")
    print("=" * 60)
    
    # Simulate AI analyzer fallback
    from ai_analyzer import AIAnalyzer
    analyzer = AIAnalyzer(api_key="dummy_key")
    
    # Use fallback analysis
    analysis = analyzer._fallback_analysis(parsed_logs, "Demo mode - no API call")
    
    print("\n🔍 Root Cause Analysis:")
    print("-" * 60)
    print(f"  {analysis.get('root_cause')}")
    
    print("\n🔧 Suggested Fixes:")
    print("-" * 60)
    for i, fix in enumerate(analysis.get('suggested_fixes', []), 1):
        print(f"  {i}. {fix}")
    
    print("\n🎯 Affected APIs:")
    print("-" * 60)
    for api in analysis.get('affected_apis', []):
        print(f"  - {api}")
    
    print(f"\n📊 Severity: {analysis.get('severity')}")
    print(f"🎯 Confidence: {analysis.get('confidence')}")
    
    return analysis


def test_incident_report(analysis):
    """Test incident report generation"""
    print("\n" + "=" * 60)
    print("TEST 3: Incident Report Generation")
    print("=" * 60)
    
    reporter = IncidentReporter()
    
    # Generate markdown summary
    summary = reporter.generate_summary(analysis)
    print("\n📝 Markdown Summary:")
    print("-" * 60)
    print(summary)
    
    # Generate alert message
    alert = reporter.generate_alert_message(analysis)
    print("\n🚨 Alert Message:")
    print("-" * 60)
    print(alert)
    
    # Generate Slack message
    slack_msg = reporter.generate_slack_message(analysis)
    print("\n💬 Slack Message Format:")
    print("-" * 60)
    print(f"  Blocks: {len(slack_msg.get('blocks', []))} sections")
    print(f"  Color: {slack_msg.get('attachments', [{}])[0].get('color', 'N/A')}")


def test_demo_scenario():
    """Run complete demo scenario"""
    print("\n" + "=" * 60)
    print("🎬 DEMO SCENARIO: HTTP 500 Backend Timeout")
    print("=" * 60)
    
    print("\n📤 Step 1: Upload log file")
    print("   File: demo_example.log")
    print("   Content: HTTP 500 timeout from backend")
    
    # Parse logs
    parsed_logs = test_log_parsing()
    
    # Analyze
    analysis = test_fallback_analysis(parsed_logs)
    
    # Generate reports
    test_incident_report(analysis)
    
    print("\n" + "=" * 60)
    print("✅ DEMO COMPLETE")
    print("=" * 60)
    print("\nNext Steps:")
    print("  1. ✅ GitHub issue would be created automatically")
    print("  2. ✅ Alert notification would be sent")
    print("  3. ✅ Incident summary would be stored")
    print("\nExpected Results:")
    print("  ✓ Root cause identified: Backend timeout")
    print("  ✓ Fixes suggested: Check firewall, backend latency")
    print("  ✓ Affected APIs: /member/inquiry, /claim/details")
    print("  ✓ Severity: HIGH")


if __name__ == "__main__":
    print("\n" + "🤖 AI Incident Resolution Assistant - Demo Test")
    print("=" * 60)
    
    try:
        test_demo_scenario()
        print("\n✅ All tests passed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

# Made with Bob
