import React from "react";
import { MapPin, Clock, DollarSign, GraduationCap, Calendar, ArrowUpRight } from "lucide-react";
import  back  from "../../assets/jobify.png";

function JobCard({ job, onApply }) {
  const handleApply = () => {
    if (onApply) onApply(job.id);
  };

//  {
//     id: '1',
//     title: 'Senior Frontend Developer',
//     company: {
//       name: 'TechCorp Solutions',
//       logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
//     },
//     location: {
//       city: 'San Francisco',
//       postalCode: '94102',
//     },
//     contractType: 'Full-time',
//     hours: '40h/week',
//     salary: '$120,000 - $160,000/year',
//     experience: '5+ years',
//     education: "Bachelor's Degree",
//     datePosted: '2 days ago',


  const contractColors = {
    "CDI": "bg-orange-200 text-emerald-700",
    Contract: "bg-amber-100 text-amber-700",
    "CDD": "bg-sky-100 text-sky-700",
    Freelance: "bg-violet-100 text-violet-700",
  };

  const badgeClass =
    contractColors[job.contr] ?? "bg-emerald-200 text-gray-600";

 return (
  <div
    className="group relative  backdrop-blur-sm rounded-3xl border border-gray-100 p-7
               shadow-md hover:shadow-2xl hover:-translate-y-2
               transition-all duration-300 ease-out overflow-hidden"
  >
    {/* Animated gradient top bar */}
    <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r 
                    from-indigo-400 via-blue-500 to-indigo-600
                    opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

    {/* Header */}
    <div className="flex items-start gap-4 mb-6">
      {/* Logo */}
      <div className="flex-shrink-0 w-16 h-16 rounded-2xl overflow-hidden 
                      border border-gray-100 shadow-md group-hover:scale-105
                      transition-transform duration-300">
        <img
          src={back}
          alt={job.entreprise}
          className="w-full h-full object-cover"
        />
      </div>

      {/* Title & Badge */}
      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-2 flex-wrap">
          <h3 className="text-xl font-bold text-gray-900 leading-snug group-hover:text-indigo-600 transition-colors">
            {job.title}
          </h3>

          <span
            className={`text-xs font-semibold px-3 py-1 rounded-full shadow-sm ${badgeClass}`}
          >
            {job.contractType}
          </span>
        </div>

        <p className="text-sm text-gray-500 mt-1 font-medium">
          Entreprise : {job.company.name}
        </p>
      </div>
    </div>

    {/* Info grid */}
    <div className="grid grid-cols-2 gap-x-0 gap-y-3 mb-6">
      <InfoRow icon={<MapPin className="w-6 h-6" />}>
        {job.location.city}, {job.location.postalCode}
      </InfoRow>

       {job.salary&& (
        <InfoRow icon={<DollarSign className="w-6 h-6" />}>
          {job.salary}
        </InfoRow>
      )}

      <InfoRow icon={<Clock className="w-6 h-6" />}>
        {job.hours}
      </InfoRow>

      {job.experience && (
        <InfoRow icon={<GraduationCap className="w-6 h-6" />}>
          {job.experience}
        </InfoRow>
      )}
    </div>

    {/* Divider */}
    <div className="border-t border-gray-100 mb-4" />

    {/* Footer */}
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-1 text-xs text-gray-400">
        <Calendar className="w-6 h-6" />
        <span>Posted {job.date_publication}</span>
      </div>


            <a href={job.url_origine}>
      <button
        onClick={handleApply}
        className="flex items-center gap-2 px-5 py-2 rounded-xl text-sm font-semibold
                   bg-gradient-to-r from-indigo-500 to-blue-600
                   text-white hover:from-indigo-600 hover:to-blue-700
                   active:scale-95 transition-all duration-200 shadow-md"
      >
        Voir l'offre
        <ArrowUpRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
      </button></a>
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