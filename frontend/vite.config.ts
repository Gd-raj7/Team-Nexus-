import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    host: true,
    port: 5173,
    allowedHosts: true,
    proxy: {
      '/reports': 'http://127.0.0.1:8000',
      '/incidents': 'http://127.0.0.1:8000',
      '/analyze': 'http://127.0.0.1:8000',
      '/dashboard': 'http://127.0.0.1:8000',
      '/memory': 'http://127.0.0.1:8000',
      '/agent-logs': 'http://127.0.0.1:8000',
      '/dev': 'http://127.0.0.1:8000',
      '/seed-images': 'http://127.0.0.1:8000',
      '/uploads': 'http://127.0.0.1:8000',
    },
  },
})
