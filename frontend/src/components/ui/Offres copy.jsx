import { useState, useEffect } from "react";

// --- Utility: mappe les données API vers le format de la UI ---
function mapApiJobToUiJob(apiJob) {
  // Extrait ville et code postal depuis "35 - Rennes" → "Rennes" / "35"
  const locParts = apiJob.localisation?.split(" - ") ?? [];
  const postalCode = locParts[0]?.trim() ?? "";
  const city = locParts[1]?.trim() ?? apiJob.localisation ?? "Non précisé";

  // Formate la date de publication : "2026-02-16T05:55..." → "Aujourd'hui" / "Il y a N jours"
  function formatDatePosted(isoDate) {
    if (!isoDate) return "Récemment";
    const diff = Math.floor(
      (Date.now() - new Date(isoDate).getTime()) / (1000 * 60 * 60 * 24),
    );
    if (diff === 0) return "Aujourd'hui";
    if (diff === 1) return "Hier";
    return `Il y a ${diff} jours`;
  }

  return {
    id: String(apiJob.id_offre ?? apiJob.external_id),
    title: apiJob.titre ?? "Poste non renseigné",
    company: {
      name: apiJob.entreprise ?? "Entreprise inconnue",
      logo: null, // L'API ne fournit pas de logo
    },
    location: { city, postalCode },
    contractType: apiJob.type_contrat ?? "Non précisé",
    hours: null, // Non fourni par l'API
    salary: apiJob.salaire ?? "Salaire non communiqué",
    skills: apiJob.competences_requises ?? [],
    datePosted: formatDatePosted(apiJob.date_publication),
    url: apiJob.url_origine ?? null,
    source: apiJob.source ?? null,
    description: apiJob.description ?? "",
    isActive: apiJob.est_active ?? true,
  };
}

// --- Composant : Initiales de l'entreprise (placeholder logo) ---
function CompanyAvatar({ name }) {
  const initials = name
    .split(/[\s-]+/)
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase() ?? "")
    .join("");

  // Couleur déterministe selon le nom
  const colors = [
    ["#1a1a2e", "#e94560"],
    ["#0f3460", "#e94560"],
    ["#16213e", "#0f3460"],
    ["#1b4332", "#52b788"],
    ["#3d0066", "#c77dff"],
    ["#7b2d00", "#ff9f1c"],
  ];
  const idx =
    name.split("").reduce((acc, c) => acc + c.charCodeAt(0), 0) % colors.length;
  const [bg, accent] = colors[idx];

  return (
    <div
      style={{
        width: 48,
        height: 48,
        borderRadius: 10,
        background: bg,
        color: accent,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "'DM Mono', monospace",
        fontWeight: 700,
        fontSize: 16,
        flexShrink: 0,
        border: `1.5px solid ${accent}33`,
      }}
    >
      {initials || "?"}
    </div>
  );
}

// --- Composant : Badge ---
function Badge({ children, variant = "default" }) {
  const styles = {
    default: {
      background: "#1e293b",
      color: "#94a3b8",
      border: "1px solid #334155",
    },
    contract: {
      background: "#0f2744",
      color: "#60a5fa",
      border: "1px solid #1e40af55",
    },
    skill: {
      background: "#1a1a1a",
      color: "#a3a3a3",
      border: "1px solid #2a2a2a",
    },
    active: {
      background: "#052e16",
      color: "#4ade80",
      border: "1px solid #16a34a55",
    },
  };
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        padding: "3px 10px",
        borderRadius: 6,
        fontSize: 12,
        fontFamily: "'DM Mono', monospace",
        whiteSpace: "nowrap",
        ...styles[variant],
      }}
    >
      {children}
    </span>
  );
}

