import hashlib
from typing import Union

def compute_sha256(data: Union[bytes, str]) -> str:
    """
    Computes deterministic SHA-256 hash of bytes or string.
    Returns 0x-prefixed 64-character hex string representing bytes32 for Ethereum smart contracts.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    
    sha = hashlib.sha256(data)
    digest_hex = sha.hexdigest()
    return f"0x{digest_hex}"

def verify_hash_match(calculated_hash: str, expected_hash: str) -> bool:
    """
    Compares two hashes case-insensitively, handling optional 0x prefixes.
    """
    c = calculated_hash.lower()
    e = expected_hash.lower()
    if not c.startswith("0x"):
        c = f"0x{c}"
    if not e.startswith("0x"):
        e = f"0x{e}"
    return c == e
