// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title AcademicCertificateRegistry
 * @dev Blockchain-based registry for academic certificate verification.
 * Stores only cryptographic hashes and verification records off-chain privacy preservation.
 */
contract AcademicCertificateRegistry is Ownable {

    struct Certificate {
        bytes32 certificateHash; // SHA-256 hash of the generated PDF document
        address issuer;          // Wallet address of the issuing institution
        uint256 issuedAt;        // Block timestamp when issued
        bool revoked;            // Revocation state flag
    }

    // keccak256(bytes(certificateId)) => Certificate record
    mapping(bytes32 => Certificate) private certificates;

    // Authorized educational institutions / issuer wallets
    mapping(address => bool) public authorizedIssuers;

    // Events
    event IssuerAuthorized(address indexed issuer);
    event IssuerRevoked(address indexed issuer);
    event CertificateIssued(
        string certificateId,
        bytes32 indexed certificateHash,
        address indexed issuer,
        uint256 issuedAt
    );
    event CertificateRevoked(
        string certificateId,
        address indexed issuer,
        uint256 revokedAt
    );

    // Custom Errors for gas optimization and explicit revert reasons
    error UnauthorizedIssuer(address caller);
    error OnlyOriginalIssuerCanRevoke(address caller, address originalIssuer);
    error CertificateAlreadyExists(string certificateId);
    error CertificateNotFound(string certificateId);
    error CertificateAlreadyRevoked(string certificateId);
    error InvalidCertificateHash();
    error InvalidIssuerAddress();

    modifier onlyAuthorizedIssuer() {
        if (!authorizedIssuers[msg.sender]) {
            revert UnauthorizedIssuer(msg.sender);
        }
        _;
    }

    /**
     * @dev Initialize contract with owner as contract administrator
     */
    constructor() Ownable(msg.sender) {}

    /**
     * @notice Authorize an institution wallet to issue certificates
     * @param _issuer Wallet address of the institution
     */
    function authorizeIssuer(address _issuer) external onlyOwner {
        if (_issuer == address(0)) {
            revert InvalidIssuerAddress();
        }
        authorizedIssuers[_issuer] = true;
        emit IssuerAuthorized(_issuer);
    }

    /**
     * @notice Revoke an institution wallet's issuing authorization
     * @param _issuer Wallet address of the institution
     */
    function revokeIssuer(address _issuer) external onlyOwner {
        if (_issuer == address(0)) {
            revert InvalidIssuerAddress();
        }
        authorizedIssuers[_issuer] = false;
        emit IssuerRevoked(_issuer);
    }

    /**
     * @notice Check whether a given address is an authorized certificate issuer
     * @param _issuer Wallet address to check
     */
    function isAuthorizedIssuer(address _issuer) external view returns (bool) {
        return authorizedIssuers[_issuer];
    }

    /**
     * @notice Issue a new certificate on the blockchain
     * @param _certificateId Unique identifier of the certificate (e.g. CERT-2026-0001)
     * @param _certificateHash SHA-256 cryptographic hash of the certificate document
     */
    function issueCertificate(
        string calldata _certificateId,
        bytes32 _certificateHash
    ) external onlyAuthorizedIssuer {
        if (_certificateHash == bytes32(0)) {
            revert InvalidCertificateHash();
        }

        bytes32 certKey = keccak256(bytes(_certificateId));
        if (certificates[certKey].issuedAt != 0) {
            revert CertificateAlreadyExists(_certificateId);
        }

        certificates[certKey] = Certificate({
            certificateHash: _certificateHash,
            issuer: msg.sender,
            issuedAt: block.timestamp,
            revoked: false
        });

        emit CertificateIssued(_certificateId, _certificateHash, msg.sender, block.timestamp);
    }

    /**
     * @notice Verify a certificate by ID and document hash
     * @param _certificateId Unique certificate identifier
     * @param _certificateHash SHA-256 hash of the certificate document to compare
     * @return exists True if certificate exists on-chain
     * @return hashMatches True if provided hash matches on-chain fingerprint
     * @return revoked True if certificate has been revoked
     * @return issuer Address of the issuing institution
     * @return issuedAt Timestamp when certificate was issued
     */
    function verifyCertificate(
        string calldata _certificateId,
        bytes32 _certificateHash
    ) external view returns (
        bool exists,
        bool hashMatches,
        bool revoked,
        address issuer,
        uint256 issuedAt
    ) {
        bytes32 certKey = keccak256(bytes(_certificateId));
        Certificate memory cert = certificates[certKey];

        if (cert.issuedAt == 0) {
            return (false, false, false, address(0), 0);
        }

        exists = true;
        hashMatches = (cert.certificateHash == _certificateHash);
        revoked = cert.revoked;
        issuer = cert.issuer;
        issuedAt = cert.issuedAt;
    }

    /**
     * @notice Revoke an issued certificate
     * @param _certificateId Unique certificate identifier
     */
    function revokeCertificate(string calldata _certificateId) external {
        bytes32 certKey = keccak256(bytes(_certificateId));
        Certificate storage cert = certificates[certKey];

        if (cert.issuedAt == 0) {
            revert CertificateNotFound(_certificateId);
        }

        if (cert.issuer != msg.sender) {
            revert OnlyOriginalIssuerCanRevoke(msg.sender, cert.issuer);
        }

        if (cert.revoked) {
            revert CertificateAlreadyRevoked(_certificateId);
        }

        cert.revoked = true;
        emit CertificateRevoked(_certificateId, msg.sender, block.timestamp);
    }

    /**
     * @notice Get on-chain status of a certificate by ID
     * @param _certificateId Unique certificate identifier
     * @return exists True if certificate exists
     * @return certificateHash Stored SHA-256 hash
     * @return issuer Address of the issuing institution
     * @return issuedAt Timestamp when certificate was issued
     * @return revoked Revocation status
     */
    function getCertificateStatus(
        string calldata _certificateId
    ) external view returns (
        bool exists,
        bytes32 certificateHash,
        address issuer,
        uint256 issuedAt,
        bool revoked
    ) {
        bytes32 certKey = keccak256(bytes(_certificateId));
        Certificate memory cert = certificates[certKey];

        if (cert.issuedAt == 0) {
            return (false, bytes32(0), address(0), 0, false);
        }

        return (
            true,
            cert.certificateHash,
            cert.issuer,
            cert.issuedAt,
            cert.revoked
        );
    }
}
