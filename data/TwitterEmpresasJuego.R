#Script para la extracción de Twitter a través de API  (Usuarios empresas juego)

  #App previamente creada para esta práctica 
  #Sitio de la App "Juego" https://apps.twitter.com/app/14410452/show (con login twitter)
  
  #Carga de librería twitteR con las funciones de extracción
    library(twitteR)
  #Carga de la librería ROAuth para autenticación en la conexión
    library(ROAuth)
  
  #Credenciales para la conexión a través de dev.twitter.com
    clave_API <- "hash_clave_API"
    clave_API_Secreta <- "hash_clave_API_secreta" 
    token <- "hash_token"
    token_secreto <- "hash_token_secreto"
  
  # Establecimiento de la conexión con la API de Twitter
    #Función setup_twitter_oauth gestona el conjunto de credenciales de autenticación 
    #para una sesión de la librería TwitterR del paquete httr paquete que, a su vez, 
    #permite configurar funciones para trabajar con protocolos de autenticación
    setup_twitter_oauth (clave_API, clave_API_Secreta, token, token_secreto)
  
  #Creamos lista completa para toda las empresas (tengan o no usuario de twitter)
    listadeusuarios <- c('Bluesblock, SA','CodereApuestas','Concursos_multiplataformas', 'CasinoGranMad','Eurojuego','JS2015Games', 'loterias_es', 'Suertia', 'MARCAapuestas', '888pokerSpain', 'JueggingES', 'Starvegas SA', 'Betfair_ES', 'BetwayES', 'CasinoBcnES', 'sportium', 'ijuego', 'ebingo_es','apuestasRETA','bwin_es','Paston_es','EurobetInternational','circus_es','GoldenPark_Esp','GtechSpain','bet365_es','Interwetten_Esp','Titanbet_Espana','KambiSpain','luckia_es','Marathonbet_es','merkurmagic','Paf consulting','carcaj','StarCasino_ES','PokerStarsSpain','wanabet_es','planetwin365es','Kirolbet_es','WilliamHillES','Yobingo','Casino777es','botemania','Cigagameonline','HillsideEspa_aLeisure','NetEntGamming','PrimaNetworks','PtEntretenimientoonline','enracha','BingoTombola','ventura24','vivelasuerte')
  
  #Lanzamos búsqueda datos sobre usuarios específicos que si tienen cuenta de Twitter
  #Función lookupUsers permite extraer la información simultaneamente de un conjunto 
  #de usuarios sin cargar la API con cola de solicitudes
    usodetwitter <- lookupUsers(c('CodereApuestas','CasinoGranMad','Eurojuego','loterias_es', 'Suertia', 'MARCAapuestas', '888pokerSpain', 'JueggingES', 'Betfair_ES', 'BetwayES', 'CasinoBcnES', 'sportium','ebingo_es','apuestasRETA','bwin_es','Paston_es','circus_es','GoldenPark_Esp','bet365_es','Interwetten_Esp','Titanbet_Espana','luckia_es','Marathonbet_es','merkurmagic','StarCasino_ES','PokerStarsSpain','wanabet_es','planetwin365es','Kirolbet_es','WilliamHillES','Yobingo','Casino777es','botemania','enracha','BingoTombola','ventura24','vivelasuerte'), includeNA=TRUE)
  
  #Devuelve variables para cada usuario: 
    #description, describe el usuario
    #statusesCount, recoge la actividad del usuario, incluyendo retweets
    #followersCount, recoge el número de seguidores del usuario
    #favoritesCount, recoge los tweets o retweets que han sido marcados como favoritos por el usuario 
    #friendsCount, recoge el número de usuarios a los que sigue este usuario
    #url, incorpora la dirección web que ha incluido el usuario
    #name, recoge el nombre del usuario en su cuenta
    #created, indica en que fecha fue creado el usuario
    #protected, indica si los tweets e información de la cuenta está o no protegida
    #verified, indica si el usuario ha verificado la cuenta
    #screenName, indica el nombre o alias del usuario
    #location, aparece recogido si existe una localización específica de usuario           
    #lang, indica el idioma autoidentificado por el usuario
    #id, es el número de identificación único del usuario para twitter
    #listedcount, indica el número de listas públicas del que el usuario es parte
    #followRequestSent, si se ha enviado solicitud de amistad
    #profileImageUrl, sitio donde se encuentra la imagen del perfil del usuario
  #almacenamos los resultados para las variables extraidas en matriz "usodetwitter"


