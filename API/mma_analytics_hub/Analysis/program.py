import pandas as pd

def get_all_fighters_names(df):
    # Retorna lista com todos os nomes únicos, ordenados alfabeticamente
    names = df['name'].dropna().unique()
    return sorted(names.tolist())


def get_fighter_by_name(df, fighter_name):
    fighter_name = fighter_name.strip().lower()
    # Buscar linha pelo nome
    fighter_row = df[df['name'] == fighter_name]
    
    if fighter_row.empty:
        return None  # ou lançar exceção, dependendo do uso
    
    # Pegar a primeira ocorrência e converter para dict
    fighter_data = fighter_row.iloc[0].to_dict()
    
    # Converter NaN para None para JSON
    fighter_data = {k: (None if pd.isna(v) else v) for k, v in fighter_data.items()}
    
    return fighter_data


def get_all_weight_classes(df):
    # Pega a coluna weight_class, remove nulos e valores duplicados e ordena
    if 'weight_class' not in df.columns:
        return []
    categories = df['weight_class'].dropna().unique()
    return sorted(categories.tolist())


def get_fighters_by_weight_class(df, category):
    category = category.strip().lower()
    if 'weight_class' not in df.columns:
        return []

    # Normaliza categoria para busca case-insensitive
    df['weight_class_lower'] = df['weight_class'].str.lower()
    
    # Busca lutadores na categoria
    fighters_in_cat = df[df['weight_class_lower'] == category]['name'].dropna().unique()
    
    # Remove coluna temporária criada
    df.drop(columns=['weight_class_lower'], inplace=True)
    
    return sorted(fighters_in_cat.tolist())


def unify_fighters_data(df_with_age, df_with_wins_and_loses, df_master_fights, df_upcomingFights):
    def clean_name(name):
        if pd.isna(name):
            return name
        return name.strip().lower()
    
    # Renomear coluna para padronizar
    if 'fighter_name' in df_with_age.columns:
        df_with_age = df_with_age.rename(columns={'fighter_name': 'name'})
    else:
        raise KeyError("df_with_age não possui coluna 'fighter_name'")

    # Padronizar nomes em df_with_age
    df_with_age['name'] = df_with_age['name'].apply(clean_name)

    # Padronizar nomes em df_with_wins_and_loses
    if 'name' in df_with_wins_and_loses.columns:
        df_with_wins_and_loses['name'] = df_with_wins_and_loses['name'].apply(clean_name)
        # Corrigir erro de digitação na coluna losses
        if 'lossess' in df_with_wins_and_loses.columns:
            df_with_wins_and_loses.rename(columns={'lossess': 'losses'}, inplace=True)
    else:
        raise KeyError("df_with_wins_and_loses não possui coluna 'name'")

    # Padronizar nomes nos dfs de lutas: df_master_fights e df_upcomingFights
    for df in [df_master_fights, df_upcomingFights]:
        if 'RedFighter' in df.columns and 'BlueFighter' in df.columns:
            df['RedFighter'] = df['RedFighter'].apply(clean_name)
            df['BlueFighter'] = df['BlueFighter'].apply(clean_name)
        else:
            raise KeyError("DataFrame não possui colunas 'RedFighter' e 'BlueFighter'")

    # Merge dos dfs de lutadores perfil no campo 'name'
    df_fighters = pd.merge(
        df_with_age,
        df_with_wins_and_loses,
        on='name',
        how='outer',
        suffixes=('_age', '_stats')
    )

    # Extrair nomes únicos dos lutadores das lutas
    fighters_master = set(df_master_fights['RedFighter'].dropna().unique()) | set(df_master_fights['BlueFighter'].dropna().unique())
    fighters_upcoming = set(df_upcomingFights['RedFighter'].dropna().unique()) | set(df_upcomingFights['BlueFighter'].dropna().unique())
    all_fighters_from_fights = fighters_master | fighters_upcoming

    # Criar DataFrame com todos lutadores de lutas
    df_fighters_from_fights = pd.DataFrame({'name': list(all_fighters_from_fights)})

    # Fazer outer join para garantir todos lutadores no dataframe final
    df_final = pd.merge(
        df_fighters,
        df_fighters_from_fights,
        on='name',
        how='outer'
    )

    # Remover duplicados e ordenar
    df_final = df_final.drop_duplicates(subset='name').sort_values('name').reset_index(drop=True)

    return df_final

df_with_age = pd.read_csv("database\\pro_mma_fighters_withAge.csv")
df_with_wins_and_loses = pd.read_csv("database\\ufc-fighters-statistics_WithWinsAndLoses.csv")
df_master_fights = pd.read_csv("database\\ufc-masterFights.csv")
df_upcomingFights = pd.read_csv("database\\upcomingFights.csv")
df_final = unify_fighters_data(df_with_age, df_with_wins_and_loses, df_master_fights, df_upcomingFights)
