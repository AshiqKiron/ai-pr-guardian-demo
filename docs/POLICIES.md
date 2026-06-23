# 📋 Policy Configuration Guide

## Policy Structure

Each policy in `.ai-guardrails/policies.yaml` has:

```yaml
policies:
  - id: "unique_identifier"
    name: "Human Readable Name"
    severity: "critical|high|medium|low"
    enabled: true
    rules:
      - type: "regex"
        pattern: "YOUR_REGEX"
        message: "Violation message"
