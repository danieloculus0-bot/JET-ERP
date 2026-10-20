# JERP
### JET-ERP | An Axiom enterprise platform

**Local-first enterprise operations. BEAN-connected intelligence. Jetson-ready deployment.**

> **Status: architecture and integration planning.** This repository is an initial project foundation, not a working ERP release. No production capabilities, Jetson compatibility, or integrations are claimed until implemented and tested.

JERP is the enterprise resource planning layer of the **Axiom** software ecosystem. It is designed to bring quoting, purchasing, inventory, manufacturing, quality, maintenance, people, and business reporting into a coherent experience while preserving independently useful engineering tools.

The name **JERP** is the user-facing product identity; **JET-ERP** is the repository and technical project name.

## Product principles

- **Local-first:** operate on an organization's own hardware and network, with deliberate backup and recovery.
- **Jetson-first, not Jetson-only:** target NVIDIA Jetson ARM64/JetPack Linux, while supporting x86-64 Linux and browser-based clients through stable service interfaces.
- **One coherent suite:** shared navigation, identity, data contracts, component styling, and accessibility across Axiom modules.
- **No invented integration:** a connector is considered functional only when tested against the actual target system.
- **BEAN is evidence-aware:** model suggestions, tool actions, source records, and execution receipts remain distinguishable.
- **Human-authorized transactions:** purchasing, financial posting, payroll, and external commitments follow explicit authorization policies.
- **Graceful degradation:** core ERP workflows should remain usable when BEAN or remote inference is unavailable.

## Initial functional domains

| Domain | Intended scope | Current status |
| --- | --- | --- |
| Customers and sales | CRM, RFQs, quotes, orders | Planned |
| Estimating | EZstimate BOM extraction, costing, material forecasting | Integration planned |
| Purchasing | Requisitions, approval, supplier POs, receiving | Planned |
| Inventory | Parts, stock, locations, lots, reservations, traceability | Planned |
| Manufacturing | Jobs, routings, work centers, WIP, dispatch | Planned |
| Engineering | PDM, drawings, revisions, EZ-FEA, EZ Methods | Integration planned |
| Quality | EZ-FAIR, NCR/CAR, inspections, RMA, audit trails | Integration planned |
| Maintenance | PM-Tracker assets, tasks, completion records | Integration planned |
| Finance | Job costing, invoice/accounting connectors, reconciliation | Planned |
| Workforce | Training, qualification, permissions, time capture | Planned |
| Intelligence | BEAN reasoning, forecasting, diagnostics, evidence | Integration planned |

**External ERP integration** (including JobBoss² where permitted interfaces exist) is a separate adapter effort. JERP must not assume undocumented API access.

## UI design system: Axiom / JERP

A single reusable UI package should drive JERP and, progressively, the Axiom suite. The aesthetic is a high-contrast, dark industrial interface with vivid NVIDIA-inspired green accents, informally the **Mountain Dew goth** design language.

### Proposed design tokens

```css
:root {
  --axiom-bg: #0b0f0b;
  --axiom-surface: #151c16;
  --axiom-surface-raised: #202a21;
  --axiom-border: #334235;
  --axiom-text: #f1f6ef;
  --axiom-text-muted: #a8b6a7;
  --axiom-green: #76b900; /* NVIDIA-inspired accent */
  --axiom-green-bright: #a3e635;
  --axiom-focus: #b8ff55;
  --axiom-danger: #ef6b65;
  --axiom-warning: #eabf57;
  --axiom-radius: 10px;
}
```

Use green for focus, selection, active navigation, and primary actions, **not** as the only indicator of status. Preserve keyboard navigation, visible focus, readable contrast, responsive layouts, and large touch targets for shop-floor terminals. Do not use NVIDIA trademarks or logos in a way that implies NVIDIA sponsorship.

### Shared shell contract (proposed)

- App switcher: JERP, EZstimate, EZ-FEA, PDM, Quality, PM-Tracker, BEAN.
- Persistent global search and contextual entity navigation.
- Common breadcrumbs, notifications, user/session indicator, and module status.
- Standard table/grid behavior: sorting, filtering, copy/paste, bulk edit, and drag-fill where applicable.
- Consistent entity detail views and document revision display.
- BEAN side panel showing source context, proposed action, confidence/limitations, and execution evidence.
- Per-module capability detection and offline/degraded indicators.

