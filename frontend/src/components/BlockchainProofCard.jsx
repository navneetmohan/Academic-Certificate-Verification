import React, { useState } from 'react';
import { Copy, Check, ExternalLink, ShieldCheck, Database, FileCode, Clock, Hash } from 'lucide-react';
import { blockchainService } from '../services/api';

export default function BlockchainProofCard({
  certificateId,
  certificateHash,
  blockchainTxHash,
  issuerAddress,
  issuedAt,
  issuedAtIso
}) {
  const [copiedHash, setCopiedHash] = useState(false);
  const [copiedTx, setCopiedTx] = useState(false);
  const [txDetails, setTxDetails] = useState(null);
  const [loadingTx, setLoadingTx] = useState(false);

  const copyToClipboard = (text, type) => {
    navigator.clipboard.writeText(text);
    if (type === 'hash') {
      setCopiedHash(true);
      setTimeout(() => setCopiedHash(false), 2000);
    } else {
      setCopiedTx(true);
      setTimeout(() => setCopiedTx(false), 2000);
    }
  };

  const handleInspectTx = async () => {
    if (!blockchainTxHash) return;
    setLoadingTx(true);
    try {
      const data = await blockchainService.getTransaction(blockchainTxHash);
      setTxDetails(data);
    } catch (err) {
      console.error("Failed to load tx details", err);
    } finally {
      setLoadingTx(false);
    }
  };

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-700/60 shadow-xl space-y-5">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-brand-500/10 text-brand-400 border border-brand-500/20">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white tracking-wide">Blockchain Proof & Integrity</h3>
            <p className="text-xs text-slate-400">Cryptographically anchored to Ethereum EVM ledger</p>
          </div>
        </div>
        <span className="px-2 py-0.5 rounded text-[11px] font-mono font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          On-Chain Verified
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Certificate Hash (SHA-256) */}
        <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1.5 md:col-span-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="flex items-center gap-1.5 font-medium">
              <Hash className="w-3.5 h-3.5 text-brand-400" />
              Document SHA-256 Fingerprint (bytes32)
            </span>
            <button
              onClick={() => copyToClipboard(certificateHash, 'hash')}
              className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-white transition-colors"
            >
              {copiedHash ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
              {copiedHash ? 'Copied' : 'Copy'}
            </button>
          </div>
          <p className="font-mono text-xs text-brand-300 break-all bg-slate-950/60 p-2 rounded border border-slate-800/80">
            {certificateHash || 'Pending computation...'}
          </p>
        </div>

        {/* Blockchain Transaction Hash */}
        <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1.5">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="flex items-center gap-1.5 font-medium">
              <FileCode className="w-3.5 h-3.5 text-indigo-400" />
              Transaction Hash
            </span>
            {blockchainTxHash && (
              <button
                onClick={() => copyToClipboard(blockchainTxHash, 'tx')}
                className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-white transition-colors"
              >
                {copiedTx ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                {copiedTx ? 'Copied' : 'Copy'}
              </button>
            )}
          </div>
          <p className="font-mono text-xs text-slate-200 break-all bg-slate-950/60 p-2 rounded border border-slate-800/80">
            {blockchainTxHash ? `${blockchainTxHash.slice(0, 14)}...${blockchainTxHash.slice(-10)}` : 'N/A'}
          </p>
        </div>

        {/* Issuer Wallet */}
        <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1.5">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="flex items-center gap-1.5 font-medium">
              <Database className="w-3.5 h-3.5 text-emerald-400" />
              Authorized Issuer Wallet
            </span>
          </div>
          <p className="font-mono text-xs text-slate-200 break-all bg-slate-950/60 p-2 rounded border border-slate-800/80">
            {issuerAddress ? `${issuerAddress.slice(0, 10)}...${issuerAddress.slice(-8)}` : 'Academic Registry Contract'}
          </p>
        </div>

        {/* On-Chain Timestamp */}
        <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1.5 md:col-span-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="flex items-center gap-1.5 font-medium">
              <Clock className="w-3.5 h-3.5 text-amber-400" />
              On-Chain Registration Timestamp
            </span>
            <span className="text-[11px] text-slate-500 font-mono">
              UNIX: {issuedAt || 'N/A'}
            </span>
          </div>
          <p className="text-xs text-slate-200 font-mono bg-slate-950/60 p-2 rounded border border-slate-800/80">
            {issuedAtIso || (issuedAt ? new Date(issuedAt * 1000).toUTCString() : 'Recorded at block issuance')}
          </p>
        </div>
      </div>

      {/* Live Transaction Inspector */}
      {blockchainTxHash && (
        <div className="pt-2">
          {!txDetails ? (
            <button
              onClick={handleInspectTx}
              disabled={loadingTx}
              className="text-xs text-brand-400 hover:text-brand-300 font-medium flex items-center gap-1 transition-colors"
            >
              <ExternalLink className="w-3.5 h-3.5" />
              {loadingTx ? 'Inspecting Blockchain Node...' : 'Inspect Live Transaction Receipt'}
            </button>
          ) : (
            <div className="p-3.5 rounded-xl bg-slate-950/90 border border-brand-500/30 text-xs font-mono space-y-1.5">
              <div className="text-brand-400 font-semibold mb-1 flex items-center justify-between">
                <span>Receipt From Local EVM Block #{txDetails.block_number}</span>
                <span className="text-[10px] text-emerald-400">Status: SUCCESS (1)</span>
              </div>
              <div className="grid grid-cols-2 gap-2 text-slate-300 text-[11px]">
                <div>From: <span className="text-slate-400">{txDetails.from_address?.slice(0, 10)}...</span></div>
                <div>To: <span className="text-slate-400">{txDetails.to_address?.slice(0, 10)}...</span></div>
                <div>Gas Used: <span className="text-slate-400">{txDetails.gas_used}</span></div>
                <div>Confirmations: <span className="text-emerald-400">{txDetails.confirmations}</span></div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
