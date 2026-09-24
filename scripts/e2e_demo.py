import sys
import os
import requests
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def log_step(step_num, title):
    print(f"\n{'='*70}")
    print(f"STEP {step_num}: {title.upper()}")
    print(f"{'='*70}")

def main():
    print("Starting End-to-End Blockchain Certificate Verification Demonstration...\n")

    # 1. Health check
    log_step(1, "Verify System Status & Blockchain Connectivity")
    res = requests.get(f"{BASE_URL}/")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health = res.json()
    print(f"[*] API Status: {health['status']}")
    print(f"[*] Blockchain Connected: {health['blockchain_connected']}")
    print(f"[*] Contract Address: {health['contract_address']}")
    assert health['blockchain_connected'] is True, "Blockchain not connected!"

    # 2. Institution Login
    log_step(2, "Institution Login & Authentication")
    login_payload = {
        "email": "admin@university.edu",
        "password": "adminpassword123"
    }
    res = requests.post(f"{BASE_URL}/api/auth/login", json=login_payload)
    assert res.status_code == 200, f"Login failed: {res.text}"
    auth_data = res.json()
    token = auth_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"[✓] Logged in as: {auth_data['institution']['name']}")
    print(f"[✓] Issuer Wallet Address: {auth_data['institution']['wallet_address']}")
    print(f"[✓] JWT Access Token Generated: {token[:20]}...")

    # 3. Issue Certificate
    log_step(3, "Issue Academic Certificate on Blockchain")
    student_payload = {
        "student_name": "Sophia Elena Martinez",
        "student_id": "MSU-CS-2026-042",
        "degree": "Bachelor of Science in Computer Science & Engineering",
        "department": "School of Computing & Information Systems",
        "institution_name": "Metropolitan State University",
        "graduation_year": 2026,
        "certificate_type": "Bachelor of Science Degree",
        "issue_date": "2026-09-24"
    }
    res = requests.post(f"{BASE_URL}/api/certificates", json=student_payload, headers=headers)
    assert res.status_code == 201, f"Issuance failed: {res.text}"
    cert_data = res.json()
    cert_id = cert_data["certificate_id"]
    cert_hash = cert_data["certificate_hash"]
    tx_hash = cert_data["blockchain_tx_hash"]
    print(f"[✓] Certificate ID Generated: {cert_id}")
    print(f"[✓] Document SHA-256 Hash: {cert_hash}")
    print(f"[✓] Blockchain Transaction Hash: {tx_hash}")
    print(f"[✓] Verification URL: {cert_data['verification_url']}")

    # 4. Download Generated PDF
    log_step(4, "Download Issued PDF Credential")
    res = requests.get(f"{BASE_URL}/api/certificates/{cert_id}/download")
    assert res.status_code == 200, f"Download failed: {res.text}"
    original_pdf_bytes = res.content
    print(f"[✓] Downloaded PDF ({len(original_pdf_bytes)} bytes)")
    assert original_pdf_bytes.startswith(b"%PDF-"), "Invalid PDF header!"

    # 5. Employer / Third-Party Verification by ID
    log_step(5, "Public Verification by Certificate ID")
    res = requests.get(f"{BASE_URL}/api/verify/{cert_id}")
    assert res.status_code == 200, f"Verification failed: {res.text}"
    verify_res = res.json()
    print(f"[*] Verification Verdict: {verify_res['status']}")
    print(f"[*] Authentic: {verify_res['is_authentic']}")
    print(f"[*] Issuing Institution: {verify_res['institution_name']}")
    print(f"[*] Issuer Wallet: {verify_res['issuer_address']}")
    print(f"[*] Message: {verify_res['message']}")
    assert verify_res["status"] == "VALID", f"Expected VALID, got {verify_res['status']}"
    assert verify_res["is_authentic"] is True

    # 6. Employer Verification by Uploading Original PDF
    log_step(6, "Public Verification by Uploading Authentic PDF Document")
    files = {"file": ("original_certificate.pdf", original_pdf_bytes, "application/pdf")}
    res = requests.post(f"{BASE_URL}/api/verify", files=files, data={"certificate_id": cert_id})
    assert res.status_code == 200, f"File verification failed: {res.text}"
    upload_res = res.json()
    print(f"[*] Uploaded PDF Status: {upload_res['status']}")
    print(f"[*] Calculated Hash: {upload_res['calculated_hash']}")
    print(f"[*] Blockchain Hash: {upload_res['onchain_hash']}")
    print(f"[*] Hash Matches: {upload_res['hash_matches']}")
    assert upload_res["status"] == "VALID"
    assert upload_res["hash_matches"] is True
    print("[✓] RESULT: VALID CERTIFICATE - Cryptographic Fingerprint Verified on Blockchain!")

    # 7. Tampering Demonstration
    log_step(7, "Tampering Attack Demonstration (Altered PDF Document)")
    print("[!] Simulating malicious forgery: modifying student grade / degree in PDF binary...")
    tampered_bytes = bytearray(original_pdf_bytes)
    # Alter 10 bytes in the document stream
    for i in range(150, 160):
        tampered_bytes[i] = (tampered_bytes[i] + 7) % 256
    tampered_bytes = bytes(tampered_bytes)

    files_tampered = {"file": ("tampered_certificate.pdf", tampered_bytes, "application/pdf")}
    res = requests.post(f"{BASE_URL}/api/verify", files=files_tampered, data={"certificate_id": cert_id})
    assert res.status_code == 200, f"Tampered verification failed: {res.text}"
    tamper_res = res.json()
    print(f"[*] Tampered PDF Status: {tamper_res['status']}")
    print(f"[*] Altered Document Hash: {tamper_res['calculated_hash']}")
    print(f"[*] Immutable Blockchain Hash: {tamper_res['onchain_hash']}")
    print(f"[*] Hash Matches: {tamper_res['hash_matches']}")
    print(f"[*] Message: {tamper_res['message']}")
    assert tamper_res["status"] == "INVALID", f"Expected INVALID, got {tamper_res['status']}"
    assert tamper_res["hash_matches"] is False
    print("[✓] RESULT: DETECTED FORGERY / TAMPERING - Cryptographic SHA-256 mismatch!")

    # 8. Certificate Revocation on Blockchain
    log_step(8, "Authorized Institution Revokes Certificate")
    print(f"[!] Submitting revokeCertificate('{cert_id}') transaction to smart contract...")
    res = requests.post(f"{BASE_URL}/api/certificates/{cert_id}/revoke", headers=headers)
    assert res.status_code == 200, f"Revocation failed: {res.text}"
    revoke_data = res.json()
    print(f"[✓] Certificate Revocation Confirmed on Ledger!")
    print(f"[✓] Revocation Tx Hash: {revoke_data['blockchain_tx_hash']}")
    print(f"[✓] Off-chain Revoked Flag: {revoke_data['revoked']}")

    # 9. Verifying Revoked Certificate
    log_step(9, "Public Verification of Revoked Certificate")
    res = requests.get(f"{BASE_URL}/api/verify/{cert_id}")
    assert res.status_code == 200, f"Revoked verification failed: {res.text}"
    revoked_verify = res.json()
    print(f"[*] Revoked Status Verdict: {revoked_verify['status']}")
    print(f"[*] Is Revoked Flag: {revoked_verify['is_revoked']}")
    print(f"[*] Authentic: {revoked_verify['is_authentic']}")
    print(f"[*] Message: {revoked_verify['message']}")
    assert revoked_verify["status"] == "REVOKED", f"Expected REVOKED, got {revoked_verify['status']}"
    assert revoked_verify["is_revoked"] is True
    assert revoked_verify["is_authentic"] is False
    print("[✓] RESULT: CERTIFICATE REVOKED - Smart Contract Blocked Unauthorized Usage!")

    # 10. Unknown Certificate Test
    log_step(10, "Verification of Unknown / Non-Existent Certificate")
    res = requests.get(f"{BASE_URL}/api/verify/CERT-FAKE-9999")
    assert res.status_code == 200
    unknown_res = res.json()
    print(f"[*] Unknown Certificate Status: {unknown_res['status']}")
    assert unknown_res["status"] == "NOT_FOUND"
    print("[✓] RESULT: CERTIFICATE NOT FOUND on Blockchain!")

    # 11. Transaction Receipt Inspector Test
    log_step(11, "Live Blockchain Transaction Receipt Inspector")
    res = requests.get(f"{BASE_URL}/api/blockchain/transaction/{tx_hash}")
    assert res.status_code == 200, f"Transaction inspector failed: {res.text}"
    tx_details = res.json()
    print(f"[✓] Block Number: {tx_details['block_number']}")
    print(f"[✓] Gas Used: {tx_details['gas_used']}")
    print(f"[✓] From (Issuer): {tx_details['from_address']}")
    print(f"[✓] To (Contract): {tx_details['to_address']}")
    print(f"[✓] Confirmations: {tx_details['confirmations']}")

    print("\n" + "="*70)
    print("ALL 11 END-TO-END DEMONSTRATION STEPS COMPLETED WITH 100% SUCCESS!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
