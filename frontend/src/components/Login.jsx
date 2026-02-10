import { useState } from "react";
import { useNavigate , Link } from "react-router-dom";
import "../style/style.css";
//import api from "../api";


function Login() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("username", username);
      formData.append("password", password);

      const response = await api.post("/api/v1/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      localStorage.setItem("token", response.data.access_token);
      navigate("/welcome");
    } catch (err) {
      setError(err.response?.data?.detail || "Erreur de connexion");
    } finally {
      setLoading(false);
    }
  };

  return (

  <div className="login-container">
      <div className="login-background">
        <div className="bg-decoration bg-decoration-1"></div>
        <div className="bg-decoration bg-decoration-2"></div>
      </div>
      
      <div className="login-card">
        <div className="login-header">
          <div className="login-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
          </div>
          <h1 className="login-title">JOB SEARCH</h1>
          </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email" className="form-label"> Addresse Email</label>
            <div className="input-wrapper">
              <svg className="input-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect width="20" height="16" x="2" y="4" rx="2"/>
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
              </svg>
              <input
                type="email"
                id="email"
                placeholder="votre@email.com"
                //value={use}
                onChange={(e) => setUsername(e.target.value)}
                className="form-input"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <div className="form-label-row">
              <label htmlFor="password" className="form-label">Mot de passe</label>
              </div>
            <div className="input-wrapper">
              <svg className="input-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                placeholder="Entrer votre mot de passe"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-input"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="password-toggle"
                aria-label="Toggle password visibility"
              >
                {showPassword ? (
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"/>
                    <path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"/>
                    <path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"/>
                    <path d="m2 2 20 20"/>
                  </svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                )}
              </button>
            </div>
          </div>

          <button type="submit" className="submit-button">
            <span style={{ color: "white", textDecoration: "none" }}>{loading ? "Connexion en cours..." : "Se connecter"}</span>
          </button>
        </form>
                {error && (
          <div style ={{ color: "red", marginTop: "25px", textAlign: "center" }}>
            ❌ {error}
          </div>
        )}

        <p className="signup-text">
          Vous n'avez pas de compte ?{" "}
          <Link to="/register" className="signup-link">S'inscrire</Link>
        </p>
      </div>

      {/* <div className="security-badge">
        🔒 Your data is secure and encrypted
      </div> */}
    </div>
  );
}
export default Login;
