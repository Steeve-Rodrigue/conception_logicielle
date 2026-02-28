import { useState, useEffect } from "react";
import api from "../../api/api";

export function useProfile() {
  //const [completion, /*setCompletion*/] = useState(0);
  const [profile, setProfile] = useState(null);
  const [editedProfile, setEditedProfile] = useState(null);
  const [isSkillEditing, setIsSkillEditing] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [toastMessage, setToastMessage] = useState("");
  const [skills, setSkills] = useState([]);
  const [newSkill, setNewSkill] = useState({
    nom_competence: "",
    niveau: "",
    categorie: "",
  });

  const data = editedProfile ?? profile;
  useEffect(() => {
    const fetchProfil = async () => {
      try {
        const response = await api.get("api/profiles/me");
        setProfile(response.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchProfil();
  }, []);

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        const response = await api.get("api/profiles/skill_list");
        setSkills(response.data.competences);
      } catch (err) {
        console.error(err);
      }
    };
    fetchSkills();
  }, []);

  // useEffect(() => {
  //   const fetchCompletion = async () => {
  //     try {
  //       const response = await api.get("api/profiles/completion");
  //       setCompletion(response.data.taux_completion);
  //     } catch (err) {
  //       console.error(err);
  //     }
  //   };
  //   fetchCompletion();
  // }, []);

  const update = (fields) => {
    setEditedProfile((prev) => ({ ...prev, ...fields }));
  };

  const handleSave = async () => {
    try {
      await api.put("api/profiles/update", editedProfile);
      setToastMessage("Profil mis à jour !");
      setProfile(editedProfile);
      setIsEditing(false);
    } catch (err) {
      console.error(err);
      setToastMessage("erreur lors de la sauvegarde du profil");
    }
  };

  const addSkill = async () => {
    if (!newSkill.nom_competence.trim()) return;
    try {
      await api.post("api/profiles/skills", newSkill);
      const response = await api.get("api/profiles/skill_list");
      setSkills(response.data.competences);
      setNewSkill({ nom_competence: "", niveau: "", categorie: "" });
      setToastMessage("Compétence ajoutée !");
    } catch (err) {
      console.error(err);
      setToastMessage("Erreur lors de l'ajout");
    }
  };

  const deleteSkill = async (id_user_skill) => {
    try {
      await api.delete(`api/profiles/skills/${id_user_skill}`);
      setSkills(skills.filter((s) => s.id_user_skill !== id_user_skill));
      setToastMessage("Compétence supprimée !");
    } catch (err) {
      console.error(err);
      setToastMessage("Erreur lors de la suppression");
    }
  };

  return {
    data,
    profile,
    //completion,
    isEditing,
    setIsEditing,
    editedProfile,
    setEditedProfile,
    newSkill,
    skills,
    setNewSkill,
    toastMessage,
    setToastMessage,
    update,
    handleSave,
    addSkill,
    deleteSkill,
    isSkillEditing,
    setIsSkillEditing,
  };
}
