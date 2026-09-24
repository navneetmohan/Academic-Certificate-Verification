# Privacy Architecture & Student Data Protection

## 1. The Conflict Between Blockchains and Data Privacy

Public and consortium blockchains are **immutable** and **globally transparent**. Once data is written to a block, it can never be altered, deleted, or scrubbed.

This characteristic creates a severe conflict with modern privacy legislation:
- **General Data Protection Regulation (GDPR)**: Mandates the "Right to Erasure" (Article 17) and "Data Minimization" (Article 5).
- **Family Educational Rights and Privacy Act (FERPA)**: Strictly prohibits the unauthorized disclosure of student educational records and personally identifiable information.

If a student's name, identification number, GPA, disciplinary status, or home address were committed directly to smart contract storage, the educational institution would permanently violate these privacy mandates.

---

## 2. CertLedger Privacy Design Principles

### Principle 1: Zero Student PII On-Chain
The `AcademicCertificateRegistry` smart contract never stores or processes:
- Student names
- Student identification or roll numbers
- Grades, marks, CGPA, or performance metrics
- Email addresses or telephone numbers
- Physical residential addresses

### Principle 2: Cryptographic Pseudonymity via One-Way Hashing
The on-chain certificate fingerprint is computed via:
$$\text{certificateHash} = \text{SHA-256}(\text{Canonical PDF Bytes})$$

Because SHA-256 is computationally infeasible to invert (pre-image resistance), an observer viewing the public blockchain ledger cannot reverse-engineer the student's name, degree, or personal information from the 32-byte hash `0x4a20...e56e`.

### Principle 3: Unlinkability
Each certificate is identified on-chain by a pseudorandom or sequential opaque token (e.g., `CERT-2026-0001`). No correlation between different credentials earned by the same student can be discovered by crawling the blockchain, preventing profiling and data harvesting.

---

## 3. Privacy Comparison

| Data Field | Stored On Blockchain? | Stored Off-Chain? | Visibility |
| :--- | :---: | :---: | :--- |
| **Certificate ID** | Yes | Yes | Public verification token |
| **SHA-256 Hash** | Yes | Yes | Public integrity proof |
| **Issuer Address** | Yes | Yes | Public institutional wallet |
| **Block Timestamp** | Yes | Yes | Public minting timestamp |
| **Revoked Flag** | Yes | Yes | Public validity indicator |
| **Student Full Name** | **NO** | Yes | Private / Controlled off-chain |
| **Student Roll / ID** | **NO** | Yes | Private / Controlled off-chain |
| **Complete PDF File** | **NO** | Yes | Held by student / university |
