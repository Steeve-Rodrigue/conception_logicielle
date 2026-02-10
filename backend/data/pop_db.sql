-- ============================================================================
-- Script de population des données
-- ============================================================================

-- Utilisateur admin (mot de passe: Admin123!)
INSERT INTO app.utilisateurs (email, pseudo, nom, prenom, mdp_hash)
VALUES (
    'admin@ensai.fr',
    'admin',
    'Admin',
    'System',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIYFR8N8yG'
);

-- Utilisateur test (mot de passe: Test123!)
INSERT INTO app.utilisateurs (email, pseudo, nom, prenom, mdp_hash)
VALUES (
    'test@ensai.fr',
    'test_user',
    'Test',
    'Utilisateur',
    '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi'
);