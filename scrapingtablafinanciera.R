Mediante el siguiente código en R de la pagina web http://ranking-empresas.eleconomista.es/sector-9200.html
extraigo los resultados de la tabla
install.packages("xml2")
library("xml2")
library("rvest")
url.facturacion<- "http://ranking-empresas.eleconomista.es/sector-9200.html"
tabla_temp_fact<- read_html(url.facturacion)
tabla_temp_fact<- html_nodes(tabla_temp_fact, "table")
tabla_temp_fact
length(tabla_temp_fact)
sapply(tabla_temp_fact,class)
html_table(tabla_temp_fact,fill=TRUE)
#sapply(tabla_temp, function(x) dim(html_table(x, header=false, fill = TRUE)))
facturacion<- html_table(tabla_temp_fact,fill=TRUE)
facturacion
write.csv(facturacion, file="facturacion.csv") #guardamos en un archivo CSV.
 @srodriguezcep
  
            
 
Write 
