''' Librerias
'''
import pandas as pd
import os 
import numpy as np
from datetime import datetime


''' Generacion de registro de actualizaciones
'''
registro = open('registro.csv', 'a')
registro = open('registro.csv', 'r')
if registro.read()=='':
    registro = open('registro.csv', 'a')
    registro.write('Nombre_Archivo;Fecha\n')
registro.close()

regis_df = pd.read_csv('C:\\Users\\Willy\\Desktop\\Ale\\HENRY\\P_I\\DS-PI-ProyectoIndividual\\registro.csv', sep=';')
contenido = os.listdir('C:\\Users\\Willy\\Desktop\\Ale\\HENRY\\P_I\\DS-PI-ProyectoIndividual\\Datasets')
print(regis_df)
bool = True
bool2= True

''' Carga de archivos nuevos
'''
for archivo in contenido:
    registro = open('registro.csv', 'a')
    if any(regis_df['Nombre_Archivo']==archivo):
        pass
    elif 'Clien' in archivo:
        if bool:
            cliente = pd.read_csv('C:\\Users\\Willy\\Desktop\\Ale\\HENRY\\P_I\\DS-PI-ProyectoIndividual\\Datasets\\Clientes.csv', delimiter=';')
            #cliente.drop(columns='col10', inplace=True)
            bool = False
            linea = f'{archivo};{datetime.now()}\n'
            registro.write(linea)
        else:
            cliente_añadir = pd.read_csv(f'C:\\Users\\Willy\\Desktop\\Ale\\HENRY\\P_I\\DS-PI-ProyectoIndividual\\Datasets\\{archivo}', delimiter=';')
            #cliente_añadir.drop(columns='col10', inplace=True)
            cliente_aux = pd.concat([cliente, cliente_añadir], axis=0)
            cliente = cliente_aux

            linea = f'{archivo};{datetime.now()}\n'
            registro.write(linea)
    elif 'Venta' in archivo:
        if any(regis_df['Nombre_Archivo']==archivo):
            pass
        elif 'Venta' in archivo:
            if bool2:
                venta = pd.read_csv('C:\\Users\\Willy\\Desktop\\Ale\\HENRY\\P_I\\DS-PI-ProyectoIndividual\\Datasets\\Venta.csv', delimiter=',')
                bool2 = False
                linea = f'{archivo};{datetime.now()}\n'
                registro.write(linea)
            else:
                venta_añadir = pd.read_csv(f'C:\\Users\\Willy\\Desktop\\Ale\\HENRY\\P_I\\DS-PI-ProyectoIndividual\\Datasets\\{archivo}', delimiter=',')
                #cliente_añadir.drop(columns='col10', inplace=True)
                venta_aux = pd.concat([venta, venta_añadir], axis=0)
                venta = venta_aux

                linea = f'{archivo};{datetime.now()}\n'
                registro.write(linea)
    registro.close()
    regis_df = pd.read_csv('C:\\Users\\Willy\\Desktop\\Ale\\HENRY\\P_I\\DS-PI-ProyectoIndividual\\registro.csv', sep=';')
'''Se guarda la actualizacion '''



'''Limpieza y normalizacion de cliente'''
#Duplicados

# Columnas
cliente.columns=["ID","Provincia","Nombre_y_Apellido","Domicilio","Telefono","Edad","Localidad","Longitud","Latitud", 'col10']   
cliente.set_index('ID', inplace=True)
# Reemplazo de faltantes
cliente["Provincia"].fillna("Sin Dato",inplace=True)
cliente["Nombre_y_Apellido"].fillna("Sin Dato",inplace=True)
cliente["Domicilio"].fillna("Sin Dato",inplace=True)
cliente["Telefono"].fillna("Sin Dato",inplace=True)
cliente["Localidad"].fillna("Sin Dato",inplace=True)
cliente["Latitud"].fillna("0.0",inplace=True)
cliente['Longitud'].fillna("0.0",inplace=True)         

#Mayusculas o minusculas
for j in [1,2,5]:
    for i in range(len(cliente)):
        cliente.iloc[i,j]=cliente.iloc[i,j].title()
#Conversion de tipos de datos
cliente["Longitud"]=[x.replace(',',".") for x in cliente["Longitud"]]
cliente["Latitud"]=[x.replace(',','.') for x in cliente["Longitud"]]
cliente["Latitud"]=pd.to_numeric(cliente["Latitud"],errors="coerce")
cliente["Longitud"]=pd.to_numeric(cliente["Longitud"],errors="coerce")
cliente["Longitud"]=cliente["Longitud"].astype(float)
cliente["Latitud"]=cliente["Latitud"].astype(float)        
cliente.drop('col10', axis=1, inplace=True)

'''Limpieza y normalizacion de venta
'''
# Valores Faltantes
venta.dropna(inplace=True)
#Outliers precio y cantidad. 
venta = venta[(venta['Precio']>venta['Precio'].quantile(q=0.1))&(venta['Precio']<venta['Precio'].quantile(q=0.9))]
venta = venta[venta['Cantidad']<31]
venta["Cantidad"]=venta["Cantidad"].astype(int)        




venta.to_csv('venta_calidad.csv', header=True)
cliente.to_csv('cliente_calidad.csv', header=True, index=False)