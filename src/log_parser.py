"""
Log Parser Module
Parses DataPower, APIC, and JAVA logs to extract relevant incident information
"""

import re
from typing import List, Dict, Optional
from datetime import datetime
from dateutil import parser as date_parser


class LogParser:
    """Parser for various log formats"""
    
    def __init__(self):
        self.log_patterns = {
            'datapower': {
                'error': r'\[error\]|\[ERROR\]',
                'timestamp': r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',
                'api': r'API:\s*([^\s]+)',
                'status_code': r'HTTP/\d\.\d\s+(\d{3})',
                'timeout': r'timeout|timed out|connection timeout',
                'backend': r'backend|upstream|target'
            },
            'apic': {
                'error': r'ERROR|SEVERE|FATAL',
                'timestamp': r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}',
                'api': r'api[:/]\s*([^\s]+)',
                'status_code': r'status[:\s]+(\d{3})',
                'gateway': r'gateway|apigw'
            },
            'java': {
                'error': r'Exception|ERROR|SEVERE',
                'timestamp': r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}',
                'stack_trace': r'at\s+[\w\.$]+\(',
                'api': r'endpoint[:/]\s*([^\s]+)|path[:/]\s*([^\s]+)',
                'connection': r'Connection|Socket|Network'
            }
        }
    
    def parse(self, log_content: str, filename: str = "") -> List[Dict]:
        """
        Parse log content and extract structured information
        
        Args:
            log_content: Raw log content
            filename: Original filename for type detection
            
        Returns:
            List of parsed log entries
        """
        log_type = self._detect_log_type(log_content, filename)
        lines = log_content.split('\n')
        
        parsed_entries = []
        current_entry = None
        
        for line in lines:
            if not line.strip():
                continue
                
            # Check if this is an error line
            if self._is_error_line(line, log_type):
                # Save previous entry if exists
                if current_entry:
                    parsed_entries.append(current_entry)
                
                # Start new entry
                current_entry = {
                    'log_type': log_type,
                    'timestamp': self._extract_timestamp(line, log_type),
                    'error_message': line.strip(),
                    'status_code': self._extract_status_code(line, log_type),
                    'api_endpoint': self._extract_api(line, log_type),
                    'raw_line': line,
                    'additional_context': []
                }
            elif current_entry:
                # Add context to current entry
                current_entry['additional_context'].append(line.strip())
        
        # Add last entry
        if current_entry:
            parsed_entries.append(current_entry)
        
        # If no errors found, create a general entry
        if not parsed_entries:
            parsed_entries.append({
                'log_type': log_type,
                'timestamp': None,
                'error_message': log_content[:500],  # First 500 chars
                'status_code': self._extract_status_code(log_content, log_type),
                'api_endpoint': self._extract_api(log_content, log_type),
                'raw_line': log_content,
                'additional_context': []
            })
        
        return parsed_entries
    
    def _detect_log_type(self, content: str, filename: str) -> str:
        """Detect log type from content or filename"""
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        if 'datapower' in filename_lower or 'dp' in filename_lower:
            return 'datapower'
        elif 'apic' in filename_lower or 'api-connect' in filename_lower:
            return 'apic'
        elif '.java' in filename_lower or 'java' in content_lower[:200]:
            return 'java'
        
        # Content-based detection
        if 'datapower' in content_lower or 'mpgw' in content_lower:
            return 'datapower'
        elif 'api gateway' in content_lower or 'apigw' in content_lower:
            return 'apic'
        elif 'exception' in content_lower or 'at java.' in content_lower:
            return 'java'
        
        return 'general'
    
    def _is_error_line(self, line: str, log_type: str) -> bool:
        """Check if line contains error indicators"""
        if log_type in self.log_patterns:
            pattern = self.log_patterns[log_type].get('error', '')
            return bool(re.search(pattern, line, re.IGNORECASE))
        return 'error' in line.lower() or 'exception' in line.lower()
    
    def _extract_timestamp(self, line: str, log_type: str) -> Optional[str]:
        """Extract timestamp from log line"""
        if log_type in self.log_patterns:
            pattern = self.log_patterns[log_type].get('timestamp', '')
            match = re.search(pattern, line)
            if match:
                try:
                    # Try to parse and standardize
                    dt = date_parser.parse(match.group(0))
                    return dt.isoformat()
                except:
                    return match.group(0)
        return None
    
    def _extract_status_code(self, text: str, log_type: str) -> Optional[int]:
        """Extract HTTP status code"""
        if log_type in self.log_patterns:
            pattern = self.log_patterns[log_type].get('status_code', '')
            match = re.search(pattern, text)
            if match:
                try:
                    return int(match.group(1))
                except:
                    pass
        
        # Generic status code pattern
        match = re.search(r'\b(4\d{2}|5\d{2})\b', text)
        if match:
            return int(match.group(1))
        
        return None
    
    def _extract_api(self, text: str, log_type: str) -> Optional[str]:
        """Extract API endpoint from log"""
        if log_type in self.log_patterns:
            pattern = self.log_patterns[log_type].get('api', '')
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Return first non-None group
                for group in match.groups():
                    if group:
                        return group
        
        # Generic API path pattern
        match = re.search(r'/[\w/-]+(?:/[\w/-]+)*', text)
        if match:
            path = match.group(0)
            # Filter out common non-API paths
            if not any(x in path for x in ['/usr/', '/var/', '/etc/', '/tmp/']):
                return path
        
        return None
    
    def analyze_patterns(self, parsed_entries: List[Dict]) -> Dict:
        """
        Analyze parsed entries for common patterns
        
        Returns:
            Dictionary with pattern analysis
        """
        if not parsed_entries:
            return {}
        
        status_codes = [e.get('status_code') for e in parsed_entries if e.get('status_code')]
        api_endpoints = [e.get('api_endpoint') for e in parsed_entries if e.get('api_endpoint')]
        
        # Check for timeout patterns
        timeout_count = sum(
            1 for e in parsed_entries 
            if 'timeout' in e.get('error_message', '').lower()
        )
        
        # Check for connection issues
        connection_issues = sum(
            1 for e in parsed_entries
            if any(word in e.get('error_message', '').lower() 
                   for word in ['connection', 'refused', 'reset', 'closed'])
        )
        
        return {
            'total_errors': len(parsed_entries),
            'status_codes': list(set(status_codes)),
            'affected_apis': list(set(api_endpoints)),
            'timeout_errors': timeout_count,
            'connection_errors': connection_issues,
            'log_types': list(set(e.get('log_type') for e in parsed_entries))
        }

# Made with Bob
