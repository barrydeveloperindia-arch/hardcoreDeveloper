# Englabs Autopilot: Master Architecture & Strategy
**Version:** 1.0 (Zero-Dependency Edition)
**Date:** May 20, 2026

## 1. Executive Vision
The Englabs Autopilot is a 100% self-hosted, multi-agent Manufacturing Execution System (MES). It operates without third-party SaaS dependencies (No Zoho Books). It utilizes local PostgreSQL for double-entry accounting, Docker for containerized agent isolation, and LangGraph for AI orchestration (GOKU).

## 2. Hardware BOM (The Edge Node)
To guarantee processing speed and network security, the system runs on the following physical on-premise hardware:
*   **CPU:** Intel Core Ultra 9 285K (24-Core)
*   **RAM:** 128GB DDR5
*   **GPU:** NVIDIA RTX 5080 (for local vector embeddings and offline LLM fallback)
*   **Network:** Dual-LAN. `eth0` connects to the internet (Outlook/Gemini). `eth1` is physically air-gapped and connected strictly to the HP Jet Fusion 4200 local subnet.

## 3. The 5-Phase Multi-Agent Architecture
### Phase 1: Core Infrastructure
*   **Docker-Compose:** Traefik (Proxy), Redis (Message Broker), and PostgreSQL + `pgvector` (Database & Memory).
*   **Strict Pydantic Validation:** All data entering the system is validated via strict schemas before hitting the DB.

### Phase 2: Double-Entry Financial Core (Zero Zoho)
*   **Ledger:** Native `accounts`, `journal_entries`, and `invoices` tables in Postgres.
*   **Rule:** Transactions must be atomic. If `Credits != Debits`, the transaction rolls back.
*   **Invoicing:** Autonomously generated offline via `FPDF` in Python, removing SaaS branding.

### Phase 3: LangGraph Orchestration (GOKU)
*   **Outlook Daemon (Email Topologies):** Autonomously polls via MSAL based on strict mailbox heuristics:
    *   `enquiries@englabs.co.uk`: Routes to GOKU for RFQ extraction (strips signatures, extracts `.step` / `.stl`).
    *   `admin1@englabs.co.uk`: Routes to the Financial Agent for invoice, BharatNXT, and bank reconciliation.
    *   `marketing1@englabs.co.uk`: Routes to GOKU for outbound campaign management.
    *   `bharata@englabs.co.uk` & `salila@englabs.co.uk`: Executive bypass. The AI will strictly *ignore* these mailboxes unless explicitly @mentioned to preserve privacy and prevent hallucinated replies to stakeholders.
*   **GOKU Router:** Classifies intent from the `enquiries` funnel and delegates CAD parsing to specialized background workers via Redis.

### Phase 4: Manufacturability & Quotation Engine
*   **Constraint 1 (Bounding Box):** Checks if X, Y, or Z exceeds 375mm. If true -> `REJECT_OVERSIZE`.
*   **Constraint 2 (Trapped Powder):** Compares Mesh Volume to Bounding Box Volume. If hollow without escape holes -> `WARNING_TRAPPED_POWDER`.
*   **Costing:** Price = (Volume * Material Density * Cost per kg) + (Bounding Box Z-height * Machine Rate) + Markup.

### Phase 5: Shop Floor Telemetry (Hardware)
*   **Printer Poller:** Listens to HP MJF 4200 API on the air-gapped LAN.
*   **Mixer Overfill Rescue:** If error code `0051-0008-0001` triggers, the system pauses the MES dispatch queue and fires an emergency alert.

## 4. Strict Test-Driven Development (TDD) SOP
No business logic may be written without a failing `pytest` assertion.
*   **CAD Mocking:** Feasibility logic is tested against standard geometrical stubs (e.g., 10x10x10 cube) to guarantee mathematical perfection.
*   **Hardware Mocking:** The HP API is simulated with JSON payloads to test error-catching (e.g., Mixer Overfill) without physical hardware risks.
*   **CI/CD:** 100% line coverage is strictly required for the financial transaction (`journal_entries`) modules.
