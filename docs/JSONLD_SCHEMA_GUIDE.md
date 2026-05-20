# JSON-LD Schema Guide for AI Incident Resolution

This guide explains the JSON-LD schema structure used for incident visualization and knowledge graph representation.

## Overview

The AI Incident Resolution system uses JSON-LD with `@graph` structure to represent incidents as interconnected nodes and relationships. This enables:

- **Graph Visualization**: Visualize incidents and their relationships in graph databases
- **Semantic Querying**: Query incident data using SPARQL or similar semantic query languages
- **Knowledge Graph Integration**: Integrate with enterprise knowledge graphs
- **Linked Data**: Connect incidents across systems using standard web technologies

## Schema Location

- **Schema Definition**: `config/incident_schema.json`
- **Context**: `http://incident-resolution.ai/ontology#`

## Node Types

### 1. Incident
The root node representing a production incident.

**Properties:**
- `incidentId`: Unique identifier
- `timestamp`: When the incident occurred
- `severity`: CRITICAL, HIGH, MEDIUM, LOW
- `status`: OPEN, IN_PROGRESS, RESOLVED, CLOSED
- `title`: Brief incident title
- `description`: Detailed description
- `confidence`: AI confidence level (HIGH, MEDIUM, LOW)

**Relationships:**
- `hasRootCause` → RootCause
- `hasSuggestedFix` → SuggestedFix
- `affectsAPI` → API
- `hasLogEntry` → LogEntry
- `triggeredBy` → LogEntry

### 2. RootCause
Identified root cause of the incident.

**Properties:**
- `causeId`: Unique identifier
- `root_cause`: Description of the root cause
- `category`: NETWORK, BACKEND, AUTHENTICATION, CONFIGURATION, RESOURCE
- `confidence`: Confidence score (0-100)
- `detectedAt`: When identified

**Relationships:**
- `relatedTo` → Other incidents or causes
- `triggeredBy` → LogEntry

### 3. SuggestedFix
Recommended resolution steps.

**Properties:**
- `fixId`: Unique identifier
- `suggested_fixes`: Fix description
- `priority`: Priority order (1 = highest)
- `estimatedTime`: Time to implement
- `complexity`: LOW, MEDIUM, HIGH
- `status`: PENDING, IN_PROGRESS, COMPLETED, FAILED

**Relationships:**
- `resolvedBy` → Person or system
- `dependsOn` → Other fixes

### 4. API
Affected API endpoint.

**Properties:**
- `apiId`: Unique identifier
- `affected_apis`: API endpoint path
- `method`: HTTP method (GET, POST, PUT, DELETE, PATCH)
- `statusCode`: HTTP status code
- `errorRate`: Error rate percentage
- `requestCount`: Number of affected requests

**Relationships:**
- `dependsOn` → BackendService
- `impacts` → Other APIs or services

### 5. LogEntry
Individual log entry.

**Properties:**
- `logId`: Unique identifier
- `timestamp`: When logged
- `logType`: DATAPOWER, APIC, JAVA, GENERAL
- `errorMessage`: Error message
- `stackTrace`: Stack trace if available
- `severity`: Log severity level

**Relationships:**
- `triggeredBy` → Event or condition

### 6. BackendService
Backend service involved.

**Properties:**
- `serviceId`: Unique identifier
- `serviceName`: Service name
- `endpoint`: Service URL
- `status`: UP, DOWN, DEGRADED
- `responseTime`: Average response time (ms)

**Relationships:**
- `impacts` → APIs
- `relatedTo` → Other services

### 7. AdditionalCheck
Diagnostic check to perform.

**Properties:**
- `checkId`: Unique identifier
- `description`: Check description
- `status`: PENDING, COMPLETED, SKIPPED
- `result`: Check result

**Relationships:**
- `relatedTo` → Incident or fix

### 8. GitHubIssue
GitHub issue created for tracking.

**Properties:**
- `issueId`: GitHub issue number
- `url`: Issue URL
- `title`: Issue title
- `labels`: Issue labels
- `createdAt`: Creation timestamp

**Relationships:**
- `relatedTo` → Incident

## Example: Complete Incident Graph

