// frontend/src/api/client.ts — базовый HTTP-клиент
import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost/api", // backend
  headers: {
    "Content-Type": "application/json",
  },
});