## Integration architecture

```text
Axiom shared UI / component library
             |
      JERP application shell
             |
    Versioned API and event contracts
       /       |         \
  ERP core  Suite adapters  BEAN Bridge
     |          |             |
  Database   EZstimate     Evidence and
  + audit    PDM, FEA      reasoning tools
  records    Quality, PM
             |
     External ERP connectors
```

**System-of-record rule:** define ownership of each entity before synchronizing it. A part number, customer, quote, job, supplier, and revision must have stable identifiers and provenance. Never silently overwrite the source system with inferred AI output.

### Proposed contract conventions

- REST/JSON for initial synchronous APIs; version endpoints explicitly.
- Events for asynchronous transitions (quote approved, PO issued, material received, inspection released).
- Idempotency keys for transactional commands.
- Correlation IDs for cross-module traceability.
- Explicit `source_system`, `source_id`, `revision`, timestamps, and actor identity.
- File references and hashes for drawings, BOMs, and evidence.
- Typed connector capabilities, health checks, and test fixtures.
- BEAN suggestions are separate from confirmed business facts and executed commands.

Example **proposed** event (not implemented):

```json
{
  "schema_version": "1.0",
  "event_type": "purchase_request.approved",
  "event_id": "example-event-id",
  "correlation_id": "example-quote-id",
  "source_system": "jerp",
  "actor_id": "example-authorized-user",
  "purchase_request_id": "example-pr-id",
  "approved_at": "2026-10-20T18:00:00Z"
}
```

## Target deployment

1. **Jetson workstation:** supported JetPack Linux, local UI/browser, JERP services, database, optional local BEAN inference. Hardware model and RAM must be validated.
2. **Shop server:** a Jetson or conventional Linux host serving multiple authenticated browsers.
3. **Mixed fleet:** ARM64 and x86-64 services and clients, with platform-specific adapters where required.
4. **Windows application dependency:** remote Windows execution or a separately verified compatibility layer; do not assume x86 Wine binaries run natively on Jetson ARM64.

A USB installer/recovery path is a future deliverable, not a verified capability.

## Suggested repository layout (planned)

```text
apps/
  jerp-web/           # Browser UI and Axiom shell
  jerp-api/           # Enterprise API
packages/
  axiom-ui/           # Shared theme, tokens, components
  contracts/          # Versioned schemas and event definitions
  bean-bridge/        # BEAN connector and evidence contracts
  connectors/         # External ERP and Axiom module adapters
infra/
  jetson/             # JetPack deployment and hardware checks
  containers/         # Optional service deployment
tests/
  contracts/
  integration/
  e2e/
docs/
  architecture/
  decisions/
```

This is a proposed structure, not a claim that the folders exist.

## Implementation sequence

1. Inventory actual Axiom repositories, APIs, auth methods, and UI patterns; record verified capabilities.
2. Establish the shared Axiom design-token package and reusable navigation shell.
3. Define entity ownership, versioned contracts, identity, audit logging, and permissions.
4. Implement a thin JERP vertical slice: RFQ → quote → approved purchase request, with mock adapters clearly labeled.
5. Replace mocks with tested EZstimate, PDM, and BEAN Bridge integrations.
6. Test Jetson ARM64 deployment and realistic shop-floor browser workflows.
7. Expand inventory, jobs, purchasing, receiving, quality, and finance adapters only after evidence-backed integration tests.

## Acceptance criteria for the first integrated demo

- JERP launches in the same visual shell as another Axiom module.
- An imported drawing/BOM retains revision and source provenance.
- A quote can be created and traced to its originating document.
- An approved purchase request emits a documented, idempotent event.
- BEAN can analyze context without silently executing purchasing actions.
- All cross-module calls and failures appear in traceable logs.
- Demo mode is clearly identified; no mock response is presented as a live ERP transaction.
- ARM64 deployment is demonstrated on real Jetson hardware before it is advertised as supported.

## Licensing and contributions

**License: not yet selected.** Do not assume this repository is open-source or that code may be redistributed merely because it is publicly visible. License and contribution policies will be documented before third-party distribution.

---

**JERP by Axiom** · BEAN-connected · NVIDIA-green-inspired design · Built for real organizational workflows.
