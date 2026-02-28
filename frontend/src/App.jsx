import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./components/Login/Login";
import Register from "./components/Register/Register";
import Accueil from "./components/Accueil/Accueil";
import Offres from "./components/Offres/Offres";
import Profile from "./components/Profile/Profile";
import VoirOffre from "./components/Voir_offre.jsx/VoirOffre";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Accueil />} />
        <Route path="/Offres" element={<Offres />} />
        <Route path="/Profile" element={<Profile />} />
        <Route path="/accueil" element={<Accueil />} />
        <Route path="/VoirOffre/:id_offre" element={<VoirOffre />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
