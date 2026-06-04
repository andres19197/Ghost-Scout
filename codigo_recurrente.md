# descargar o verificar si estan los datos de las 5 grandes ligas
import os

ROL_ATRIBUTOS = ['Pass', 'Carry', 'Dribble', 'Pressure', 'Shot', 'Ball Recovery', 'Miscontrol', 'Dispossessed']  # placeholder — cambiar por rol

competicion_id_15_16 = {
    'La_Liga': 11, 
    'Bundesliga': 9, 
    'Premier_League': 2, 
    'Serie_A': 12,
    'Ligue_1': 7
}

for nombre in competicion_id_15_16.keys():
    path_raw = f'data/raw/eventos_{nombre}_15_16.parquet'
    path_processed = f'data/processed/eventos_{nombre}_15_16_filtrado.parquet'
    
    if os.path.exists(path_processed):
        print(f'{nombre}: ya procesado, saltando')
        continue
        
    df_comp = pd.read_parquet(path_raw, filters=[('type', 'in', ROL_ATRIBUTOS)])
    df_comp.to_parquet(path_processed, index=False)
    print(f'{nombre}: {df_comp.shape} guardado en processed')
    del df_comp


    #meter a substitutos y actualizar el valor de minutos de los que salen
    for _, row in salen.iterrows():
        jugadores_completo.loc[jugadores_completo['nombre'] == row['nombre'], 'minutes_played'] = row['min_final']

    for _, row in entran.iterrows():
        min_reales = minuto_final - row['min_entrada']
        jugadores_completo.loc[jugadores_completo['nombre'] == row['nombre'], 'minutes_played'] = min_reales
        if 'posicion' in row:
            jugadores_completo.loc[jugadores_completo['nombre'] == row['nombre'], 'posicion'] = row['posicion']