```json
{
  "@context": {
    "@vocab": "http://schema.org/",
    "incident": "http://incident-resolution.ai/ontology#",
    "hasRootCause": {"@id": "incident:hasRootCause", "@type": "@id"},
    "hasSuggestedFix": {"@id": "incident:hasSuggestedFix", "@type": "@id"},
    "affectsAPI": {"@id": "incident:affectsAPI", "@type": "@id"},
    "hasLogEntry": {"@id": "incident:hasLogEntry", "@type": "@id"}
  },
  "@graph": [
    {
      "@id": "incident:inc-2026-001",
      "@type": "incident:Incident",
      "incidentId": "incident:inc-2026-001",
      "timestamp": "2026-05-19T14:30:00Z",
      "severity": "HIGH",
      "status": "OPEN",
      "title": "Backend connection timeout",
      "description": "Multiple API endpoints experiencing timeout errors when connecting to backend service",
      "confidence": "HIGH",
      "hasRootCause": ["incident:cause-001"],
      "hasSuggestedFix": ["incident:fix-001", "incident:fix-002", "incident:fix-003"],
      "affectsAPI": ["incident:api-001", "incident:api-002"],
      "hasLogEntry": ["incident:log-001", "incident:log-002"]
    },
    {
      "@id": "incident:cause-001",
      "@type": "incident:RootCause",
      "causeId": "incident:cause-001",
      "root_cause": "Backend service connection timeout due to firewall rule blocking port 8443",
      "category": "NETWORK",
      "confidence": 90,
      "detectedAt": "2026-05-19T14:31:00Z"
    },
    {
      "@id": "incident:fix-001",
      "@type": "incident:SuggestedFix",
      "fixId": "incident:fix-001",
      "suggested_fixes": "Check firewall rules between gateway and backend service on port 8443",
      "priority": 1,
      "estimatedTime": "15-30 minutes",
      "complexity": "LOW",
      "status": "PENDING"
    },
    {
      "@id": "incident:fix-002",
      "@type": "incident:SuggestedFix",
      "fixId": "incident:fix-002",
      "suggested_fixes": "Verify backend service is running and accessible on port 8443",
      "priority": 2,
      "estimatedTime": "15-30 minutes",
      "complexity": "LOW",
      "status": "PENDING"
    },
    {
      "@id": "incident:fix-003",
      "@type": "incident:SuggestedFix",
      "fixId": "incident:fix-003",
      "suggested_fixes": "Review network connectivity and latency between gateway and backend",
      "priority": 3,
      "estimatedTime": "30-60 minutes",
      "complexity": "MEDIUM",
      "status": "PENDING"
    },
    {
      "@id": "incident:api-001",
      "@type": "incident:API",
      "apiId": "incident:api-001",
      "affected_apis": "/member/inquiry",
      "method": "POST",
      "statusCode": 504,
      "errorRate": 85.5,
      "requestCount": 342
    },
    {
      "@id": "incident:api-002",
      "@type": "incident:API",
      "apiId": "incident:api-002",
      "affected_apis": "/claim/details",
      "method": "GET",
      "statusCode": 504,
      "errorRate": 78.2,
      "requestCount": 156
    },
    {
      "@id": "incident:log-001",
      "@type": "incident:LogEntry",
      "logId": "incident:log-001",
      "timestamp": "2026-05-19T14:30:15Z",
      "logType": "DATAPOWER",
      "errorMessage": "HTTP 504 Gateway Timeout - Backend connection timeout after 30s",
      "severity": "HIGH"
    },
    {
      "@id": "incident:log-002",
      "@type": "incident:LogEntry",
      "logId": "incident:log-002",
      "timestamp": "2026-05-19T14:30:16Z",
      "logType": "DATAPOWER",
      "errorMessage": "Connection refused to backend service at 10.20.30.40:8443",
      "severity": "HIGH"
    }
  ]
}
```

## Relationship Types

### hasRootCause
Links an Incident to its identified RootCause.

**Example:**
```json
{
  "@id": "incident:inc-001",
  "hasRootCause": ["incident:cause-001"]
}
```

### hasSuggestedFix
Links an Incident to recommended SuggestedFix nodes.

**Example:**
```json
{
  "@id": "incident:inc-001",
  "hasSuggestedFix": ["incident:fix-001", "incident:fix-002"]
}
```

