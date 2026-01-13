// frontend/src/api/client.ts — базовый HTTP-клиент
// Назначение: единая точка работы с backend API

import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost/api",
  headers: {
    "Content-Type": "application/json",
  },
});
