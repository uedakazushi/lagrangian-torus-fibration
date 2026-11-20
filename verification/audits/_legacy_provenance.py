"""Check provenance hashes of archived certificates after *path-only* source changes.

The archived JSON remains immutable. For a verification script whose quoted
legacy source-directory tokens were updated, undo only those precise tokens
in memory and compare the original bytes with the archived checksum. This
does not waive SHA-256 checks of mathematical code or input data.
"""
from hashlib import sha256
from pathlib import Path
import re

_QUOTED_CANONICAL = re.compile(
    r"""(['"])papers/sections/(paper_arithmetic|paper_surgery|paper|notes)(?=/|\1)"""
)


def matches_archived_source(path: Path, archived_sha256: str) -> bool:
    raw = Path(path).read_bytes()
    if sha256(raw).hexdigest() == archived_sha256:
        return True
    try:
        source = raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    original_layout_source = _QUOTED_CANONICAL.sub(
        lambda match: match.group(1) + match.group(2), source
    )
    return (
        original_layout_source != source
        and sha256(original_layout_source.encode("utf-8")).hexdigest()
        == archived_sha256
    )
