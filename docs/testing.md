# Testing & Verification Report

## 1. Test Strategy Overview

The CertLedger platform employs a three-tiered testing strategy:
1. **Smart Contract Unit Tests**: 17 Mocha/Chai/Ethers tests validating smart contract access controls, edge cases, and all 8 specification requirements.
2. **Backend Unit & Integration Tests**: 12 Pytest tests covering cryptographic SHA-256 formatting, avalanche sensitivity, JWT authentication, and mocked verification states.
3. **End-to-End Demonstration**: Automated 11-step integration script against a live running Hardhat node and live FastAPI server.

---

## 2. Smart Contract Test Matrix (`blockchain/test/`)

Run command: `npm test` inside `blockchain/`

| Test ID | Test Scenario | Expected Outcome | Actual Result |
| :--- | :--- | :--- | :---: |
| **TC-SC-01** | Owner authorizes new institution wallet | Emits `IssuerAuthorized`, sets true | **PASS** |
| **TC-SC-02** | Owner revokes institution authorization | Emits `IssuerRevoked`, sets false | **PASS** |
| **TC-SC-03** | Unauthorized wallet attempts to authorize | Reverts `OwnableUnauthorizedAccount` | **PASS** |
| **TC-SC-04** | Unauthorized wallet attempts to revoke authorization | Reverts `OwnableUnauthorizedAccount` | **PASS** |
| **TC-SC-05** | Authorized institution issues certificate (Req 1) | Emits `CertificateIssued`, stores on-chain | **PASS** |
| **TC-SC-06** | Unauthorized wallet attempts issuance (Req 2) | Reverts `UnauthorizedIssuer` | **PASS** |
| **TC-SC-07** | Duplicate certificate ID submission (Req 8) | Reverts `CertificateAlreadyExists` | **PASS** |
| **TC-SC-08** | Zero certificate hash submission | Reverts `InvalidCertificateHash` | **PASS** |
| **TC-SC-09** | Verify valid certificate with matching hash (Req 3) | Returns `exists=true, hashMatches=true` | **PASS** |
| **TC-SC-10** | Verify certificate with modified hash (Req 4) | Returns `exists=true, hashMatches=false` | **PASS** |
| **TC-SC-11** | Verify non-existent certificate ID | Returns `exists=false` | **PASS** |
| **TC-SC-12** | Authorized issuer revokes certificate (Req 5) | Emits `CertificateRevoked`, sets `revoked=true` | **PASS** |
| **TC-SC-13** | Verify certificate after revocation (Req 6) | Returns `exists=true, revoked=true` | **PASS** |
| **TC-SC-14** | Unauthorized wallet attempts revocation (Req 7) | Reverts `OnlyOriginalIssuerCanRevoke` | **PASS** |
| **TC-SC-15** | Rival authorized issuer attempts revocation | Reverts `OnlyOriginalIssuerCanRevoke` | **PASS** |
| **TC-SC-16** | Re-revoking an already revoked certificate | Reverts `CertificateAlreadyRevoked` | **PASS** |
| **TC-SC-17** | Revoking a non-existent certificate | Reverts `CertificateNotFound` | **PASS** |

---

## 3. Backend Test Matrix (`backend/tests/`)

Run command: `.\venv\Scripts\python -m pytest -v` inside `backend/`

| Test ID | Test Name | Tested Feature | Actual Result |
| :--- | :--- | :--- | :---: |
| **TC-BE-01** | `test_root_endpoint` | Root API service status and docs URL | **PASS** |
| **TC-BE-02** | `test_auth_login_successful` | JWT creation with seeded admin credentials | **PASS** |
| **TC-BE-03** | `test_auth_login_invalid_password` | 401 response on invalid credentials | **PASS** |
| **TC-BE-04** | `test_get_current_user_authenticated` | Protected route `/api/auth/me` with JWT | **PASS** |
| **TC-BE-05** | `test_verify_non_existent_certificate` | Status `NOT_FOUND` on unknown cert | **PASS** |
| **TC-BE-06** | `test_verify_revoked_certificate` | Status `REVOKED` on revoked record | **PASS** |
| **TC-BE-07** | `test_verify_valid_certificate` | Status `VALID` on authentic record | **PASS** |
| **TC-BE-08** | `test_pdf_generation_magic_bytes` | ReportLab PDF header `%PDF-` validation | **PASS** |
| **TC-BE-09** | `test_compute_sha256_format` | 0x-prefixed 66-character bytes32 output | **PASS** |
| **TC-BE-10** | `test_deterministic_hashing` | Reproducible SHA-256 for identical inputs | **PASS** |
| **TC-BE-11** | `test_tamper_sensitivity_avalanche_effect` | Avalanche effect on single byte change | **PASS** |
| **TC-BE-12** | `test_verify_hash_match_case_insensitivity` | Case-insensitive hash comparison | **PASS** |

---

## 4. End-to-End Live Blockchain Demonstration (`scripts/e2e_demo.py`)

Run command: `.\backend\venv\Scripts\python scripts/e2e_demo.py`

| Step | Operation | Result |
| :---: | :--- | :--- |
| **1** | System connectivity check | Connected to local EVM contract `0x5FbDB2315678afecb367f032d93F642f64180aa3` |
| **2** | Institution Admin Login | JWT access token obtained for Metropolitan State University |
| **3** | Issue Certificate | PDF created, SHA-256 generated, mined into block #1 |
| **4** | Download Certificate PDF | Downloaded 5,113 bytes of valid PDF diploma |
| **5** | Verify by ID | Smart contract returned `VALID` |
| **6** | Verify by Uploading Original PDF | Document hash matched blockchain hash -> `VALID` |
| **7** | Tamper Attack Demonstration | 10 bytes modified in PDF -> Hash mismatch -> `INVALID / MODIFIED` |
| **8** | Revoke Certificate | Called `revokeCertificate()` -> mined into block #2 |
| **9** | Verify Revoked Certificate | Smart contract returned `REVOKED` |
| **10** | Unknown Certificate Lookup | Queried fake ID -> returned `NOT_FOUND` |
| **11** | Transaction Inspector | Block #3 confirmed on Hardhat ledger with gas metrics |
