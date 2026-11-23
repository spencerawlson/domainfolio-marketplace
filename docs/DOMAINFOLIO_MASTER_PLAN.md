# DomainFolio — Master Plan (Option B)

| Field | Value |
|---|---|
| Status | **Phase 1 design — for Spencer's review. No repo created, nothing pushed, nothing deployed.** |
| Basis | Phase 0 audit (`docs/DOMAINFOLIO_AUDIT.md`, `main` @ `6da17767`) and Implementation Plan Outline (both in `~/workspace/domainfolio-audit/docs/`). |
| Decision | **Option B** — build the marketplace as a modular monolith ALONGSIDE the existing lander app. The lander stays live and untouched until the marketplace can replace it. Chosen by Spencer 2026-11-23. |
| Stack | Next.js 15 + TypeScript + Tailwind (web) · Python FastAPI (api) · PostgreSQL 16 · Meilisearch · Redis + Celery · Docker · GitHub Actions. Observability: Prometheus/Grafana/Loki (staging/prod stage). |
| Work dir | `~/workspace/domainfolio-monolith/` (local only — no GitHub repo yet) |

## 1. What this plan is

This is the build plan for the multi-vendor marketplace in the master
prompt, sequenced as reviewable stages. Each stage ends with: features
completed, files changed, DB changes, tests executed with exact
results, security considerations, blockers, next actions. **No stage
starts until Spencer approves the previous stage's report**, and the
production gates in §5 are separate approvals each.

Non-goals for this plan: the lander app (untouched; its own fixes —
login rate limiting, spoofable rate-limit key, server-side minimum
offer — are a separate small change set Spencer can approve
independently); any real-money activation; any paid account.

## 2. Ground rules (from the master prompt — non-negotiable)

1. **Never activate a listing without ownership verification** (DNS TXT
   challenge; DNS control alone is not conclusive legal ownership).
2. **Never represent a payment as secured without authoritative
   provider confirmation.** No internal escrow or customer-funds
   custody, ever. Escrow provider adapters only.
3. **Stripe Connect is not assumed approved.** Platform billing code
   stays behind `STRIPE_CONNECT_ENABLED=false` until the provider
   approves this business model.
4. **Never fabricate** domain inventory, sales figures, testimonials,
   or trust certifications — including in demos, screenshots, and
   seeded data. Empty states stay empty until real data exists.
5. **Never deploy publicly or activate real financial transactions
   without explicit approval** (per step, not blanket).
6. Distinguish implemented / tested / blocked / proposed in every
   report. Never claim a test passed unless it was executed.
7. Preserve working code. Small, reviewable stages. Docs alongside
   implementation.

## 3. P0 — Marketplace MVP

Order matters; each stage unblocks the next. The skeleton (Phase 1,
this step) is Stage 0.

### Stage 0 — Skeleton (this step) ✅ design + shells

- Docs: this plan, `SYSTEM_ARCHITECTURE.md`, `DATABASE_SCHEMA.md`
  (draft).
- Monolith skeleton: Next.js shell, FastAPI shell with the 11 module
  boundaries, Postgres migration chain (`0001_initial`), Docker
  Compose local dev, CI workflow.
- Health endpoints only; escrow adapter interface + sandbox stub.
- Tests: backend skeleton suite, frontend format-helper suite.
- **Exit criteria:** both suites green as executed in the sandbox;
  compose file YAML-valid (Docker itself is not available in the
  sandbox — `docker compose up` is validated in CI / on a Docker host).

### Stage 1 — Repo, CI, and lander fixes (separate approval)

- Create the GitHub repo (name/visibility: Spencer decides) and push
  this skeleton. CI green on first push.
- The three lander-app fixes from the audit (login rate limiting,
  `CF-Connecting-IP`, server-side `min_offer`) as their own small PR
  in `spencerawlson/domainfolio` — **not** in this repo.
- **Exit criteria:** CI green; lander fixes merged only on his go.

### Stage 2 — Accounts & identity

- Buyer/seller accounts, orgs + member permissions, email
  verification, password recovery, TOTP MFA, passkey (WebAuthn)
  support, session records that can be revoked, activity history,
  login anomaly detection, RBAC + server-side authorization checks.