### affectsAPI
Links an Incident to affected API endpoints.

**Example:**
```json
{
  "@id": "incident:inc-001",
  "affectsAPI": ["incident:api-001", "incident:api-002"]
}
```

### hasLogEntry
Links an Incident to related LogEntry nodes.

**Example:**
```json
{
  "@id": "incident:inc-001",
  "hasLogEntry": ["incident:log-001", "incident:log-002"]
}
```

### dependsOn
Indicates dependency between nodes (e.g., API depends on BackendService).

**Example:**
```json
{
  "@id": "incident:api-001",
  "dependsOn": ["incident:service-001"]
}
```

### impacts
Indicates impact relationship (e.g., BackendService impacts API).

**Example:**
```json
{
  "@id": "incident:service-001",
  "impacts": ["incident:api-001", "incident:api-002"]
}
```

### triggeredBy
Indicates what triggered an event (e.g., Incident triggered by LogEntry).

**Example:**
```json
{
  "@id": "incident:inc-001",
  "triggeredBy": ["incident:log-001"]
}
```

### resolvedBy
Indicates what resolved an issue (e.g., Incident resolved by SuggestedFix).

**Example:**
```json
{
  "@id": "incident:inc-001",
  "resolvedBy": ["incident:fix-001"]
}
```

### relatedTo
Generic relationship between related nodes.

**Example:**
```json
{
  "@id": "incident:cause-001",
  "relatedTo": ["incident:cause-002"]
}
```

## Visualization

The JSON-LD @graph structure can be visualized using:

1. **Neo4j**: Import as property graph
2. **GraphDB**: Load as RDF triples
3. **D3.js**: Render as force-directed graph
4. **Cytoscape.js**: Interactive network visualization
5. **Apache Jena**: SPARQL queries

### Example Neo4j Cypher Query

```cypher
// Find all high-severity incidents with their root causes
MATCH (i:Incident)-[:hasRootCause]->(rc:RootCause)
WHERE i.severity = 'HIGH'
RETURN i, rc
```

### Example SPARQL Query

```sparql
PREFIX incident: <http://incident-resolution.ai/ontology#>

SELECT ?incident ?rootCause ?api
WHERE {
  ?incident a incident:Incident ;
            incident:hasRootCause ?rootCause ;
            incident:affectsAPI ?api .
  FILTER (?severity = "HIGH")
}
```

## Integration with Python Code

The `incident_reporter.py` module includes a `generate_jsonld_report()` method that automatically generates JSON-LD format:

```python
from incident_reporter import IncidentReporter

reporter = IncidentReporter()

# Generate JSON-LD report
jsonld_report = reporter.generate_jsonld_report(
    analysis=analysis_results,
    parsed_logs=log_entries,
    incident_id="incident:inc-2026-001"
)

# Save to file
with open('incident_graph.json', 'w') as f:
    json.dump(jsonld_report, f, indent=2)
```

## Benefits

1. **Standardization**: Uses W3C JSON-LD standard
2. **Interoperability**: Works with any RDF/graph database
3. **Semantic Queries**: Enable complex relationship queries
4. **Visualization**: Easy to visualize in graph tools
5. **Knowledge Graphs**: Build enterprise incident knowledge graphs
6. **Machine Learning**: Train ML models on graph structure
7. **Pattern Detection**: Identify recurring incident patterns

## Best Practices

1. **Use Unique IDs**: Always use unique identifiers for nodes
2. **Maintain Relationships**: Keep relationship links up to date
3. **Add Context**: Include relevant context in descriptions
4. **Version Control**: Track schema changes over time
5. **Validate**: Validate JSON-LD structure before storage
6. **Index**: Index key properties for fast queries
7. **Archive**: Archive resolved incidents for historical analysis

## Tools and Libraries

- **Python**: `rdflib`, `pyld`
- **JavaScript**: `jsonld.js`
- **Validation**: JSON-LD Playground (https://json-ld.org/playground/)
- **Visualization**: Neo4j Browser, GraphDB Workbench
- **Query**: Apache Jena, RDF4J

---

**For more information, see:**
- JSON-LD Specification: https://www.w3.org/TR/json-ld/
- Schema.org: https://schema.org/
- RDF Primer: https://www.w3.org/TR/rdf11-primer/