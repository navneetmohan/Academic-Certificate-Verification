import os
import json
import logging
from typing import Dict, Any, Optional
from web3 import Web3
from web3.exceptions import ContractLogicError, TransactionNotFound

logger = logging.getLogger(__name__)

class BlockchainService:
    def __init__(self):
        self.rpc_url = os.getenv("BLOCKCHAIN_RPC_URL", "http://127.0.0.1:8545")
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        # Hardhat Account #1 (Default authorized issuer wallet)
        self.issuer_private_key = os.getenv(
            "ISSUER_PRIVATE_KEY",
            "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"
        )
        self.issuer_address = os.getenv(
            "DEFAULT_INSTITUTION_WALLET",
            "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
        )

        self.contract_address = os.getenv("CONTRACT_ADDRESS")
        self.contract_abi = None
        self.contract = None

        self._load_contract_metadata()

    def _load_contract_metadata(self):
        """Loads contract address and ABI from disk or env"""
        data_path = os.path.join(os.path.dirname(__file__), "contract_data.json")
        if os.path.exists(data_path):
            try:
                with open(data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if not self.contract_address:
                        self.contract_address = data.get("contractAddress")
                    self.contract_abi = data.get("abi")
            except Exception as e:
                logger.warning(f"Could not load contract_data.json: {e}")

        if self.contract_address and self.contract_abi and self.w3.is_connected():
            checksum_address = Web3.to_checksum_address(self.contract_address)
            self.contract = self.w3.eth.contract(address=checksum_address, abi=self.contract_abi)
            logger.info(f"Loaded contract at {checksum_address}")

    def ensure_contract(self):
        """Re-checks contract loading if it wasn't available at startup"""
        if self.contract is None:
            self._load_contract_metadata()
        if self.contract is None:
            raise RuntimeError(
                "Smart contract is not loaded. Please deploy AcademicCertificateRegistry to Hardhat first."
            )

    def is_connected(self) -> bool:
        try:
            return self.w3.is_connected()
        except Exception:
            return False

    def get_latest_block_number(self) -> int:
        if not self.is_connected():
            return 0
        return self.w3.eth.block_number

    def is_authorized_issuer(self, address: str) -> bool:
        self.ensure_contract()
        chk_address = Web3.to_checksum_address(address)
        return self.contract.functions.isAuthorizedIssuer(chk_address).call()

    def issue_certificate(self, certificate_id: str, certificate_hash: str) -> Dict[str, Any]:
        """
        Executes issueCertificate on the smart contract using the authorized issuer private key.
        """
        self.ensure_contract()

        # Format certificate_hash to bytes32
        if certificate_hash.startswith("0x"):
            hash_bytes = bytes.fromhex(certificate_hash[2:])
        else:
            hash_bytes = bytes.fromhex(certificate_hash)

        account = self.w3.eth.account.from_key(self.issuer_private_key)
        nonce = self.w3.eth.get_transaction_count(account.address)

        tx = self.contract.functions.issueCertificate(
            certificate_id,
            hash_bytes
        ).build_transaction({
            "from": account.address,
            "nonce": nonce,
            "gas": 300000,
            "gasPrice": self.w3.eth.gas_price
        })

        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.issuer_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)

        if receipt.status != 1:
            raise RuntimeError(f"Certificate issuance transaction failed. Tx: {tx_hash.hex()}")

        return {
            "tx_hash": tx_hash.hex(),
            "block_number": receipt.blockNumber,
            "gas_used": receipt.gasUsed,
            "issuer": account.address
        }

    def verify_certificate(self, certificate_id: str, certificate_hash: str) -> Dict[str, Any]:
        """
        Calls verifyCertificate on the smart contract without gas.
        """
        self.ensure_contract()

        if certificate_hash.startswith("0x"):
            hash_bytes = bytes.fromhex(certificate_hash[2:])
        else:
            hash_bytes = bytes.fromhex(certificate_hash)

        exists, hash_matches, revoked, issuer, issued_at = self.contract.functions.verifyCertificate(
            certificate_id,
            hash_bytes
        ).call()

        return {
            "exists": exists,
            "hash_matches": hash_matches,
            "revoked": revoked,
            "issuer": issuer,
            "issued_at": issued_at
        }

    def get_certificate_status(self, certificate_id: str) -> Dict[str, Any]:
        """
        Calls getCertificateStatus on the smart contract.
        """
        self.ensure_contract()

        exists, cert_hash_bytes, issuer, issued_at, revoked = self.contract.functions.getCertificateStatus(
            certificate_id
        ).call()

        cert_hash_hex = "0x" + cert_hash_bytes.hex() if exists else None

        return {
            "exists": exists,
            "certificate_hash": cert_hash_hex,
            "issuer": issuer if exists else None,
            "issued_at": issued_at if exists else 0,
            "revoked": revoked if exists else False
        }

    def revoke_certificate(self, certificate_id: str) -> Dict[str, Any]:
        """
        Executes revokeCertificate on the smart contract.
        """
        self.ensure_contract()

        account = self.w3.eth.account.from_key(self.issuer_private_key)
        nonce = self.w3.eth.get_transaction_count(account.address)

        tx = self.contract.functions.revokeCertificate(
            certificate_id
        ).build_transaction({
            "from": account.address,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": self.w3.eth.gas_price
        })

        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.issuer_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)

        if receipt.status != 1:
            raise RuntimeError(f"Certificate revocation transaction failed. Tx: {tx_hash.hex()}")

        return {
            "tx_hash": tx_hash.hex(),
            "block_number": receipt.blockNumber,
            "gas_used": receipt.gasUsed,
            "issuer": account.address
        }

    def get_transaction_details(self, tx_hash_str: str) -> Dict[str, Any]:
        """
        Fetches live transaction details and receipt from the blockchain.
        """
        if not self.is_connected():
            return {"error": "Blockchain node not connected"}

        try:
            tx = self.w3.eth.get_transaction(tx_hash_str)
            receipt = self.w3.eth.get_transaction_receipt(tx_hash_str)
            block = self.w3.eth.get_block(receipt.blockNumber)
            current_block = self.w3.eth.block_number

            return {
                "tx_hash": tx_hash_str,
                "block_number": receipt.blockNumber,
                "from_address": tx["from"],
                "to_address": tx["to"],
                "gas_used": receipt.gasUsed,
                "status": receipt.status,
                "timestamp": block.timestamp,
                "confirmations": max(0, current_block - receipt.blockNumber + 1)
            }
        except TransactionNotFound:
            return {"error": "Transaction not found on blockchain"}
        except Exception as e:
            return {"error": str(e)}

blockchain_service = BlockchainService()
