import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Award, CheckCircle2, AlertTriangle, Blocks, PlusCircle, ArrowUpRight, Search, FileText } from 'lucide-react';
import { statsService, certificateService } from '../services/api';
import StatusBadge from '../components/StatusBadge';

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [certificates, setCertificates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [statsData, certsData] = await Promise.all([
          statsService.getDashboardStats(),
          certificateService.list()
        ]);
        setStats(statsData);
        setCertificates(certsData);
      } catch (err) {
        console.error("Dashboard data load error", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Institution Dashboard</h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Metropolitan State University • Blockchain Registry Portal
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/issue"
            className="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-medium text-sm flex items-center gap-2 shadow-lg shadow-brand-600/25 transition-all"
          >
            <PlusCircle className="w-4 h-4" />
            Issue New Certificate
          </Link>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Total Issued */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase tracking-wider">Total Certificates</span>
            <div className="p-2 rounded-lg bg-brand-500/10 text-brand-400">
              <Award className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-white">
            {loading ? '...' : stats?.total_certificates ?? 0}
          </div>
          <p className="text-[11px] text-slate-400">Total registered in ledger</p>
        </div>

        {/* Valid / Active */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase tracking-wider">Active & Valid</span>
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-emerald-400">
            {loading ? '...' : stats?.valid_certificates ?? 0}
          </div>
          <p className="text-[11px] text-slate-400">Cryptographically authentic</p>
        </div>

        {/* Revoked */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase tracking-wider">Revoked</span>
            <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
              <AlertTriangle className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-amber-400">
            {loading ? '...' : stats?.revoked_certificates ?? 0}
          </div>
          <p className="text-[11px] text-slate-400">On-chain revocation flag set</p>
        </div>

        {/* Blockchain Status */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-semibold uppercase tracking-wider">Blockchain Ledger</span>
            <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
              <Blocks className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className={`w-2.5 h-2.5 rounded-full ${stats?.blockchain_connected ? 'bg-emerald-400' : 'bg-red-400 animate-pulse'}`}></span>
            <span className="text-lg font-bold text-white">
              {stats?.blockchain_connected ? `Block #${stats.latest_block}` : 'Offline'}
            </span>
          </div>
          <p className="text-[11px] text-slate-400 font-mono truncate" title={stats?.contract_address}>
            {stats?.contract_address ? `${stats.contract_address.slice(0, 10)}...${stats.contract_address.slice(-6)}` : 'Deploying...'}
          </p>
        </div>
      </div>

      {/* Recent Issuances Table */}
      <div className="glass-card rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div>
            <h2 className="text-base font-semibold text-white">Recent Certificate Issuances</h2>
            <p className="text-xs text-slate-400">Latest academic credentials registered to the blockchain</p>
          </div>
          <Link
            to="/certificates"
            className="text-xs font-semibold text-brand-400 hover:text-brand-300 flex items-center gap-1"
          >
            View All ({certificates.length})
            <ArrowUpRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {loading ? (
          <div className="py-12 text-center text-slate-400 text-sm">Loading certificate records...</div>
        ) : certificates.length === 0 ? (
          <div className="py-16 text-center space-y-3">
            <FileText className="w-10 h-10 text-slate-600 mx-auto" />
            <p className="text-sm text-slate-300 font-medium">No certificates issued yet</p>
            <p className="text-xs text-slate-500">Issue your first blockchain-anchored credential to begin.</p>
            <Link
              to="/issue"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-medium"
            >
              <PlusCircle className="w-3.5 h-3.5" />
              Issue First Certificate
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/60 text-slate-400 font-medium uppercase tracking-wider border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Certificate ID</th>
                  <th className="py-3 px-4">Student Name</th>
                  <th className="py-3 px-4">Degree & Dept</th>
                  <th className="py-3 px-4">Issue Date</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {certificates.slice(0, 5).map((cert) => (
                  <tr key={cert.certificate_id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-3.5 px-4 font-mono font-medium text-brand-300">
                      {cert.certificate_id}
                    </td>
                    <td className="py-3.5 px-4 font-medium text-white">
                      {cert.student_name}
                    </td>
                    <td className="py-3.5 px-4 text-slate-300">
                      <div>{cert.degree}</div>
                      <div className="text-[11px] text-slate-500">{cert.department}</div>
                    </td>
                    <td className="py-3.5 px-4 text-slate-400">
                      {cert.issue_date}
                    </td>
                    <td className="py-3.5 px-4">
                      <StatusBadge revoked={cert.revoked} />
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <Link
                        to={`/certificate/${cert.certificate_id}`}
                        className="text-brand-400 hover:text-brand-300 font-medium hover:underline text-xs"
                      >
                        Inspect Proof →
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
