import pytest
from app.utils.hashing import compute_sha256, verify_hash_match

def test_compute_sha256_format():
    data = b"Official Academic Degree Certificate Sample"
    cert_hash = compute_sha256(data)
    assert cert_hash.startswith("0x")
    assert len(cert_hash) == 66  # 0x + 64 hex characters
    # Check that remaining characters are valid hexadecimal
    int(cert_hash[2:], 16)

def test_deterministic_hashing():
    data1 = b"Identical Certificate Content"
    data2 = b"Identical Certificate Content"
    assert compute_sha256(data1) == compute_sha256(data2)

def test_tamper_sensitivity_avalanche_effect():
    """
    Validates that modifying even a single character or byte
    produces a completely different cryptographic fingerprint.
    """
    original = b"Student: Alice Smith | Degree: B.S. Computer Science | Year: 2026"
    tampered = b"Student: Alice Smith | Degree: M.S. Computer Science | Year: 2026"

    hash_orig = compute_sha256(original)
    hash_tamp = compute_sha256(tampered)

    assert hash_orig != hash_tamp
    assert not verify_hash_match(hash_orig, hash_tamp)

def test_verify_hash_match_case_insensitivity():
    sample_hash = "0x3a7bd117c2445e994917462ec5ab2eeae3c85bb049e3bf8e2a3962d3a39e7b23"
    upper_hash = sample_hash.upper()
    without_prefix = sample_hash[2:]

    assert verify_hash_match(sample_hash, upper_hash)
    assert verify_hash_match(sample_hash, without_prefix)
    assert not verify_hash_match(sample_hash, "0x0000000000000000000000000000000000000000000000000000000000000000")
