const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("Starting deployment of AcademicCertificateRegistry...");

  const [deployer, institutionAccount] = await hre.ethers.getSigners();

  console.log(`Deploying contracts with deployer (admin): ${deployer.address}`);
  console.log(`Default institution account to authorize: ${institutionAccount.address}`);

  const AcademicCertificateRegistry = await hre.ethers.getContractFactory("AcademicCertificateRegistry");
  const registry = await AcademicCertificateRegistry.deploy();
  await registry.waitForDeployment();

  const contractAddress = await registry.getAddress();
  console.log(`AcademicCertificateRegistry deployed to: ${contractAddress}`);

  // Authorize the institution account
  console.log(`Authorizing institution wallet ${institutionAccount.address}...`);
  const authTx = await registry.authorizeIssuer(institutionAccount.address);
  await authTx.wait();
  console.log(`Institution wallet authorized successfully.`);

  // Prepare deployment artifact for backend
  const artifactPath = path.join(
    __dirname,
    "../artifacts/contracts/AcademicCertificateRegistry.sol/AcademicCertificateRegistry.json"
  );
  const artifactData = JSON.parse(fs.readFileSync(artifactPath, "utf8"));

  const deploymentInfo = {
    contractAddress: contractAddress,
    network: hre.network.name,
    chainId: (await hre.ethers.provider.getNetwork()).chainId.toString(),
    adminAddress: deployer.address,
    authorizedIssuer: institutionAccount.address,
    abi: artifactData.abi,
    deployedAt: new Date().toISOString()
  };

  // Save to blockchain folder
  const localDest = path.join(__dirname, "../deployed_contract.json");
  fs.writeFileSync(localDest, JSON.stringify(deploymentInfo, null, 2));
  console.log(`Deployment info saved to: ${localDest}`);

  // Save to backend folder
  const backendDestDir = path.join(__dirname, "../../backend/app/blockchain");
  if (!fs.existsSync(backendDestDir)) {
    fs.mkdirSync(backendDestDir, { recursive: true });
  }
  const backendDest = path.join(backendDestDir, "contract_data.json");
  fs.writeFileSync(backendDest, JSON.stringify(deploymentInfo, null, 2));
  console.log(`Deployment info saved to backend: ${backendDest}`);
}

main().catch((error) => {
  console.error("Deployment failed:", error);
  process.exitCode = 1;
});
