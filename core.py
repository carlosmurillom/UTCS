from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import math

# Constants
J2000_TT = datetime(2000, 1, 1, 11, 58, 55, 816000, tzinfo=timezone.utc)
# J2000 TT expressed in UTC at epoch (TT - UTC = 64.184 s at epoch)

TAI_MINUS_UTC_CURRENT = 37  # update from IERS if needed
TT_MINUS_TAI = 32.184

SECONDS_PER_UD = 10**5
SECONDS_PER_UC = 10**7
SECONDS_PER_UY = 10**8


@dataclass(frozen=True)
class UTCSTimestamp:
    UY: int
    UC: int
    UD: int
    SSSSS: int

    def __str__(self):
        sign = "+" if self.UY >= 0 else "-"
        return f"{sign}{abs(self.UY):04d}.{self.UC:02d}.{self.UD:03d}.{self.SSSSS:05d}"


def utc_to_tt_seconds(utc_dt: datetime) -> float:
    if utc_dt.tzinfo is None:
        raise ValueError("UTC datetime must be timezone-aware")

    delta_utc = (utc_dt - J2000_TT).total_seconds()
    tt_minus_utc_epoch = 64.184
    tt_minus_utc_now = TAI_MINUS_UTC_CURRENT + TT_MINUS_TAI

    correction = tt_minus_utc_now - tt_minus_utc_epoch
    return delta_utc + correction


def delta_to_utcs(delta_seconds: float) -> UTCSTimestamp:
    delta_int = math.floor(delta_seconds)

    UY = math.floor(delta_int / SECONDS_PER_UY)
    r1 = delta_int % SECONDS_PER_UY

    UC = math.floor(r1 / SECONDS_PER_UC)
    r2 = r1 % SECONDS_PER_UC

    UD = math.floor(r2 / SECONDS_PER_UD)
    SSSSS = r2 % SECONDS_PER_UD

    return UTCSTimestamp(UY, UC, UD, SSSSS)


def utc_to_utcs(utc_dt: datetime) -> UTCSTimestamp:
    delta = utc_to_tt_seconds(utc_dt)
    return delta_to_utcs(delta)


def utcs_to_delta(ts: UTCSTimestamp) -> int:
    return (
        ts.UY * SECONDS_PER_UY
        + ts.UC * SECONDS_PER_UC
        + ts.UD * SECONDS_PER_UD
        + ts.SSSSS
    )


# CCSDS 301.0-B-4 coarse/fine encoding
def encode_cuc(delta_seconds: float, coarse_bytes=4, fine_bytes=2) -> bytes:
    delta_int = int(math.floor(delta_seconds))
    fractional = delta_seconds - delta_int

    coarse = delta_int.to_bytes(coarse_bytes, byteorder="big", signed=True)

    if fine_bytes > 0:
        fine_scale = 2 ** (8 * fine_bytes)
        fine_int = int(math.floor(fractional * fine_scale))
        fine = fine_int.to_bytes(fine_bytes, byteorder="big", signed=False)
        return coarse + fine
    else:
        return coarse
