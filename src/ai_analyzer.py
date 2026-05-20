class AIAnalyzer:

    async def analyze_incident(self, log_content: str, log_type: str):

        error_text = log_content.lower()

        root_cause = "Unknown issue"
        severity = "LOW"
        fixes = []
        apis = []

        ssl_detected = False

        # =========================
        # SSL / TLS ISSUES (FIXED)
        # =========================
        if (
            "ssl" in error_text
            or "tls" in error_text
            or "handshake" in error_text
            or "certificate" in error_text
        ):
            ssl_detected = True

            root_cause = "SSL/TLS handshake failure between systems"
            severity = "HIGH"

            fixes.extend([
                "Verify SSL certificate validity",
                "Check DataPower truststore configuration",
                "Validate backend TLS configuration",
                "Ensure certificate chain is complete",
                "Check cipher suite compatibility"
            ])

            apis.append("DataPower / Backend Connection")

        # =========================
        # Timeout Issues
        # =========================
        if "timeout" in error_text:
            root_cause = "Backend timeout issue"
            severity = "HIGH"

            fixes.extend([
                "Check backend availability",
                "Verify firewall/network",
                "Increase timeout settings"
            ])

        # =========================
        # HTTP 500 (CRITICAL override)
        # =========================
        if "500" in error_text:
            severity = "CRITICAL"
            root_cause = "Internal server error in backend service"

        # =========================
        # Connection Refused
        # =========================
        if "connection refused" in error_text:
            root_cause = "Backend connection refused"

            fixes.extend([
                "Check backend server status",
                "Verify backend port accessibility",
                "Check firewall rules"
            ])

        # =========================
        # Java Null Pointer
        # =========================
        if "nullpointerexception" in error_text:
            root_cause = "Java Null Pointer Exception"

            fixes.extend([
                "Check object initialization",
                "Validate null handling",
                "Review application stack trace"
            ])

        # =========================
        # MQ Errors
        # =========================
        if "mqrc" in error_text or "queue manager" in error_text:
            root_cause = "IBM MQ connectivity issue"

            fixes.extend([
                "Verify MQ channel status",
                "Check queue manager availability",
                "Validate MQ credentials"
            ])

        # =========================
        # DataPower
        # =========================
        if "datapower" in error_text:
            apis.append("DataPower Service")
            fixes.append("Review DataPower service logs")

        # =========================
        # APIC
        # =========================
        if "apic" in error_text:
            apis.append("API Connect Gateway")
            fixes.append("Verify APIC gateway policies")

        # =========================
        # API Detection
        # =========================
        if "/member/inquiry" in error_text:
            apis.append("/member/inquiry")

        if "/claim/details" in error_text:
            apis.append("/claim/details")

        if "/payment/process" in error_text:
            apis.append("/payment/process")

        # =========================
        # FINAL CLEANUP (IMPORTANT FIX)
        # =========================
        fixes = list(set(fixes))
        apis = list(set(apis))

        # If SSL detected, ensure it is NOT downgraded accidentally
        if ssl_detected and severity != "CRITICAL":
            severity = "HIGH"

        return {
            "root_cause": root_cause,
            "severity": severity,
            "suggested_fixes": fixes,
            "affected_apis": apis,
            "github_issue_url": None
        }