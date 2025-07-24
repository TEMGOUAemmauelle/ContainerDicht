#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re
import sys
from typing import List, Tuple

def clean_and_convert(df: pd.DataFrame) -> pd.DataFrame:
    """Convertit les colonnes numériques et nettoie les données"""
    for col in df.columns:
        if col not in ['runtime', 'type', 'power_file']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def extract_metrics(log_content: str) -> Tuple[List[float], List[float]]:
    """Extrait les métriques de latence et débit depuis le contenu du log"""
    latencies = []
    throughputs = []
    
    # Expression régulière améliorée pour capturer les métriques
    pattern = re.compile(
        r"Latence moyenne: (\d+\.\d+) ms.*?Throughput: (\d+\.\d+) inférences/sec",
        re.DOTALL
    )
    
    # Pour chaque correspondance dans le fichier log
    for match in pattern.finditer(log_content):
        latencies.append(float(match.group(1)))
        throughputs.append(float(match.group(2)))
    
    return latencies, throughputs

def main():
    current_dir = Path.cwd()
    print(f"Analyse des résultats dans : {current_dir}")

    try:
        # 1. Charger le CSV principal
        df = pd.read_csv(current_dir / 'benchmark_summary.csv')
        
        # 2. Nettoyer les données
        df = clean_and_convert(df)
        
        # 3. Extraire les métriques des logs
        log_files = list(current_dir.glob('raw_output_*.log'))
        if not log_files:
            raise FileNotFoundError("Aucun fichier log trouvé")
        if len(log_files) > 1:
            print(f"⚠️ Attention: Plusieurs fichiers logs trouvés, utilisation du premier: {log_files[0]}")
        
        with open(log_files[0], 'r', encoding='utf-8') as f:
            log_content = f.read()
        
        latencies, throughputs = extract_metrics(log_content)
        
        print(f"Nombre de mesures de latence trouvées: {len(latencies)}")
        print(f"Nombre de mesures de débit trouvées: {len(throughputs)}")
        print(f"Nombre de lignes dans le CSV: {len(df)}")
        
        if len(latencies) != len(df):
            print(f"⚠️ Attention: {len(latencies)} métriques trouvées pour {len(df)} lignes dans le CSV")
        
        # 4. Ajouter les nouvelles colonnes
        metrics_df = pd.DataFrame({
            'latency_ms': latencies[:len(df)],  # On tronque au besoin
            'throughput': throughputs[:len(df)]  # On tronque au besoin
        })
        final_df = pd.concat([df, metrics_df], axis=1)
        
        # 5. Vérification finale des types
        final_df = clean_and_convert(final_df)
        
        # Afficher un échantillon pour vérification
        print("\nAperçu des données:")
        print(final_df[['runtime', 'latency_ms', 'throughput']].head())
        
        # 6. Sauvegarder
        final_df.to_csv(current_dir / 'final_results.csv', index=False)
        print(f"\n✅ Données sauvegardées dans: final_results.csv")
        
        # 7. Générer des graphiques
        try:
            plt.figure(figsize=(15, 10))
            
            # Graphique 1: Latence
            plt.subplot(2, 2, 1)
            final_df.boxplot(column='latency_ms', by='runtime')
            plt.title('Latence (ms) par runtime')
            plt.suptitle('')
            plt.ylabel('Latence (ms)')
            
            # Graphique 2: Débit
            plt.subplot(2, 2, 2)
            final_df.boxplot(column='throughput', by='runtime')
            plt.title('Débit (inf/s) par runtime')
            plt.suptitle('')
            plt.ylabel('Débit (inférences/sec)')
            
            # Graphique 3: Énergie
            plt.subplot(2, 2, 3)
            final_df.groupby('runtime')['avg_pkg_watt'].mean().plot.bar()
            plt.title('Puissance moyenne (W) par runtime')
            plt.ylabel('Puissance (W)')
            
            plt.tight_layout()
            plt.savefig(current_dir / 'performance_comparison.png')
            print(f"✅ Graphiques sauvegardés dans: performance_comparison.png")
            
        except Exception as plot_error:
            print(f"⚠️ Erreur lors de la génération des graphiques: {str(plot_error)}")

    except Exception as e:
        print(f"❌ Erreur critique: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
