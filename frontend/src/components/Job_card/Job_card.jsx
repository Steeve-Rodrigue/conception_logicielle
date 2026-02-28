import {
  MapPin,
  Clock,
  DollarSign,
  GraduationCap,
  Calendar,
  ArrowUpRight,
} from "lucide-react";
import { Link } from "react-router-dom";
import { useJobCard } from "./useJob_card";
import back from "../../assets/jobify.png";

function JobCard({ job, onApply }) {
  const { handleApply, badgeClass, formatRelativeDate, formatSalary } =
    useJobCard({ job, onApply });

  return (
    <div
      className="group relative  backdrop-blur-sm rounded-3xl border border-gray-100 p-7
               shadow-md hover:shadow-2xl hover:-translate-y-2
               transition-all duration-300 ease-out overflow-hidden"
    >
      {/* Animated gradient top bar */}
      <div
        className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r 
                    from-indigo-400 via-blue-500 to-indigo-600
                    opacity-0 group-hover:opacity-100 transition-opacity duration-300"
      />

      {/* Header */}
      <div className="flex items-start gap-4 mb-6">
        {/* Logo */}
        <div
          className="flex-shrink-0 w-16 h-16 rounded-2xl overflow-hidden 
                      border border-gray-100 shadow-md group-hover:scale-105
                      transition-transform duration-300"
        >
          <img
            src={back}
            alt={job.entreprise}
            className="w-full h-full object-cover"
          />
        </div>

        {/* Title & Badge */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2 flex-wrap">
            <h3 className="text-lg font-bold text-gray-900 leading-snug group-hover:text-indigo-600 transition-colors">
              {job.titre}
            </h3>

            <span
              className={`text-xs font-semibold px-3 py-1 rounded-full shadow-sm ${badgeClass}`}
            >
              {job.type_contrat}
            </span>
          </div>

          <p className="text-sm text-gray-500 mt-1 font-medium">
            Entreprise : {job.entreprise}
          </p>
        </div>
      </div>

      {/* Info grid */}
      <div className="grid grid-cols-2  gap-y-3 mb-6">
        <InfoRow icon={<MapPin className="w-6 h-6" />}>
          {job.localisation}
        </InfoRow>

        {job.salaire && (
          <InfoRow icon={<DollarSign className="w-6 h-6" />}>
            {formatSalary(job.salaire)}
          </InfoRow>
        )}
        {job.hours && (
          <InfoRow icon={<Clock className="w-6 h-6" />}>{job.hours}</InfoRow>
        )}

        {job.experience && (
          <InfoRow icon={<GraduationCap className="w-6 h-6" />}>
            {job.experience}
          </InfoRow>
        )}
      </div>

      {/* Divider */}
      <div className="border-t border-gray-100 mb-5" />

      {/* Footer */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1 text-xs text-gray-500">
          <Calendar className="w-6 h-6" />
          <span>Publié {formatRelativeDate(job.date_publication)}</span>
        </div>

        <Link to={`/VoirOffre/${job.id_offre}`}>
          <button
            onClick={handleApply}
            className="flex items-center gap-2 px-5 py-2 rounded-xl text-sm font-semibold
                   bg-gradient-to-r from-indigo-500 to-blue-600
                   text-white hover:from-indigo-600 hover:to-blue-700
                   active:scale-95 transition-all duration-200 shadow-md"
          >
            Voir l'offre
            <ArrowUpRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
          </button>
        </Link>
      </div>
    </div>
  );
}

/* Reusable row item */
function InfoRow({ icon, children }) {
  return (
    <div className="flex items-center gap-2 text-sm text-gray-600 min-w-0">
      <span className="text-gray-400 flex-shrink-0">{icon}</span>
      <span className="truncate">{children}</span>
    </div>
  );
}

export default JobCard;
