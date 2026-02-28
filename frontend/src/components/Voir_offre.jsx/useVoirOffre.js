import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import api from "../../api/api";

export const useVoirOffre = () => {
  const { id_offre } = useParams();
  const [offre, setOffre] = useState({
    id_offre: null,
    external_id: "",
    titre: "",
    entreprise: "",
    description: "",
    localisation: "",
    type_contrat: "",
    salaire: "",
    competences_requises: [],
    url_origine: "",
    date_publication: "",
    source: "",
    est_active: true,
  });

  useEffect(() => {
    const fetchOffre = async () => {
      try {
        const response = await api.get(`jobs/${id_offre}`);
        setOffre(response.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchOffre();
  }, [id_offre]);

  return { offre };
};
