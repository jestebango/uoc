import urllib
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

pd.set_option('display.max_colwidth', -1)

#------------------------------------------------------------------------------------------------------------
# FUNCIONES
#------------------------------------------------------------------------------------------------------------

# Devuelve una única separando los elementos por comas a partir de los elementos de una lista
def lista_cadena(lista):
    
    enCadena=""
    if (len(lista)==1):
        enCadena=enCadena+lista[0]
    else:
        for elto in lista:            
            enCadena=enCadena+elto
            if (elto!=lic[len(lic)-1]):
                enCadena=enCadena+','           
    return enCadena 

# Función que realiza una petición POST con los datos del formulario y devuelve una respuesta
# Sólo se realiza la petición cuando hay como mucho 5 epígrafes (LÍMITE IMPUESTO POR EL FORMULARIO)

def peticionPOST(nom='',direccion='',cpostal='',municipio='',epigrafes=''):
    
    urlSUBMIT = "http://www.camaras.org/censo/cgi-bin/listado.php"
    valoresForm = {'empresa' : nom,'direccion' : direccion,'cpostal' : cpostal,'municipios':municipios,'epigrafes' : epigrafes,'seccion':seccion}
    param = urllib.parse.urlencode(valoresForm)
    param = param.encode('ascii')
    req = urllib.request.Request(url=urlSUBMIT,data=param,method='POST')
    res = urllib.request.urlopen(req)
    return res
    

# Función que devuelve en forma de dataframe nombre, url y localidad de cada delegación
# de la lista de resultados

def extractURL(url):
    
    soup = BeautifulSoup(url,"lxml")    
        
    contenidos = soup.find("form").find_all(attrs={'class':'txt10gris'})
    
    nombre = list()
    enlace = list()
    localidad = list()
       
    for entrada in contenidos[::2]:

        nombre.append(entrada.find("a").text)
        enlace.append("http://mercurio.camaras.org/censo/" + entrada.find("a").get("href"))
        localidad.append(entrada.findNextSibling().text.strip())
        
    sedes = pd.DataFrame({'Nombre':nombre,'Enlace':enlace,'Localidad':localidad},columns=['Nombre','Enlace','Localidad'])  
    return sedes


# Recibe el dataframe con nombre, enlace y delegación y lo completa accediendo a cada página con la dirección
def extraerDeleg(df):
    
    direcciones = list()
    
    for direc in df.Enlace:
        
        print('Extrayendo dirección de: ' + direc)
        res = urllib.request.urlopen(direc)
        soup = BeautifulSoup(res,"lxml")  
        contenidos = soup.find_all(attrs={'class':'txt11gris'})
        #nomFinal = contenidos[0].text
        linea1 = contenidos[1].text
        linea2 = contenidos[2].text
        dirFinal = linea1 + ' , ' + linea2
        print(dirFinal)
        direcciones.append(dirFinal)
    
    # Las direcciones se añaden al dataframe como una variable adicional
    df['DirCompleta'] = direcciones    
        
    return(df)

#*****************************************************************************************

#codigos = "9692,9693,9694,9695,9696,9697,9821,9822,9825" # Problema: el formulario sólo admite 5 códigos como máximo
#incluir 9825 ORGANIZ. APUESTAS DEPORTIVAS, LOTERIA
codigos = "9825"
direccion=''
cpostal=''
municipios=''
seccion='censo'

# DATASETS cargados en memoria (operadores y código de localidades obtenido del INE)

# El código de municipio se compone de cinco dígitos: los dos primeros corresponden
# al código de la provincia y los tres restantes al del municipio dentro de ésta. 
# Asimismo se publica un sexto dígito de control que, asignado mediante una regla
# de cálculo, permite la detección de errores de grabación y codificación.


dfOperadores= pd.read_csv('operadoresDGOJ.csv',encoding='utf-8')

try:
    dfCM = pd.read_excel('10codmun.xls',header=1,dtype={'CPRO':str,'CMUN':str})
    dfCM['COD'] = dfCM['CPRO'] + dfCM['CMUN'] # Se unifican columnas y se elimina dígito de control
    dfCM['COD'] = dfCM['COD'].apply(lambda x: x[:-1])
    dfCM = dfCM.drop(['CPRO','CMUN'],axis=1) # Se eliminan columnas redundantes para liberar memoria
except:
    print("Fichero de códigos de municipios INE no está en la ruta del script")

# Almacena resultados de todas las consultas realizadas (en cada iteración una empresa)
dfURL = pd.DataFrame(columns=['Nombre','Enlace','Localidad'])

# PRIMER PASO: Scracping de URLs de las empresas operadoras de juego (resultados de las tablas)

for datos in dfOperadores.Nombre:
    
    nombreReducido = datos.split(',')[0]
    print('Procesando: ' + datos + ' #### Keyword en formulario: ' + nombreReducido)
    try:
        respuesta = peticionPOST(nom=nombreReducido,epigrafes=codigos)
        dfSedes = extractURL(respuesta)
    
        #Si no hay resultados, se vuelve a buscar pero sólo con la primera palabra de la empresa (Ej: CODERE ONLINE -> CODERE)
        if dfSedes.empty:
                
            nombreReducido2 = datos.split(' ')[0]
            print(nombreReducido + " no muestra resultados. Probando con: " + nombreReducido2)    
            respuesta = peticionPOST(nom=nombreReducido2,epigrafes=codigos)
            dfSedes = extractURL(respuesta)                    
    
        dfURL = dfURL.append(dfSedes)
    except: 
        print('Error al consultar los datos de ' + datos)

#dfURL.to_csv('ficheroURL.csv',index=False,encoding='utf-8')
#eliminar duplicados antes de consultas

# SEGUNDO PASO: Scraping de las direcciones de cada URL (delegación)

dfSedesFinal = extraerDeleg(dfURL)
print(dfSedesFinal)
dfSedesFinal.to_csv('ficheroSedes.csv',index=False, encoding='utf-8')


# BUCLE PRINCIPAL: para cada empresa lo ideal sería
#    1. Reducir el nombre (eliminación de SA, SAU,...)
#    2. Enviar formulario sólo con nombre
#       Posibles resultados:
#         i. (BUCLE) Se devuelven más de 50 empresas -> relanzar búsqueda por localidades (nombre + localidad)
#            Posibles resultados:
#               a. Se devuelven más de 50 empresas en una misma localidad 
#               b. Se devuelven menos de 50 empresas en una misma localidad
#               c. Localidad sin resultados#                        
#         ii. No se devuelve ninguna empresa (reducir el nombre de la empresa a la primera palabra)
#         iii. Resultados menores de 50 empresas
#
# Por simplicidad no se relanzan las búsquedas (más específicas) y se almacenan los resultados
# devueltos, teniendo en cuenta que se pierde información (hay más delegaciones en esa localidad).

