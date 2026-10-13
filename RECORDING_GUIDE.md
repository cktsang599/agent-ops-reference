# 3-minute code walkthrough — Frank Yip

**Before recording**

- Start the FastAPI server on 127.0.0.1; open the dashboard and GitHub README.
- Keep the title "Independent reference implementation" visible. Do not call this production code or disclose private repositories.

**0:00–0:25: Problem framing**

> Hi, I'm Frank Yip. This is an independent reference implementation using synthetic order data. I built it to show how I would design an operational agent with real safety boundaries: read-only evidence, policy checks, human review, and testable outcomes.

**0:25–1:10: Read-only workflow**

> First, here's a shipment exception. The workflow selects read-only lookup tools, returns supporting evidence, and proposes a draft action. It does not send a message or modify an order. The default planner is deliberately deterministic, so anyone can run the demo without credentials.

Run `SYN-1001` and point to the trace.

**1:10–1:55: Human approval**

> Address or billing changes require a separate approval state. The model cannot override this policy. Even when a reviewer approves, this demo only records the decision; it never changes external data. In a production system I'd connect this to authenticated permissions and explicit write APIs after further testing.

Run `SYN-1004`, approve it, and point to the audit log.

**1:55–2:25: Idempotency / failure boundary**

> Operational systems are retried. Here, repeating the same idempotency key returns the same action rather than creating a second operation. The audit history is persisted locally in SQLite.

Click "Replay same key".

**2:25–3:05: Tests + model boundary**

> I also included an offline golden set and automated tests. Optional model-backed classification is behind an explicit switch. The model only suggests an intent; a deterministic policy validates its result, and sensitive actions always require review. This is a reference architecture, not the original proprietary system I built at work.

Open `/api/evaluation` or show `pytest` output. End by showing README and repository link.
