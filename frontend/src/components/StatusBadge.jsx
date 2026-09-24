import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle, HelpCircle } from 'lucide-react';

export default function StatusBadge({ status, revoked = false, className = '' }) {
  // Normalize status
  const s = (status || (revoked ? 'REVOKED' : 'VALID')).toUpperCase();

  if (s === 'VALID' || s === 'ACTIVE') {
    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 ${className}`}>
        <CheckCircle2 className="w-3.5 h-3.5" />
        VALID / AUTHENTIC
      </span>
    );
  }

  if (s === 'REVOKED') {
    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20 ${className}`}>
        <AlertTriangle className="w-3.5 h-3.5" />
        REVOKED
      </span>
    );
  }

  if (s === 'INVALID' || s === 'MODIFIED') {
    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/20 ${className}`}>
        <XCircle className="w-3.5 h-3.5" />
        INVALID / MODIFIED
      </span>
    );
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-500/10 text-slate-400 border border-slate-500/20 ${className}`}>
      <HelpCircle className="w-3.5 h-3.5" />
      NOT FOUND
    </span>
  );
}
