export function useJobCard({ job, onApply }) {
  const handleApply = () => {
    if (onApply) onApply(job.id);
  };

  const contractColors = {
    CDI: "bg-orange-200 text-emerald-700",
    Contract: "bg-amber-100 text-amber-700",
    CDD: "bg-sky-100 text-sky-700",
    Freelance: "bg-violet-100 text-violet-700",
  };

  const badgeClass =
    contractColors[job.type_contrat] ?? "bg-emerald-200 text-gray-600";

  const formatRelativeDate = (dateString) => {
    const now = new Date();
    const date = new Date(dateString);

    const diffInSeconds = Math.floor((now - date) / 1000);

    const minutes = Math.floor(diffInSeconds / 60);
    const hours = Math.floor(diffInSeconds / 3600);
    const days = Math.floor(diffInSeconds / 86400);

    if (diffInSeconds < 60) {
      return "À l’instant";
    } else if (minutes < 60) {
      return `Il y a ${minutes} minute${minutes > 1 ? "s" : ""}`;
    } else if (hours < 24) {
      return `Il y a ${hours} heure${hours > 1 ? "s" : ""}`;
    } else if (days === 1) {
      return "Hier";
    } else {
      return `Il y a ${days} jours`;
    }
  };

  const formatSalary = (text) => {
    const numbers = text.match(/\d+/g);

    if (!numbers || numbers.length < 2) {
      return text; // retourne "Non renseigné"
    }

    return `${numbers[0]} - ${numbers[2]} €`;
  };

  return {
    handleApply,
    badgeClass,
    formatRelativeDate,
    formatSalary,
  };
}
