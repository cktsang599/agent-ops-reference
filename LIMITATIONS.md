# Boundaries and limitations

This repo is a **public portfolio reference implementation**, not a production deployment or the original Watchdives / MolGraph source code.

- All names, requests, orders and events are invented. Nothing came from Sticker Mule or a user/customer database.
- **No external writes** are implemented; the app cannot email a customer, modify a shipment, approve proofs, refund payments, or call vendor APIs.
- The default planner is **deterministic**, not a language model. The UI and evaluation label this explicitly. Optional LLM mode requires an opt-in environment variable and separate API key. The API key is never needed for a demo.
- The LLM is restricted to *advisory classification*. It does not choose arbitrary tools or override deterministic risk policy. A production implementation would require a thorough threat model and adversarial evaluations beyond this illustration.
- `X-Demo-Role` illustrates a role policy but is **not identity verification**; any caller can forge it. The service must only be run on loopback (127.0.0.1). A public deployment would require OIDC/session authentication, authorization at a trusted gateway and CSRF/CORS review.
- SQLite helps demonstrate idempotency in one local process. A production queue would need robust concurrency control, lease/timeouts, dead-letter queues, stronger deduplication across workflow versions, observability, and disaster recovery.
- The five golden cases verify a fixed regression baseline and **do not establish LLM accuracy or real-world customer outcomes**.
- No financial savings, reduced ticket counts or customer impact are claimed; those require measured production data.
- This example is not affiliated with Sticker Mule, Watchdives or MolGraph.
