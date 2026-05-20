class AIAnalyzer:

    async def analyze_incident(self, log_content: str, log_type: str):

        error_text = log_content.lower()

        root_cause = "Unknown issue"
        severity = "LOW"
        fixes = []
        apis = []

        # ============================================
        # Backend Timeout Issues
        # ============================================
        if "timeout" in error_text:

            root_cause = "Backend timeout issue"

            severity = "CRITICAL"

            fixes.extend([
                "Check backend availability",
                "Verify firewall/network",
                "Increase timeout settings"
            ])

            apis.append("/member/inquiry")

        # ============================================
        # SSL / Certificate Issues
        # ============================================
        elif "ssl" in error_text or "certificate" in error_text:

            root_cause = "SSL certificate validation failure"

            severity = "HIGH"

            fixes.extend([
                "Verify backend SSL certificate",
                "Import certificate into DataPower truststore",
                "Check certificate expiry",
                "Validate TLS handshake configuration"
            ])

            apis.append("SECURE_BACKEND_API")

        # ============================================
        # APIC Gateway Timeout
        # ============================================
        elif "gateway timeout" in error_text or "unable to reach backend" in error_text:

            root_cause = "Backend service unreachable from APIC gateway"

            severity = "CRITICAL"

            fixes.extend([
                "Check backend service availability",
                "Validate APIC endpoint configuration",
                "Verify firewall connectivity",
                "Increase timeout thresholds"
            ])

            apis.append("/apic/gateway")

        # ============================================
        # Java Heap Memory Issues
        # ============================================
        elif "outofmemoryerror" in error_text or "java heap space" in error_text:

            root_cause = "Java heap memory exhaustion"

            severity = "CRITICAL"

            fixes.extend([
                "Increase JVM heap size using -Xmx",
                "Analyze memory leaks",
                "Restart impacted application",
                "Review heap dump for analysis"
            ])

            apis.append("JAVA_APPLICATION")

        # ============================================
        # Database Connectivity Issues
        # ============================================
        elif "jdbc" in error_text or "database connection refused" in error_text:

            root_cause = "Database connectivity failure"

            severity = "HIGH"

            fixes.extend([
                "Verify database availability",
                "Check JDBC configuration",
                "Validate DB credentials",
                "Check firewall/network connectivity"
            ])

            apis.append("DATABASE_SERVICE")

        # ============================================
        # JWT Authentication Issues
        # ============================================
        elif "jwt" in error_text or "token validation failed" in error_text:

            root_cause = "JWT authentication failure"

            severity = "HIGH"

            fixes.extend([
                "Verify JWT signing certificate",
                "Validate token expiration",
                "Check issuer/audience configuration",
                "Reissue authentication token"
            ])

            apis.append("/auth/token")

        # ============================================
        # Kubernetes Pod Crash
        # ============================================
        elif "crashloopbackoff" in error_text or "container restarted" in error_text:

            root_cause = "Kubernetes pod crash loop"

            severity = "CRITICAL"

            fixes.extend([
                "Check pod logs",
                "Verify container startup configuration",
                "Check resource limits",
                "Inspect Kubernetes events"
            ])

            apis.append("KUBERNETES_CLUSTER")

        # ============================================
        # IBM MQ Issues
        # ============================================
        elif "mqrc_q_mgr_not_available" in error_text or "mq connection failed" in error_text:

            root_cause = "IBM MQ Queue Manager unavailable"

            severity = "HIGH"

            fixes.extend([
                "Verify Queue Manager status",
                "Check MQ channel configuration",
                "Validate MQ network connectivity",
                "Restart MQ services if needed"
            ])

            apis.append("IBM_MQ")

        # ============================================
        # Generic Internal Server Errors
        # ============================================
        elif "500" in error_text or "internal server error" in error_text:

            root_cause = "Internal server application failure"

            severity = "HIGH"

            fixes.extend([
                "Check application logs",
                "Validate backend service health",
                "Restart application services",
                "Inspect recent deployments"
            ])

            apis.append("/internal/api")

        # ============================================
        # Default Unknown Issue
        # ============================================
        else:

            fixes.extend([
                "Review complete application logs",
                "Verify infrastructure health",
                "Check backend connectivity"
            ])

        return {
            "root_cause": root_cause,
            "severity": severity,
            "suggested_fixes": fixes,
            "affected_apis": apis,
            "github_issue_url": None
        }