- Replaces the audit's High finding (§6.1.2) by design: no shared
  credential anywhere in the marketplace.
- **Exit criteria:** auth test set (registration, verification,
  login, MFA enrol/verify, session revoke, RBAC negative tests) green;
  no endpoint returns data to an unauthorized caller in the test set.

### Stage 3 — Ownership verification

- Domain normalization + IDN handling, DNS TXT challenges, secure
  expiring tokens, propagation retries, verification history,
  periodic re-verification, revocation, duplicate-listing prevention,
  suspicious ownership-change detection, admin review queue.
- **Hard rule:** a listing cannot become active without a passed
  verification. Disputed ownership goes to manual review.
- **Exit criteria:** verification test set green incl. expired-token
  rejection, duplicate prevention, and re-verification scheduling.

### Stage 4 — Listings & portfolio

- Single + bulk CSV import, portfolio overview, categorization,
  fixed/min-offer/negotiable pricing, bulk price updates, listing
  expiry, seller analytics (visits, offers), sales history, export.
- Lander rendering: the marketplace serves seller landing pages; the
  old lander app keeps serving Spencer's four names until the cutover
  decision (§6).
- **Exit criteria:** import test set green (valid CSV, bad rows
  rejected with row-level errors, duplicates rejected); listing
  lifecycle tests green.

### Stage 5 — Search

- Meilisearch index synced from listings (create/update/delete via
  Celery), filters by TLD / price / length / keyword / category /
  listing type, saved searches, watchlists, buyer notifications.
- **Exit criteria:** search test set green; index-sync tests prove a
  listing change reaches search within the sync job's contract.

### Stage 6 — Offers engine

