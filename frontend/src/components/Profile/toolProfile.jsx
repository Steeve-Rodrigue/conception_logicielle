export const SectionTitle = ({ title }) => (
  <div className="flex items-center gap-3 mb-6">
    <div className="w-9 h-9 rounded-xl bg-blue-50 flex items-center justify-center"></div>
    <h2 className="text-lg font-semibold text-blue-600 tracking-wide uppercase">
      {title}
    </h2>
    <div className="flex-1 h-px bg-gray-100" />
  </div>
);

export const Field = ({ label, children }) => (
  <div className="flex flex-col gap-1.5">
    <label className="text-xs font-semibold text-gray-400 uppercase tracking-widest">
      {label}
    </label>
    {children}
  </div>
);

export const StyledInput = ({ disabled, ...props }) => (
  <input
    disabled={disabled}
    {...props}
    className={`w-full px-4 py-1 rounded-xl text-sm font-medium transition-all outline-none border
      ${
        disabled
          ? "bg-gray-50 text-gray-700 border-transparent cursor-default"
          : "bg-white border-blue-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 text-gray-800 shadow-sm"
      } ${props.className ?? ""}`}
  />
);
// export const CompletionChart = ({ completion }) => (
//   <div className="flex flex-col items-center gap-2">
//     <div className="relative w-20 h-20">
//       <svg className="w-20 h-20 -rotate-90" viewBox="0 0 36 36">
//         <circle cx="18" cy="18" r="15.9" fill="none" stroke="#e0e7ff" strokeWidth="3" />
//         <circle
//           cx="18" cy="18" r="15.9" fill="none"
//           stroke="url(#grad)" strokeWidth="3"
//           strokeDasharray={`${completion} ${100 - completion}`}
//           strokeLinecap="round"
//         />
//         <defs>
//           <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
//             <stop offset="0%" stopColor="#6366f1" />
//             <stop offset="100%" stopColor="#3b82f6" />
//           </linearGradient>
//         </defs>
//       </svg>
//       <span className="absolute inset-0 flex items-center justify-center text-lg font-bold text-indigo-600">
//         {completion}%
//       </span>
//     </div>
//     <p className="text-xs text-gray-500 font-medium">Profil complété</p>
//   </div>
// );
