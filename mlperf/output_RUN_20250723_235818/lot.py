import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# === CONFIGURATION ===
FINAL_RESULTS_CSV = "final_results.csv"  # Fichier déjà complet avec latence/débit
PLOTS_DIR = "./plots_grouped_run1"
os.makedirs(PLOTS_DIR, exist_ok=True)

# === CHARGEMENT DES DONNÉES ===
df = pd.read_csv(FINAL_RESULTS_CSV)

# Nettoyage des données
cols_to_clean = ["duration_ms", "avg_pkg_watt", "avg_cor_watt", 
                "avg_gfx_watt", "avg_cpu_c6", "latency_ms", "throughput"]
for col in cols_to_clean:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df["iteration"] = pd.to_numeric(df["iteration"], errors="coerce")

# Filtrage (si nécessaire)
df = df[df["type"] == "run"]  # Supprimez cette ligne si vous voulez toutes les données

# === FONCTIONS DE VISUALISATION ===
def plot_grouped_bar(df, y_metric, title, ylabel, filename):
    """Génère un diagramme en barres groupées"""
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="iteration", y=y_metric, hue="runtime", palette="Set2")
    plt.title(title)
    plt.xlabel("Itération")
    plt.ylabel(ylabel)
    plt.legend(title="Runtime", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, filename), bbox_inches='tight', dpi=300)
    plt.close()

def plot_grouped_line(df, y_metric, title, ylabel, filename):
    """Génère un diagramme en lignes"""
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="iteration", y=y_metric, hue="runtime", 
                style="runtime", markers=True, dashes=False, 
                markersize=8, palette="Set1")
    plt.title(title)
    plt.xlabel("Itération")
    plt.ylabel(ylabel)
    plt.legend(title="Runtime", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, filename), bbox_inches='tight', dpi=300)
    plt.close()

# === LISTE DES MÉTRIQUES À VISUALISER ===
metrics = [
    ("duration_ms", "Durée d'exécution", "ms"),
    ("avg_pkg_watt", "Consommation énergétique (Package)", "W"),
    ("avg_cor_watt", "Consommation énergétique (Core)", "W"),
    ("avg_gfx_watt", "Consommation énergétique (GFX)", "W"),
    ("avg_cpu_c6", "Temps en état C6", "%"),
    ("latency_ms", "Latence moyenne", "ms"),
    ("throughput", "Débit", "inférences/sec")
]

# === GÉNÉRATION DES GRAPHIQUES ===
for col, name, unit in metrics:
    # Graphiques en barres
    plot_grouped_bar(df, col, f"{name} par Itération", f"{name} ({unit})", f"bar_{col}.png")
    
    # Graphiques en lignes
    plot_grouped_line(df, col, f"{name} par Itération", f"{name} ({unit})", f"line_{col}.png")

# === STATISTIQUES GLOBALES ===
stats_df = df.groupby("runtime")[["latency_ms", "throughput", "duration_ms"]].agg(["mean", "std"])
print("\nStatistiques globales :")
print(stats_df)

# Sauvegarde des statistiques
stats_df.to_csv(os.path.join(PLOTS_DIR, "performance_stats.csv"))
print(f"\n✅ Tous les graphiques générés dans : {PLOTS_DIR}")
print(f"📊 Statistiques sauvegardées dans : {os.path.join(PLOTS_DIR, 'performance_stats.csv')}")
