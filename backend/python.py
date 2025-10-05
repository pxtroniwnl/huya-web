import pandas as pd # Importa la libreria de pandas con el prefijo de pd
import numpy as np # Importa la libreria de numpy con el prefijo de np
import xarray as xr # Importa la libreria de xarray con el prefijo de xr
import earthaccess # Importa la libreria de earthaccess
import dask # Importa la libreria de dask
import h5py # Importa la libreria de h5py

auth = earthaccess.login(strategy = "prompt") # iniciar sesion en earthdata

latitud =  10.43 # float(input("Latitud Frontend: "))
longitud = -75.54 # float(input("Longitud Frontend: "))

# definir un area rectangular alrededor del lugar (0.3° en cada direccion)
area_evaluada = (
    round(longitud - 0.3, 2),
    round(latitud - 0.3, 2),
    round(longitud + 0.3, 2),
    round(latitud + 0.3, 2)
)

fecha_inicio = "2014-01-01" #input("Fecha Inicio Frontend (Formato: YYYY-MM-DD): ")
fecha_fin = "2014-01-05" #input("Fecha Fin Frontend (Formato: YYYY-MM-DD): ")

# Funcion para acceder a los archivos 
def accesoarchivo(shortname, ver):
    archivo = earthaccess.search_data(
        short_name = shortname, # Nombre dataset
        version = ver, # Version dataset
        temporal=(fecha_inicio, fecha_fin), # Rango de fechas elegido por el usuario
        bounding_box=area_evaluada # Area rectangular
    )
    return archivo

# Acceder a los 4 datasets principales
archivos_precip = accesoarchivo("GPM_3IMERGDF", "07") # (Dataset, Version)
archivos_wind = accesoarchivo("GLDAS_CLSM025_D", "2.0")
archivos_humedad = accesoarchivo("GLDAS_CLSM025_D", "2.0")
archivos_temperatura = accesoarchivo("M2SDNXSLV", "5.12.4") 

# Verificacion archivos existentes
print(f"Archivos encontrados (Precipitacion): {len(archivos_precip)}")
print(f"Archivos encontrados (Velocidad Viento): {len(archivos_wind)}")
print(f"Archivos encontrados (Humedad): {len(archivos_humedad)}")
print(f"Archivos encontrados (Temperatura): {len(archivos_temperatura)}")

# Guardar los archivos en las variables
lluvia_arch = earthaccess.open(archivos_precip)
wind_arch = earthaccess.open(archivos_wind)
humedad_arch = earthaccess.open(archivos_humedad)
presion_arch = earthaccess.open(archivos_humedad)
temperatura_arch = earthaccess.open(archivos_temperatura)

# VERIFICACION VARIABLE (Se puede remover al final de aqui hasta la linea 63 al final del proyecto)

lista_temporal = []

with h5py.File(temperatura_arch[0], "r") as f: # Recorrer el archivo seleccionado (sus variables principalmente)
    f.visit(lambda name: lista_temporal.append(name)) # Guardar los nombres de las variables del dataset en una lista
    #f.visit(print) # codigo en caso de quese necesite revisar las variables en el dataset determinado

for lista in lista_temporal: # Recorrer la lista de variables del dataset para confirmar si se encuentra la buscada
    if(lista == "precipitation"):
        print("Si esta la variable precipitation")

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

rango_fechas = pd.date_range(start=fecha_inicio, end=fecha_fin, freq="D") # Calcular el rango de fechas entre la fecha de inicio y fecha de fin seleccionadas por el usuario (en una frequencia por dia)
df_temperatura["time"] = rango_fechas[:len(df_temperatura)] # Reemplazar cada dato de time en el dataframe de temperatura por los datos de rango de fechas previamente obtenidos
daily_precip.index = rango_fechas # Reemplazar los indices de tiempo por los calculados en el rango de fechas
daily_wind.index = rango_fechas # Reemplazar los indices de tiempo por los calculados en el rango de fechas
daily_humedad.index = rango_fechas # Reemplazar los indices de tiempo por los calculados en el rango de fechas
daily_presion.index = rango_fechas # Reemplazar los indices de tiempo por los calculados en el rango de fechas
daily_temperatura = df_temperatura.groupby("time")["Celsius"].mean() # Agrupar por dia la temperatura media

df_final = pd.concat([ # Unir todos los dataframes en un solo dataframe con encabezados (todos en valores medios diarios)
    daily_precip.rename("Precipitacion (%)"),
    daily_wind.rename("Viento (km/h)"),
    daily_humedad.rename("Humedad (%)"),
    daily_presion.rename("PresionAtm (hPa)"),
    daily_temperatura.rename("Temperatura (°C)")
], axis=1)

df_final = df_final.reset_index().rename(columns={"index": "Fecha"}) # Reiniciar el indice y cambiarle el nombre a la columna

print(df_final) # Mostrar el dataframe final