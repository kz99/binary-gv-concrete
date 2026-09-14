import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => ({
  base: mode === 'pages' ? '/binary-gv-concrete-observatory/' : '/',
  plugins: [react()],
}));
