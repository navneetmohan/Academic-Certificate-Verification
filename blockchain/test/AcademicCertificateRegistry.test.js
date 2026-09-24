const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AcademicCertificateRegistry", function () {
  let registry;
  let owner;
  let authorizedIssuer;
  let unauthorizedWallet;
  let anotherIssuer;

  const validCertId = "CERT-2026-0001";
  const validCertHash = ethers.keccak256(ethers.toUtf8Bytes("Sample Academic Certificate PDF Content"));
  const modifiedCertHash = ethers.keccak256(ethers.toUtf8Bytes("Tampered Certificate Content"));

  beforeEach(async function () {
    [owner, authorizedIssuer, unauthorizedWallet, anotherIssuer] = await ethers.getSigners();

    const AcademicCertificateRegistry = await ethers.getContractFactory("AcademicCertificateRegistry");
    registry = await AcademicCertificateRegistry.deploy();
    await registry.waitForDeployment();

    // Authorize authorizedIssuer
    await registry.authorizeIssuer(authorizedIssuer.address);
  });

  describe("Issuer Management & Authorization", function () {
    it("Should allow the owner to authorize an issuer", async function () {
      expect(await registry.isAuthorizedIssuer(anotherIssuer.address)).to.be.false;
      await expect(registry.authorizeIssuer(anotherIssuer.address))
        .to.emit(registry, "IssuerAuthorized")
        .withArgs(anotherIssuer.address);
      expect(await registry.isAuthorizedIssuer(anotherIssuer.address)).to.be.true;
    });

    it("Should allow the owner to revoke an authorized issuer", async function () {
      expect(await registry.isAuthorizedIssuer(authorizedIssuer.address)).to.be.true;
      await expect(registry.revokeIssuer(authorizedIssuer.address))
        .to.emit(registry, "IssuerRevoked")
        .withArgs(authorizedIssuer.address);
      expect(await registry.isAuthorizedIssuer(authorizedIssuer.address)).to.be.false;
    });

    it("Should prevent non-owners from authorizing issuers", async function () {
      await expect(
        registry.connect(unauthorizedWallet).authorizeIssuer(anotherIssuer.address)
      ).to.be.revertedWithCustomError(registry, "OwnableUnauthorizedAccount");
    });

    it("Should prevent non-owners from revoking issuers", async function () {
      await expect(
        registry.connect(unauthorizedWallet).revokeIssuer(authorizedIssuer.address)
      ).to.be.revertedWithCustomError(registry, "OwnableUnauthorizedAccount");
    });
  });

  describe("Certificate Issuance", function () {
    // Test 1: Authorized institution issues certificate -> SUCCESS
    it("Test 1: Authorized institution issues certificate successfully", async function () {
      const tx = await registry
        .connect(authorizedIssuer)
        .issueCertificate(validCertId, validCertHash);

      await expect(tx)
        .to.emit(registry, "CertificateIssued")
        .withArgs(validCertId, validCertHash, authorizedIssuer.address, (await ethers.provider.getBlock("latest")).timestamp);

      const status = await registry.getCertificateStatus(validCertId);
      expect(status.exists).to.be.true;
      expect(status.certificateHash).to.equal(validCertHash);
      expect(status.issuer).to.equal(authorizedIssuer.address);
      expect(status.revoked).to.be.false;
    });

    // Test 2: Unauthorized wallet attempts issuance -> REVERT
    it("Test 2: Unauthorized wallet attempts issuance -> REVERT", async function () {
      await expect(
        registry
          .connect(unauthorizedWallet)
          .issueCertificate(validCertId, validCertHash)
      ).to.be.revertedWithCustomError(registry, "UnauthorizedIssuer")
        .withArgs(unauthorizedWallet.address);
    });

    // Test 8: Duplicate certificate ID -> REVERT
    it("Test 8: Duplicate certificate ID -> REVERT", async function () {
      await registry
        .connect(authorizedIssuer)
        .issueCertificate(validCertId, validCertHash);

      await expect(
        registry
          .connect(authorizedIssuer)
          .issueCertificate(validCertId, validCertHash)
      ).to.be.revertedWithCustomError(registry, "CertificateAlreadyExists")
        .withArgs(validCertId);
    });

    it("Should revert if certificate hash is zero", async function () {
      await expect(
        registry
          .connect(authorizedIssuer)
          .issueCertificate("CERT-ZERO", ethers.ZeroHash)
      ).to.be.revertedWithCustomError(registry, "InvalidCertificateHash");
    });
  });

  describe("Certificate Verification", function () {
    beforeEach(async function () {
      await registry
        .connect(authorizedIssuer)
        .issueCertificate(validCertId, validCertHash);
    });

    // Test 3: Verify valid certificate -> VALID
    it("Test 3: Verify valid certificate with matching hash -> VALID", async function () {
      const result = await registry.verifyCertificate(validCertId, validCertHash);
      expect(result.exists).to.be.true;
      expect(result.hashMatches).to.be.true;
      expect(result.revoked).to.be.false;
      expect(result.issuer).to.equal(authorizedIssuer.address);
      expect(result.issuedAt).to.be.greaterThan(0);
    });

    // Test 4: Modify certificate hash -> INVALID
    it("Test 4: Modify certificate hash -> INVALID (hashMatches == false)", async function () {
      const result = await registry.verifyCertificate(validCertId, modifiedCertHash);
      expect(result.exists).to.be.true;
      expect(result.hashMatches).to.be.false;
      expect(result.revoked).to.be.false;
      expect(result.issuer).to.equal(authorizedIssuer.address);
    });

    it("Should return exists=false for non-existent certificate ID", async function () {
      const result = await registry.verifyCertificate("NON-EXISTENT-CERT", validCertHash);
      expect(result.exists).to.be.false;
      expect(result.hashMatches).to.be.false;
      expect(result.revoked).to.be.false;
      expect(result.issuer).to.equal(ethers.ZeroAddress);
      expect(result.issuedAt).to.equal(0);
    });
  });

  describe("Certificate Revocation", function () {
    beforeEach(async function () {
      await registry
        .connect(authorizedIssuer)
        .issueCertificate(validCertId, validCertHash);
    });

    // Test 5: Authorized issuer revokes certificate -> REVOKED
    it("Test 5: Authorized issuer revokes certificate successfully", async function () {
      const tx = await registry
        .connect(authorizedIssuer)
        .revokeCertificate(validCertId);

      await expect(tx)
        .to.emit(registry, "CertificateRevoked")
        .withArgs(validCertId, authorizedIssuer.address, (await ethers.provider.getBlock("latest")).timestamp);

      const status = await registry.getCertificateStatus(validCertId);
      expect(status.exists).to.be.true;
      expect(status.revoked).to.be.true;
    });

    // Test 6: Verify certificate after revocation -> REVOKED
    it("Test 6: Verify certificate after revocation -> REVOKED", async function () {
      await registry.connect(authorizedIssuer).revokeCertificate(validCertId);

      const result = await registry.verifyCertificate(validCertId, validCertHash);
      expect(result.exists).to.be.true;
      expect(result.hashMatches).to.be.true;
      expect(result.revoked).to.be.true;
    });

    // Test 7: Unauthorized user attempts revocation -> REVERT
    it("Test 7: Unauthorized user attempts revocation -> REVERT", async function () {
      await expect(
        registry.connect(unauthorizedWallet).revokeCertificate(validCertId)
      ).to.be.revertedWithCustomError(registry, "OnlyOriginalIssuerCanRevoke")
        .withArgs(unauthorizedWallet.address, authorizedIssuer.address);
    });

    it("Should prevent another authorized issuer from revoking someone else's certificate", async function () {
      // Authorize another issuer
      await registry.authorizeIssuer(anotherIssuer.address);

      await expect(
        registry.connect(anotherIssuer).revokeCertificate(validCertId)
      ).to.be.revertedWithCustomError(registry, "OnlyOriginalIssuerCanRevoke")
        .withArgs(anotherIssuer.address, authorizedIssuer.address);
    });

    it("Should revert when attempting to revoke an already revoked certificate", async function () {
      await registry.connect(authorizedIssuer).revokeCertificate(validCertId);

      await expect(
        registry.connect(authorizedIssuer).revokeCertificate(validCertId)
      ).to.be.revertedWithCustomError(registry, "CertificateAlreadyRevoked")
        .withArgs(validCertId);
    });

    it("Should revert when attempting to revoke a non-existent certificate", async function () {
      await expect(
        registry.connect(authorizedIssuer).revokeCertificate("NON-EXISTENT")
      ).to.be.revertedWithCustomError(registry, "CertificateNotFound")
        .withArgs("NON-EXISTENT");
    });
  });
});
