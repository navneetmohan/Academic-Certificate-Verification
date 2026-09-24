import React, { useState } from 'react';
import { Search, Upload, ShieldCheck, XCircle, AlertTriangle, HelpCircle, FileText, CheckCircle2, ArrowRight, Zap, RefreshCw } from 'lucide-react';
import { verifyService } from '../services/api';
import BlockchainProofCard from '../components/BlockchainProofCard';

export default function VerifyPage() {
  const [activeTab, setActiveTab] = useState('upload'); // 'upload' | 'id' | 'tamper'
  const [certificateId, setCertificateId] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Quick tamper demo states
  const [tamperCertId, setTamperCertId] = useState('CERT-2026-0001');

  const handleVerifyById = async (e) => {
    e?.preventDefault();
    if (!certificateId.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await verifyService.verifyById(certificateId.trim());
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.message || 'Verification service unreachable.');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyFile = async (e) => {
    e?.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await verifyService.verifyFile(file, certificateId ? certificateId.trim() : null);
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.message || 'File verification failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleRunTamperTest = async () => {
    if (!tamperCertId.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await verifyService.testTamper(tamperCertId.trim());
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Tamper simulation failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Title */}
      <div className="text-center space-y-2">
        <div className="inline-flex p-3 rounded-2xl bg-brand-500/10 text-brand-400 border border-brand-500/20 mb-1">
          <ShieldCheck className="w-8 h-8" />
        </div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Academic Credential Verifier</h1>
        <p className="text-xs sm:text-sm text-slate-400 max-w-xl mx-auto">
          Verify digital diploma authenticity, detect document tampering, and check smart contract revocation status in real time.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex p-1 rounded-2xl bg-slate-900 border border-slate-800 max-w-md mx-auto">
        <button
          onClick={() => { setActiveTab('upload'); setResult(null); setError(null); }}
          className={`flex-1 py-2 text-xs font-semibold rounded-xl transition-all ${
            activeTab === 'upload' ? 'bg-brand-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
          }`}
        >
          Verify by PDF Upload
        </button>
        <button
          onClick={() => { setActiveTab('id'); setResult(null); setError(null); }}
          className={`flex-1 py-2 text-xs font-semibold rounded-xl transition-all ${
            activeTab === 'id' ? 'bg-brand-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
          }`}
        >
          Verify by ID
        </button>
        <button
          onClick={() => { setActiveTab('tamper'); setResult(null); setError(null); }}
          className={`flex-1 py-2 text-xs font-semibold rounded-xl transition-all ${
            activeTab === 'tamper' ? 'bg-amber-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
          }`}
        >
          Tamper Demo
        </button>
      </div>

      {/* Tab 1: PDF Upload Form */}
      {activeTab === 'upload' && (
        <form onSubmit={handleVerifyFile} className="glass-card rounded-3xl p-6 sm:p-8 border border-slate-800 space-y-5">
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300">Optional Certificate ID</label>
            <input
              type="text"
              value={certificateId}
              onChange={(e) => setCertificateId(e.target.value)}
              placeholder="e.g. CERT-2026-0001 (optional, can be auto-detected)"
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300">Upload PDF Degree Certificate</label>
            <div className="border-2 border-dashed border-slate-700 hover:border-brand-500/60 rounded-2xl p-8 text-center bg-slate-900/40 transition-colors">
              <Upload className="w-8 h-8 text-slate-400 mx-auto mb-2" />
              <p className="text-xs text-slate-300 font-medium">
                {file ? file.name : 'Click to select or drag and drop official PDF certificate'}
              </p>
              <p className="text-[10px] text-slate-500 mt-1">Accepts original or modified PDF for integrity verification</p>
              <input
                type="file"
                accept="application/pdf"
                onChange={(e) => setFile(e.target.files[0])}
                className="mt-4 block mx-auto text-xs text-slate-400 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-brand-600 file:text-white hover:file:bg-brand-500 cursor-pointer"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || !file}
            className="w-full py-3 px-4 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-medium text-sm transition-all shadow-lg shadow-brand-600/30 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {loading ? 'Computing SHA-256 & Querying Blockchain...' : 'Verify Cryptographic Fingerprint'}
          </button>
        </form>
      )}

      {/* Tab 2: ID Search Form */}
      {activeTab === 'id' && (
        <form onSubmit={handleVerifyById} className="glass-card rounded-3xl p-6 sm:p-8 border border-slate-800 space-y-5">
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300">Certificate Identifier</label>
            <input
              type="text"
              required
              value={certificateId}
              onChange={(e) => setCertificateId(e.target.value)}
              placeholder="e.g. CERT-2026-0001"
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading || !certificateId.trim()}
            className="w-full py-3 px-4 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-medium text-sm transition-all shadow-lg shadow-brand-600/30 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {loading ? 'Querying Smart Contract...' : 'Verify on Blockchain'}
          </button>
        </form>
      )}

      {/* Tab 3: Tamper Demonstration Helper */}
      {activeTab === 'tamper' && (
        <div className="glass-card rounded-3xl p-6 sm:p-8 border border-amber-500/30 space-y-5">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <Zap className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Live Tamper Detection Demonstration</h3>
              <p className="text-xs text-slate-400">
                Simulates an altered certificate to prove that modifying even 1 byte causes a cryptographic hash mismatch
              </p>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2 text-xs">
            <label className="font-semibold text-slate-300">Target Certificate ID to Tamper:</label>
            <input
              type="text"
              value={tamperCertId}
              onChange={(e) => setTamperCertId(e.target.value)}
              className="w-full px-3.5 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white font-mono text-xs focus:outline-none focus:border-amber-500"
            />
            <p className="text-slate-500 text-[11px]">
              This will load the certificate, alter 10 bytes of its internal PDF stream, re-calculate the SHA-256 hash, and test it against the smart contract.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
            <button
              type="button"
              disabled={loading}
              onClick={handleRunTamperTest}
              className="py-3 px-4 rounded-xl bg-red-600 hover:bg-red-500 text-white font-bold text-xs shadow-lg shadow-red-600/25 transition-all flex items-center justify-center gap-2"
            >
              <XCircle className="w-4 h-4" />
              {loading ? 'Simulating Tampering...' : 'Test Tampered Certificate (Expect INVALID)'}
            </button>
            <button
              type="button"
              disabled={loading}
              onClick={() => {
                setCertificateId(tamperCertId);
                setActiveTab('id');
                // trigger direct check
                setTimeout(() => handleVerifyById(), 100);
              }}
              className="py-3 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-lg shadow-emerald-600/25 transition-all flex items-center justify-center gap-2"
            >
              <CheckCircle2 className="w-4 h-4" />
              Test Authentic Record (Expect VALID)
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-300 text-xs flex items-center gap-2.5">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Authoritative Verification Result Display */}
      {result && (
        <div className="space-y-6 pt-4 animate-in fade-in slide-in-from-bottom-3 duration-300">
          {/* 1. Case: VALID */}
          {result.status === 'VALID' && (
            <div className="p-6 rounded-3xl bg-emerald-950/40 border-2 border-emerald-500/50 shadow-2xl space-y-4">
              <div className="flex items-center gap-3">
                <div className="p-3 rounded-2xl bg-emerald-500/20 text-emerald-400">
                  <CheckCircle2 className="w-8 h-8" />
                </div>
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400 block">
                    Authoritative Verification Passed
                  </span>
                  <h2 className="text-2xl font-extrabold text-white">✓ CERTIFICATE VERIFIED</h2>
                  <p className="text-xs text-emerald-200 mt-0.5">{result.message}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs p-4 rounded-2xl bg-slate-950/80 border border-slate-800">
                <div>
                  <span className="text-slate-400 block mb-0.5">Certificate ID:</span>
                  <span className="text-white font-mono font-bold">{result.certificate_id}</span>
                </div>
                <div>
                  <span className="text-slate-400 block mb-0.5">Issuing Institution:</span>
                  <span className="text-white font-medium">{result.institution_name || 'Authorized Institution'}</span>
                </div>
                <div>
                  <span className="text-slate-400 block mb-0.5">Conferred Degree:</span>
                  <span className="text-white font-medium">{result.degree || 'Degree Program'}</span>
                </div>
                <div>
                  <span className="text-slate-400 block mb-0.5">Issue Date:</span>
                  <span className="text-white font-medium">{result.issue_date || result.issued_at_iso}</span>
                </div>
              </div>
            </div>
          )}

          {/* 2. Case: INVALID / MODIFIED */}
          {result.status === 'INVALID' && (
            <div className="p-6 rounded-3xl bg-red-950/40 border-2 border-red-500/50 shadow-2xl space-y-4">
              <div className="flex items-center gap-3">
                <div className="p-3 rounded-2xl bg-red-500/20 text-red-400">
                  <XCircle className="w-8 h-8" />
                </div>
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-red-400 block">
                    Cryptographic Hash Mismatch
                  </span>
                  <h2 className="text-2xl font-extrabold text-white">✕ CERTIFICATE INVALID / MODIFIED</h2>
                  <p className="text-xs text-red-200 mt-0.5">{result.message}</p>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-slate-950/90 border border-red-500/30 text-xs font-mono space-y-2">
                <div>
                  <span className="text-red-400 font-bold block mb-1">Calculated Uploaded Hash:</span>
                  <span className="text-slate-300 break-all">{result.calculated_hash}</span>
                </div>
                <div className="pt-2 border-t border-slate-800">
                  <span className="text-emerald-400 font-bold block mb-1">On-Chain Recorded Hash:</span>
                  <span className="text-slate-300 break-all">{result.onchain_hash}</span>
                </div>
              </div>
            </div>
          )}

          {/* 3. Case: REVOKED */}
          {result.status === 'REVOKED' && (
            <div className="p-6 rounded-3xl bg-amber-950/40 border-2 border-amber-500/50 shadow-2xl space-y-4">
              <div className="flex items-center gap-3">
                <div className="p-3 rounded-2xl bg-amber-500/20 text-amber-400">
                  <AlertTriangle className="w-8 h-8" />
                </div>
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400 block">
                    Institutional Revocation Enforced
                  </span>
                  <h2 className="text-2xl font-extrabold text-white">⚠ CERTIFICATE REVOKED</h2>
                  <p className="text-xs text-amber-200 mt-0.5">{result.message}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs p-4 rounded-2xl bg-slate-950/80 border border-slate-800">
                <div>
                  <span className="text-slate-400 block mb-0.5">Certificate ID:</span>
                  <span className="text-white font-mono font-bold">{result.certificate_id}</span>
                </div>
                <div>
                  <span className="text-slate-400 block mb-0.5">Status:</span>
                  <span className="text-amber-400 font-bold">REVOKED ON-CHAIN</span>
                </div>
              </div>
            </div>
          )}

          {/* 4. Case: NOT FOUND */}
          {result.status === 'NOT_FOUND' && (
            <div className="p-6 rounded-3xl bg-slate-900 border-2 border-slate-700 shadow-2xl space-y-3">
              <div className="flex items-center gap-3">
                <div className="p-3 rounded-2xl bg-slate-800 text-slate-400">
                  <HelpCircle className="w-8 h-8" />
                </div>
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    No Blockchain Record
                  </span>
                  <h2 className="text-2xl font-extrabold text-white">? CERTIFICATE NOT FOUND</h2>
                  <p className="text-xs text-slate-300 mt-0.5">{result.message}</p>
                </div>
              </div>
            </div>
          )}

          {/* Detailed Proof Component */}
          {result.certificate_id && result.status !== 'NOT_FOUND' && (
            <BlockchainProofCard
              certificateId={result.certificate_id}
              certificateHash={result.onchain_hash}
              blockchainTxHash={result.tx_hash}
              issuerAddress={result.issuer_address}
              issuedAt={result.issued_at}
              issuedAtIso={result.issued_at_iso}
            />
          )}
        </div>
      )}
    </div>
  );
}
