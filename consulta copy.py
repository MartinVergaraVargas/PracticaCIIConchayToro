# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 12:41:03 2022

@author: grojasg
"""

import requests
import pandas as pd
import json
import openpyxl
#Conexión con API
apiUrl = "https://cyt2.mastertic.cl/api/v1"
apiBaseUrl = "https://cyt2.mastertic.cl"
email = "genoveva.rojas@conchaytoro.cl"      
password="genoveva.rojas@conchaytoro.cl"
tokenAccess = None
tokenRefresh = None

def token():
    info = dict({"email": email, "password": password})
    respuesta = requests.post(f"{apiBaseUrl}/login/", info)
    respuesta.raise_for_status()
    if respuesta.status_code == 200:
        #print(respuesta.json())
        return respuesta.json()
        
def refresh():
    info = dict({"refresh": tokenRefresh})
    respuesta = requests.post(f"{apiBaseUrl}/login/refresh/", info)
    respuesta.raise_for_status()
    if respuesta.status_code == 200:
        token = respuesta.json()
        return token['access']

def getFundosByValle(valleId):
    headers = dict({"Authorization": f"Bearer {tokenAccess}"})
    #print(headers)
    respuesta = requests.get(f"{apiUrl}/fundos/valle/{valleId}/",headers=headers)
    respuesta.raise_for_status()
    if respuesta.status_code == 200:
        return respuesta.json()
      
def getCuartelesByFundo(fundoId):
    headers = dict({"Authorization": f"Bearer {tokenAccess}"})
    #print(headers)
    #params = dict({})
    respuesta = requests.get(f"{apiUrl}/cuarteles/byfundo/{fundoId}/",headers=headers)
    respuesta.raise_for_status()
    if respuesta.status_code == 200:
        return respuesta.json()

def getCuartelRaster(fundoId,cuartelId,fecha):
    headers = dict({"Authorization": f"Bearer {tokenAccess}"})
    #print(headers)
    respuesta = requests.get(f"{apiBaseUrl}/proncos/api/v1/raster/{fundoId}/{cuartelId}/{fecha}",headers=headers)
    respuesta.raise_for_status()
    if respuesta.status_code == 200:
        data = respuesta.content
        return data

def getFundoRasters(fundoId,fecha):
    headers = dict({"Authorization": f"Bearer {tokenAccess}"})
    #print(headers)
    respuesta = requests.get(f"{apiBaseUrl}/proncos/api/v1/raster/{fundoId}/{fecha}",headers=headers)
    respuesta.raise_for_status()
    if respuesta.status_code == 200:
        data = respuesta.content
        return data


def getRendimientoByFundo(fundoId):
    headers = dict({"Authorization": f"Bearer {tokenAccess}"})
    #print(headers)
    respuesta = requests.get(f"{apiBaseUrl}/proncos/api/v1/cuarteles/rendimiento/cosecha/byfundo/{fundoId}/",headers=headers)
    respuesta.raise_for_status()
    if respuesta.status_code == 200:
        data = respuesta.json()
        return data
    
def getFechaRasterFundoCuartel(fundoId):
    headers = dict({"Authorization": f"Bearer {tokenAccess}"})
    #print(headers)
    respuesta = requests.get(f"{apiUrl}/fundos/{fundoId}/rasters/all",headers=headers)
    respuesta.raise_for_status()
    if respuesta.status_code == 200:
        data = respuesta.json()
        return data

tokens = token()
tokenAccess = tokens.get('access')
tokenRefresh = tokens.get('refresh')
tokenAccess=refresh()
#%%
print(tokenAccess)

raster = getCuartelRaster(2,114,'2022-11-04')
with open('lourdesCuartel114.tif',"wb") as f :
    f.write(raster)
print(getRendimientoByFundo(2))
print(getFechaRasterFundoCuartel(2))


valle1 = getFundosByValle(1)
valle2 = getFundosByValle(2)
valle3 = getFundosByValle(3)
valle4 = getFundosByValle(4)
valle5 = getFundosByValle(5)
valle6 = getFundosByValle(6)
valle7 = getFundosByValle(7)
valle8 = getFundosByValle(8)



print("leyo fundos")
fundos = valle1+valle2+valle3+valle4+valle5+valle6+valle7
cuarteles = []
for i in range(0,len(fundos)) :
    datos=getCuartelesByFundo(fundos[i]['id'])
    print("analizando fundo: "+fundos[i]['nombre'])
    for j in range(0,len(datos)) :
        cuartel={}
        cuartel['fundo'] = fundos[i]['nombre']
        cuartel['num'] = datos[j]['nombre']
        cuartel['aptitud'] = datos[j]['aptitud']['nombre']
        cuartel['sistConduccion'] = datos[j]['sistema_conduccion']['nombre']
        cuarteles.append(cuartel)

wb = openpyxl.Workbook()
hoja = wb.active
# Crea la fila del encabezado con los títulos
hoja.append(('Fundo', 'Cuartel', 'aptitud', 'SistConduccion'))
for cuartel in cuarteles:
    hoja.append((cuartel['fundo'],cuartel['num'],cuartel['aptitud'],cuartel['sistConduccion']))
wb.save('infoCuarteles.xlsx')
#for i in range(0,len(cuarteles)) :
#    print(cuarteles[i])


