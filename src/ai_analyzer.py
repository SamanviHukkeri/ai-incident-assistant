class AIAnalyzer:

    async def analyze_incident(self, log_content: str, log_type: str):

        error_text = log_content.lower()

        root_cause = "Unknown issue"
        severity = "LOW"
        fixes = []
        apis = []
        timeline = []

        if "timeout" in error_text:

            root_cause = "Backend timeout issue"
            severity = "CRITICAL"

            fixes.extend([
                "Check backend availability",
                "Verify firewall/network",
                "Increase timeout settings"
            ])

            apis.append("/member/inquiry")

            timeline.extend([
                "Step 1: Backend timeout detected",
                "Step 2: API gateway waited for backend response",
                "Step 3: Backend response exceeded timeout threshold",
                "Step 4: API request failed with timeout or HTTP 500",
                "Step 5: Support team should verify backend latency and network path"
            ])

        elif "ssl" in error_text or "certificate" in error_text or "handshake" in error_text:

            root_cause = "SSL/TLS certificate validation failure"
            severity = "HIGH"

            fixes.extend([
                "Verify backend SSL certificate",
                "Import certificate into DataPower truststore",
                "Check certificate expiry",
                "Validate TLS handshake configuration"
            ])

            apis.append("SECURE_BACKEND_API")

            timeline.extend([
                "Step 1: SSL/TLS handshake failure detected",
                "Step 2: DataPower attempted secure backend connection",
                "Step 3: Certificate or TLS validation failed",
                "Step 4: Backend API call was blocked",
                "Step 5: Support team should verify truststore and certificate chain"
            ])

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

            timeline.extend([
                "Step 1: APIC gateway attempted backend call",
                "Step 2: Backend service did not respond",
                "Step 3: Gateway timeout was triggered",
                "Step 4: Client request failed",
                "Step 5: Support team should validate APIC backend routing"
            ])

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

            timeline.extend([
                "Step 1: Java application memory usage increased",
                "Step 2: JVM heap reached maximum allocation",
                "Step 3: OutOfMemoryError was thrown",
                "Step 4: Application request processing failed",
                "Step 5: Support team should review heap dump and memory settings"
            ])

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

            timeline.extend([
                "Step 1: Application attempted database connection",
                "Step 2: JDBC connection request failed",
                "Step 3: Database service was unavailable or refused connection",
                "Step 4: Backend transaction failed",
                "Step 5: Support team should verify DB health and JDBC configuration"
            ])

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

            timeline.extend([
                "Step 1: API request received with JWT token",
                "Step 2: Token validation was triggered",
                "Step 3: JWT signature or claims validation failed",
                "Step 4: Authentication request was rejected",
                "Step 5: Support team should verify token issuer, audience, and signing keys"
            ])

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

            timeline.extend([
                "Step 1: Kubernetes pod started",
                "Step 2: Container failed during startup or runtime",
                "Step 3: Kubernetes restarted the container",
                "Step 4: Repeated failures caused CrashLoopBackOff",
                "Step 5: Support team should inspect pod logs and resource limits"
            ])

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

            timeline.extend([
                "Step 1: Application attempted IBM MQ connection",
                "Step 2: Queue Manager was not available",
                "Step 3: MQ connection failed",
                "Step 4: Message processing was interrupted",
                "Step 5: Support team should verify Queue Manager and channel status"
            ])

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

            timeline.extend([
                "Step 1: API request reached backend application",
                "Step 2: Backend application encountered an internal error",
                "Step 3: HTTP 500 response was generated",
                "Step 4: Client request failed",
                "Step 5: Support team should check application logs and recent deployments"
            ])

        else:

            fixes.extend([
                "Review complete application logs",
                "Verify infrastructure health",
                "Check backend connectivity"
            ])

            timeline.extend([
                "Step 1: Incident message received",
                "Step 2: No known pattern matched",
                "Step 3: Manual log review is required",
                "Step 4: Support team should check related systems",
                "Step 5: Add new pattern if issue repeats"
            ])

        fixes = list(dict.fromkeys(fixes))
        apis = list(dict.fromkeys(apis))
        timeline = list(dict.fromkeys(timeline))

        return {
            "root_cause": root_cause,
            "severity": severity,
            "suggested_fixes": fixes,
            "affected_apis": apis,
            "incident_timeline": timeline,
            "github_issue_url": None
        }