- Offer creation, counteroffers, acceptance/rejection, expiration,
  seller minimum thresholds (**enforced server-side** — fixes the
  audit's functional bug), negotiation history, spam/abuse controls,
  withdrawal rules.
- Concurrency: accepting an offer locks the listing row
  (`SELECT … FOR UPDATE`); a second concurrent accept fails cleanly.
  Accepted offer creates the controlled transaction workflow.
- **Exit criteria:** concurrency test (two simultaneous accepts — one
  wins, one fails, no double sale) green; offer lifecycle tests green.

### Stage 7 — Escrow (sandbox only)

- Escrow.com sandbox adapter behind the provider interface; sandbox
  transaction create, status sync, webhook signature verification,
  idempotent event processing (dedup on provider event id),
  settlement/refund/dispute state machine, reconciliation report.
- **Exit criteria:** sandbox end-to-end (create → pay → transfer →
  settle) green against the sandbox; webhook replay test proves
  idempotency; a test proves an unsigned webhook is rejected.

### Stage 8 — Transfers

- Same-registrar push + inter-registrar transfer workflows,
  registrar-specific instructions, auth-code handling (never in
  ordinary logs), status tracking, deadlines, buyer confirmation,
  evidence collection, failed-transfer recovery, cancellation/disputes.
- **Exit criteria:** transfer state-machine tests green; auth-code
  log-scan test proves no auth code reaches logs.

### Stage 9 — Admin, moderation, billing config

- Admin dashboard: user/seller/listing/transaction/escrow/transfer
  monitoring, fraud alerts, disputes, commission config, analytics,
  revenue reports, audit logs, security events, system health.
- Admin MFA mandatory. Separation of duties; sensitive actions logged.
- Commission engine: deterministic, versioned, auditable (proposed
  rates in §7 — **proposals, not decisions**). GMV / commission /
  processing / refunds / taxes / net separated.
- Security headers on every response; login rate limiting; backups.
- **Exit criteria:** admin permission tests green (negative tests for
  every admin action); audit-log tests green; backup/restore test
  green.

### Stage 10 — P0 launch gates (no public launch without all of these)

- Full Phase 15 test list executed (unit, integration, E2E,
  concurrency) with exact results reported.
- Staging deploy + smoke test; production deploy plan + rollback
  rehearsed; observability (Prometheus/Grafana/Loki) live.
- **Separate approvals:** staging deploy, production deploy, first
  real-money transaction (sandbox first, always).

## 4. P1 — Marketplace expansion

- Bulk portfolio tools + bulk price updates (scale the Stage 4 base).
- Custom landing pages for sellers, with anti-phishing routing
  guards (a seller domain must never become a phishing host:
  verified ownership + content allowlist + abuse reporting).
- Seller analytics + sales history + export (scale Stage 4).
- Brokerage: verified broker accounts, 15% broker-assisted tier.
- **Auction engine:** timed auctions, starting bids, reserves,
  minimum increments, bid history, anti-sniping extensions, closing,
  winner notification, auction→escrow conversion, shill-bidding
  detection. Server-authoritative timestamps, transactional bids.
  **No public launch until bidding + payment + disputes pass
  dedicated testing.**

## 5. P2 — Intelligence and distribution

- AI valuations — **clearly labeled estimates**; comps only when
  reliable data exists; never fabricated comps, traffic, history, or
  accuracy claims. AI never authorizes transfers, releases payments,
  or overrides fraud controls.
- Natural-language search, buyer-intent matching, portfolio valuation
  estimates, pricing recommendations, domain categorization,
  suspicious-listing detection.
- Registrar partnerships, automated transfers, advanced portfolio
  management.

## 6. The lander cutover (decision, not a stage)

The four live names (axionory.com $3,330 Reserved, trivantaq.com
$2,260, opsnestly.com $1,730, ventoryn.app $30,000) sell through
Afternic today at 25% with own nameservers; the 60-day lock lifts
≈ 2026-12-14. Before the marketplace lists any of them:

- Explicit delist-on-sale policy so a name cannot sell twice
  (Afternic + marketplace).
- Decide whether the lander app is retired, re-pointed at the new
  backend, or kept as the portfolio front door.
- The `fedserv-snapshot` host checkout is never merged with `main`
  (CRLF vs LF) — any lander change goes through the existing
  pull-and-rebuild flow.

## 7. Monetization (proposed — NOT decided)

From the master prompt; confirm or change before any billing code is
written. No paid subscription or featured listing activates without
explicit approval.

| Item | Proposed |
|---|---|
| Domain listings | Free |
| Standard successful sale | 10% |
| High-volume sellers | 8% (subject to eligibility) |
| Broker-assisted sale | 15% |
| Featured listing | $9–$29 |
| Portfolio Pro | $19/month |
| Portfolio Business | $79/month |

Commission calculations are deterministic, versioned, and auditable;
every rate change is a new version, never an edit.

## 8. Decisions only Spencer can make (blockers until answered)

1. Repo name / visibility for this monolith (Stage 1).
2. Escrow.com sandbox account — whose identity, who signs up.
3. Stripe — pursue Connect for this model or not.
4. Pricing (§7) — confirm or change.
5. Afternic policy (§6) — delist-on-sale rule.
6. Legal/tax — Canadian privacy (PIPEDA / Quebec Law 25) for holding
   other people's data and money; money-transmitter review for
   payout flows. No compliance claim is made in this plan.
7. Hosting — where the marketplace deploys (staging first); the
   lander stays on `fedserv-snapshot`.

## 9. Risks (summary — full register is `docs/RISK_REGISTER.md`,
written in a later stage)

- **Double-sale** (Afternic + marketplace) — mitigated by §6 policy.
- **Unverified listing / fraud** — mitigated by Stage 3 gates.
- **Escrow webhook spoofing / replay** — mitigated by signature
  verification + idempotent processing (Stage 7 tests).
- **Concurrent Buy Now** — mitigated by row locks + concurrency
  tests (Stage 6).
- **Provider approval** — Stripe Connect may be refused; escrow
  integration may need a business entity. Both are Stage 7/9
  blockers, flagged early, not late.
- **Scope creep into AI** — P2 stays after P0/P1; AI never touches
  money movement.

## 10. Per-stage report contract

Every stage report contains: features completed · files created or
modified · database changes · tests executed + exact results ·
security considerations · outstanding blockers · next recommended
actions. A stage is not "done" until its exit criteria are met and
reported.

---

*Plan source: Phase 0 audit + Implementation Plan Outline, Option B
chosen 2026-11-23. Work dir: `~/workspace/domainfolio-monolith/`.*
