import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { Activity, FileText, Sun, Moon, Shield } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import CitizenReport from './pages/CitizenReport';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import './index.css';

function AppShell() {
  const { theme, toggleTheme } = useTheme();

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: 'var(--bg-primary)' }}>
      {/* Navigation */}
      <nav style={{
        background: 'var(--bg-secondary)',
        borderBottom: '1px solid var(--border-primary)',
        padding: '0 24px',
        display: 'flex',
        alignItems: 'center',
        height: 58,
        position: 'sticky',
        top: 0,
        zIndex: 50,
        backdropFilter: 'blur(16px)',
        transition: 'background 0.2s ease, border-color 0.2s ease',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginRight: 32 }}>
          <div style={{
            background: 'linear-gradient(135deg, #0ea5e9 0%, #3b82f6 50%, #6366f1 100%)',
            padding: '6px',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 16px rgba(14, 165, 233, 0.4)'
          }}>
            <Shield size={18} color="#ffffff" />
          </div>
          <div>
            <span style={{ fontWeight: 800, fontSize: 16, letterSpacing: '-0.02em', color: 'var(--text-primary)' }}>
              Civic<span style={{ color: 'var(--accent-blue)' }}>Nexus</span>
            </span>
            <span style={{
              marginLeft: 6,
              fontSize: 9,
              color: '#38bdf8',
              background: 'rgba(56, 189, 248, 0.12)',
              border: '1px solid rgba(56, 189, 248, 0.25)',
              padding: '1.5px 6px',
              borderRadius: 4,
              fontWeight: 700,
              letterSpacing: '0.04em',
            }}>
              AI MATRIX
            </span>
          </div>
        </div>

        <div style={{ display: 'flex', gap: 6 }}>
          <NavLink to="/" end style={({ isActive }) => ({
            padding: '7px 14px',
            borderRadius: 8,
            fontSize: 13,
            fontWeight: 600,
            color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
            background: isActive ? 'var(--bg-tertiary)' : 'transparent',
            border: isActive ? '1px solid var(--border-primary)' : '1px solid transparent',
            textDecoration: 'none',
            display: 'flex',
            alignItems: 'center',
            gap: 7,
            transition: 'all 0.15s ease',
          })}>
            <Activity size={15} />
            Command Center
          </NavLink>
          <NavLink to="/report" style={({ isActive }) => ({
            padding: '7px 14px',
            borderRadius: 8,
            fontSize: 13,
            fontWeight: 600,
            color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
            background: isActive ? 'var(--bg-tertiary)' : 'transparent',
            border: isActive ? '1px solid var(--border-primary)' : '1px solid transparent',
            textDecoration: 'none',
            display: 'flex',
            alignItems: 'center',
            gap: 7,
            transition: 'all 0.15s ease',
          })}>
            <FileText size={15} />
            Citizen Portal
          </NavLink>
        </div>

        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 14 }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            fontSize: 11,
            fontWeight: 500,
            color: '#10b981',
            background: 'rgba(16, 185, 129, 0.08)',
            border: '1px solid rgba(16, 185, 129, 0.2)',
            padding: '3px 10px',
            borderRadius: 999
          }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#10b981', display: 'inline-block' }} />
            Autonomous Multi-Agent Matrix Live
          </div>

          {/* Light / Dark mode toggle */}
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            style={{
              padding: '7px',
              borderRadius: 8,
              background: 'var(--bg-tertiary)',
              border: '1px solid var(--border-primary)',
              cursor: 'pointer',
              color: 'var(--text-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.15s ease'
            }}
          >
            {theme === 'dark' ? <Sun size={15} /> : <Moon size={15} />}
          </button>
        </div>
      </nav>

      {/* Routes */}
      <main style={{ flex: 1, padding: '24px 28px' }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/report" element={<CitizenReport />} />
        </Routes>
      </main>

      {/* Footer */}
      <footer style={{
        borderTop: '1px solid var(--border-primary)',
        padding: '12px 24px',
        fontSize: 11,
        color: 'var(--text-tertiary)',
        textAlign: 'center',
        background: 'var(--bg-secondary)',
        transition: 'border-color 0.2s ease',
      }}>
        CivicNexus AI — Autonomous Urban Incident Intelligence Matrix by <strong>Team Nexus</strong>. AI-generated civic infrastructure hypothesis.
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <AppShell />
      </BrowserRouter>
    </ThemeProvider>
  );
}
