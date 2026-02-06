-- ============================================================================
-- Nous permet de peupler les tables
-- ============================================================================

-- Utilisateur admin (mot de passe: Admin123!)
INSERT INTO app.utilisateurs (email, nom, prenom, mdp_hash, est_admin)
VALUES (
    'admin@ensai.fr',
    'Admin',
    'System',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIYFR8N8yG',
    TRUE
);
