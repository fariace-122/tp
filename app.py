"""
DATA SENSE ANALYTICS v2.0
Application d'Analyse de Données - INF232 EC2
Thèmes : Login (Enfer) / Application (Cieux)
Prof. Rollin Francis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO, StringIO
import base64
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Machine Learning
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import (r2_score, mean_squared_error, mean_absolute_error,
                            accuracy_score, precision_score, recall_score, f1_score,
                            confusion_matrix, classification_report, silhouette_score)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Parsing de fichiers
import openpyxl
from PyPDF2 import PdfReader
from docx import Document
import csv

# Imports locaux
from utils.auth import initialize_session_state, login, logout, require_auth

# =============================================================================
# CONFIGURATION INITIALE
# =============================================================================

def load_css(file_path):
    """Charge un fichier CSS personnalisé"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # Ignorer si le fichier n'existe pas

# =============================================================================
# PAGE DE LOGIN - THÈME ENFER
# =============================================================================

def login_page():
    """Page de connexion avec thème de l'Enfer"""
    
    # Configuration de la page
    st.set_page_config(
        page_title="Data Sense Analytics - Login",
        page_icon="🔥",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Charger le CSS de l'Enfer
    load_css('assets/hellfire.css')
    
    # Initialisation session
    initialize_session_state()
    
    # Centrer le contenu
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Espace
        for _ in range(3):
            st.write("")
        
        # Logo et titre
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="font-size: 3.5rem; margin-bottom: 0;">⚡ DATA SENSE ⚡</h1>
            <h2 style="font-size: 2rem; margin-top: 0;">ANALYTICS</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Symbole démoniaque
        st.markdown("""
        <div class="login-decoration">
            🔥 👁️ 🔥<br>
            <span style="font-size: 20px;">Le Savoir à Tout Prix</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Formulaire de connexion
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "👤 NOM D'UTILISATEUR",
                placeholder="Votre âme...",
                key="login_username"
            )
            
            password = st.text_input(
                "🔑 MOT DE PASSE",
                type="password",
                placeholder="••••••••",
                key="login_password"
            )
            
            col_btn1, col_btn2 = st.columns([2, 1])
            
            with col_btn1:
                submitted = st.form_submit_button(
                    "SIGNER LE PACTE",
                    use_container_width=True
                )
            
            with col_btn2:
                st.markdown("""
                <div style="text-align: right; padding-top: 10px;">
                    <span style="color: #ff6666; font-size: 12px;">
                        Tentative: {}/5
                    </span>
                </div>
                """.format(st.session_state.login_attempts), unsafe_allow_html=True)
        
        if submitted:
            if username and password:
                with st.spinner("🔥 Invocation en cours..."):
                    time.sleep(1)
                    if login(username, password):
                        st.success("😈 Le pacte est scellé !")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        remaining = 5 - st.session_state.login_attempts
                        if remaining > 0:
                            st.error(f"❌ Accès refusé ! {remaining} tentatives restantes.")
                        else:
                            st.error("💀 COMPTE BLOQUÉ - Revenez dans 15 minutes")
            else:
                st.warning("⚠️ Invoquez votre nom et votre sceau !")
        
        # Pied de page
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #ff6666; font-size: 12px;">
            <p>© 2024 Data Sense Analytics - INF232 EC2</p>
            <p style="color: #ff4500;">"Le savoir est un pouvoir... à quel prix ?"</p>
            <br>
            <p style="font-size: 10px; opacity: 0.6;">
                Identifiants par défaut: admin / admin123
            </p>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# APPLICATION PRINCIPALE - THÈME CIEUX
# =============================================================================

@require_auth
def main_app():
    """Application principale avec thème des Cieux"""
    
    # Configuration de la page
    st.set_page_config(
        page_title="Data Sense Analytics",
        page_icon="☁️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Charger le CSS des Cieux
    load_css('assets/heaven.css')
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="color: #1e3c72; font-size: 2rem;">☁️ DATA SENSE</h1>
            <h3 style="color: #2a5298;">ANALYTICS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Info utilisateur
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.8); padding: 10px; border-radius: 10px;">
            <p>👤 <strong>{st.session_state.username}</strong></p>
            <p>🎭 <strong>{st.session_state.role}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Upload de fichier
        st.markdown("### 📂 Importation Divine")
        
        uploaded_file = st.file_uploader(
            "Déposez votre fichier de données",
            type=['csv', 'xlsx', 'xls', 'pdf', 'docx', 'txt'],
            help="Formats supportés : CSV, Excel, PDF, Word, TXT"
        )
        
        # Déconnexion
        st.markdown("---")
        if st.button("🚪 Quitter le Paradis", use_container_width=True):
            logout()
            st.rerun()
        
        # Pied de sidebar
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; font-size: 0.8rem; color: #2c3e50;">
            <p>🎓 INF232 EC2</p>
            <p>Prof. Rollin Francis</p>
            <p style="color: #87ceeb;">✨ Thème Céleste ✨</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Contenu principal
    if uploaded_file is None:
        welcome_page()
    else:
        df = load_data(uploaded_file)
        if df is not None:
            st.session_state.current_df = df
            display_analysis_dashboard(df)

def welcome_page():
    """Page d'accueil céleste"""
    
    st.markdown("""
    <div style="text-align: center; padding: 50px 0;">
        <h1 style="font-size: 4rem;">☁️ Bienvenue au Paradis des Données ☁️</h1>
        <p style="font-size: 1.5rem; color: #2c3e50;">Votre voyage analytique commence ici</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cartes de fonctionnalités
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.9); padding: 30px; border-radius: 20px; text-align: center;">
            <h2>📊 Analyse Univariée</h2>
            <p>Statistiques descriptives, distributions, boxplots et plus encore</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.9); padding: 30px; border-radius: 20px; text-align: center;">
            <h2>🔗 Analyse Bivariée</h2>
            <p>Corrélations, relations entre variables, matrices de corrélation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.9); padding: 30px; border-radius: 20px; text-align: center;">
            <h2>🤖 Machine Learning</h2>
            <p>Régression, Classification, Clustering, ACP</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Démo des données
    st.markdown("---")
    st.markdown("### 📈 Aperçu Rapide")
    
    # Générer des données de démonstration
    np.random.seed(42)
    demo_data = pd.DataFrame({
        'Age': np.random.randint(20, 60, 100),
        'Salaire': np.random.randint(30000, 120000, 100),
        'Expérience': np.random.randint(1, 30, 100),
        'Satisfaction': np.random.randint(1, 10, 100)
    })
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.dataframe(demo_data.head(10), use_container_width=True)
    
    with col_b:
        fig = px.scatter(
            demo_data, x='Expérience', y='Salaire',
            title="Exemple : Expérience vs Salaire",
            trendline="ols",
            color_discrete_sequence=['#87ceeb']
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

def load_data(uploaded_file):
    """Charge les données depuis différents formats"""
    try:
        file_name = uploaded_file.name
        file_ext = file_name.split('.')[-1].lower()
        
        with st.spinner("📤 Chargement des données célestes..."):
            if file_ext == 'csv':
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            elif file_ext in ['xlsx', 'xls']:
                df = pd.read_excel(uploaded_file)
            elif file_ext == 'pdf':
                reader = PdfReader(uploaded_file)
                text = "\n".join([page.extract_text() for page in reader.pages])
                df = pd.DataFrame({'Contenu': [text]})
                st.info("📄 Contenu PDF extrait. Traitement limité.")
            elif file_ext == 'docx':
                doc = Document(uploaded_file)
                text = "\n".join([para.text for para in doc.paragraphs])
                df = pd.DataFrame({'Contenu': [text]})
                st.info("📄 Contenu Word extrait. Traitement limité.")
            elif file_ext == 'txt':
                text = uploaded_file.read().decode('utf-8')
                df = pd.DataFrame({'Contenu': [text]})
            else:
                st.error(f"Format non supporté : {file_ext}")
                return None
        
        st.success(f"✅ Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
        return df
    
    except Exception as e:
        st.error(f"❌ Erreur de chargement : {str(e)}")
        return None

def display_analysis_dashboard(df):
    """Affiche le tableau de bord d'analyse"""
    
    # En-tête
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>📊 Tableau de Bord Analytique</h1>
        <p style="color: #2c3e50;">Explorez, Visualisez, Comprenez</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métriques rapides
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Lignes", f"{df.shape[0]:,}")
    with col2:
        st.metric("📊 Colonnes", df.shape[1])
    with col3:
        st.metric("🔢 Numériques", len(df.select_dtypes(include=[np.number]).columns))
    with col4:
        st.metric("📝 Catégorielles", len(df.select_dtypes(include=['object']).columns))
    
    # Aperçu des données
    with st.expander("🔍 Aperçu des Données", expanded=True):
        st.dataframe(df.head(15), use_container_width=True)
        
        # Info sur les types
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**📊 Types de données :**")
            st.write(df.dtypes.value_counts())
        with col_b:
            st.markdown("**⚠️ Valeurs manquantes :**")
            missing = df.isnull().sum()
            missing = missing[missing > 0]
            if len(missing) > 0:
                st.write(missing)
            else:
                st.success("Aucune valeur manquante !")
    
    # Onglets d'analyse
    tabs = st.tabs([
        "📊 Univariée",
        "🔗 Bivariée",
        "📐 Régression",
        "🔽 ACP",
        "🎯 Classification",
        "🔮 Clustering"
    ])
    
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Onglet Univarié
    with tabs[0]:
        univariate_analysis(df, num_cols)
    
    # Onglet Bivarié
    with tabs[1]:
        bivariate_analysis(df, num_cols, cat_cols)
    
    # Onglet Régression
    with tabs[2]:
        regression_analysis(df, num_cols)
    
    # Onglet ACP
    with tabs[3]:
        pca_analysis(df, num_cols)
    
    # Onglet Classification
    with tabs[4]:
        classification_analysis(df, num_cols, cat_cols)
    
    # Onglet Clustering
    with tabs[5]:
        clustering_analysis(df, num_cols)

def univariate_analysis(df, num_cols):
    """Analyse univariée"""
    st.markdown("### 📊 Analyse Univariée")
    
    if not num_cols:
        st.warning("Aucune colonne numérique disponible.")
        return
    
    col_to_analyze = st.selectbox("Choisir une variable", num_cols)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Statistiques
        st.markdown("#### 📈 Statistiques Descriptives")
        
        stats = {
            'Effectif': len(df[col_to_analyze].dropna()),
            'Moyenne': df[col_to_analyze].mean(),
            'Médiane': df[col_to_analyze].median(),
            'Écart-type': df[col_to_analyze].std(),
            'Minimum': df[col_to_analyze].min(),
            'Maximum': df[col_to_analyze].max(),
            'Q1': df[col_to_analyze].quantile(0.25),
            'Q3': df[col_to_analyze].quantile(0.75),
            'Asymétrie': df[col_to_analyze].skew(),
            'Kurtosis': df[col_to_analyze].kurtosis()
        }
        
        stats_df = pd.DataFrame({
            'Statistique': list(stats.keys()),
            'Valeur': [f"{v:.3f}" if isinstance(v, float) else str(v) for v in stats.values()]
        })
        
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        # Métriques en cartes
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Moyenne", f"{df[col_to_analyze].mean():.2f}")
        with c2:
            st.metric("Médiane", f"{df[col_to_analyze].median():.2f}")
        with c3:
            st.metric("Écart-type", f"{df[col_to_analyze].std():.2f}")
    
    with col2:
        # Histogramme
        fig = px.histogram(
            df, x=col_to_analyze,
            nbins=30,
            title=f"Distribution de {col_to_analyze}",
            color_discrete_sequence=['#87ceeb'],
            marginal="box"
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    
    # Boxplot
    fig_box = px.box(
        df, y=col_to_analyze,
        title=f"Boîte à Moustaches - {col_to_analyze}",
        color_discrete_sequence=['#ffd700']
    )
    fig_box.update_layout(template="plotly_white")
    st.plotly_chart(fig_box, use_container_width=True)

def bivariate_analysis(df, num_cols, cat_cols):
    """Analyse bivariée"""
    st.markdown("### 🔗 Analyse Bivariée")
    
    subtab1, subtab2, subtab3 = st.tabs([
        "Numérique vs Numérique",
        "Numérique vs Catégoriel",
        "Matrice de Corrélation"
    ])
    
    with subtab1:
        if len(num_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_var = st.selectbox("Variable X", num_cols, key="x_bivar")
            with col2:
                y_var = st.selectbox("Variable Y", num_cols, key="y_bivar", 
                                    index=min(1, len(num_cols)-1))
            
            # Nuage de points avec régression
            fig = px.scatter(
                df, x=x_var, y=y_var,
                title=f"{x_var} vs {y_var}",
                trendline="ols",
                color_discrete_sequence=['#87ceeb']
            )
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
            # Coefficient de corrélation
            corr = df[x_var].corr(df[y_var])
            st.info(f"📊 Coefficient de corrélation de Pearson : **{corr:.4f}**")
            
            # Interprétation
            if abs(corr) > 0.7:
                st.success("✅ Forte corrélation")
            elif abs(corr) > 0.3:
                st.warning("⚠️ Corrélation modérée")
            else:
                st.info("ℹ️ Faible corrélation")
        else:
            st.info("Besoin d'au moins 2 colonnes numériques.")
    
    with subtab2:
        if num_cols and cat_cols:
            num_var = st.selectbox("Variable Numérique", num_cols, key="num_cat")
            cat_var = st.selectbox("Variable Catégorielle", cat_cols, key="cat_var")
            
            # Boxplot par catégorie
            fig = px.box(
                df, x=cat_var, y=num_var,
                title=f"{num_var} par {cat_var}",
                color=cat_var,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
            # Violin plot
            fig_violin = px.violin(
                df, x=cat_var, y=num_var,
                title=f"Distribution de {num_var} par {cat_var}",
                color=cat_var,
                box=True,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_violin.update_layout(template="plotly_white")
            st.plotly_chart(fig_violin, use_container_width=True)
        else:
            st.info("Besoin de colonnes numériques ET catégorielles.")
    
    with subtab3:
        if len(num_cols) >= 2:
            corr_matrix = df[num_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto='.2f',
                color_continuous_scale='RdBu_r',
                title="Matrice de Corrélation",
                zmin=-1, zmax=1
            )
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Besoin d'au moins 2 colonnes numériques.")

def regression_analysis(df, num_cols):
    """Analyse de régression"""
    st.markdown("### 📐 Analyse de Régression")
    
    reg_type = st.radio(
        "Type de régression",
        ["Régression Simple", "Régression Multiple"],
        horizontal=True
    )
    
    if reg_type == "Régression Simple":
        if len(num_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_var = st.selectbox("Variable explicative (X)", num_cols, key="x_reg")
            with col2:
                y_var = st.selectbox("Variable cible (Y)", num_cols, key="y_reg",
                                    index=min(1, len(num_cols)-1))
            
            # Modèle
            X = df[x_var].values.reshape(-1, 1)
            y = df[y_var].values
            
            # Supprimer les NaN
            mask = ~(np.isnan(X.flatten()) | np.isnan(y))
            X = X[mask]
            y = y[mask]
            
            if len(X) > 1:
                model = LinearRegression()
                model.fit(X, y)
                y_pred = model.predict(X)
                
                # Métriques
                r2 = r2_score(y, y_pred)
                mse = mean_squared_error(y, y_pred)
                mae = mean_absolute_error(y, y_pred)
                
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("R²", f"{r2:.4f}")
                with col_m2:
                    st.metric("MSE", f"{mse:.4f}")
                with col_m3:
                    st.metric("MAE", f"{mae:.4f}")
                
                st.info(f"📐 Équation : Y = {model.intercept_:.3f} + {model.coef_[0]:.3f} × X")
                
                # Graphique
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=X.flatten(), y=y, mode='markers',
                    name='Données',
                    marker=dict(color='#87ceeb', size=8)
                ))
                fig.add_trace(go.Scatter(
                    x=X.flatten(), y=y_pred, mode='lines',
                    name='Régression',
                    line=dict(color='#ffd700', width=3)
                ))
                fig.update_layout(
                    title=f"Régression : {y_var} = f({x_var})",
                    xaxis_title=x_var,
                    yaxis_title=y_var,
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Pas assez de données valides.")
        else:
            st.warning("Besoin d'au moins 2 colonnes numériques.")
    
    else:  # Régression Multiple
        if len(num_cols) >= 3:
            y_var = st.selectbox("Variable cible (Y)", num_cols, key="y_multi")
            x_vars = st.multiselect(
                "Variables explicatives (X)",
                [col for col in num_cols if col != y_var],
                default=[col for col in num_cols if col != y_var][:min(3, len(num_cols)-1)]
            )
            
            if x_vars:
                X = df[x_vars].dropna()
                y = df.loc[X.index, y_var]
                
                if len(X) > len(x_vars):
                    # Standardisation
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)
                    
                    model = LinearRegression()
                    model.fit(X_scaled, y)
                    y_pred = model.predict(X_scaled)
                    
                    r2 = r2_score(y, y_pred)
                    adj_r2 = 1 - (1-r2)*(len(y)-1)/(len(y)-len(x_vars)-1)
                    
                    st.metric("R² Ajusté", f"{adj_r2:.4f}")
                    
                    # Coefficients
                    coef_df = pd.DataFrame({
                        'Variable': ['Constante'] + x_vars,
                        'Coefficient': [model.intercept_] + list(model.coef_)
                    })
                    st.dataframe(coef_df, use_container_width=True)
                    
                    # Prédit vs Observé
                    fig = px.scatter(
                        x=y, y=y_pred,
                        labels={'x': 'Observé', 'y': 'Prédit'},
                        title="Valeurs Observées vs Prédites",
                        color_discrete_sequence=['#87ceeb']
                    )
                    fig.add_trace(go.Scatter(
                        x=[y.min(), y.max()],
                        y=[y.min(), y.max()],
                        mode='lines',
                        name='Parfait',
                        line=dict(color='#ffd700', dash='dash')
                    ))
                    fig.update_layout(template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Pas assez de données pour la régression multiple.")
        else:
            st.warning("Besoin d'au moins 3 colonnes numériques.")

def pca_analysis(df, num_cols):
    """Analyse en Composantes Principales"""
    st.markdown("### 🔽 Analyse en Composantes Principales (ACP)")
    
    if len(num_cols) >= 3:
        n_components = st.slider("Nombre de composantes", 2, min(5, len(num_cols)), 2)
        
        # Préparation
        X = df[num_cols].dropna()
        
        if len(X) > n_components:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            pca = PCA(n_components=n_components)
            X_pca = pca.fit_transform(X_scaled)
            
            # Variance expliquée
            exp_var = pca.explained_variance_ratio_
            cum_var = np.cumsum(exp_var)
            
            # Graphique
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[f'PC{i+1}' for i in range(n_components)],
                y=exp_var,
                name='Variance expliquée',
                marker_color='#87ceeb'
            ))
            fig.add_trace(go.Scatter(
                x=[f'PC{i+1}' for i in range(n_components)],
                y=cum_var,
                name='Variance cumulée',
                mode='lines+markers',
                line=dict(color='#ffd700', width=3)
            ))
            fig.update_layout(
                title="Variance Expliquée par Composante",
                template="plotly_white",
                yaxis_title="Proportion"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Projection 2D
            pca_df = pd.DataFrame(X_pca[:, :2], columns=['PC1', 'PC2'])
            
            fig_proj = px.scatter(
                pca_df, x='PC1', y='PC2',
                title="Projection sur PC1 et PC2",
                color_discrete_sequence=['#87ceeb'],
                opacity=0.7
            )
            fig_proj.update_layout(template="plotly_white")
            st.plotly_chart(fig_proj, use_container_width=True)
            
            # Loadings
            loadings = pd.DataFrame(
                pca.components_.T,
                columns=[f'PC{i+1}' for i in range(n_components)],
                index=num_cols
            )
            
            st.markdown("#### 📊 Contributions des Variables")
            fig_load = px.imshow(
                loadings,
                text_auto='.2f',
                color_continuous_scale='RdBu_r',
                title="Matrice de Chargement",
                zmin=-1, zmax=1
            )
            fig_load.update_layout(template="plotly_white")
            st.plotly_chart(fig_load, use_container_width=True)
        else:
            st.warning("Pas assez de données complètes pour l'ACP.")
    else:
        st.warning("Besoin d'au moins 3 colonnes numériques.")

def classification_analysis(df, num_cols, cat_cols):
    """Classification supervisée"""
    st.markdown("### 🎯 Classification Supervisée")
    
    if cat_cols and num_cols:
        target = st.selectbox("Variable cible (catégorielle)", cat_cols, key="target_clf")
        features = st.multiselect(
            "Variables prédictives",
            num_cols,
            default=num_cols[:min(3, len(num_cols))]
        )
        
        if features:
            # Préparation
            df_clean = df[features + [target]].dropna()
            
            if len(df_clean) > 20:
                X = df_clean[features].values
                
                le = LabelEncoder()
                y = le.fit_transform(df_clean[target])
                
                # Split
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.3, random_state=42, stratify=y if len(np.unique(y)) > 1 else None
                )
                
                # Standardisation
                scaler = StandardScaler()
                X_train = scaler.fit_transform(X_train)
                X_test = scaler.transform(X_test)
                
                # Choix du modèle
                model_type = st.selectbox(
                    "Algorithme",
                    ["Régression Logistique", "KNN", "Arbre de Décision", "Forêt Aléatoire"]
                )
                
                if model_type == "Régression Logistique":
                    model = LogisticRegression(max_iter=1000, random_state=42)
                elif model_type == "KNN":
                    k = st.slider("Nombre de voisins (K)", 1, 15, 5)
                    model = KNeighborsClassifier(n_neighbors=k)
                elif model_type == "Arbre de Décision":
                    model = DecisionTreeClassifier(random_state=42, max_depth=5)
                else:
                    model = RandomForestClassifier(random_state=42, n_estimators=100)
                
                # Entraînement
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                
                # Métriques
                accuracy = accuracy_score(y_test, y_pred)
                
                st.success(f"🎯 Précision : **{accuracy:.2%}**")
                
                # Matrice de confusion
                cm = confusion_matrix(y_test, y_pred)
                
                fig = px.imshow(
                    cm,
                    text_auto=True,
                    labels=dict(x="Prédit", y="Réel"),
                    x=le.classes_,
                    y=le.classes_,
                    color_continuous_scale='Blues',
                    title="Matrice de Confusion"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Rapport détaillé
                if len(np.unique(y)) <= 10:
                    st.markdown("#### 📋 Rapport de Classification")
                    report = classification_report(y_test, y_pred, 
                                                  target_names=le.classes_.astype(str),
                                                  output_dict=True)
                    st.dataframe(pd.DataFrame(report).transpose())
            else:
                st.warning("Pas assez de données pour la classification.")
    else:
        st.warning("Besoin de colonnes numériques ET catégorielles.")

def clustering_analysis(df, num_cols):
    """Clustering non-supervisé"""
    st.markdown("### 🔮 Clustering - K-Means")
    
    if len(num_cols) >= 2:
        features = st.multiselect(
            "Variables pour le clustering",
            num_cols,
            default=num_cols[:min(3, len(num_cols))]
        )
        
        if len(features) >= 2:
            n_clusters = st.slider("Nombre de clusters (K)", 2, 8, 3)
            
            # Préparation
            X = df[features].dropna()
            
            if len(X) > n_clusters:
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                
                # K-Means
                kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                clusters = kmeans.fit_predict(X_scaled)
                
                # Résultats
                df_clustered = X.copy()
                df_clustered['Cluster'] = clusters
                
                # Visualisation
                if len(features) >= 3:
                    fig = px.scatter_3d(
                        df_clustered,
                        x=features[0],
                        y=features[1],
                        z=features[2],
                        color='Cluster',
                        title="Clustering K-Means (3D)",
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig = px.scatter(
                        df_clustered,
                        x=features[0],
                        y=features[1],
                        color='Cluster',
                        title="Clustering K-Means (2D)",
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Statistiques par cluster
                st.markdown("#### 📊 Statistiques par Cluster")
                cluster_stats = df_clustered.groupby('Cluster')[features].mean()
                cluster_stats['Effectif'] = df_clustered.groupby('Cluster').size()
                st.dataframe(cluster_stats, use_container_width=True)
                
                # Méthode du coude
                st.markdown("#### 📐 Méthode du Coude")
                inertias = []
                K_range = range(1, min(11, len(X)))
                
                for k in K_range:
                    km = KMeans(n_clusters=k, random_state=42, n_init=10)
                    km.fit(X_scaled)
                    inertias.append(km.inertia_)
                
                fig_elbow = px.line(
                    x=list(K_range), y=inertias,
                    markers=True,
                    title="Évolution de l'Inertie",
                    labels={'x': 'K', 'y': 'Inertie'}
                )
                fig_elbow.update_traces(line_color='#87ceeb', marker_color='#ffd700')
                fig_elbow.update_layout(template="plotly_white")
                st.plotly_chart(fig_elbow, use_container_width=True)
                
                # Score de silhouette
                if n_clusters > 1:
                    sil_score = silhouette_score(X_scaled, clusters)
                    st.info(f"📊 Score de silhouette : **{sil_score:.4f}**")
            else:
                st.warning("Pas assez de données pour le clustering.")
    else:
        st.warning("Besoin d'au moins 2 colonnes numériques.")

# =============================================================================
# POINT D'ENTRÉE PRINCIPAL
# =============================================================================

def main():
    """Fonction principale"""
    
    initialize_session_state()
    
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()