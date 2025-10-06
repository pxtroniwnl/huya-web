# Importar librerias
from sklearn.ensemble import RandomForestRegressor # Modelo Predictivo
import pandas as pd 
import numpy as np 
import xarray as xr 
import earthaccess 
import dask 
import h5py 
import json
import sys
import os

# Verificar si se recibieron parámetros desde PHP
if len(sys.argv) > 1:
    # Leer parámetros del archivo temporal
    params_file = sys.argv[1]
    with open(params_file, 'r') as f:
        params = json.load(f)
    
    latitud = params['latitud'] # FRONTEND
    longitud = params['longitud'] # FRONTEND
    fecha_inicio = params['fecha_inicio'] # FRONTEND
    fecha_fin = params['fecha_fin'] # FRONTEND
else:
    # Valores por defecto para pruebas
    # Valores por defecto si no se proporcionan desde el frontend
    latitud = latitud if latitud else 10.43
    longitud = longitud if longitud else -75.54
    fecha_inicio = fecha_inicio if fecha_inicio else "2025-10-05"
    fecha_fin = fecha_fin if fecha_fin else "2025-10-11"

auth = earthaccess.login(strategy="prompt") # iniciar sesion en earthdata

# definir un area rectangular alrededor del lugar (0.3° en cada direccion)
area_evaluada = (
    round(longitud - 0.3, 2),
    round(latitud - 0.3, 2),
    round(longitud + 0.3, 2),
    round(latitud + 0.3, 2)
)

# Las fechas ahora se obtienen desde el frontend arriba

# Definir el año maximo segun los datasets y la cantidad de años que se van a tomar en cuenta a partir de este año maximo
año_maximo = 2014
numero_años = 5

# Convertir los strings a unidades de tiempo
tiempo_inicio = pd.to_datetime(fecha_inicio)
tiempo_fin = pd.to_datetime(fecha_fin)
rangos = [] # Lista para guardar los intervalos de años
for i in range(numero_años): # Ciclo para sacar los intervalos de tiempo para cada año a partir del año maximo
    año_eva = año_maximo - i # Para evaluar año por año de adelante hacia atras
    fecha_itemp = tiempo_inicio.replace(year=año_eva) # Copiar el valor a predecir y reemplazar unicamente el año (conservando el dia y mes) para la fecha de inicio
    fecha_ftemp = tiempo_fin.replace(year=año_eva) # Copiar el valor a predecir y reemplazar unicamente el año (conservando el dia y mes) para la fecha de fin
    rangos.append((fecha_itemp.strftime("%Y-%m-%d"), fecha_ftemp.strftime("%Y-%m-%d"))) # agregar los intervalos de años en la lista (manejandolo como una lista de listas)

# Funcion para acceder a los archivos 
def accesoarchivo(shortname, ver, fecha1, fecha2):
    archivo = earthaccess.search_data(
        short_name = shortname, # Nombre dataset
        version = ver, # Version dataset
        temporal=(fecha1, fecha2), # Rango de fechas elegido por el usuario
        bounding_box=area_evaluada # Area rectangular
    )
    return archivo

# Listas para almacenar los archivos de cada dataset
archivos_precip = []
archivos_wind = []
archivos_temperatura = []

# Acceder a los 4 datasets principales
for i in range(numero_años):
    archivos_precip.extend(accesoarchivo("GPM_3IMERGDF", "07", rangos[i][0], rangos[i][1]))
    archivos_wind.extend(accesoarchivo("GLDAS_CLSM025_D", "2.0", rangos[i][0], rangos[i][1]))
    archivos_temperatura.extend(accesoarchivo("M2SDNXSLV", "5.12.4", rangos[i][0], rangos[i][1]))

# Guardar los archivos en las variables
lluvia_arch = earthaccess.open(archivos_precip)
wind_arch = earthaccess.open(archivos_wind)
humedad_arch = earthaccess.open(archivos_wind)
presion_arch = earthaccess.open(archivos_wind)
temperatura_arch = earthaccess.open(archivos_temperatura)

