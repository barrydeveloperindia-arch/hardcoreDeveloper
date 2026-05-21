# 🧠 Local Knowledge Item (KI): Englabs Autopilot

This localized Knowledge Item serves as the master reference for future AI agents working on the Englabs Autopilot repository.

## 📌 Metadata
*   **Domain:** Manufacturing Execution System (MES) & Multi-Agent Orchestration
*   **Repository:** `barrydeveloperindia-arch/hardcoreDeveloper`
*   **Key Modules:** `src/supervisor.py`, `src/cad_worker.py`, `src/shopfloor_worker.py`
*   **Associated Handover:** [ARCHITECTURE_HANDOVER.md](docs/architecture/ARCHITECTURE_HANDOVER.md)

---

## 🔑 Crucial Architectural Patterns

### 1. Zero-Dependency & Self-Hosted Core
To prevent data leaks and maintain complete operational control, the system is designed to run 100% on local hardware:
- **No SaaS Integrations:** Zoho Books is replaced by native PostgreSQL database schemas tracking transactions atomically.
- **pgvector Integration:** Vector storage resides locally within the PostgreSQL database (`ankane/pgvector` Docker image).

### 2. Multi-Agent langGraph & MSAL Topologies
The incoming email router (`GokuRouter`) processes and directs emails based on strict sender/recipient domains and files:
- `.step` or `.stl` attachments routing to the CAD parsing agent.
- Status inquiries routing to the shop floor tracking agent.
- `bharata@` and `salila@` domains are bypassed completely to ensure executive privacy.

### 3. Hardware Interceptor Logic
- **HP MJF 4200 API Polling:** Telemetry listening is performed asynchronously on the isolated printer subnet (`eth1`).
- **Mixer Overfill Alert:** Exception monitoring intercepts error code `0051-0008-0001` to pause production queues.

---

## 🧪 Testing & Validation Standards
- Every feature must be built TDD first.
- **Mocking:** Geometry computations and printer API responses are mocked statically in `tests/` using simple pytest fixtures.
