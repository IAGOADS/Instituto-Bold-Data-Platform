# utils/metrics.py
import pandas as pd
import numpy as np

def calculate_kpis(df):
    """Calculates general KPIs for the dashboard"""
    if df is None or df.empty:
        return {
            "total_inscritos": 0, "total_aprovados": 0, "total_reprovados": 0,
            "taxa_aprovacao": 0, "cidades_impactadas": 0, "estados_impactados": 0
        }
        
    total_inscritos = len(df)
    
    # Normalização preventiva do status
    status_sert = df["status"].astype(str).str.strip().str.lower()
    total_aprovados = (status_sert == "aprovado").sum()
    total_reprovados = (status_sert == "reprovado").sum()
    
    taxa_aprovacao = (total_aprovados / total_inscritos) * 100 if total_inscritos > 0 else 0
    
    cidades_impactadas = df["cidade"].nunique() if "cidade" in df.columns else 0
    estados_impactados = df["estado"].nunique() if "estado" in df.columns else 0
    
    return {
        "total_inscritos": total_inscritos,
        "total_aprovados": total_aprovados,
        "total_reprovados": total_reprovados,
        "taxa_aprovacao": taxa_aprovacao,
        "cidades_impactadas": cidades_impactadas, # CORRIGIDO: de cities_impactadas para cidades_impactadas
        "estados_impactados": estados_impactados
    }

def calculate_inclusion_index(df):
    """Calculates the Inclusion Index using flexible string contains."""
    if df is None or df.empty:
        return 0.0
        
    cond_mulher = df["genero"].astype(str).str.lower().str.contains("fem", na=False)
    cond_raca = df["grupo_etnico"].astype(str).str.lower().str.contains("preta|parda|indí", na=False)
    cond_renda = df["renda_familiar"].astype(str).str.lower().str.contains("até 1|1 a 2|baixo|mínimo", na=False)
    cond_pcd = df["pcd"].astype(str).str.lower().str.contains("sim", na=False)
    
    inclusion_union = cond_mulher | cond_raca | cond_renda | cond_pcd
    return (inclusion_union.sum() / len(df)) * 100

def calculate_vulnerability_index(df):
    """Calculates the Social Vulnerability Index with real dataset string safety."""
    if df is None or df.empty:
        return 0.0
        
    crit_renda = df["renda_familiar"].astype(str).str.lower().str.contains("até 1|1 a 2|baixo|mínimo", na=False).astype(int)
    crit_emprego = df["empregabilidade"].astype(str).str.lower().str.contains("desemp|autôn", na=False).astype(int)
    crit_escola = df["escolaridade"].astype(str).str.lower().str.contains("médio|incompleto", na=False).astype(int)
    
    vulnerability_score = crit_renda + crit_emprego + crit_escola
    vulnerable_participants = vulnerability_score >= 2
    return (vulnerable_participants.sum() / len(df)) * 100

def calculate_transformation_potential(df):
    """Calculates the Potential of Social Transformation with flexible strings."""
    if df is None or df.empty:
        return 0.0
        
    cond_desemprego = df["empregabilidade"].astype(str).str.lower().str.contains("desemp", na=False)
    cond_sem_exp = df["tempo_experiencia"].astype(str).str.lower().str.contains("sem exp|não tenho", na=False)
    cond_baixa_renda = df["renda_familiar"].astype(str).str.lower().str.contains("até 1|1 a 2|baixo|mínimo", na=False)
    cond_baixa_escola = df["escolaridade"].astype(str).str.lower().str.contains("médio|incompleto", na=False)
    
    transformation_union = cond_desemprego | cond_sem_exp | cond_baixa_renda | cond_baixa_escola
    return (transformation_union.sum() / len(df)) * 100