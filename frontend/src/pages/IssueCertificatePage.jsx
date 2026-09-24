import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Award, ShieldCheck, CheckCircle2, AlertCircle, Sparkles, FileText, ArrowRight, Download } from 'lucide-react';
import { certificateService } from '../services/api';

export default function IssueCertificatePage() {
  const navigate = useNavigate();
  const today = new Date().toISOString().split('T')[0];

  const [formData, setFormData] = useState({
    student_name: 'Sophia Elena Martinez',
    student_id: 'MSU-CS-2026-042',
    degree: 'Bachelor of Science in Computer Science & Engineering',
    department: 'School of Computing and Information Systems',
    institution_name: 'Metropolitan State University',
    graduation_year: 2026,
    certificate_type: 'Bachelor of Science Degree',
    issue_date: today,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [issuedCert, setIssuedCert] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'graduation_year' ? parseInt(value, 10) || '' : value,
    }));
  };

  const handleFillPreset = (presetType) => {
    if (presetType === 'cs') {
      setFormData({
        student_name: 'Alexander James Vance',
        student_id: 'MSU-CS-2026-089',
        degree: 'Master of Science in Cybersecurity & Blockchain Technologies',
        department: 'Department of Electrical & Computer Engineering',
        institution_name: 'Metropolitan State University',
        graduation_year: 2026,
        certificate_type: 'Master of Science Degree',
        issue_date: today,
      });
    } else {
      setFormData({
        student_name: 'Sophia Elena Martinez',
        student_id: 'MSU-CS-2026-042',
        degree: 'Bachelor of Science in Computer Science & Engineering',
        department: 'School of Computing and Information Systems',
        institution_name: 'Metropolitan State University',
        graduation_year: 2026,
        certificate_type: 'Bachelor of Science Degree',
        issue_date: today,
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await certificateService.issue(formData);
      setIssuedCert(res);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to issue certificate on the blockchain.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Issue Academic Certificate</h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Generates a tamper-evident PDF credential and writes its SHA-256 fingerprint to the smart contract
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => handleFillPreset('cs')}
            className="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center gap-1.5 transition-colors"
          >
            <Sparkles className="w-3.5 h-3.5 text-brand-400" />
            Load Sample Master's
          </button>
        </div>
      </div>

      {/* Success Modal / Banner */}
      {issuedCert && (
        <div className="p-6 rounded-2xl bg-emerald-950/40 border border-emerald-500/40 shadow-2xl space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-emerald-500/20 text-emerald-400">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Certificate Successfully Issued & Anchored!</h3>
                <p className="text-xs text-emerald-300">
                  Transaction recorded and confirmed on the Hardhat Ethereum EVM ledger.
                </p>
              </div>
            </div>
            <span className="font-mono text-sm font-bold text-brand-300 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
              {issuedCert.certificate_id}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono p-4 rounded-xl bg-slate-950/80 border border-slate-800">
            <div>
              <span className="text-slate-400 block mb-1">SHA-256 Fingerprint (bytes32):</span>
              <span className="text-brand-300 break-all">{issuedCert.certificate_hash}</span>
            </div>
            <div>
              <span className="text-slate-400 block mb-1">Blockchain Tx Hash:</span>
              <span className="text-indigo-300 break-all">{issuedCert.blockchain_tx_hash}</span>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <a
              href={certificateService.getDownloadUrl(issuedCert.certificate_id)}
              target="_blank"
              rel="noreferrer"
              className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs flex items-center gap-2 shadow-lg shadow-emerald-600/30 transition-all"
            >
              <Download className="w-3.5 h-3.5" />
              Download Official PDF
            </a>
            <button
              onClick={() => navigate(`/certificate/${issuedCert.certificate_id}`)}
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-medium text-xs flex items-center gap-2 border border-slate-700 transition-all"
            >
              Inspect Certificate Proof
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setIssuedCert(null)}
              className="px-4 py-2 rounded-xl text-slate-400 hover:text-white text-xs"
            >
              Issue Another
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-300 text-xs flex items-center gap-2.5">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Grid: Form + Live Preview */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Form Column */}
        <div className="lg:col-span-7">
          <form onSubmit={handleSubmit} className="glass-card rounded-2xl p-6 border border-slate-800 space-y-5">
            <h2 className="text-base font-semibold text-white flex items-center gap-2">
              <Award className="w-4 h-4 text-brand-400" />
              Student Credential Details
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5 sm:col-span-2">
                <label className="text-xs font-medium text-slate-300">Student Full Name</label>
                <input
                  type="text"
                  name="student_name"
                  required
                  value={formData.student_name}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-medium text-slate-300">Student ID / Roll No</label>
                <input
                  type="text"
                  name="student_id"
                  required
                  value={formData.student_id}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-medium text-slate-300">Graduation Year</label>
                <input
                  type="number"
                  name="graduation_year"
                  required
                  min={1950}
                  max={2100}
                  value={formData.graduation_year}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                />
              </div>

              <div className="space-y-1.5 sm:col-span-2">
                <label className="text-xs font-medium text-slate-300">Conferred Degree Title</label>
                <input
                  type="text"
                  name="degree"
                  required
                  value={formData.degree}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                />
              </div>

              <div className="space-y-1.5 sm:col-span-2">
                <label className="text-xs font-medium text-slate-300">Academic Department / Faculty</label>
                <input
                  type="text"
                  name="department"
                  required
                  value={formData.department}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-medium text-slate-300">Certificate Type</label>
                <input
                  type="text"
                  name="certificate_type"
                  required
                  value={formData.certificate_type}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-medium text-slate-300">Conferral / Issue Date</label>
                <input
                  type="date"
                  name="issue_date"
                  required
                  value={formData.issue_date}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-medium text-sm transition-all shadow-lg shadow-brand-600/30 flex items-center justify-center gap-2 disabled:opacity-50 mt-4"
            >
              {loading ? (
                <>
                  <span className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></span>
                  Hashing & Signing Blockchain Tx...
                </>
              ) : (
                <>
                  <ShieldCheck className="w-4 h-4" />
                  Issue Certificate & Sign Blockchain Transaction
                </>
              )}
            </button>
          </form>
        </div>

        {/* Live Document Preview Column */}
        <div className="lg:col-span-5 space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="font-semibold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
              <FileText className="w-3.5 h-3.5 text-brand-400" />
              Live Certificate Layout Preview
            </span>
            <span className="text-[11px] text-slate-500">Auto-updates</span>
          </div>

          <div className="p-6 rounded-2xl bg-[#fdfbf7] text-[#0f2744] shadow-2xl border-4 border-[#0f2744] relative min-h-[380px] flex flex-col justify-between overflow-hidden">
            {/* Inner gold border */}
            <div className="absolute inset-1.5 border border-[#c59b27] pointer-events-none" />

            {/* Header */}
            <div className="text-center space-y-1 pt-2">
              <p className="text-[9px] font-bold tracking-widest text-[#c59b27] uppercase">Official Diploma</p>
              <h3 className="font-serif font-bold text-sm tracking-wide uppercase">
                {formData.institution_name || 'Metropolitan State University'}
              </h3>
              <div className="w-16 h-0.5 bg-[#c59b27] mx-auto" />
            </div>

            {/* Body */}
            <div className="text-center space-y-2 py-4">
              <p className="font-serif italic text-[11px] text-slate-600">This is to certify that</p>
              <h4 className="font-sans font-bold text-base text-[#0f2744] tracking-tight">
                {formData.student_name || 'Student Name'}
              </h4>
              <p className="text-[9px] text-slate-500 font-mono">
                Student ID: {formData.student_id || '---'}
              </p>
              <p className="font-serif italic text-[10px] text-slate-600">
                has completed the prescribed curriculum and is conferred the degree of
              </p>
              <p className="font-sans font-bold text-xs text-[#0f2744]">
                {formData.degree || 'Degree Program'}
              </p>
              <p className="text-[10px] text-slate-600">
                {formData.department} • Class of {formData.graduation_year}
              </p>
            </div>

            {/* Footer */}
            <div className="pt-4 border-t border-slate-300 flex items-end justify-between text-[9px] text-slate-600">
              <div>
                <span className="font-bold text-[#0f2744] block">CERT-2026-XXXX</span>
                <span>Date: {formData.issue_date}</span>
              </div>
              <div className="w-12 h-12 bg-slate-200 border border-slate-400 rounded flex items-center justify-center text-[7px] text-center font-mono">
                [QR CODE]
              </div>
              <div className="text-right">
                <span className="font-bold text-[#0f2744] block">Dr. Eleanor Vance</span>
                <span>President</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
