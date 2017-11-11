#Limpieza del DataSet
getwd()
datos_aux<-read.csv2("provincias.csv", sep=",",na.strings = "NA")
datos_aux
datos=data.frame(datos_aux$Nombre, datos_aux$Población,
                 datos_aux$Porcentaje.población,datos_aux$Densidad..hab..km².,
                 datos_aux$Comunidad.autónoma)
write.csv(datos, file="datos.csv")