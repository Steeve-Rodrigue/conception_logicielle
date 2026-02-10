import { Link } from "react-router-dom";

const Welcome = () => {
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "linear-gradient(135deg, #f5f7fa, #c3cfe2)",
      }}
    >
      <div
        style={{
          maxWidth: "600px",
          background: "#fff",
          padding: "3rem",
          borderRadius: "12px",
          boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
          textAlign: "center",
        }}
      >
        {/* Titre */}
        <h1 style={{ marginBottom: "1rem" }}>
           Bienvenue sur <span style={{ color: "#2563eb" }}>JOB SEARCH</span>
        </h1>

        {/* Description */}
        <p style={{ fontSize: "1.05rem", color: "#555", lineHeight: 1.6 }}>
          JOB SEARCH est une plateforme conçue pour aider les étudiants à
          <strong> trouver, organiser et suivre leurs candidatures de stage</strong>.
          Centralisez vos démarches et gagnez en efficacité.
        </p>

        {/* Call to action */}
        <h2 style={{ marginTop: "2rem" }}> Prêt à commencer ?</h2>
        <p style={{ color: "#666" }}>
          Connectez-vous ou créez un compte pour démarrer votre recherche dès maintenant.
        </p>

        {/* Boutons */}
        <div style={{ marginTop: "2rem", display: "flex", gap: "1rem", justifyContent: "center" }}>
          <Link to="/login">
            <button
              style={{
                padding: "0.7rem 1.5rem",
                background: "#2563eb",
                color: "#fff",
                border: "none",
                borderRadius: "8px",
                cursor: "pointer",
                fontSize: "1rem",
              }}
            >
              Se connecter
            </button>
          </Link>

          <Link to="/register">
            <button
              style={{
                padding: "0.7rem 1.5rem",
                background: "#e5e7eb",
                color: "#111",
                border: "none",
                borderRadius: "8px",
                cursor: "pointer",
                fontSize: "1rem",
              }}
            >
              Créer un compte
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