# Funcion para crear dataframes
def creardataframe(archivo_espe):
    lista_datos = []
    
    # Verificacion manual del archivo esperado para la eleccion de la variable a tomar en cuenta
    if(archivo_espe == lluvia_arch):
        variable = "precipitation"
    if(archivo_espe == wind_arch):
        variable = "Wind_f_tavg"
    if(archivo_espe == humedad_arch):
        variable = "Qair_f_tavg"
    if(archivo_espe == presion_arch):
        variable = "Psurf_f_tavg"
    if(archivo_espe == temperatura_arch):
        variable = "T2MMEAN"
    
    # recorrer el archivo para sacar las variables determinadas (latitud, longitud, tiempo y la variable seleccionada anteriormente)
    for archivo in archivo_espe:
        with h5py.File(archivo, "r") as f:
            lat = f["lat"][:] # Seleccion variables para dataframe
            lon = f["lon"][:]
            time = f["time"][:] 
            var = f[variable][:]


            lat_index = np.where((lat >= area_evaluada[1]) & (lat <= area_evaluada[3]))[0] # guardar la posicion/index de los datos (latitud) segun el area evaluada
            lon_index = np.where((lon >= area_evaluada[0]) & (lon <= area_evaluada[2]))[0] # guardar la posicion/index de los datos (longitud) segun el area evaluada

            var_sel = var[:, lat_index[:, None], lon_index] # Filtrar los datos de la variable a analizar dentro del area evaluada
            lat_sel = lat[lat_index] # Latitudes filtradas 
            lon_sel = lon[lon_index] # Longitudes filtradas

            fecha_base = pd.to_datetime("1980-01-06") # Fecha base para dar formato a la variable time (aunque despues esto se cambia)
            for t_index, t in enumerate(time): # Iterar para cada dia
                fecha = fecha_base + pd.to_timedelta(int(t), unit="D") # Convierte la variable de tiempo en una fecha real/legible (con formato año-mes-dia)

                datos_ext = var_sel[t_index, :, :] # extraer los datos para ese dia
                lat_grid, lon_grid = np.meshgrid(lat_sel, lon_sel, indexing="ij") # crear una malla para las coordenadas (latitud y longitud)
                df_temporal = pd.DataFrame({ # Crear un dataframe temporal con los valores (dividido por columnas)
                    "time": [fecha] * datos_ext.size,
                    "lat": lat_grid.flatten(),
                    "lon": lon_grid.flatten(),
                    variable: datos_ext.flatten()
                })
                lista_datos.append(df_temporal) # añade el dataframe temporal a la lista
    return lista_datos # se retorna la lista para manejar los datos

# Funcion para manejar la variable de humedad (dado que esta es humedad especifica y necesitamos porcentaje de humedad)
def manejohumedad(archivo_espe):
    lista_datos = []
    # recorrer el archivo para sacar las variables determinadas (latitud, longitud, tiempo, humedad especifica, presion atmosferica, temperatura)
    for archivo in archivo_espe:
        with h5py.File(archivo, "r") as f:
            lat = f["lat"][:]
            lon = f["lon"][:]
            time = f["time"][:] 
            var1 = f["Qair_f_tavg"][:] # Humedad especifica
            var2 = f["Psurf_f_tavg"][:] # presion en Pa
            var3 = f["Tair_f_tavg"][:] # Temperatura en kelvin


            lat_index = np.where((lat >= area_evaluada[1]) & (lat <= area_evaluada[3]))[0] # guardar la posicion/index de los datos (latitud) segun el area evaluada
            lon_index = np.where((lon >= area_evaluada[0]) & (lon <= area_evaluada[2]))[0] # guardar la posicion/index de los datos (longitud) segun el area evaluada

            var_sel1 = var1[:, lat_index[:, None], lon_index] # Filtrar los datos de la variable humedad especifica dentro del area evaluada
            var_sel2 = var2[:, lat_index[:, None], lon_index] # Filtrar los datos de la variable presion atmosferica dentro del area evaluada
            var_sel3 = var3[:, lat_index[:, None], lon_index] # Filtrar los datos de la variable temperatura dentro del area evaluada
            lat_sel = lat[lat_index] # Latitudes filtradas 
            lon_sel = lon[lon_index] # Longitudes filtradas 

            fecha_base = pd.to_datetime("1980-01-06") # Fecha base para dar formato a la variable time (aunque despues esto se cambia)
            for t_index, t in enumerate(time): # Iterar para cada dia
                date = fecha_base + pd.to_timedelta(int(t), unit="D") # Convierte la variable de tiempo en una fecha real/legible (con formato año-mes-dia)

                arr1 = var_sel1[t_index, :, :] # extraer los datos de humedad especifica para ese dia
                arr2 = var_sel2[t_index, :, :] # extraer los datos de presion atmosferica para ese dia
                arr3 = var_sel3[t_index, :, :] # extraer los datos de temperatura para ese dia
                lat_grid, lon_grid = np.meshgrid(lat_sel, lon_sel, indexing="ij") # crear una malla para las coordenadas (latitud y longitud)
                df_temporal = pd.DataFrame({ # Crear un dataframe temporal con los valores (dividido por columnas)
                    "time": [date] * arr1.size,
                    "lat": lat_grid.flatten(),
                    "lon": lon_grid.flatten(),
                    "Qair_f_tavg": arr1.flatten(),
                    "Psurf_f_tavg": arr2.flatten(),
                    "Tair_f_tavg": arr3.flatten()
                })
                lista_datos.append(df_temporal) # añade el dataframe temporal a la lista
    return lista_datos # se retorna la lista para manejar los datos

