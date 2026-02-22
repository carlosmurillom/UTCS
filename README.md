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
```

## Example Python
```bash
from datetime import datetime, timezone
from utcs.core import utc_to_utcs

utc = datetime(2026, 2, 18, 18, 35, 36, tzinfo=timezone.utc)
print(utc_to_utcs(utc))
```

## Output
```bash
+0008.02.047.11800
```
## CCSDS Encoding Example Python
```bash
from utcs.core import encode_cuc, utc_to_tt_seconds

delta = utc_to_tt_seconds(utc)
packet_bytes = encode_cuc(delta, coarse_bytes=4, fine_bytes=2)
```
