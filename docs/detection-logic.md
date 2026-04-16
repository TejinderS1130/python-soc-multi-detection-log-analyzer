# SOC Detection Logic Documentation

## Overview

This document explains the detection logic used in the SOC Multi-Attack Log Analyzer.

The system processes authentication logs and applies correlation rules to identify suspicious behavior.

---

## Detection Rules

### 1. Brute Force Detection
- Condition: ≥ 5 failed login attempts from same IP
- Risk Score: +40
- Severity: Medium+

---

### 2. Password Spraying Detection
- Condition: Multiple usernames targeted from single IP
- Risk Score: +30
- Severity: Medium

---

### 3. Account Compromise Detection (Critical)
- Condition:
  - Multiple failed attempts
  - Followed by successful login
- Risk Score: +50
- Severity: CRITICAL

---

## Correlation Logic

The system correlates:

- Failed login attempts
- Unique usernames targeted
- Successful authentication events

This allows detection of multi-stage attacks.

---

## Risk Scoring Model

| Detection Type | Score |
|---------------|------|
| Brute Force | 40 |
| Password Spraying | 30 |
| Account Compromise | 50 |

---

## Severity Mapping

| Score | Severity |
|------|---------|
| ≥ 80 | CRITICAL |
| ≥ 50 | HIGH |
| ≥ 30 | MEDIUM |
| < 30 | LOW |

---

## SOC Value

This detection model simulates real-world SOC capabilities:

- Multi-event correlation  
- Risk-based prioritization  
- Attack pattern detection  
- Automated alert generation  

---

## Conclusion

This project demonstrates how raw log data can be transformed into actionable security insights using detection engineering principles.
