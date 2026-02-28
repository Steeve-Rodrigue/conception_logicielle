import React, { useEffect } from "react";

/* =========================================================
   BUTTON
========================================================= */
export const Button = ({
  children,
  onClick,
  type = "button",
  variant = "primary",
  size = "md",
  className = "",
  disabled = false,
}) => {
  const base =
    "rounded-lg font-medium transition flex items-center justify-center";

  const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700",
    outline: "border border-gray-300 hover:bg-gray-100",
    danger: "bg-red-600 text-white hover:bg-red-700",
  };

  const sizes = {
    sm: "text-sm px-3 py-1.5",
    md: "text-sm px-4 py-2",
    lg: "text-base px-6 py-3",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${base} ${variants[variant]} ${sizes[size]} ${className} ${
        disabled ? "opacity-50 cursor-not-allowed" : ""
      }`}
    >
      {children}
    </button>
  );
};

/* =========================================================
   INPUT
========================================================= */
export const Input = ({ className = "", ...props }) => {
  return (
    <input
      {...props}
      className={`w-full border border-gray-300 rounded-lg px-3 py-2 text-sm 
      focus:outline-none focus:ring-2 focus:ring-blue-500 
      ${className}`}
    />
  );
};

const Field = ({ label, children }) => (
  <div className="space-y-1.5">
    <Label>{label}</Label>
    {children}
  </div>
);
/* =========================================================
   LABEL
========================================================= */
export const Label = ({ children, className = "", ...props }) => {
  return (
    <label
      {...props}
      className={`text-sm font-medium text-gray-700 ${className}`}
    >
      {children}
    </label>
  );
};

/* =========================================================
   BADGE
========================================================= */
export const Badge = ({ children, className = "" }) => {
  return (
    <div
      className={`inline-flex items-center bg-purple-600 text-white 
      px-4 py-1.5 text-sm rounded-full ${className}`}
    >
      {children}
    </div>
  );
};

/* =========================================================
   TOAST
========================================================= */
export const Toast = ({ message, duration = 2500, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      if (onClose) onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  return (
    <div
      className="fixed top-5 right-5 bg-black text-white 
      px-5 py-3 rounded-xl shadow-lg z-50"
    >
      {message}
    </div>
  );
};
