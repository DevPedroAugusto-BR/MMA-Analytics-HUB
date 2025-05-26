import pandas as pd

from program import (
    get_all_fighters_names,
    get_fighter_by_name,
    get_all_weight_classes,
    get_fighters_by_weight_class,
    unify_fighters_data
)

df_with_age = pd.read_csv("MMA-Analytics-HUB\database\pro_mma_fighters_withAge.csv")
df_with_wins_and_loses = pd.read_csv("MMA-Analytics-HUB\database\ufc-fighters-statistics_WithWinsAndLoses.csv")
df_master_fights = pd.read_csv("MMA-Analytics-HUB\database\ufc-masterFights.csv")
df_upcomingFights = pd.read_csv("MMA-Analytics-HUB\database\upcomingFights.csv")


df_final = unify_fighters_data(df_with_age, df_with_wins_and_loses, df_master_fights, df_upcomingFights)

# Exemplo: todos os nomes
print(get_all_fighters_names(df_final))

# Exemplo: dados do lutador
print(get_fighter_by_name(df_final, "jon jones"))

# Exemplo: categorias
print(get_all_weight_classes(df_final))


# Exemplo: lutadores por categoria
print(get_fighters_by_weight_class(df_final, "light heavyweight"))

print(get_fighter_by_name(df_final, "charles oliveira"))