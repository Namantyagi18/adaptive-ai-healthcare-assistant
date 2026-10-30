import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LanguageProvider } from './context/LanguageContext';
import { AuthProvider } from './context/AuthContext';
import { Sidebar } from './components/layout/Sidebar';
import { Header } from './components/layout/Header';
import { Footer } from './components/layout/Footer';

// Pages
import { Home } from './pages/Home';
import { Assistant } from './pages/Assistant';
import { HealthcareMap } from './pages/HealthcareMap';
import { FindHealthcare } from './pages/FindHealthcare';
import { Documents } from './pages/Documents';
import { VoiceAssistant } from './pages/VoiceAssistant';
import { CommunityCare } from './pages/CommunityCare';
import { SafetyCenter } from './pages/SafetyCenter';
import { Settings } from './pages/Settings';

export const AppContent: React.FC = () => {
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-cyan-500 selection:text-slate-950 overflow-x-hidden">
      {/* Left Sidebar Navigation */}
      <Sidebar
        isMobileOpen={isMobileSidebarOpen}
        onMobileClose={() => setIsMobileSidebarOpen(false)}
        isCollapsed={isSidebarCollapsed}
        onToggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
      />

      {/* Main Content Area */}
      <div
        className={`flex-1 flex flex-col min-w-0 transition-all duration-300 ease-in-out ${
          isSidebarCollapsed ? 'md:ml-[72px]' : 'md:ml-[260px]'
        }`}
      >
        <Header
          onMobileMenuOpen={() => setIsMobileSidebarOpen(true)}
          isSidebarCollapsed={isSidebarCollapsed}
        />

        <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/assistant" element={<Assistant />} />
            <Route path="/healthcare-map" element={<HealthcareMap />} />
            <Route path="/find-healthcare" element={<FindHealthcare />} />
            <Route path="/documents" element={<Documents />} />
            <Route path="/voice-assistant" element={<VoiceAssistant />} />
            <Route path="/community-care" element={<CommunityCare />} />
            <Route path="/safety" element={<SafetyCenter />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <LanguageProvider>
      <AuthProvider>
        <BrowserRouter>
          <AppContent />
        </BrowserRouter>
      </AuthProvider>
    </LanguageProvider>
  );
};

export default App;
