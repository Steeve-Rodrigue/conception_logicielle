/* 

import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // ton FastAPI

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Votre fichier api.js
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");  // ← Récupère le token
  console.log("Intercepteur de requête - Token trouvé:", token ? "Oui" : "Non");
  console.log(token);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;  // ← L'ajoute à la requête
  }
  return config;
});

export default api;
 */