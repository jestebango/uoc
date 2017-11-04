install.packages("xml2")
library("xml2")
library("rvest")
url.provincias<- "https://es.wikipedia.org/wiki/Anexo:Provincias_y_ciudades_aut%C3%B3nomas_de_Espa%C3%B1a"
tabla_temp<- read_html(url.provincias)
tabla_temp <- html_nodes(tabla_temp, "table")
tabla_temp
length(tabla_temp)
sapply(tabla_temp,class)
html_table(tabla_temp,fill=TRUE)
#sapply(tabla_temp, function(x) dim(html_table(x, header=false, fill = TRUE)))
provincias<- html_table(tabla_temp,fill=TRUE)
provincias
write.csv(provincias, file="provincias.csv") #guardamos en un archivo CSV.
getwd()
