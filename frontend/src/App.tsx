import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { Activity, FileText, Sun, Moon } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import CitizenReport from './pages/CitizenReport';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import './index.css';

function AppShell() {
  const { theme, toggleTheme } = useTheme();

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Navigation */}
      <nav style={{
        background: 'var(--bg-secondary)',
        borderBottom: '1px solid var(--border-primary)',
        padding: '0 24px',
        display: 'flex',
        alignItems: 'center',
        height: 52,
        position: 'sticky',
        top: 0,
        zIndex: 50,
        transition: 'background 0.2s ease, border-color 0.2s ease',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginRight: 32 }}>
          <Activity size={18} color="var(--accent-blue)" />
          <span style={{ fontWeight: 700, fontSize: 15, letterSpacing: '-0.01em' }}>
            CivicIQ
          </span>
          <span style={{
            fontSize: 10,
            color: 'var(--text-tertiary)',
            background: 'var(--bg-tertiary)',
            padding: '1px 6px',
            borderRadius: 3,
            fontWeight: 500,
          }}>
            PROTOTYPE
          </span>
        </div>

        <div style={{ display: 'flex', gap: 4 }}>
          <NavLink to="/" end style={({ isActive }) => ({
            padding: '6px 12px',
            borderRadius: 5,
            fontSize: 13,
            fontWeight: 500,
            color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
            background: isActive ? 'var(--bg-tertiary)' : 'transparent',
            textDecoration: 'none',
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            transition: 'all 0.15s ease',
          })}>
            <Activity size={14} />
            Dashboard
          </NavLink>
          <NavLink to="/report" style={({ isActive }) => ({
            padding: '6px 12px',
            borderRadius: 5,
            fontSize: 13,
            fontWeight: 500,
            color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
            background: isActive ? 'var(--bg-tertiary)' : 'transparent',
            textDecoration: 'none',
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            transition: 'all 0.15s ease',
          })}>
            <FileText size={14} />
            Submit Report
          </NavLink>
        </div>

        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>
            Prototype uses synthetic civic data for demonstration
          </span>

          {/* Light / Dark mode toggle */}
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
          </button>
        </div>
      </nav>

      {/* Routes */}
      <main style={{ flex: 1, padding: '20px 24px' }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/report" element={<CitizenReport />} />
        </Routes>
      </main>

      {/* Footer */}
      <footer style={{
        borderTop: '1px solid var(--border-primary)',
        padding: '10px 24px',
        fontSize: 11,
        color: 'var(--text-tertiary)',
        textAlign: 'center',
        transition: 'border-color 0.2s ease',
      }}>
        Prototype uses synthetic civic data for demonstration. All root-cause output is AI-generated civic incident hypothesis.
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