// --- Composant : Carte d'offre ---
function JobCard({ job, onClick }) {
  const [hovered, setHovered] = useState(false);

  return (
    <div
      onClick={() => onClick(job)}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background: hovered ? "#111827" : "#0d1117",
        border: hovered ? "1px solid #334155" : "1px solid #1e293b",
        borderRadius: 14,
        padding: "20px 22px",
        cursor: "pointer",
        transition: "all 0.18s ease",
        transform: hovered ? "translateY(-2px)" : "translateY(0)",
        boxShadow: hovered
          ? "0 8px 32px rgba(0,0,0,0.4)"
          : "0 2px 8px rgba(0,0,0,0.2)",
        display: "flex",
        flexDirection: "column",
        gap: 14,
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", gap: 14, alignItems: "flex-start" }}>
        {job.company.logo ? (
          <img
            src={job.company.logo}
            alt={job.company.name}
            style={{
              width: 48,
              height: 48,
              borderRadius: 10,
              objectFit: "cover",
            }}
          />
        ) : (
          <CompanyAvatar name={job.company.name} />
        )}
        <div style={{ flex: 1, minWidth: 0 }}>
          <div
            style={{
              fontSize: 15,
              fontWeight: 600,
              color: "#f1f5f9",
              fontFamily: "'Sora', sans-serif",
              marginBottom: 3,
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
          >
            {job.title}
          </div>
          <div
            style={{
              fontSize: 13,
              color: "#64748b",
              fontFamily: "'DM Mono', monospace",
            }}
          >
            {job.company.name}
          </div>
        </div>
        <div
          style={{
            fontSize: 11,
            color: "#475569",
            fontFamily: "'DM Mono', monospace",
            flexShrink: 0,
          }}
        >
          {job.datePosted}
        </div>
      </div>

      {/* Métadonnées */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
        <Badge variant="contract">{job.contractType}</Badge>
        <Badge variant="default">
          <span style={{ marginRight: 5 }}>📍</span>
          {job.location.city}
          {job.location.postalCode ? ` (${job.location.postalCode})` : ""}
        </Badge>
        {job.salary && job.salary !== "Salaire non communiqué" && (
          <Badge variant="default">
            <span style={{ marginRight: 5 }}>💰</span>
            {job.salary}
          </Badge>
        )}
      </div>

      {/* Compétences */}
      {job.skills.length > 0 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
          {job.skills.map((skill) => (
            <Badge key={skill} variant="skill">
              {skill}
            </Badge>
          ))}
        </div>
      )}

      {/* Footer */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          {job.source && (
            <span
              style={{
                fontSize: 11,
                color: "#374151",
                fontFamily: "'DM Mono', monospace",
              }}
            >
              via {job.source.replace("_", " ")}
            </span>
          )}
          {job.isActive && <Badge variant="active">● actif</Badge>}
        </div>
        {job.url && (
          <a
            href={job.url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
            style={{
              fontSize: 12,
              color: "#3b82f6",
              textDecoration: "none",
              fontFamily: "'DM Mono', monospace",
              padding: "5px 12px",
              border: "1px solid #1e40af55",
              borderRadius: 6,
              background: "#0f2744",
              transition: "background 0.15s",
            }}
          >
            Voir l'offre →
          </a>
        )}
      </div>
    </div>
  );
}

// --- Composant : Modal de détail ---
function JobModal({ job, onClose }) {
  if (!job) return null;

  useEffect(() => {
    const handleKey = (e) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [onClose]);

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.7)",
        backdropFilter: "blur(4px)",
        zIndex: 1000,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: 20,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: "#0d1117",
          border: "1px solid #1e293b",
          borderRadius: 18,
          padding: "30px",
          maxWidth: 680,
          width: "100%",
          maxHeight: "85vh",
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: 20,
        }}
      >
        {/* Header */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
          }}
        >
          <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
            <CompanyAvatar name={job.company.name} />
            <div>
              <h2
                style={{
                  margin: 0,
                  color: "#f1f5f9",
                  fontFamily: "'Sora', sans-serif",
                  fontSize: 18,
                  fontWeight: 700,
                }}
              >
                {job.title}
              </h2>
              <p
                style={{
                  margin: "4px 0 0",
                  color: "#64748b",
                  fontFamily: "'DM Mono', monospace",
                  fontSize: 13,
                }}
              >
                {job.company.name} · {job.location.city}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            style={{
              background: "transparent",
              border: "1px solid #1e293b",
              color: "#64748b",
              borderRadius: 8,
              width: 34,
              height: 34,
              cursor: "pointer",
              fontSize: 18,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              flexShrink: 0,
            }}
          >
            ×
          </button>
        </div>

        {/* Badges */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          <Badge variant="contract">{job.contractType}</Badge>
          <Badge variant="default">📍 {job.location.city}</Badge>
          {job.salary !== "Salaire non communiqué" && (
            <Badge variant="default">💰 {job.salary}</Badge>
          )}
          {job.isActive && <Badge variant="active">● Actif</Badge>}
        </div>

        {/* Compétences */}
        {job.skills.length > 0 && (
          <div>
            <p
              style={{
                color: "#94a3b8",
                fontFamily: "'DM Mono', monospace",
                fontSize: 12,
                marginBottom: 8,
                marginTop: 0,
              }}
            >
              COMPÉTENCES
            </p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
              {job.skills.map((s) => (
                <Badge key={s} variant="skill">
                  {s}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Description */}
        {job.description && (
          <div>
            <p
              style={{
                color: "#94a3b8",
                fontFamily: "'DM Mono', monospace",
                fontSize: 12,
                marginBottom: 8,
                marginTop: 0,
              }}
            >
              DESCRIPTION
            </p>
            <div
              style={{
                color: "#94a3b8",
                fontSize: 14,
                fontFamily: "'Sora', sans-serif",
                lineHeight: 1.7,
                whiteSpace: "pre-line",
                background: "#060910",
                borderRadius: 10,
                padding: "14px 16px",
                border: "1px solid #1e293b",
                maxHeight: 300,
                overflowY: "auto",
              }}
            >
              {job.description}
            </div>
          </div>
        )}

        {/* CTA */}
        {job.url && (
          <a
            href={job.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: "block",
              textAlign: "center",
              background: "#1d4ed8",
              color: "#fff",
              borderRadius: 10,
              padding: "12px 20px",
              textDecoration: "none",
              fontFamily: "'Sora', sans-serif",
              fontWeight: 600,
              fontSize: 14,
              transition: "background 0.15s",
            }}
          >
            Postuler sur {job.source?.replace("_", " ") ?? "le site officiel"} →
          </a>
        )}
      </div>
    </div>
  );
}

// --- Composant principal ---
export default function Offres({ apiBaseUrl = "http://localhost:8000" }) {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedJob, setSelectedJob] = useState(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function fetchJobs() {
      try {
        setLoading(true);
        setError(null);
        const res = await fetch(`${apiBaseUrl}/jobs/`);
        if (!res.ok) throw new Error(`Erreur ${res.status}: ${res.statusText}`);
        const data = await res.json();
        // Gère les deux cas : tableau direct ou { results: [...] }
        const rawJobs = Array.isArray(data) ? data : (data.results ?? []);
        setJobs(rawJobs.map(mapApiJobToUiJob));
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchJobs();
  }, [apiBaseUrl]);

  const filteredJobs = jobs.filter((job) => {
    const q = search.toLowerCase();
    return (
      job.title.toLowerCase().includes(q) ||
      job.company.name.toLowerCase().includes(q) ||
      job.location.city.toLowerCase().includes(q) ||
      job.skills.some((s) => s.toLowerCase().includes(q))
    );
  });

  return (
    <>
      {/* Import fonts */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=DM+Mono:wght@400;500&display=swap');
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0d1117; }
        ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
      `}</style>

      <div
        style={{
          minHeight: "100vh",
          background: "#060910",
          padding: "40px 20px",
          fontFamily: "'Sora', sans-serif",
        }}
      >
        {/* En-tête */}
        <div style={{ maxWidth: 800, margin: "0 auto 32px" }}>
          <h1
            style={{
              color: "#f1f5f9",
              fontSize: 28,
              fontWeight: 700,
              margin: "0 0 4px",
            }}
          >
            Offres d'emploi
          </h1>
          <p
            style={{
              color: "#475569",
              margin: "0 0 24px",
              fontFamily: "'DM Mono', monospace",
              fontSize: 13,
            }}
          >
            {loading
              ? "Chargement…"
              : `${filteredJobs.length} offre${filteredJobs.length !== 1 ? "s" : ""} disponible${filteredJobs.length !== 1 ? "s" : ""}`}
          </p>

          {/* Barre de recherche */}
          <input
            type="text"
            placeholder="Rechercher par titre, entreprise, ville, compétence…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{
              width: "100%",
              padding: "12px 18px",
              background: "#0d1117",
              border: "1px solid #1e293b",
              borderRadius: 10,
              color: "#f1f5f9",
              fontFamily: "'DM Mono', monospace",
              fontSize: 14,
              outline: "none",
              transition: "border-color 0.15s",
            }}
            onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
            onBlur={(e) => (e.target.style.borderColor = "#1e293b")}
          />
        </div>

        {/* Contenu */}
        <div style={{ maxWidth: 800, margin: "0 auto" }}>
          {loading && (
            <div
              style={{
                textAlign: "center",
                padding: "60px 0",
                color: "#475569",
                fontFamily: "'DM Mono', monospace",
              }}
            >
              <div style={{ fontSize: 32, marginBottom: 12 }}>⟳</div>
              Chargement des offres…
            </div>
          )}

          {error && (
            <div
              style={{
                background: "#1a0a0a",
                border: "1px solid #7f1d1d",
                borderRadius: 12,
                padding: "20px 24px",
                color: "#fca5a5",
                fontFamily: "'DM Mono', monospace",
                fontSize: 13,
              }}
            >
              <strong>Erreur de chargement :</strong> {error}
            </div>
          )}

          {!loading && !error && filteredJobs.length === 0 && (
            <div
              style={{
                textAlign: "center",
                padding: "60px 0",
                color: "#475569",
                fontFamily: "'DM Mono', monospace",
              }}
            >
              Aucune offre trouvée pour "{search}"
            </div>
          )}

          {!loading && !error && (
            <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
              {filteredJobs.map((job) => (
                <JobCard key={job.id} job={job} onClick={setSelectedJob} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Modal */}
      <JobModal job={selectedJob} onClose={() => setSelectedJob(null)} />
    </>
  );
}
