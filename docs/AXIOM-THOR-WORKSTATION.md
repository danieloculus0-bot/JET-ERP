# AXIOM THOR

## Jetson AGX Thor workstation concept

**Status: proposed architecture, not a working or benchmarked product.**

AXIOM THOR is a proposed ARM64 industrial workstation and shared intelligence server built around NVIDIA Jetson AGX Thor, JERP, BEAN, and the Axiom engineering suite.

### Vision

A compact, local-first workstation for manufacturing and engineering. One coherent Axiom UI provides access to JERP, EZstimate, EZ-FEA, PDM, quality, maintenance, and BEAN. The workstation may also serve authenticated browser clients on a local shop network.

### Stack

| Layer | Proposed responsibility |
| --- | --- |
| JetPack Linux | Supported ARM64 operating system and NVIDIA acceleration |
| Axiom UI | Shared dark interface, NVIDIA-inspired green theme, app switcher |
| JERP | Orders, purchasing, inventory, jobs, quality, enterprise workflows |
| BEAN Bridge | Local reasoning, evidence, diagnostics, authorized actions |
| Engineering adapters | EZstimate, EZ-FEA, PDM, quality, maintenance |
| Data services | Local SSD, versioned contracts, audit records, backups |

### Deployment modes

1. **Desk workstation:** monitor and keyboard, local JERP services and optional BEAN inference.
2. **Shop intelligence server:** shared JERP and BEAN services for authenticated lightweight terminals.

### Example workflow

BEAN reviews authorized JERP job and inventory records, consults EZstimate forecasts, identifies potential material shortages, and prepares sourced purchase recommendations. External purchase commitments require explicit approval. Recommendations must never be presented as completed transactions.

### Constraints

- Thor is ARM64, not a drop-in host for x86-64 Puppy images or Windows executables.
- GPU AI performance does not guarantee CAD, FEA, or general-purpose CPU performance.
- Verify model memory, thermal limits, power, storage, concurrency, software licensing, and network reliability on real hardware.
- Preserve core ERP operation if BEAN is offline.
- NVIDIA-inspired styling does not imply NVIDIA endorsement.

### Validation roadmap

- [ ] Confirm Thor model, RAM, storage, JetPack and peripherals.
- [ ] Boot JetPack and validate SSD persistence, display and network.
- [ ] Run the JERP API and shared Axiom browser UI on ARM64.
- [ ] Demonstrate traceable cross-module integration using real adapters.
- [ ] Benchmark BEAN inference latency, GPU memory and temperature.
- [ ] Test concurrent terminals and measure responsiveness.
- [ ] Benchmark real EZstimate and EZ-FEA workloads against x86.
- [ ] Test authentication, offline behavior, backup restore and recovery.
- [ ] Publish reproducible test evidence before claiming support.

### UI identity

Use the shared Axiom design tokens defined in the repository README: near-black surfaces, high-contrast typography, NVIDIA-inspired green accents, and the Mountain Dew goth visual language.

**AXIOM THOR by Axiom. A proposed JERP workstation and BEAN intelligence platform.**
