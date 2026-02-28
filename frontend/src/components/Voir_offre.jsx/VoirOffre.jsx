import { ArrowUpRight, MapPin, Euro, Briefcase, Calendar } from "lucide-react";
import { Search } from "lucide-react";
import { Link } from "react-router-dom";
import { useVoirOffre } from "./useVoirOffre";

export default function VoirOffre() {
  const { offre } = useVoirOffre();
  return (
    <div className=" bg-white sm:py-10  lg:py-5">
      {/* HEADER */}
      <header>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <Search className="w-8 h-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">JOBPILOT</span>
            </div>
            <div className="flex items-center gap-5">
              <Link
                to="/accueil"
                className="px-6 py-2.5 text-gray-700 hover:text-blue-700 hover:underline transition-colors"
              >
                Accueil
              </Link>
              <Link
                to="/Offres"
                className="px-6 py-2.5 text-gray-700 hover:text-blue-700 hover:underline transition-colors"
              >
                Offres d'emploi
              </Link>
              <Link
                to="/profile"
                className="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Consulter son profil
              </Link>
            </div>
          </div>
        </div>
      </header>

      <div className="bg-gradient-to-r from-indigo-50 via-indigo-200 to-white py-1">
        <div className="max-w-7xl mx-auto px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
          {/* Texte */}
          <div className="text-center sm:text-left">
            <h3 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-blue-500 bg-clip-text text-transparent">
              Consultation
            </h3>
          </div>

          {/* <CompletionChart completion={completion}/> */}
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 py-10 space-y-6 sm:py-11 lg:py-4">
        {/* HERO CARD */}
        <div className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 rounded-2xl p-8 text-white shadow-xl">
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/4" />
          <div className="absolute bottom-0 left-1/2 w-48 h-48 bg-white/5 rounded-full translate-y-1/2" />
          <div className="relative flex justify-between items-start">
            <div className="flex items-center gap-5">
              <div className="w-16 h-16 bg-white/20 backdrop-blur rounded-3xl flex items-center justify-center border border-white/300">
                <Briefcase className="w-14 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold tracking-tight">
                  {offre.titre}
                </h1>
              </div>
              <div>
                <h1 className="text-2xl font-bold tracking-tight">
                  Entreprise : {offre.entreprise}
                </h1>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-6xl mx-auto px-6 py-10 space-y-6 sm:py-12 lg:py-8">
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 space-y-8">
            {/* Informations clés */}
            <div>
              <div className="flex items-center gap-3 mb-5">
                <div className="w-1 h-6 bg-gradient-to-b from-indigo-500 to-blue-600 rounded-full" />
                <h2 className="text-base font-bold text-gray-800 uppercase tracking-widest">
                  Informations clés
                </h2>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="flex flex-col gap-2 p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl border border-blue-100">
                  <span className="text-xs font-semibold text-indigo-400 uppercase tracking-widest">
                    Localisation
                  </span>
                  <span className="text-sm font-semibold text-gray-700 flex items-center gap-1.5">
                    <MapPin className="w-4 h-4 text-indigo-500 flex-shrink-0" />
                    {offre.localisation}
                  </span>
                </div>
                <div className="flex flex-col gap-2 p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl border border-blue-100">
                  <span className="text-xs font-semibold text-indigo-400 uppercase tracking-widest">
                    Contrat
                  </span>
                  <span className="text-sm font-semibold text-gray-700 flex items-center gap-1.5">
                    <Briefcase className="w-4 h-4 text-indigo-500 flex-shrink-0" />
                    {offre.type_contrat}
                  </span>
                </div>
                <div className="flex flex-col gap-2 p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl border border-blue-100">
                  <span className="text-xs font-semibold text-indigo-400 uppercase tracking-widest">
                    Salaire
                  </span>
                  <span className="text-sm font-semibold text-gray-700 flex items-center gap-1.5">
                    <Euro className="w-4 h-4 text-indigo-500 flex-shrink-0" />
                    {offre.salaire}
                  </span>
                </div>
                <div className="flex flex-col gap-2 p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl border border-blue-100">
                  <span className="text-xs font-semibold text-indigo-400 uppercase tracking-widest">
                    Publié
                  </span>
                  <span className="text-sm font-semibold text-gray-700 flex items-center gap-1.5">
                    <Calendar className="w-4 h-4 text-indigo-500 flex-shrink-0" />
                    {new Date(offre.date_publication).toLocaleDateString(
                      "fr-FR",
                    )}
                  </span>
                </div>
              </div>
            </div>

            <div className="h-px bg-gray-100" />

            {/* Compétences requises */}
            <div>
              <div className="flex items-center gap-3 mb-5">
                <div className="w-1 h-6 bg-gradient-to-b from-indigo-500 to-blue-600 rounded-full" />
                <h2 className="text-base font-bold text-gray-800 uppercase tracking-widest">
                  Compétences requises
                </h2>
              </div>
              <div className="flex flex-wrap gap-2">
                {offre.competences_requises.length === 0 && (
                  <p className="text-sm text-gray-400 italic">
                    Aucune compétence renseignée
                  </p>
                )}
                {offre.competences_requises.map((comp, i) => (
                  <span
                    key={i}
                    className="px-3.5 py-1.5 bg-indigo-50 text-indigo-700 rounded-full text-sm font-medium border border-indigo-100 hover:bg-indigo-100 transition-colors"
                  >
                    {comp}
                  </span>
                ))}
              </div>
            </div>

            <div className="h-px bg-gray-100" />

            {/* Description */}
            <div>
              <div className="flex items-center gap-3 mb-5">
                <div className="w-1 h-6 bg-gradient-to-b from-indigo-500 to-blue-600 rounded-full" />
                <h2 className="text-base font-bold text-gray-800 uppercase tracking-widest">
                  Description du poste
                </h2>
              </div>
              <p className="text-gray-600 text-sm leading-relaxed whitespace-pre-line">
                {offre.description}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
