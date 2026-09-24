import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import IssueCertificatePage from './pages/IssueCertificatePage';
import CertificatesListPage from './pages/CertificatesListPage';
import CertificateDetailPage from './pages/CertificateDetailPage';
import VerifyPage from './pages/VerifyPage';
import DirectVerifyPage from './pages/DirectVerifyPage';

import { authService } from './services/api';

function ProtectedRoute({ children }) {
  if (!authService.isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

export default function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen bg-slate-950 text-slate-100 selection:bg-brand-500 selection:text-white">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/issue"
              element={
                <ProtectedRoute>
                  <IssueCertificatePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/certificates"
              element={
                <ProtectedRoute>
                  <CertificatesListPage />
                </ProtectedRoute>
              }
            />
            <Route path="/certificate/:id" element={<CertificateDetailPage />} />
            <Route path="/verify" element={<VerifyPage />} />
            <Route path="/verify/:id" element={<DirectVerifyPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}
