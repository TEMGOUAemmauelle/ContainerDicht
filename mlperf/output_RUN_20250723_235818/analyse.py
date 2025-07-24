#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re
import sys

def main():
    current_dir = Path.cwd()
    print(f"Analyzing results in: {current_dir}")

    # Vérification des fichiers requis
    required_files = ['benchmark_summary.csv', 'raw_output_*.log']
    if not list(current_dir.glob('raw_output_*.log')):
        print("❌ Fichier raw_output_*.log introuvable")
        sys.exit(1)
    if not (current_dir / 'benchmark_summary.csv').exists():
        print("❌ Fichier benchmark_summary.csv introuvable")
        sys.exit(1)

    # Traitement des données
    try:
        # 1. Lire le CSV principal
        df = pd.read_csv(current_dir / 'benchmark_summary.csv')
        
        # 2. Extraire les métriques des logs
        log_file = next(current_dir.glob('raw_output_*.log'))
        with open(log_file, 'r') as f:
            log_content = f.read()
        
        pattern = r"Latence moyenne: (\d+\.\d+) ms.*Throughput: (\d+\.\d+) inférences/sec"
        matches = re.findall(pattern, log_content.replace("\n", " "))
        
        if not matches:
            print("❌ Aucune métrique trouvée dans les logs")
            sys.exit(1)
            
        # 3. Fusionner les données
        metrics_df = pd.DataFrame(matches, columns=['latency_ms', 'throughput'])
        final_df = pd.concat([df, metrics_df], axis=1)
        
        # 4. Sauvegarder les résultats complets
        final_df.to_csv(current_dir / 'final_results.csv', index=False)
        print(f"✅ Données fusionnées sauvegardées dans: {current_dir}/final_results.csv")
        
        # 5. Générer des graphiques simples
        plt.figure(figsize=(15, 5))
        
        # Graphique de latence
        plt.subplot(1, 3, 1)
        final_df.boxplot(column='latency_ms', by='runtime')
        plt.title('Comparaison de latence')
        plt.suptitle('')
        plt.ylabel('ms')
        
        # Graphique de throughput
        plt.subplot(1, 3, 2)
        final_df.boxplot(column='throughput', by='runtime')
        plt.title('Comparaison de débit')
        plt.suptitle('')
        plt.ylabel('inférences/sec')
        
        # Graphique de puissance
        plt.subplot(1, 3, 3)
        final_df.groupby('runtime')['avg_pkg_watt'].mean().plot.bar()
        plt.title('Consommation énergétique moyenne')
        plt.ylabel('Watts')
        
        plt.tight_layout()
        plt.savefig(current_dir / 'performance_comparison.png')
        print(f"✅ Graphiques sauvegardés dans: {current_dir}/performance_comparison.png")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
