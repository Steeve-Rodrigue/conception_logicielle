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
    nom VARCHAR(100),
    prenom VARCHAR(100),
    mdp_hash VARCHAR(255) NOT NULL,
    est_admin BOOLEAN DEFAULT FALSE,
    date_creation TIMESTAMP DEFAULT NOW(),
    date_derniere_connexion TIMESTAMP
);

-- Index pour optimiser la recherche par email
CREATE INDEX idx_utilisateurs_email ON app.utilisateurs(email);

