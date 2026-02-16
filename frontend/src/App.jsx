import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./components/Login";
import Register from "./components/Register";
import Welcome from "./components/Welcome";
import Accueil from "./components/Accueil";
import Offres from "./components/Offres";
import welcome from "./components/Welcome";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Accueil />} />
        <Route path="/Offres" element={<Offres />} />
        <Route path="/accueil" element={<Accueil />} />
        <Route path="/login" element={<Login />} />
        <Route path="/welcome"  element={<Welcome />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
