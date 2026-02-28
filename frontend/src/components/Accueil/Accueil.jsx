import {
  Search,
  Menu,
  ArrowRight,
  Briefcase,
  Users,
  TrendingUp,
  Shield,
} from "lucide-react";
import { Link } from "react-router-dom";
import image1 from "../../assets/image.jpg";

function Accueil() {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-white/95 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <Search className="w-8 h-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">JOBPILOT</span>
            </div>

            <div className="flex items-center gap-4">
              <button className="px-6 py-2.5 text-gray-700 hover:text-blue-700 hover:underline transition-colors">
                <Link to="/login">Se connecter</Link>
              </button>
              <button className="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <Link to="/register">S'enregistrer</Link>
              </button>
              <button className="sm:hidden">
                <Menu className="w-6 h-6 text-gray-600" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section with Large Image */}
      <section className="relative min-h-[85vh] flex items-center">
        {/* Background Image */}
        <div className="absolute inset-0 z-0">
          <img
            src={image1}
            alt="Professional working"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-r from--white-400  via-blue-900/71 to-indigo-700"></div>
        </div>

        {/* Content */}
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/20 backdrop-blur-sm text-white rounded-full mb-6 border border-white/20">
              <TrendingUp className="w-4 h-4" />
              <span className="text-sm font-medium">
                {" "}
                Retrouve 1M+ de professionnels recherchant la carierre de leur
                rêve
              </span>
            </div>

            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight">
              Trouve l'emploi de tes rêves en quelques clics
            </h1>

            <p className="text-xl md:text-2xl text-blue-50 mb-10 leading-relaxed">
              Entrez en contact avec des milliers d'entreprises de premier plan
              et découvrez des opportunités qui correspondent à vos compétences
              et à vos passions. c'est entièrement gratuit!{" "}
            </p>

            <div className="flex flex-col sm:flex-row gap-4 mb-12">
              <button className="group px-8 py-4 bg-white text-blue-600 rounded-xl hover:bg-blue-50 transition-all hover:scale-105 shadow-xl font-medium text-lg inline-flex items-center justify-center gap-2">
                <Link to="/register">Creer un compte gratuitement</Link>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
            </div>

            <div className="flex flex-wrap items-center gap-6 text-white/90">
              <div className="flex items-center gap-2">
                <svg
                  className="w-5 h-5 text-green-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <span>Pas de carte de credit</span>
              </div>
              <div className="flex items-center gap-2">
                <svg
                  className="w-5 h-5 text-green-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <span>100% Gratuit</span>
              </div>
              <div className="flex items-center gap-2">
                <svg
                  className="w-5 h-5 text-green-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className=" border-gray-100 mt-8 pt-1 text-center text-gray-400 text-sm">
        <p>&copy; 2026 JOBPILOT. All rights reserved.</p>
      </footer>
    </div>
  );
}
export default Accueil;
