import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Download, ArrowLeft, Share2, Check, ExternalLink, ShieldCheck, QrCode, FileText } from 'lucide-react';
import { certificateService } from '../services/api';
import BlockchainProofCard from '../components/BlockchainProofCard';
import StatusBadge from '../components/StatusBadge';

export default function CertificateDetailPage() {
  const { id } = useParams();
  const [cert, setCert] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [copiedLink, setCopiedLink] = useState(false);

  useEffect(() => {
    async function loadCert() {
      setLoading(true);
      try {
        const data = await certificateService.get(id);
        setCert(data);
      } catch (err) {
        setError('Certificate not found or failed to load.');
      } finally {
        setLoading(false);
      }
    }
    loadCert();
  }, [id]);

  const copyVerifyLink = () => {
    const url = `${window.location.origin}/verify/${id}`;
    navigator.clipboard.writeText(url);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2000);
  };

  if (loading) {
    return <div className="py-24 text-center text-slate-400 text-sm">Loading certificate details...</div>;
  }

  if (error || !cert) {
    return (
      <div className="max-w-xl mx-auto py-24 text-center space-y-4">
        <h2 className="text-xl font-bold text-white">Certificate Not Found</h2>
        <p className="text-xs text-slate-400">{error}</p>
        <Link to="/certificates" className="text-brand-400 text-xs font-semibold hover:underline">
          ← Back to Registry
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Breadcrumb */}
      <div className="flex items-center justify-between">
        <Link to="/certificates" className="text-xs text-slate-400 hover:text-white flex items-center gap-1.5 transition-colors">
          <ArrowLeft className="w-3.5 h-3.5" />
          Back to Certificates Registry
        </Link>
        <div className="flex items-center gap-2">
          <button
            onClick={copyVerifyLink}
            className="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center gap-1.5 transition-colors"
          >
            {copiedLink ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Share2 className="w-3.5 h-3.5" />}
            {copiedLink ? 'Link Copied!' : 'Share Verification Link'}
          </button>
          <a
            href={certificateService.getDownloadUrl(cert.certificate_id)}
            target="_blank"
            rel="noreferrer"
            className="px-4 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 hover:bg-emerald-500 text-white flex items-center gap-1.5 shadow-lg shadow-emerald-600/30 transition-all"
          >
            <Download className="w-3.5 h-3.5" />
            Download PDF
          </a>
        </div>
      </div>

      {/* Main Overview Card */}
      <div className="glass-card rounded-3xl p-6 sm:p-8 border border-slate-800 shadow-2xl relative overflow-hidden space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2.5 mb-1.5">
              <span className="font-mono text-sm font-bold text-brand-300 bg-slate-900 px-3 py-1 rounded-lg border border-slate-800">
                {cert.certificate_id}
              </span>
              <StatusBadge revoked={cert.revoked} />
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
              {cert.student_name}
            </h1>
            <p className="text-xs text-slate-400 mt-1 font-mono">
              Student ID: {cert.student_id} • Conferred by {cert.institution_name}
            </p>
          </div>

          <div className="text-right">
            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Issue Date</span>
            <span className="text-sm font-semibold text-white">{cert.issue_date}</span>
          </div>
        </div>

        {/* Degree & Academic Program */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
            <span className="text-slate-400 block mb-1">Degree Title</span>
            <span className="text-white font-semibold text-sm">{cert.degree}</span>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
            <span className="text-slate-400 block mb-1">Department</span>
            <span className="text-white font-medium">{cert.department}</span>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
            <span className="text-slate-400 block mb-1">Graduation Class</span>
            <span className="text-white font-semibold text-sm">Class of {cert.graduation_year}</span>
          </div>
        </div>

        {/* Public Verifier Action Link */}
        <div className="p-4 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-brand-500/20 text-brand-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-xs font-bold text-white">Public Verification Endpoint</h4>
              <p className="text-[11px] text-slate-300">Third-parties and employers can independently verify this credential.</p>
            </div>
          </div>
          <Link
            to={`/verify/${cert.certificate_id}`}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-brand-600 hover:bg-brand-500 text-white flex items-center gap-1.5 shrink-0 transition-colors"
          >
            Open Verification Portal
            <ExternalLink className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Blockchain Proof Card */}
      <BlockchainProofCard
        certificateId={cert.certificate_id}
        certificateHash={cert.certificate_hash}
        blockchainTxHash={cert.blockchain_tx_hash}
        issuerAddress={cert.institution?.wallet_address}
        issuedAt={Math.floor(new Date(cert.created_at).getTime() / 1000)}
        issuedAtIso={cert.created_at}
      />
    </div>
  );
}
