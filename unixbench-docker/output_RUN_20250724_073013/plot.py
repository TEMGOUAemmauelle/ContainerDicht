import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === CONFIGURATION ===
ORIGINAL_CSV = "benchmark_summary.csv"
CLEANED_CSV = "./results_summary_cleaned.csv"
PLOTS_DIR = "./plots_grouped_run1"
os.makedirs(PLOTS_DIR, exist_ok=True)

# === CORRECTION DU CSV : fusionner les décimales mal séparées ===
def fix_csv_format(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            if line.startswith("iteration"):
                f.write(line)
            else:
                parts = line.strip().split(",")
                if len(parts) > 9:
                    try:
                        fixed = parts[:4]  # iteration, runtime, type, duration_ms
                        watts = [".".join([parts[i], parts[i+1]]) for i in range(4, 11, 2)]
                        fixed.extend(watts)
                        fixed.append(parts[-1])  # power_file
                        f.write(",".join(fixed) + "\n")
                    except IndexError:
                        print(f"[⚠] Ligne malformée ignorée : {line}")
                else:
                    f.write(line)

fix_csv_format(ORIGINAL_CSV, CLEANED_CSV)

# === CHARGEMENT DES DONNÉES ===
df = pd.read_csv(CLEANED_CSV)

# Nettoyage
cols_to_float = ["duration_ms", "avg_pkg_watt", "avg_cor_watt", "avg_gfx_watt", "avg_cpu_c6"]
for col in cols_to_float:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df["iteration"] = pd.to_numeric(df["iteration"], errors="coerce")
df = df[df["type"] == "run"]

# === BARPLOT GROUPÉ PAR ITÉRATION ===
def plot_grouped_bar(df, y_metric, title, ylabel, filename):
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="iteration", y=y_metric, hue="runtime", palette="Set2")
    plt.title(title)
    plt.xlabel("Itération")
    plt.ylabel(ylabel)
    plt.legend(title="Runtime")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, filename))
    plt.close()

# === LINEPLOT GROUPÉ PAR ITÉRATION ===
def plot_grouped_line(df, y_metric, title, ylabel, filename):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="iteration", y=y_metric, hue="runtime", marker="o", palette="Set1")
    plt.title(title)
    plt.xlabel("Itération")
    plt.ylabel(ylabel)
    plt.legend(title="Runtime")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, filename))
    plt.close()

# === GRAPHIQUES À GÉNÉRER (BARPLOTS) ===
plot_grouped_bar(df, "duration_ms", "Durée par Itération et Runtime", "Durée (ms)", "grouped_duration.png")
plot_grouped_bar(df, "avg_pkg_watt", "PkgWatt par Itération et Runtime", "Consommation PkgWatt", "grouped_pkgwatt.png")
plot_grouped_bar(df, "avg_cor_watt", "CorWatt par Itération et Runtime", "Consommation CorWatt", "grouped_corwatt.png")
plot_grouped_bar(df, "avg_gfx_watt", "GFXWatt par Itération et Runtime", "Consommation GFXWatt", "grouped_gfxwatt.png")
plot_grouped_bar(df, "avg_cpu_c6", "CPU%C6 par Itération et Runtime", "Taux CPU%C6", "grouped_cpu_c6.png")

# === GRAPHIQUES À GÉNÉRER (LINEPLOTS) ===
plot_grouped_line(df, "duration_ms", "Durée par Itération et Runtime (Line)", "Durée (ms)", "line_duration.png")
plot_grouped_line(df, "avg_pkg_watt", "PkgWatt par Itération et Runtime (Line)", "Consommation PkgWatt", "line_pkgwatt.png")
plot_grouped_line(df, "avg_cor_watt", "CorWatt par Itération et Runtime (Line)", "Consommation CorWatt", "line_corwatt.png")
plot_grouped_line(df, "avg_gfx_watt", "GFXWatt par Itération et Runtime (Line)", "Consommation GFXWatt", "line_gfxwatt.png")
plot_grouped_line(df, "avg_cpu_c6", "CPU%C6 par Itération et Runtime (Line)", "Taux CPU%C6", "line_cpu_c6.png")

print(f"\n✅ Diagrammes en bandes (bar) et en lignes (line) générés dans : {PLOTS_DIR}")
print(f"📄 CSV corrigé : {CLEANED_CSV}")
