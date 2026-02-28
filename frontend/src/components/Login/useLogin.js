import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api";

export function useLogin() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [mdp, setMdp] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await api.post("/auth/login", { email, mdp });
      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem(
        "utilisateur",
        JSON.stringify(response.data.utilisateur),
      );
      navigate("/Offres");
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (typeof detail === "string") {
        setError(detail);
      } else if (Array.isArray(detail)) {
        setError(detail.map((e) => e.msg).join(", "));
      } else {
        setError("Erreur de connexion");
      }
    } finally {
      setLoading(false);
    }
  };

  return {
    email,
    setEmail,
    mdp,
    setMdp,
    error,
    loading,
    showPassword,
    setShowPassword,
    handleSubmit,
  };
}
