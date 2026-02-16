import { Search, Menu, ArrowRight, Briefcase, Users, TrendingUp, Shield } from "lucide-react";
import { useNavigate , Link } from "react-router-dom";
import { useState, useEffect, use } from "react";
import Job_card from "./Job_card";
import api from "../api/api";

function Offres() {

  const [job, setJobs] = useState([]);

  useEffect(() => {
    // appel à l'API pour récupérer les offres d'emploi
  const fetchJobs = async () => {
    try {
      const response = await api.get("/jobs");
      setJobs(response.data.results); // Assurez-vous que la structure de la réponse correspond à vos attentes
    } catch (error) {
      console.error("Erreur lors de la récupération des offres d'emploi :", error);
    }
  };    
    fetchJobs();
  }, []);


    const sampleJobs = [
      {
        id: '1',
        title: 'Senior Frontend Developer',
        company: {
          name: 'TechCorp Solutions',
          logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
        },
        location: {
          city: 'San Francisco',
          postalCode: '94102',
        },
        contractType: 'Full-time',
        hours: '40h/week',
        salary: '$120,000 - $160,000/year',
        experience: '5+ years',
        education: "Bachelor's Degree",
        datePosted: '2 days ago',
      }
    ];

    const [user, setUser] = useState(null);
    useEffect(() => {
    const storedUser = localStorage.getItem("utilisateur");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    }, []);

  return (
<div className="flex-col bg-white  px-4 sm:px-1 md:px-8 lg:px-1 py-6 sm:py-10 lg:py-5">

      {/* Header */}
      <header className="bg-white/9 backdrop-blur-sm   ">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <Search className="w-8 h-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">JOBPILOT</span>
            </div>
            
            <div className="flex items-center gap-5">
                <Link to="/accueil" className="px-6 py-2.5 text-gray-700 hover:text-blue-700 hover:underline transition-colors">Accueil</Link>
                <Link to="/Offres" className="px-6 py-2.5 text-gray-700 hover:text-blue-700 hover:underline transition-colors">Offres d'emploi</Link>
                <Link to="/register" className="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">Consulter son profil</Link>
             
            </div>
          </div>
        </div>
      </header>
        <div className="min-h-screen bg-gray-90">
        {/* Hero Section */}
        {user && (
            <div className="bg-gradient-to-r from-white-100  via-indigo-300  to-white py-1">
            <div className="max-w-7xl mx-auto px-6 py-8 text-center sm:text-left" >
                <h1 className="text-4xl font-bold text-gray-900">
                👋 Bonjour, <span className="text-blue-600">{user.prenom}</span> 
                </h1>
                <p className="mt-3 text-gray-700 text-lg">
                Découvrez les meilleures opportunités adaptées à votre profil.
                </p>
            </div>
            </div>
        )}

        {/* Jobs Section */}
        <section className=" max-w-8xl mx-auto px-40 py-12  ">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-2">
            <h2 className="text-3xl font-bold text-gray-900">Positions Disponibles</h2>
            <span className="text-gray-500 text-sm sm:text-base">{job.length} offres trouvées</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {job.map((job) => (
            <Job_card key={job.id} job={job} />
            ))}
        </div>
        </section>    
    </div>

    {/* Footer */}
        <footer className="mt-auto bg-gray-50 border-t border-gray-200 text-center py-6 text-gray-500 text-sm">
        &copy; 2026 JOBPILOT. Tous droits réservés.
        </footer>

    </div>
  );
}
export default Offres;  