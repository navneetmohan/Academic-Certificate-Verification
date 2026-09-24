# Architecture Specification: Blockchain Academic Certificate Verification

## 1. Executive Summary

The **CertLedger** system implements a hybrid on-chain/off-chain decentralized architecture for the issuance, verification, and revocation of academic credentials. The system balances immutable blockchain integrity proofs with the strict privacy and efficiency requirements of higher educational institutions.

---

## 2. Fundamental Architectural Decision: Hybrid Storage Model

A foundational question in blockchain application design is:
> *Should complete digital documents (e.g., PDF certificates) be stored directly on-chain, or should only cryptographic commitments and minimal verification state be recorded?*

### The Decision: **Off-Chain Content, On-Chain Fingerprints**

In this micro-project:
1. **On-Chain**: Stored strictly within Ethereum Virtual Machine (EVM) smart contract storage:
   - `bytes32 certificateHash`: The 256-bit SHA-256 digest of the canonical PDF document.
   - `address issuer`: The authorized institution wallet address that minted the record.
   - `uint256 issuedAt`: The immutable block timestamp of issuance.
   - `bool revoked`: The cryptographic revocation state flag.
2. **Off-Chain**: Stored within relational storage (PostgreSQL/SQLite) and the file system:
   - Student Personally Identifiable Information (PII): Full Name, Student ID, Registration Number.
   - Program Details: Conferred Degree, Academic Department, Honors, Year of Graduation.
   - Issued Document: The rendered, high-resolution PDF certificate with embedded verification QR code.

---

## 3. Justification & Trade-Off Analysis

| Criteria | On-Chain PDF Storage | Hybrid Model (CertLedger) | Justification |
| :--- | :--- | :--- | :--- |
| **Student Privacy** | Complete exposure to public ledger watchers | Zero PII on-chain; private data never enters mempool | Complies with GDPR Right to be Forgotten and FERPA privacy regulations. |
| **Storage & Gas Costs** | Exorbitant (~$500 - $5,000+ per 100KB on public EVM) | Minimal fixed cost (1 `SSTORE` for 32-byte hash) | Highly scalable; transactions require only ~96,000 gas units. |
| **Tamper Detection** | Document verified internally | SHA-256 cryptographic avalanche effect | Modifying a single character off-chain causes a 100% hash mismatch against the ledger. |
| **Revocation Velocity** | Difficult or requires state replacement | Instantaneous boolean update (`revoked = true`) | Authorized issuer can immediately revoke compromised credentials. |

---

## 4. Component Architecture

```
[Institution Admin] ---------> [React 18 / Tailwind Frontend]
                                           |
                                  REST API (JSON / JWT)
                                           v
                                [FastAPI Backend Engine]
                                   /       |         \
                                  /        |          \
                 [ReportLab PDF Engine]    |    [SQLAlchemy ORM]
                          |                |           |
                   [SHA-256 Hash]          |     [(PostgreSQL / SQLite)]
                          \                |
                           v               v
                        [Web3.py Client Service]
                                   |
                                JSON-RPC
                                   v
             [AcademicCertificateRegistry.sol Smart Contract]
                                   |
                      [Local Hardhat EVM Node]
```

### A. Frontend Layer (React 18 + Vite + Tailwind CSS)
- **Institution Dashboard**: Provides issuance analytics, active/revoked credential KPIs, and recent issuance records.
- **Issuance Studio**: Form with real-time diploma layout rendering and automatic blockchain transaction signing.
- **Verification Portal**: Multi-modal verification supporting Certificate ID lookup, PDF upload with client/server hash comparison, and a live Tamper Demonstration interface.
- **QR Landing Endpoint (`/verify/:id`)**: Displays immediate, tamper-evident cryptographic verdicts upon scanning credentials.

### B. Backend Layer (Python 3.10 + FastAPI + Web3.py)
- **Certificate Engine**: Uses ReportLab to generate landscape-format academic diplomas with vector security seals and dynamic QR codes pointing to the verification destination.
- **Cryptographic Hasher**: Calculates canonical SHA-256 byte digests, formatted as `0x<64-hex>` strings corresponding to Solidity `bytes32`.
- **Blockchain Gateway**: Interacts with the deployed `AcademicCertificateRegistry` smart contract over JSON-RPC, handling transaction construction, nonce tracking, gas estimation, and cryptographic signing via the authorized institutional private key.

### C. Blockchain Layer (Solidity ^0.8.20 + Hardhat)
- **Access Control**: Inherits OpenZeppelin `Ownable`. Only the contract owner (system deployer) can authorize or revoke institution wallets.
- **State Registry**: Keyed by `keccak256(bytes(certificateId))` for fixed-size 32-byte key mapping.
- **Immutable Operations**:
  - `issueCertificate(string certId, bytes32 certHash)`: Records fingerprint, enforces issuer authorization, prevents duplicate IDs.
  - `verifyCertificate(string certId, bytes32 certHash)`: Pure view call returning `(exists, hashMatches, revoked, issuer, issuedAt)`.
  - `revokeCertificate(string certId)`: Only callable by the original issuing institution wallet.
