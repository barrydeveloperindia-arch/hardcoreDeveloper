# 🏗️ Englabs Autopilot Architecture Handover (Zero-Dependency MES)

This document details the architecture, component design, and operational setup for the self-hosted, multi-agent Manufacturing Execution System (MES) designed for Englabs.

## 📍 System Architecture & Core Philosophy
The Englabs Autopilot is built to run entirely on-premise without reliance on external SaaS providers (such as Zoho Books) to guarantee maximum privacy, low latency, and operational resilience.

- **Platform:** Self-hosted Docker Compose environment.
- **Database:** PostgreSQL with the `pgvector` extension for handling multi-agent memory and semantic embeddings.
- **Message Broker:** Redis for background worker task queues and state management.
- **Gateway/Proxy:** Traefik for reverse proxying and secure endpoint routing.

---

## 🖥️ Edge Node Hardware Specifications
To support local vector embeddings, CAD parsing, and air-gapped machine telemetry, the production environment runs on the following dedicated on-premise hardware:

*   **CPU:** Intel Core Ultra 9 285K (24-Core / 32-Thread)
*   **RAM:** 128GB DDR5
*   **GPU:** NVIDIA RTX 5080 (for local offline LLM fallback and vector embeddings)
*   **Network:** Dual-LAN Interface:
    *   `eth0`: WAN connection for MSAL Outlook polling and LLM APIs.
    *   `eth1`: Isolated air-gapped LAN connection strictly bound to the HP Jet Fusion 4200 printer subnet.

---

## 🧩 Component Architecture & Data Flow

### 1. Goku Supervisor Router (`src/supervisor.py`)
- **Role:** Orchestrates the incoming RFQ pipeline using LangGraph (production wrapped around Gemini 2.5 Flash).
- **Email Ingestion Topology:** Autonomously processes messages via MSAL based on strict mailbox heuristics:
    *   `enquiries@englabs.co.uk`: Routes to GOKU for RFQ extraction (strips signatures, extracts `.step`/`.stl`).
    *   `admin1@englabs.co.uk`: Routes to the Financial Agent for invoice generation, bank reconciliation, and payment gate audits (e.g. BharatNXT, Pice).
    *   `marketing1@englabs.co.uk`: Routes to GOKU for outbound campaign management.
    *   `bharata@englabs.co.uk` & `salila@englabs.co.uk`: **Executive Bypass**. The supervisor strictly ignores these mailboxes unless explicitly `@mentioned` to preserve stakeholder privacy.

### 2. CAD Worker (`src/cad_worker.py`)
- **Role:** Feeds the geometric analysis pipeline.
- **Calculations:** Determines the bounding box volume and surface dimensions.
- **Safety Constraints:**
    *   *Bounding Box:* Checks if any dimension (X, Y, Z) exceeds 375mm (`REJECT_OVERSIZE`).
    *   *Trapped Powder:* Checks volume ratios to detect hollow sections without exit holes (`WARNING_TRAPPED_POWDER`).

### 3. Shopfloor Telemetry Worker (`src/shopfloor_worker.py`)
- **Role:** Interface to the air-gapped HP MJF 4200 printer.
- **Mixer Overfill Heuristics:** Intercepts critical error code `0051-0008-0001` or "Mixer Overfill" descriptions via the local API, triggers a system pause, and broadcasts alerts to the operators.

---

## 🧪 Testing & Validation Suite
The system is built under a strict Test-Driven Development (TDD) model.
- Run tests: `pytest`
- **Mocking Strategy:**
    *   **CAD Mocking:** Uses mathematical stubs (e.g. 10x10x10 cube) to test pricing and bounding box limits without relying on actual CAD parsing libraries during local unit tests.
    *   **Hardware Mocking:** Simulates the HP MJF 4200 API with JSON payloads to verify telemetry exception handling (e.g., Mixer Overfill triggers).
- **Test Coverage:** Core financial transaction schemas require 100% test coverage.

---

## 🛠️ Directory & Repo Navigation
```
englabs-autopilot/
├── docker-compose.yml       # Stack configuration (Traefik, Redis, PostgreSQL + pgvector)
├── requirements.txt         # Pytest & dependency listing
├── autopilot_architecture_master.md  # System-wide design document
└── src/
    ├── supervisor.py        # Intent classification & LangGraph routing logic
    ├── cad_worker.py        # Volume calculation & CAD processing
    └── shopfloor_worker.py  # HP printer telemetry & alert interceptor
```

---
**Status:** ✅ Core Framework Verified & Tests Passing (6/6). Ready for local edge deployment.
