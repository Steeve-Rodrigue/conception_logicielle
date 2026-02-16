import axios from "axios";



// const api = axios.create({
//   baseURL: import.meta.env.VITE_API_BASE_URL,
// });

const API_BASE_URL = "http://127.0.0.1:8000"; // ton FastAPI

const api = axios.create({
  baseURL: API_BASE_URL,
});

/*
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
*/
export default api;
 