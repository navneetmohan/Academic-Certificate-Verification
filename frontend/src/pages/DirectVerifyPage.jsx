import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ShieldCheck, CheckCircle2, XCircle, AlertTriangle, HelpCircle, Upload, ArrowLeft, Download, ExternalLink } from 'lucide-react';
import { verifyService, certificateService } from '../services/api';
import BlockchainProofCard from '../components/BlockchainProofCard';

export default function DirectVerifyPage() {
  const { id } = useParams();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Optional PDF matching on direct QR scan
  const [file, setFile] = useState(null);
  const [fileVerifying, setFileVerifying] = useState(false);

  const fetchVerification = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await verifyService.verifyById(id);
      setResult(data);
    } catch (err) {
      console.error(err);
      setError('Verification service unavailable.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (id) {
      fetchVerification();
    }
  }, [id]);

  const handleVerifyUploadedFile = async (e) => {
    e.preventDefault();
    if (!file) return;
    setFileVerifying(true);
    try {
      const data = await verifyService.verifyFile(file, id);
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setFileVerifying(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Back button */}
      <div>
        <Link to="/verify" className="text-xs text-slate-400 hover:text-white flex items-center gap-1.5 transition-colors">
          <ArrowLeft className="w-3.5 h-3.5" />
          Back to Verification Portal
        </Link>
      </div>

      {loading ? (
        <div className="py-24 text-center space-y-3">
          <div className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-sm text-slate-300 font-medium">Querying Ethereum Smart Contract...</p>
          <p className="text-xs text-slate-500 font-mono">Certificate: {id}</p>
        </div>
      ) : error ? (
        <div className="p-6 rounded-3xl glass-card border border-red-500/30 text-center space-y-3">
          <AlertTriangle className="w-8 h-8 text-red-400 mx-auto" />
          <h2 className="text-lg font-bold text-white">Verification Error</h2>
          <p className="text-xs text-slate-300">{error}</p>
        </div>
      ) : result ? (
        <div className="space-y-6">
          {/* Big Status Banner */}
          {result.status === 'VALID' && (
            <div className="p-6 sm:p-8 rounded-3xl bg-emerald-950/40 border-2 border-emerald-500/50 shadow-2xl space-y-4">
              <div className="flex items-center gap-3.5">
                <div className="p-3 rounded-2xl bg-emerald-500/20 text-emerald-400">
                  <CheckCircle2 className="w-8 h-8" />
                </div>
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400 block">
                    QR Scan Direct Verification
                  </span>
                  <h1 className="text-2xl sm:text-3xl font-extrabold text-white">✓ CERTIFICATE VERIFIED</h1>
                  <p className="text-xs text-emerald-200 mt-0.5">{result.message}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs p-5 rounded-2xl bg-slate-950/80 border border-slate-800">
                <div>
                  <span className="text-slate-400 block mb-0.5 font-semibold">Certificate ID:</span>
                  <span className="text-white font-mono font-bold text-sm text-brand-300">{result.certificate_id}</span>
                </div>
                <div>
                  <span className="text-slate-400 block mb-0.5 font-semibold">Issuing Institution:</span>
                  <span className="text-white font-medium">{result.institution_name || 'Authorized Institution'}</span>
                </div>
                <div>
                  <span className="text-slate-400 block mb-0.5 font-semibold">Conferred Degree:</span>
                  <span className="text-white font-medium">{result.degree || 'Degree Program'}</span>
                </div>
                <div>
                  <span className="text-slate-400 block mb-0.5 font-semibold">Conferral Date:</span>
                  <span className="text-white font-medium">{result.issue_date || result.issued_at_iso}</span>
                </div>
              </div>
            </div>
          )}

          {result.status === 'INVALID' && (
            <div className="p-6 sm:p-8 rounded-3xl bg-red-950/40 border-2 border-red-500/50 shadow-2xl space-y-4">
              <div className="flex items-center gap-3.5">
                <div className="p-3 rounded-2xl bg-red-500/20 text-red-400">
                  <XCircle className="w-8 h-8" />
                </div>
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-red-400 block">
                    Cryptographic Integrity Alert
                  </span>
                  <h1 className="text-2xl sm:text-3xl font-extrabold text-white">✕ CERTIFICATE INVALID / MODIFIED</h1>
                  <p className="text-xs text-red-200 mt-0.5">{result.message}</p>
                </div>
              </div>
            </div>
          )}

          {result.status === 'REVOKED' && (
            <div className="p-6 sm:p-8 rounded-3xl bg-amber-950/40 border-2 border-amber-500/50 shadow-2xl space-y-4">
              <div className="flex items-center gap-3.5">
                <div className="p-3 rounded-2xl bg-amber-500/20 text-amber-400">
                  <AlertTriangle className="w-8 h-8" />
                </div>
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400 block">
                    Revocation Notice
                  </span>
                  <h1 className="text-2xl sm:text-3xl font-extrabold text-white">⚠ CERTIFICATE REVOKED</h1>
                  <p className="text-xs text-amber-200 mt-0.5">{result.message}</p>
                </div>
              </div>
            </div>
          )}

          {result.status === 'NOT_FOUND' && (
            <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border-2 border-slate-700 shadow-2xl space-y-3">
              <div className="flex items-center gap-3.5">
                <div className="p-3 rounded-2xl bg-slate-800 text-slate-400">
                  <HelpCircle className="w-8 h-8" />
                </div>
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    Record Does Not Exist
                  </span>
                  <h1 className="text-2xl sm:text-3xl font-extrabold text-white">? CERTIFICATE NOT FOUND</h1>
                  <p className="text-xs text-slate-300 mt-0.5">{result.message}</p>
                </div>
              </div>
            </div>
          )}

          {/* Optional: Cross-verify with a physical PDF copy */}
          {result.status !== 'NOT_FOUND' && (
            <div className="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xs font-bold text-white">Cross-Verify Physical / Downloaded PDF</h3>
                  <p className="text-[11px] text-slate-400">Upload your PDF file to test byte-by-byte SHA-256 match against this record</p>
                </div>
              </div>
              <form onSubmit={handleVerifyUploadedFile} className="flex flex-col sm:flex-row items-center gap-3 pt-1">
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="w-full text-xs text-slate-400 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-slate-800 file:text-slate-200 hover:file:bg-slate-700 cursor-pointer"
                />
                <button
                  type="submit"
                  disabled={fileVerifying || !file}
                  className="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-medium text-xs whitespace-nowrap disabled:opacity-50 transition-colors"
                >
                  {fileVerifying ? 'Checking Hash...' : 'Compare PDF Hash'}
                </button>
              </form>
            </div>
          )}

          {/* Blockchain Proof Card */}
          {result.status !== 'NOT_FOUND' && (
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
      ) : null}
    </div>
  );
}
