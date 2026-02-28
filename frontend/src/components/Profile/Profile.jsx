import {
  Plus,
  X,
  Briefcase,
  Euro,
  Calendar,
  Link2,
  Star,
  User,
  ChevronRight,
} from "lucide-react";
import { Toast } from "../ui/utils";
import { Search } from "lucide-react";
import { Link } from "react-router-dom";
import { useProfile } from "./useProfile";
import {
  Field,
  SectionTitle,
  StyledInput /*CompletionChart*/,
} from "./toolProfile";

export default function Profile() {
  const NIVEAUX_VALIDES = ["Debutant", "Intermediaire", "Avance", "Expert"];
  const CATEGORIES_VALIDES = [
    "Langage",
    "Framework",
    "Outil",
    "Soft Skill",
    "Autre",
  ];

  const {
    data,
    profile,
    /*completion,*/ setEditedProfile,
    isEditing,
    setIsEditing,
    /*isSkillEditing,*/ update,
    handleSave,
    toastMessage,
    skills,
    newSkill,
    addSkill,
    deleteSkill,
    setNewSkill,
    setToastMessage,
  } = useProfile();
  if (!profile) return <div>Chargement... Veuillez reactualiser la page</div>;
  return (
    <div className=" bg-white  sm:py-10  lg:py-5">
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
            <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-blue-500 bg-clip-text text-transparent">
              Mon Profil
            </h1>
            <p className="mt-2 text-gray-500">
              Gérez vos informations personnelles et professionnelles
            </p>
          </div>

          {/* <CompletionChart completion={completion}/> */}
        </div>
      </div>

      {toastMessage && (
        <Toast message={toastMessage} onClose={() => setToastMessage("")} />
      )}

      <div className="max-w-4xl mx-auto px-6 py-10 space-y-6 sm:py-12 lg:py-4">
        {/* HERO CARD */}
        <div className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 rounded-2xl p-8 text-white shadow-xl">
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/4" />
          <div className="absolute bottom-0 left-1/2 w-48 h-48 bg-white/5 rounded-full translate-y-1/2" />
          <div className="relative flex justify-between items-start">
            <div className="flex items-center gap-5">
              <div className="w-16 h-16 bg-white/20 backdrop-blur rounded-2xl flex items-center justify-center border border-white/30">
                <User className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold tracking-tight">
                  {profile.titre_professionnel}
                </h1>
                <div className="flex items-center gap-3 mt-3">
                  {profile.type_contrat_recherche && (
                    <span className="px-3 py-1 bg-white/20 rounded-full text-xs font-medium border border-white/20">
                      {profile.type_contrat_recherche}
                    </span>
                  )}
                  <span className="px-3 py-1 bg-white/20 rounded-full text-xs font-medium border border-white/20">
                    {profile.annees_experience} ans d'expérience
                  </span>
                </div>
              </div>
            </div>
            <div>
              {isEditing ? (
                <div className="flex gap-2">
                  <button
                    onClick={() => setIsEditing(false)}
                    className="px-4 py-2 text-sm bg-white/20 hover:bg-white/30 rounded-xl transition-all border border-white/30 font-medium"
                  >
                    Annuler
                  </button>
                  <button
                    onClick={handleSave}
                    className="px-4 py-2 text-sm bg-white text-blue-700 hover:bg-blue-50 rounded-xl transition-all font-semibold shadow-lg"
                  >
                    Enregistrer
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => {
                    setEditedProfile(profile);
                    setIsEditing(true);
                  }}
                  className="px-5 py-2.5 text-sm bg-white text-blue-700 hover:bg-blue-50 rounded-xl transition-all font-semibold shadow-lg flex items-center gap-2"
                >
                  Modifier le profil
                </button>
              )}
            </div>
          </div>
        </div>

        {/* FORM CARD */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 space-y-10">
          {/* Informations générales */}
          <div>
            <SectionTitle icon={Briefcase} title="Informations générales" />
            <div className="grid md:grid-cols-2 gap-5">
              <Field label="Titre professionnel">
                <StyledInput
                  value={data.titre_professionnel ?? ""}
                  disabled={!isEditing}
                  onChange={(e) =>
                    update({ titre_professionnel: e.target.value })
                  }
                />
              </Field>
              <Field label="LinkedIn">
                <div className="relative">
                  <Link2 className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <StyledInput
                    value={data.linkedin_url ?? ""}
                    disabled={!isEditing}
                    onChange={(e) => update({ linkedin_url: e.target.value })}
                    className="pl-9"
                  />
                </div>
              </Field>
              <Field label="Années d'expérience">
                <StyledInput
                  type="number"
                  value={data.annees_experience ?? 0}
                  disabled={!isEditing}
                  onChange={(e) =>
                    update({ annees_experience: parseInt(e.target.value) || 0 })
                  }
                />
              </Field>
              <Field label="CV (chemin)">
                <StyledInput
                  value={data.cv_path ?? ""}
                  disabled={!isEditing}
                  onChange={(e) => update({ cv_path: e.target.value })}
                />
              </Field>
            </div>
          </div>

          {/* Infos emploi */}
          <div>
            <SectionTitle icon={Euro} title="Infos Emploi" />
            <div className="grid md:grid-cols-3 gap-5">
              <Field label="Type de contrat">
                <select
                  value={data.type_contrat_recherche ?? ""}
                  disabled={!isEditing}
                  onChange={(e) =>
                    update({ type_contrat_recherche: e.target.value })
                  }
                  className={`w-full px-4 py-1 rounded-xl text-sm font-medium transition-all outline-none border
                  ${
                    !isEditing
                      ? "bg-gray-50 text-gray-700 border-transparent cursor-default"
                      : "bg-white border-blue-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 shadow-sm"
                  }`}
                >
                  <option value="">CDI</option>
                  {["CDD", "Freelance", "Stage", "Alternance"].map((type) => (
                    <option key={type} value={type}>
                      {type}
                    </option>
                  ))}
                </select>
              </Field>
              <Field label="Salaire minimum (€)">
                <div className="relative">
                  <Euro className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <StyledInput
                    type="number"
                    value={data.salaire_min_souhaite ?? 0}
                    disabled={!isEditing}
                    onChange={(e) =>
                      update({
                        salaire_min_souhaite: parseInt(e.target.value) || 0,
                      })
                    }
                    className="pl-9"
                  />
                </div>
              </Field>
              <Field label="Date de disponibilité">
                <div className="relative">
                  <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <StyledInput
                    type="date"
                    value={data.date_disponibilite ?? ""}
                    disabled={!isEditing}
                    onChange={(e) =>
                      update({ date_disponibilite: e.target.value })
                    }
                    className="pl-9"
                  />
                </div>
              </Field>
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-4xl mx-auto px-6 py-10 space-y-6 sm:py-12 lg:py-0">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 space-y-4">
          <SectionTitle icon={Star} title="Compétences" />

          {/* Formulaire ajout */}
          <div className="grid md:grid-cols-3 gap-3">
            <Field label="Nom Compétence">
              <StyledInput
                value={newSkill.nom_competence}
                onChange={(e) =>
                  setNewSkill({ ...newSkill, nom_competence: e.target.value })
                }
                placeholder="Ex: React"
              />
            </Field>
            <Field label="Niveau">
              <select
                value={newSkill.niveau}
                onChange={(e) =>
                  setNewSkill({ ...newSkill, niveau: e.target.value })
                }
                className="w-full px-4 py-2 rounded-xl text-sm border border-blue-200 focus:border-blue-500 outline-none"
              >
                <option value="">Choisir</option>
                {NIVEAUX_VALIDES.map((n) => (
                  <option key={n} value={n}>
                    {n}
                  </option>
                ))}
              </select>
            </Field>
            <Field label="Catégorie">
              <select
                value={newSkill.categorie}
                onChange={(e) =>
                  setNewSkill({ ...newSkill, categorie: e.target.value })
                }
                className="w-full px-4 py-2 rounded-xl text-sm border border-blue-200 focus:border-blue-500 outline-none"
              >
                <option value="">Choisir</option>
                {CATEGORIES_VALIDES.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </Field>
          </div>

          <button
            onClick={addSkill}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-sm font-medium transition-all"
          >
            <Plus className="w-4 h-4" />
            Ajouter
          </button>

          {/* Liste compétences */}
          <div className="mt-4 space-y-2">
            {skills.length === 0 && (
              <p className="text-sm text-gray-400 italic">
                Aucune compétence renseignée
              </p>
            )}
            {skills.map((skill) => (
              <div
                key={skill.id_user_skill}
                className="flex items-center justify-between px-4 py-3 bg-blue-50 rounded-xl border border-blue-100"
              >
                <div className="flex items-center gap-4">
                  <span className="text-sm font-semibold text-blue-700">
                    {skill.nom_competence}
                  </span>
                  {skill.niveau && (
                    <span className="text-xs text-gray-500 bg-white px-2 py-1 rounded-full border">
                      {skill.niveau}
                    </span>
                  )}
                  {skill.categorie && (
                    <span className="text-xs text-gray-500 bg-white px-2 py-1 rounded-full border">
                      {skill.categorie}
                    </span>
                  )}
                </div>
                <button
                  onClick={() => deleteSkill(skill.id_user_skill)}
                  className="w-6 h-6 rounded-full bg-blue-200 hover:bg-red-200 flex items-center justify-center transition-colors"
                >
                  <X className="w-3 h-3 text-blue-700 hover:text-red-700" />
                </button>
              </div>
            ))}
          </div>
        </div>{" "}
      </div>
    </div>
  );
}
