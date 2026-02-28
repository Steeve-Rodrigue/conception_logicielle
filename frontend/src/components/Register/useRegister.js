import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api";

export function useRegister() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    nom: "",
    prenom: "",
    email: "",
    pseudo: "",
    mdp: "",
    confirmation_mdp: "",
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await api.post("/auth/signup", formData);
      alert("✅ Inscription réussie ! Connectez-vous maintenant.");
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Erreur lors de l'inscription");
    } finally {
      setLoading(false);
    }
  };

  return {
    formData,
    error,
    loading,
    showPassword,
    setShowPassword,
    handleChange,
    handleSubmit,
  };
}
