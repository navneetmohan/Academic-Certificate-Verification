import React from 'react';
import { Shield, BookOpen, Layers, Award, Lock } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-slate-950/80 text-slate-400 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Col */}
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-white font-bold text-lg">
              <Shield className="w-5 h-5 text-brand-400" />
              <span>CertLedger Protocol</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Decentralized academic credential integrity verification system powered by Ethereum smart contracts, 
              deterministic SHA-256 cryptographic hashing, and off-chain PII protection.
            </p>
          </div>

          {/* Architecture Principles */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">
              Hybrid Architecture
            </h4>
            <ul className="space-y-2 text-xs">
              <li className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-brand-400"></span>
                <span>On-Chain: Minimum SHA-256 Hash Record</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                <span>Off-Chain: Student Privacy & Metadata</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
                <span>Smart Contract: Ownable & Role-Protected</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-gold-400"></span>
                <span>Tamper-Evident SHA-256 Avalanche</span>
              </li>
            </ul>
          </div>

          {/* SDG Alignment */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">
              UN SDG Alignment
            </h4>
            <div className="space-y-2">
              <div className="p-2 rounded bg-slate-900 border border-slate-800">
                <span className="text-[11px] font-bold text-brand-300 block">SDG 4: Quality Education</span>
                <span className="text-[10px] text-slate-400">Guarantees verifiable authenticity of degrees</span>
              </div>
              <div className="p-2 rounded bg-slate-900 border border-slate-800">
                <span className="text-[11px] font-bold text-emerald-300 block">SDG 9: Industry & Innovation</span>
                <span className="text-[10px] text-slate-400">Modern blockchain-based digital infrastructure</span>
              </div>
              <div className="p-2 rounded bg-slate-900 border border-slate-800">
                <span className="text-[11px] font-bold text-indigo-300 block">SDG 16: Strong Institutions</span>
                <span className="text-[10px] text-slate-400">Combats fraudulent academic credential forgery</span>
              </div>
            </div>
          </div>

          {/* System Spec */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">
              Technical Environment
            </h4>
            <ul className="space-y-1.5 text-xs font-mono">
              <li className="text-slate-300">Hardhat Local Node (31337)</li>
              <li className="text-slate-300">Solidity ^0.8.20 (Paris EVM)</li>
              <li className="text-slate-300">FastAPI 0.111 / Web3.py</li>
              <li className="text-slate-300">React 18 / Tailwind CSS</li>
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-slate-800/80 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© 2026 Academic Certificate Verification System. Built for educational demonstration & defense.</p>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-slate-400 font-mono">Blockchain Ready: Hardhat Localnet</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
