import urllib
import ssl
import pandas as pd
from bs4 import BeautifulSoup

# Función para devolver una cadena única separando los elementos por comas a partir de los elementos de una lista
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
    

# Con archivos locales guardados con el navegador
file1 = "file:///F:\PEC1WEBSCRAPING\Buscador de Operadores _ Dirección General de Ordenación del Juego.html"
file2 = "file:///F:\PEC1WEBSCRAPING\Buscador de Operadores _ Dirección General de Ordenación del Juego2.html"
file3 = "file:///F:\PEC1WEBSCRAPING\Buscador de Operadores _ Dirección General de Ordenación del Juego3.html"

# Creación de contexto SSL 
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# URL remotas
# CONCURSOS
url1 = "https://www.ordenacionjuego.es/es/operadores/buscar?field_got_tid=All&field_gat_tid=All&field_gct_tid=999993&field_dominio="
# APUESTAS
url2 = "https://www.ordenacionjuego.es/es/operadores/buscar?field_got_tid=All&field_gat_tid=999992&field_gct_tid=All&field_dominio="
# OTROS JUEGOS
url3 = "https://www.ordenacionjuego.es/es/operadores/buscar?field_got_tid=999991&field_gat_tid=All&field_gct_tid=All&field_dominio="

urls = (url1,url2,url3)
#urls = {file1,file2,file3}


# CON URL REMOTA

# Dos alternativas:
#   - CASO 1: No almacenar el tipo de licencia singular (concursos, apuestas u otros)
#   - CASO 2: Almacenar el tipo de licencia
# NOTA: Se ha implementado sólo el CASO 1, para el caso 2 habría que crear un campo adicional para almacenar el tipo de 
# licencia; en cada iteración un tipo diferente por lo que habría empresas repetidas con mismo nombre, url pero distintas 
# licencias. 
# Almacenar el tipo de licencia podría ser útil por ejemplo si se desea realizar un estudio más específico por categorías

# CASO 1 (sólo es necesario un diccionario para las tres iteraciones, el diccionario no admite duplicados en el índice)
# ---------------------------------------------------------------------------------------------------------------------
# datURL almacena los nombres y urls 

datURL = dict()

for url in urls:
    
    pagina = urllib.request.urlopen(url,context=ctx)
    soup = BeautifulSoup(pagina,"lxml")
    contenidos = soup.find("div",class_="view-content").find_all("a")

    for empresa in contenidos:
        nombre = empresa.text.strip()
        link = "https://www.ordenacionjuego.es" + empresa.get("href").strip()
        datURL[nombre]=link
        print(nombre,link)
        
#print(datURL)
     
# Web scraping de empresas individuales   
# Con los resultados almacenados en el diccionario datURL, se realiza scraping sobre cada página individual de cada empresa

datasetFinal = []

#url1 = "file:///F:\PEC1WEBSCRAPING\Bluesblock, SA _ Dirección General de Ordenación del Juego.html"

#url1="https://www.ordenacionjuego.es/es/op-antena3juegos"


#if url1 != '':
for url in datURL.values():

    #pagina = urllib.request.urlopen(url)
    pagina = urllib.request.urlopen(url, context=ctx)
    soup = BeautifulSoup(pagina,"lxml")
    contenidos = soup.find(attrs={'id':'operatorContent'})

    # Campo NOMBRE
    nombre = contenidos.find(attrs={'id':'operatorTitle'}).text.strip() # Strip para eliminar posibles espacios

    # Campo LICENCIAS(SINGULARES)
    licencias = contenidos.find(attrs={'id':'operatorSingular'}).find_all('li')
    lic=[]

    for licencia in licencias:
    	lic.append(licencia.text)
        
    # Se procesa para que se almacenen con la forma Concursos,Lotería,... en una cadena de texto única 
    # Se podrían haber almacenado como variables binarias (Concursos=Sí/No, Loterías=Sí/No,...)

    campoLicencias = lista_cadena(lic)
    
    # Campo DOMINIOS
    dominios = contenidos.find(attrs={'id':'opetatorBody'}).find_all('li')
    #print(dominios)
    dom=[]
    #if not dominios:
    #    dom = 'Sin_dominio'
        
    #else:
    #    for dominio in dominios:
    #    	if dominio.find('a'):
	#           	dom.append(dominio.find('a').text)

    if dominios:
        for dominio in dominios:
        	if dominio.find('a'):
	           	dom.append(dominio.find('a').text)
            
    # Se procesan los dominios recuperados para dejarlos en una única cadena
     
    campoDominios = lista_cadena(dom)

    # Se añaden al total de observaciones
    
    datasetFinal.append((nombre,campoLicencias,campoDominios))

# Peculiaridades de los datos almacenados
#   1. Licencias: puede haber operadores que al buscar en el formulario aparezcan como poseedores de licencias, pero que
#      al acceder a su URL específica no muestren ninguna licencia (ej: antena3juegos). Si se consulta la tabla se puede ver
#      que tiene la licencia extinguida. Se especifica como 'Sin licencia vigente'
#   2. Dominios: en el caso de operadores que no tengan dominio, se especifica como 'Sin dominio'
    
# ALMACENAMIENTO EN DATAFRAME
#df['date'] = pd.to_datetime(df['date']) # yyyy-mm-dd

df = pd.DataFrame(datasetFinal, columns=['Nombre','Licencias','Dominios'])
#df.head()
#df.tail()
print(df)
df.to_csv('F:\\operadoresDGOJ.csv',index=False, encoding='utf-8')
#df = pd.read_csv('operadores.csv',encoding='utf-8')

#for valores in zip(datURL.keys(),datURL.values()):
#    print(valores)


