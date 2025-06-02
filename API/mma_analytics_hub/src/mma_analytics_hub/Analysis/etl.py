from mma_analytics_hub.Analysis.program import (
    get_all_fighters_names,
    get_fighter_by_name,
    get_all_weight_classes,
    get_fighters_by_weight_class,
    unify_fighters_data,
)


from pathlib import Path
import pandas as pd

# Define a raiz do projeto (onde poetry roda)
BASE_DIR = Path(__file__).resolve().parent  # src/mma_analytics_hub/Analysis
DATABASE_DIR = BASE_DIR / "database"

# Define os caminhos completos para os arquivos
AGE_PATH = DATABASE_DIR / "pro_mma_fighters_withAge.csv"
STATS_PATH = DATABASE_DIR / "ufc-fighters-statistics_WithWinsAndLoses.csv"
MASTER_FIGHTS_PATH = DATABASE_DIR / "ufc-masterFights.csv"
UPCOMING_PATH = DATABASE_DIR / "upcomingFights.csv"

# Lê os arquivos
df_with_age = pd.read_csv(AGE_PATH)
df_with_wins_and_loses = pd.read_csv(STATS_PATH)
df_master_fights = pd.read_csv(MASTER_FIGHTS_PATH)
df_upcomingFights = pd.read_csv(UPCOMING_PATH)

# Unifica os dados
df_final = unify_fighters_data(df_with_age, df_with_wins_and_loses, df_master_fights, df_upcomingFights)


# Caminho do arquivo de saída
OUTPUT_DIR = DATABASE_DIR / "output"

# Cria a pasta 'output' dentro de 'database' se não existir
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Salva o dataframe
df_final.to_csv(OUTPUT_DIR / "fighters_data.csv", index=False)

print("Arquivo salvo com sucesso em:", OUTPUT_DIR / "fighters_data.csv")