# Crear las listas de dataframes por cada archivo
datos_precip = creardataframe(lluvia_arch)
datos_wind = creardataframe(wind_arch)
datos_humedad = manejohumedad(humedad_arch)
datos_presion = creardataframe(presion_arch)
datos_temperatura = creardataframe(temperatura_arch)

# Une los dataframes de cada lista en un solo dataframe por archivo (concatenandolos)
df_precip = pd.concat(datos_precip, ignore_index=True)
df_wind = pd.concat(datos_wind, ignore_index=True)
df_humedad = pd.concat(datos_humedad, ignore_index=True)
df_presion = pd.concat(datos_presion, ignore_index=True)
df_temperatura = pd.concat(datos_temperatura, ignore_index=True)

# Conversiones de unidades
df_precip["precip_diario"] = df_precip["precipitation"] > 0.1 # Revisar si hubo lluvia (>0.1 mm)
df_wind["wind_diario"] = df_wind["Wind_f_tavg"] * (3600/1000) # Convertir m/s a km/h
df_humedad["hPa"] = df_humedad["Psurf_f_tavg"] / 100 # Convertir Pa a hPa
df_humedad["Celsius"] = df_humedad["Tair_f_tavg"] - 273.15 # Convertir Kelvin a Celsius
df_presion["presion_diaria"] = df_presion["Psurf_f_tavg"] / 100 # Convertir Pa a hPa
df_temperatura["Celsius"] = df_temperatura["T2MMEAN"] - 273.15 # Convertir Kelvin a Celsius

# Formula de Humedad especifica a porcentaje de humedad
w  = df_humedad["Qair_f_tavg"] / (1 - df_humedad["Qair_f_tavg"]) # Razon de mezcla (kg/kg)
e  = (w * df_humedad["hPa"]) / (0.622 + w) # Presion de vapor real (hPa)
es = 6.112 * np.exp((17.67 * df_humedad["Celsius"]) / (df_humedad["Celsius"] + 243.5)) # Presion de vapor de saturacion (hPa)
df_humedad["humedad_diaria"] = 100 * e / es # Calculo de porcentaje de humedad (relativa)

daily_precip = df_precip.groupby("time")["precip_diario"].mean() * 100 # Agrupar por dia el porcentaje medio de precipitacion
daily_wind = df_wind[df_wind["wind_diario"] > 0].groupby("time")["wind_diario"].mean() # Agrupar por dia la velocidad del viento media
daily_humedad = df_humedad[df_humedad["humedad_diaria"] > 0].groupby("time")["humedad_diaria"].mean() # Agrupar por dia el porcentaje medio de humedad
daily_presion = df_presion[df_presion["presion_diaria"] > 0].groupby("time")["presion_diaria"].mean() # Agrupar por dia la presion atmosferica media

rango_fechas_total = [] # Crear rango de fechas para los datos historicos 
for i in range(numero_años):
    año_eva = año_maximo - i
    fecha_ini_temp = pd.to_datetime(fecha_inicio).replace(year=año_eva)
    fecha_fin_temp = pd.to_datetime(fecha_fin).replace(year=año_eva)
    rango_temp = pd.date_range(start=fecha_ini_temp, end=fecha_fin_temp, freq="D")
    rango_fechas_total.extend(rango_temp) # Agregar a la lista los años teniendo en cuenta los dias para poder tener todo el abanico de años-mes-dia
    
rango_fechas_total = sorted(rango_fechas_total, reverse=True) # Ordenar las fechas de manera descendente

df_temperatura["time"] = rango_fechas_total[:len(df_temperatura)] # Reemplazar cada dato de time en el dataframe de temperatura por los datos de rango de fechas previamente obtenidos
daily_precip.index = rango_fechas_total # Reemplazar los indices de tiempo por los calculados en el rango de fechas
daily_wind.index = rango_fechas_total # Reemplazar los indices de tiempo por los calculados en el rango de fechas
daily_humedad.index = rango_fechas_total # Reemplazar los indices de tiempo por los calculados en el rango de fechas
daily_presion.index = rango_fechas_total # Reemplazar los indices de tiempo por los calculados en el rango de fechas
daily_temperatura = df_temperatura.groupby("time")["Celsius"].mean() # Agrupar por dia la temperatura media

