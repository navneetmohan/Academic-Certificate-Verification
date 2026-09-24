import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, KeyRound, Mail, AlertCircle, ArrowRight, Sparkles } from 'lucide-react';
import { authService } from '../services/api';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await authService.login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password. Please verify your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const fillDemoCredentials = () => {
    setEmail('admin@university.edu');
    setPassword('adminpassword123');
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 glass-panel p-8 rounded-3xl border border-slate-800 shadow-2xl relative overflow-hidden">
        {/* Accent Glow */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="text-center space-y-2">
          <div className="inline-flex p-3 rounded-2xl bg-brand-500/10 text-brand-400 border border-brand-500/20 mb-2">
            <Shield className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Institution Portal Login</h2>
          <p className="text-xs text-slate-400">
            Authorized administrative access for universities and degree-granting institutions
          </p>
        </div>

        {/* Demo Credentials Quick Fill */}
        <div className="p-3.5 rounded-2xl bg-slate-900/90 border border-brand-500/30 flex items-center justify-between">
          <div className="space-y-0.5">
            <span className="text-[11px] font-semibold text-brand-400 flex items-center gap-1">
              <Sparkles className="w-3 h-3" />
              Demo Academic Administrator
            </span>
            <p className="text-[10px] text-slate-400">Metropolitan State University</p>
          </div>
          <button
            type="button"
            onClick={fillDemoCredentials}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-brand-600/30 text-brand-300 hover:bg-brand-600/50 border border-brand-500/40 transition-colors"
          >
            Auto-Fill Demo
          </button>
        </div>

        {error && (
          <div className="p-3.5 rounded-xl bg-red-500/10 border border-red-500/20 text-red-300 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-5">
          <div className="space-y-1.5">
            <label className="text-xs font-medium text-slate-300 flex items-center gap-1.5">
              <Mail className="w-3.5 h-3.5 text-slate-400" />
              Official Institution Email
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. admin@university.edu"
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-medium text-slate-300 flex items-center gap-1.5">
              <KeyRound className="w-3.5 h-3.5 text-slate-400" />
              Admin Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••••••"
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-medium text-sm transition-all shadow-lg shadow-brand-600/30 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {loading ? (
              'Authenticating...'
            ) : (
              <>
                Sign In to Portal
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="pt-2 text-center">
          <p className="text-[11px] text-slate-500 font-mono">
            Connected Wallet: Account #1 (0x7099...79C8)
          </p>
        </div>
      </div>
    </div>
  );
}
