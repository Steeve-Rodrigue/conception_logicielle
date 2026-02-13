-- ============================================================================
-- Script d'initialisation - Table utilisateurs uniquement
-- ============================================================================

-- Supprimer le schéma s'il existe
DROP SCHEMA IF EXISTS app CASCADE;

-- Créer le schéma
CREATE SCHEMA app;


-- ============================================================================
-- TABLE UTILISATEURS
-- ============================================================================
CREATE TABLE app.utilisateurs (
    id_utilisateur SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    pseudo VARCHAR(100) UNIQUE NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    mdp_hash VARCHAR(255) NOT NULL,
    date_creation TIMESTAMP DEFAULT NOW(),
    date_derniere_connexion TIMESTAMP
);

-- Index pour optimiser la recherche par email et pseudo
CREATE INDEX idx_utilisateurs_email ON app.utilisateurs(email);
CREATE INDEX idx_utilisateurs_pseudo ON app.utilisateurs(pseudo);


CREATE TABLE app.candidate_profile (
    id_profil SERIAL PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    titre_professionnel VARCHAR(150) NOT NULL,
    annees_experience INT DEFAULT 0,
    date_disponibilite DATE NOT NULL,
    type_contrat_recherche VARCHAR(50),
    salaire_min_souhaite INT,
    cv_path VARCHAR(500),
    linkedin_url VARCHAR(255),
    date_maj TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_utilisateur)
        REFERENCES app.utilisateurs(id_utilisateur)
        ON DELETE CASCADE
);


CREATE TABLE app.user_skill (
    id_user_skill SERIAL PRIMARY KEY,
    id_profil INT NOT NULL,
    nom_competence VARCHAR(100) NOT NULL,
    niveau VARCHAR(50) NOT NULL,
    categorie VARCHAR(50) NOT NULL,

    FOREIGN KEY (id_profil)
        REFERENCES app.candidate_profile(id_profil)
        ON DELETE CASCADE
);

CREATE TABLE app.job_offer (
    id_offre SERIAL PRIMARY KEY,
    external_id VARCHAR(100) UNIQUE NOT NULL,
    titre VARCHAR(255) NOT NULL,
    entreprise VARCHAR(255) NOT NULL,
    description TEXT,
    localisation VARCHAR(255),
    type_contrat VARCHAR(50),
    salaire VARCHAR(100),
    competences_requises TEXT[],
    date_publication TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    url_origine VARCHAR(500),
    source VARCHAR(50) DEFAULT 'france_travail',
    est_active BOOLEAN DEFAULT TRUE,
    date_maj TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
