# Blockchain Layer: Academic Certificate Registry

This module contains the Solidity smart contracts, Hardhat configuration, unit tests, and deployment automation for the decentralized credential verification system.

## Smart Contract: `AcademicCertificateRegistry.sol`

- **Solidity Version**: `^0.8.20`
- **Inheritance**: OpenZeppelin `Ownable`
- **Key Concepts**:
  - `struct Certificate`: Stores `bytes32 certificateHash`, `address issuer`, `uint256 issuedAt`, `bool revoked`.
  - `mapping(bytes32 => Certificate) certificates`: Keyed by `keccak256(bytes(certificateId))`.
  - `mapping(address => bool) authorizedIssuers`: Controlled by contract owner.

## Commands

```bash
# 1. Install dependencies
npm install

# 2. Compile contracts
npm run compile

# 3. Run all 17 automated tests
npm test

# 4. Start local Hardhat node
npm run node

# 5. Deploy contract to local node
npm run deploy:local
```
