"""
Module d'authentification - Data Sense Analytics
Gestion des sessions et vérification des identifiants
"""

import streamlit as st
import yaml
import hashlib
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

def load_config() -> Dict[str, Any]:
    """Charge la configuration depuis config.yaml"""
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # Configuration par défaut
        return {
            'users': [
                {'username': 'admin', 'password': 'admin123', 'role': 'administrator'}
            ]
        }

def hash_password(password: str) -> str:
    """Hash un mot de passe avec SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_credentials(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Vérifie les identifiants de connexion"""
    config = load_config()
    
    for user in config.get('users', []):
        if user['username'] == username:
            # Vérification simple (sans hash pour la démo)
            if user['password'] == password:
                return user
    
    return None

def initialize_session_state():
    """Initialise les variables de session"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.login_time = None
        st.session_state.login_attempts = 0
        st.session_state.last_attempt_time = None

def check_session_timeout():
    """Vérifie si la session a expiré"""
    if st.session_state.authenticated and st.session_state.login_time:
        config = load_config()
        timeout = config.get('session', {}).get('timeout_minutes', 60)
        
        elapsed = time.time() - st.session_state.login_time
        if elapsed > timeout * 60:
            logout()
            return True
    return False

def login(username: str, password: str) -> bool:
    """Tente de connecter l'utilisateur"""
    # Vérifier le nombre de tentatives
    config = load_config()
    max_attempts = config.get('session', {}).get('max_attempts', 5)
    lockout = config.get('session', {}).get('lockout_minutes', 15)
    
    if st.session_state.login_attempts >= max_attempts:
        if st.session_state.last_attempt_time:
            elapsed = time.time() - st.session_state.last_attempt_time
            if elapsed < lockout * 60:
                st.error(f"⛔ Compte bloqué. Réessayez dans {int(lockout - elapsed/60)} minutes.")
                return False
    
    # Vérifier les identifiants
    user = verify_credentials(username, password)
    
    if user:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.role = user.get('role', 'user')
        st.session_state.login_time = time.time()
        st.session_state.login_attempts = 0
        return True
    else:
        st.session_state.login_attempts += 1
        st.session_state.last_attempt_time = time.time()
        return False

def logout():
    """Déconnecte l'utilisateur"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.login_time = None
    st.rerun()

def require_auth(func):
    """Décorateur pour protéger les pages nécessitant une authentification"""
    def wrapper(*args, **kwargs):
        initialize_session_state()
        
        if not st.session_state.authenticated:
            st.error("🔒 Veuillez vous connecter pour accéder à cette page.")
            st.stop()
        
        if check_session_timeout():
            st.error("⏰ Session expirée. Veuillez vous reconnecter.")
            st.stop()
        
        return func(*args, **kwargs)
    return wrapper