import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Download, ShieldAlert, CheckCircle2, AlertTriangle, Eye, RefreshCw, PlusCircle, ArrowUpDown } from 'lucide-react';
import { certificateService } from '../services/api';
import StatusBadge from '../components/StatusBadge';

export default function CertificatesListPage() {
  const [certificates, setCertificates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [revokingId, setRevokingId] = useState(null);
  const [revokeConfirmId, setRevokeConfirmId] = useState(null);
  const [actionError, setActionError] = useState(null);

  const fetchCertificates = async () => {
    setLoading(true);
    try {
      const data = await certificateService.list();
      setCertificates(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCertificates();
  }, []);

  const handleRevoke = async (certificateId) => {
    setRevokingId(certificateId);
    setActionError(null);
    try {
      await certificateService.revoke(certificateId);
      setRevokeConfirmId(null);
      await fetchCertificates();
    } catch (err) {
      console.error(err);
      setActionError(err.response?.data?.detail || 'Failed to revoke certificate on blockchain.');
    } finally {
      setRevokingId(null);
    }
  };

  const filtered = certificates.filter((c) => {
    const s = searchTerm.toLowerCase();
    return (
      c.certificate_id.toLowerCase().includes(s) ||
      c.student_name.toLowerCase().includes(s) ||
      c.degree.toLowerCase().includes(s) ||
      c.department.toLowerCase().includes(s)
    );
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Certificates Registry</h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Complete directory of academic credentials anchored on the blockchain
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchCertificates}
            className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors"
            title="Refresh Registry"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
          <Link
            to="/issue"
            className="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-medium text-sm flex items-center gap-2 shadow-lg shadow-brand-600/25 transition-all"
          >
            <PlusCircle className="w-4 h-4" />
            Issue Certificate
          </Link>
        </div>
      </div>

      {actionError && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-300 text-xs flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>{actionError}</span>
        </div>
      )}

      {/* Search and Filters */}
      <div className="flex items-center justify-between gap-4 glass-card p-3 rounded-2xl border border-slate-800">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by student name, ID, or degree..."
            className="w-full bg-slate-900/60 pl-10 pr-4 py-2 rounded-xl text-xs text-white placeholder-slate-400 border border-slate-700/60 focus:outline-none focus:border-brand-500"
          />
        </div>
        <div className="text-xs text-slate-400 font-medium px-2">
          Showing <span className="text-white font-bold">{filtered.length}</span> records
        </div>
      </div>

      {/* Table Card */}
      <div className="glass-card rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
        {loading ? (
          <div className="py-16 text-center text-slate-400 text-sm">Loading certificates from database...</div>
        ) : filtered.length === 0 ? (
          <div className="py-16 text-center text-slate-400 text-sm">
            {searchTerm ? 'No certificates matching your search criteria.' : 'No certificates issued yet.'}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/80 text-slate-400 font-medium uppercase tracking-wider border-b border-slate-800">
                <tr>
                  <th className="py-3.5 px-4">Certificate ID</th>
                  <th className="py-3.5 px-4">Student Name</th>
                  <th className="py-3.5 px-4">Degree & Department</th>
                  <th className="py-3.5 px-4">Issue Date</th>
                  <th className="py-3.5 px-4">Blockchain Status</th>
                  <th className="py-3.5 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {filtered.map((cert) => (
                  <tr key={cert.certificate_id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-4 px-4 font-mono font-medium text-brand-300">
                      <Link to={`/certificate/${cert.certificate_id}`} className="hover:underline">
                        {cert.certificate_id}
                      </Link>
                    </td>
                    <td className="py-4 px-4 font-medium text-white">
                      {cert.student_name}
                    </td>
                    <td className="py-4 px-4 text-slate-300">
                      <div>{cert.degree}</div>
                      <div className="text-[11px] text-slate-500">{cert.department}</div>
                    </td>
                    <td className="py-4 px-4 text-slate-400">
                      {cert.issue_date}
                    </td>
                    <td className="py-4 px-4">
                      <StatusBadge revoked={cert.revoked} />
                    </td>
                    <td className="py-4 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Link
                          to={`/certificate/${cert.certificate_id}`}
                          className="p-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
                          title="View Proof & Certificate Details"
                        >
                          <Eye className="w-4 h-4" />
                        </Link>
                        <a
                          href={certificateService.getDownloadUrl(cert.certificate_id)}
                          target="_blank"
                          rel="noreferrer"
                          className="p-1.5 rounded-lg text-emerald-400 hover:bg-emerald-500/10 transition-colors"
                          title="Download PDF"
                        >
                          <Download className="w-4 h-4" />
                        </a>
                        {!cert.revoked ? (
                          <button
                            onClick={() => setRevokeConfirmId(cert.certificate_id)}
                            className="p-1.5 rounded-lg text-amber-400 hover:bg-amber-500/10 transition-colors"
                            title="Revoke Certificate on Blockchain"
                          >
                            <ShieldAlert className="w-4 h-4" />
                          </button>
                        ) : (
                          <span className="text-[10px] text-slate-500 uppercase font-mono px-2 py-1">
                            Revoked
                          </span>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Revocation Confirmation Modal */}
      {revokeConfirmId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="glass-card max-w-md w-full p-6 rounded-2xl border border-amber-500/30 space-y-4 shadow-2xl">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
                <AlertTriangle className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Revoke Certificate on Blockchain?</h3>
                <p className="text-xs text-slate-400">Irreversible smart contract state change</p>
              </div>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed">
              Are you sure you want to revoke <span className="font-mono text-white font-bold">{revokeConfirmId}</span>?
              This will submit an on-chain transaction calling <code className="text-brand-300">revokeCertificate()</code>.
              Future verification attempts by employers will permanently display <span className="text-amber-400 font-bold">REVOKED</span>.
            </p>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setRevokeConfirmId(null)}
                className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                type="button"
                disabled={revokingId === revokeConfirmId}
                onClick={() => handleRevoke(revokeConfirmId)}
                className="px-4 py-2 rounded-xl text-xs font-bold bg-amber-600 hover:bg-amber-500 text-white shadow-lg shadow-amber-600/30 transition-all flex items-center gap-2"
              >
                {revokingId === revokeConfirmId ? 'Submitting Tx...' : 'Confirm Blockchain Revocation'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
