# Security Specification & Threat Model

## 1. Security Objectives

1. **Integrity**: Ensure that any alteration to an issued academic certificate (such as student name, GPA, honors, or conferred degree) renders the certificate mathematically invalid.
2. **Authenticity**: Guarantee that only accredited and authorized academic institutions can mint certificates onto the blockchain registry.
3. **Non-Repudiation**: Ensure that issuing authorities cannot deny having issued a credential once recorded on the immutable ledger.
4. **Access Control**: Prevent unauthorized wallets or rival universities from revoking or overwriting certificates they did not issue.
5. **Read-Only Verifier Safety**: Ensure external employers and verifiers have zero execution privileges over the smart contract state.

---

## 2. Threat Modeling & Mitigations

| Threat | Attack Vector | Smart Contract / System Defense |
| :--- | :--- | :--- |
| **Unauthorized Issuance** | Rogue wallet calls `issueCertificate()` directly. | Enforced by `onlyAuthorizedIssuer` modifier. Checks `authorizedIssuers[msg.sender] == true`, reverts with custom error `UnauthorizedIssuer`. |
| **Credential Forgery / Alteration** | Attacker edits student name or degree in a PDF editor. | Changing even one bit in the PDF file completely alters its SHA-256 digest (avalanche effect). Comparison against on-chain hash fails (`hashMatches == false`), returning `INVALID / MODIFIED`. |
| **Rival Institution Revocation** | University B attempts to revoke a degree issued by University A. | Enforced by `require(cert.issuer == msg.sender)`. Reverts with custom error `OnlyOriginalIssuerCanRevoke(caller, originalIssuer)`. |
| **Silent Overwrite** | Attacker attempts to re-issue an existing `certificateId` with a different hash. | Enforced by `require(certificates[certKey].issuedAt == 0)`. Reverts with custom error `CertificateAlreadyExists(certificateId)`. |
| **Duplicate Revocation** | Issuer attempts to double-revoke an already revoked record. | Enforced by `require(!cert.revoked)`. Reverts with custom error `CertificateAlreadyRevoked(certificateId)`. |
| **Zero Hash Exploit** | Caller submits `0x000...` to bypass checks. | Enforced by `require(_certificateHash != bytes32(0))`. Reverts with custom error `InvalidCertificateHash()`. |

---

## 3. Cryptographic Proofing: The SHA-256 Avalanche Effect

SHA-256 (Secure Hash Algorithm 256-bit) is a cryptographic hash function that produces a unique 256-bit (32-byte) message digest. 

A critical property leveraged by CertLedger is the **avalanche effect**: if an input is modified even slightly (for example, flipping a single bit, modifying a student's grade from "B" to "A", or changing a single pixel in the university crest), the resulting output hash changes so radically that no correlation can be established with the original hash.

### Empirical Demonstration:
- **Authentic PDF**:
  `SHA-256: 0x4a20ade9a5c6ce8d9f0b6fef96127740c62cd784b3b3d2e6c00f8def710de56e`
- **Tampered PDF (10 bytes modified)**:
  `SHA-256: 0x2bf8beefbc42be960113398071cddf07bc0dae36d3cfe704bca8bc2398ffc793`
- **Outcome**: Immediate hash mismatch, preventing forged credentials from validating.

---

## 4. Key Management & Production Considerations

> [!WARNING]
> In this academic demonstration environment, Hardhat development private keys are used locally. For a production deployment, institutions must utilize Hardware Security Modules (HSM), Multi-Party Computation (MPC), or institutional multi-signature wallets (e.g., Safe / Gnosis Safe) to safeguard issuing private keys.
