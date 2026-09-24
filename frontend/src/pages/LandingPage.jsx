import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ShieldCheck, Search, Award, CheckCircle2, Lock, FileText, ArrowRight, Zap, RefreshCw, EyeOff } from 'lucide-react';

export default function LandingPage() {
  const [certIdInput, setCertIdInput] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (certIdInput.trim()) {
      navigate(`/verify/${certIdInput.trim()}`);
    }
  };

  return (
    <div className="space-y-16 py-8">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-12 md:py-20 text-center max-w-4xl mx-auto px-4">
        {/* Glow backdrop */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-brand-500/10 blur-[120px] rounded-full pointer-events-none -z-10" />

        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-brand-500/10 text-brand-300 border border-brand-500/20 mb-6">
          <Zap className="w-3.5 h-3.5 text-brand-400" />
          <span>Ethereum Smart Contract Verification • Hardhat Node</span>
        </div>

        <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-white tracking-tight leading-tight">
          Trustworthy Academic Credentials{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 via-brand-200 to-emerald-400">
            Anchored on Blockchain
          </span>
        </h1>

        <p className="mt-6 text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
          A hybrid on-chain/off-chain credential verification system. Smart contracts enforce authenticity and revocation while preserving student personal data off-chain.
        </p>

        {/* Quick Search Widget */}
        <form onSubmit={handleSearch} className="mt-8 max-w-xl mx-auto">
          <div className="relative flex items-center shadow-2xl rounded-2xl glass-panel p-2 border border-slate-700/80">
            <Search className="w-5 h-5 text-slate-400 ml-3" />
            <input
              type="text"
              value={certIdInput}
              onChange={(e) => setCertIdInput(e.target.value)}
              placeholder="Enter Certificate ID (e.g. CERT-2026-0001)..."
              className="w-full bg-transparent px-4 py-2.5 text-sm text-white placeholder-slate-400 focus:outline-none"
            />
            <button
              type="submit"
              className="px-5 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-medium text-sm transition-all shadow-lg shadow-brand-600/30 flex items-center gap-1.5 shrink-0"
            >
              Verify
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
          <div className="flex items-center justify-center gap-4 mt-3 text-xs text-slate-400">
            <span>Or test with PDF upload on the</span>
            <Link to="/verify" className="text-brand-400 hover:underline font-medium">
              Full Verification Portal →
            </Link>
          </div>
        </form>
      </section>

      {/* 3 User Roles Cards */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-10">
          <h2 className="text-2xl font-bold text-white">Three-Tier Architecture & Roles</h2>
          <p className="text-sm text-slate-400 mt-2">Designed for educational institutions, graduates, and employers</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Institution Admin */}
          <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4 hover:border-brand-500/40 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-brand-500/10 text-brand-400 border border-brand-500/20 flex items-center justify-center">
              <Award className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-semibold text-white">1. Institution Admin</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Authorized university wallet signs smart contract transactions to mint immutable certificate hashes. Can also trigger cryptographic revocation.
            </p>
            <ul className="text-xs text-slate-400 space-y-1.5 font-medium">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-brand-400" />
                Issue deterministic PDF certificate
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-brand-400" />
                Anchor SHA-256 fingerprint on-chain
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-brand-400" />
                Revoke compromised credentials
              </li>
            </ul>
          </div>

          {/* Student */}
          <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4 hover:border-emerald-500/40 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center justify-center">
              <FileText className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-semibold text-white">2. Student Graduate</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Receives tamper-evident PDF credential with an embedded QR code. Can share the verification link without exposing private PII on public ledgers.
            </p>
            <ul className="text-xs text-slate-400 space-y-1.5 font-medium">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                Download high-res PDF certificate
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                Shareable QR verification link
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                No wallet or gas fees required
              </li>
            </ul>
          </div>

          {/* Employer / Verifier */}
          <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4 hover:border-indigo-500/40 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 flex items-center justify-center">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-semibold text-white">3. Third-Party Verifier</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Employers upload candidates' PDF degrees or scan QR codes to instantly verify against the blockchain ledger without middleman delays.
            </p>
            <ul className="text-xs text-slate-400 space-y-1.5 font-medium">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-indigo-400" />
                Instant SHA-256 hash match
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-indigo-400" />
                Real-time revocation check
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-indigo-400" />
                Detects 1-byte PDF alterations
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Why Hybrid On-Chain/Off-Chain Architecture? */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="glass-panel rounded-3xl p-8 md:p-12 border border-slate-800">
          <div className="max-w-3xl">
            <span className="text-xs font-semibold text-brand-400 uppercase tracking-wider">
              Core Architectural Decision
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-white mt-2">
              Why Only Store Cryptographic Hashes On-Chain?
            </h2>
            <p className="text-sm text-slate-300 mt-4 leading-relaxed">
              Academic credentials contain sensitive personal data (student names, roll numbers, grades). Storing complete PDFs on a public blockchain violates privacy laws (e.g. GDPR, FERPA), wastes enormous storage gas, and creates permanent public surveillance records.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
              <EyeOff className="w-5 h-5 text-emerald-400 mb-2" />
              <h4 className="text-sm font-semibold text-white">Zero PII On-Chain</h4>
              <p className="text-xs text-slate-400 mt-1">Student names, addresses, and grades remain strictly off-chain.</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
              <Lock className="w-5 h-5 text-brand-400 mb-2" />
              <h4 className="text-sm font-semibold text-white">Cryptographic Proof</h4>
              <p className="text-xs text-slate-400 mt-1">Any modification to the PDF breaks the SHA-256 match.</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
              <Zap className="w-5 h-5 text-amber-400 mb-2" />
              <h4 className="text-sm font-semibold text-white">Minimal Gas Costs</h4>
              <p className="text-xs text-slate-400 mt-1">Storing 32 bytes of hash requires orders of magnitude less gas than megabytes of PDF.</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
              <RefreshCw className="w-5 h-5 text-indigo-400 mb-2" />
              <h4 className="text-sm font-semibold text-white">Instant Revocation</h4>
              <p className="text-xs text-slate-400 mt-1">Smart contract state flag updates immediately upon revocation.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
