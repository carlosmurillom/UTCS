# UTCS — Universal Temporal Coordinate System

Deterministic atomic timestamp representation for distributed interplanetary systems.

UTCS is NOT a new time scale.

It is a canonical integer-based representation layer over atomic coordinate time (TAI / TT), aligned with J2000.0.

---

## Why?

Modern space systems mix:

- UTC (leap seconds)
- TAI / TT (atomic)
- SCET / MET
- LMST (Mars)
- Julian Date

Leap handling and multi-scale conversion introduce representation-level divergence in distributed systems.

UTCS:

- Uses elapsed SI seconds
- Preserves strict monotonic ordering
- Avoids leap-second discontinuities in representation
- Maps cleanly onto CCSDS 301.0-B-4 CUC encoding

---

## Installation

```bash
pip install utcs