df_final = pd.concat([ # Unir todos los dataframes en un solo dataframe con encabezados (todos en valores medios diarios)
    daily_precip.rename("Precipitacion (%)"),
    daily_wind.rename("Viento (km/h)"),
    daily_humedad.rename("Humedad (%)"),
    daily_presion.rename("PresionAtm (hPa)"),
    daily_temperatura.rename("Temperatura (°C)")
], axis=1)

df_final = df_final.reset_index().rename(columns={"index": "Fecha"}) # Reiniciar el indice y cambiarle el nombre a la columna

# MODELO PREDICTIVO CON RANDOM FOREST - MULTI HORIZON
horizonte = len(pd.date_range(start=fecha_inicio, end=fecha_fin)) # Numero de dias a predecir
dias_pasado = 1 # Numero de dias pasados que se tendran en cuenta al predecir un dia en especifico

variables = ["Precipitacion (%)", "Viento (km/h)", "Humedad (%)", "PresionAtm (hPa)", "Temperatura (°C)"] # Columnas/Variables
df_randomforest = df_final[["Fecha"] + variables].copy() # Copiar el dataframe con los datos historicos y sus respectivas columnas
df_randomforest = df_randomforest.sort_values("Fecha").set_index("Fecha") # Ordenar segun la fecha y poner esta como indice

# Matrices de entrada (x) y salida (y) para la preparacion previa al random forest
X, Y = [], []
for i in range(dias_pasado, len(df_randomforest) - horizonte + 1): # Hacer un recorrido teniendo en cuenta los parametros puestos para asegurar que hayan suficientes datos para el random forest
    x_i = df_randomforest.iloc[i - dias_pasado:i].values.flatten() # Tomar los valores de las variables de los dias anteriores como entrada
    y_i = df_randomforest.iloc[i:i + horizonte].values.flatten() # Tomar los valores de las variables de los proximos dias como salida
    X.append(x_i)
    Y.append(y_i)

# Convertir las listas en arrays de numpy para poder entrenar el modelo
X_train = np.array(X)
Y_train = np.array(Y)

randomforest = RandomForestRegressor(n_estimators=200, random_state=42) # Modelo random forest
randomforest.fit(X_train, Y_train) # Entrenamiento del modelo con las matrices de entrada y salida

X_pred = df_randomforest.iloc[-dias_pasado:].values.flatten().reshape(1, -1) # Ultima entrada para generar predicciones (ultimo elemento del dataframe)

predicciones = randomforest.predict(X_pred) # Generar predicciones para el tiempo definidio
predicciones = predicciones.reshape(horizonte, len(variables)) # Organizar las predicciones en formato de tiempo y numero de variables

rango_pred = pd.date_range(start=fecha_inicio, end=fecha_fin) # Rango de fechas a predecir

# Crear dataframe para segun cada fecha los respectivos valores de la prediccion con random forest
df_pred = pd.DataFrame(predicciones, columns=variables)  
df_pred["Fecha"] = rango_pred
df_pred = df_pred[["Fecha"] + variables]

# Redondear todas las variables al entero mas cercano
df_pred[variables] = df_pred[variables].round(0)

# Calculo de medias por variable en la prediccion para el front end
medias = {
    "Precipitacion (%)": round(df_pred["Precipitacion (%)"].mean()),
    "Viento (km/h)": round(df_pred["Viento (km/h)"].mean()),
    "Humedad (%)": round(df_pred["Humedad (%)"].mean()),
    "PresionAtm (hPa)": round(df_pred["PresionAtm (hPa)"].mean()),
    "Temperatura (°C)": round(df_pred["Temperatura (°C)"].mean())
}

# Copiar dadaframe de predicciones para modificar y exportar el JSON
df_json = df_pred.copy()
# Cambio de formato de las fechas a año-mes-dia
df_json["Fecha"] = df_json["Fecha"].dt.strftime("%Y-%m-%d")

# diccionario con los datos predecidos divididos por fecha y las medias por separado
diccionario = {
    "datos": df_json.to_dict(orient="records"),
    "medias": medias
}

# creacion del archivo JSON en la ruta del backend
ruta = os.path.join(os.path.dirname(__file__), "resultados.json")
with open(ruta, "w", encoding="utf-8") as f:
    json.dump(diccionario, f, ensure_ascii=False, indent=4)

print("Procesamiento completado exitosamente")