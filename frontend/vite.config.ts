// frontend/vite.config.ts
// Назначение: конфигурация Vite (dev + production)

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/", //  ОБЯЗАТЕЛЬНО для nginx и продакшена
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost", // nginx на 80 порту
        changeOrigin: true,
      },
    },
  },
});
