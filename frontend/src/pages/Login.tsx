import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, User } from 'lucide-react';

export default function Login({ setRole }: { setRole: (role: string) => void }) {
  const navigate = useNavigate();
  const [selectedRole, setSelectedRole] = useState<'CITIZEN' | 'ADMIN'>('CITIZEN');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem('civic_nexus_role', selectedRole);
    setRole(selectedRole);
    if (selectedRole === 'ADMIN') {
      navigate('/');
    } else {
      navigate('/report');
    }
  };

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      background: 'var(--bg-primary)'
    }}>
      <div className="card" style={{ width: '100%', maxWidth: 400, padding: 32, display: 'flex', flexDirection: 'column', gap: 24 }}>
        
        <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12 }}>
          <div style={{
            background: 'linear-gradient(135deg, #0ea5e9 0%, #3b82f6 50%, #6366f1 100%)',
            padding: 12,
            borderRadius: 16,
            display: 'inline-flex',
            boxShadow: '0 0 24px rgba(14, 165, 233, 0.4)'
          }}>
            <Shield size={32} color="#ffffff" />
          </div>
          <div>
            <h2 style={{ fontSize: 24, fontWeight: 800, color: 'var(--text-primary)' }}>
              Civic<span style={{ color: 'var(--accent-blue)' }}>Nexus</span>
            </h2>
            <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginTop: 4 }}>
              Sign in to access your portal
            </p>
          </div>
        </div>

        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <button
              type="button"
              className={`btn ${selectedRole === 'CITIZEN' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setSelectedRole('CITIZEN')}
              style={{ padding: '16px 12px', display: 'flex', flexDirection: 'column', gap: 8, height: 'auto' }}
            >
              <User size={24} />
              Citizen
            </button>
            <button
              type="button"
              className={`btn ${selectedRole === 'ADMIN' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setSelectedRole('ADMIN')}
              style={{ padding: '16px 12px', display: 'flex', flexDirection: 'column', gap: 8, height: 'auto' }}
            >
              <Shield size={24} />
              Admin
            </button>
          </div>

          <button type="submit" className="btn btn-primary" style={{ width: '100%', padding: 12, justifyContent: 'center' }}>
            Continue as {selectedRole === 'ADMIN' ? 'Admin' : 'Citizen'}
          </button>
        </form>

      </div>
    </div>
  );
}
