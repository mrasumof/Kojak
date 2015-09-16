 #!/usr/local/bin/python

from pymongo import MongoClient
from bson.son import SON
import pymongo
import pandas as pd
import matplotlib.pyplot as plt

client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']
coll_parsed = db['Parsed_Articles']

countries = [u'Afganistan','Albania','Alemania','Andorra','Angola','Anguila','Antigua y Barbuda','Antillas Neerlandesas',\
             u'Antartida',u'Arabia Saudi','Argelia','Armenia',\
            'Aruba','Australia','Austria',u'Azerbaiyan','Bahamas',u'Bahrein','Bangladesh',\
            'Barbados','Belice',u'Benin','Bermudas','Bielorrusia','Bolivia','Bosnia-Herzegovina',\
            'Botsuana','Brasil',u'Brunei','Bulgaria','Burundi',u'Butan',u'Belgica','Cabo Verde',\
            'Camboya',u'Camerun',u'Canada','Chad','Chile','China','Chipre','Ciudad del Vaticano',\
            'Colombia','Comoras','Congo','Corea del Norte','Corea del Sur','Costa Rica',\
            'Costa de Marfil','Croacia','Cuba','Dinamarca','Dominica','Ecuador','Egipto',\
            'El Salvador',u'Emiratos Arabes Unidos','Eritrea','Eslovaquia','Eslovenia',u'Espana',\
            'Estados Unidos','Estonia',u'Etiopia','Filipinas','Finlandia','Fiyi','Francia',\
            u'Gabon','Gambia','Georgia','Ghana','Gibraltar','Granada','Grecia','Groenlandia',\
            'Guadalupe','Guam','Guatemala','Guayana Francesa','Guernsey','Guinea',\
            'Guinea Ecuatorial','Guinea-Bissau','Guyana',u'Haiti','Honduras',u'Hungria','India',\
            'Indonesia','Iraq','Irlanda',u'Iran','Isla Bouvet','Isla Christmas','Isla Niue',\
            'Isla Norfolk','Isla de Man','Islandia',u'Islas Caiman','Islas Cocos','Islas Cook',\
            'Islas Feroe','Islas Georgia del Sur y Sandwich del Sur','Islas Heard y McDonald',\
            'Islas Malvinas','Islas Marianas del Norte','Islas Marshall',u'Islas Salomon',\
            'Islas Turcas y Caicos',u'Islas Virgenes Britanicas',\
            u'Islas Virgenes de los Estados Unidos',\
            'Islas menores alejadas de los Estados Unidos',u'Islas Aland','Israel','Italia',\
            'Jamaica',u'Japon','Jersey','Jordania',u'Kazajistan','Kenia',u'Kirguistan','Kiribati',\
            'Kuwait','Laos','Lesoto','Letonia','Liberia','Libia','Liechtenstein','Lituania',\
            'Luxemburgo',u'Libano','Macedonia','Madagascar','Malasia','Malaui','Maldivas','Mali',\
            'Malta','Marruecos','Martinica','Mauricio','Mauritania','Mayotte','Micronesia',\
            'Moldavia','Mongolia','Montenegro','Montserrat','Mozambique','Myanmar',u'Mexico',\
            u'Monaco','Namibia','Nauru','Nepal','Nicaragua','Nigeria','Noruega','Nueva Caledonia',\
            'Nueva Zelanda',u'Niger',u'Oman',u'Pakistan','Palau','Palestina',u'Panama',\
            u'Papua Nueva Guinea','Paraguay',u'Paises Bajos',u'Peru','Pitcairn','Polinesia Francesa',\
            'Polonia','Portugal','Puerto Rico','Qatar',\
            u'Region Administrativa Especial de Hong Kong de la Republica Popular China',\
            u'Region Administrativa Especial de Macao de la Republica Popular China',\
            u'Region desconocida o no valida','Reino Unido',u'Republica Centroafricana',\
            u'Republica Checa',u'Republica Democratica del Congo',u'Republica Dominicana',u'Reunion',\
            'Ruanda',u'Rumania','Rusia','Samoa','Samoa Americana',u'San Bartolome',\
            u'San Cristobal y Nieves','San Marino',u'San Martin',u'San Pedro y Miquelon',\
            'San Vicente y las Granadinas','Santa Elena',u'Santa Lucia',u'Santo Tome y Principe',\
            'Senegal','Serbia','Serbia y Montenegro','Seychelles','Sierra Leona','Singapur',\
            'Siria','Somalia','Sri Lanka','Suazilandia',u'Sudafrica',u'Sudan','Suecia','Suiza',\
            'Surinam','Svalbard y Jan Mayen',u'Sahara Occidental','Tailandia',u'Taiwan','Tanzania',\
            u'Tayikistan','Territorio Britanico del Oceano Indico',\
            'Territorios Australes Franceses','Timor Oriental','Togo','Tokelau','Tonga',\
            'Trinidad y Tobago',u'Turkmenistan',u'Turquia','Tuvalu',u'Tunez','Ucrania','Uganda',\
            'Uruguay',u'Uzbekistan','Vanuatu','Venezuela','Vietnam','Wallis y Futuna','Yemen',\
            'Yibuti','Zambia','Zimbabue',u'brasilena',u'brasileno','venezolano','venezolana']

tot_intern = 0

for each in coll_parsed.find({"international":"N"}):
    article_body = each['body']
    article_link = each['link']
    
    article_words = article_body.split()
    
    international = False
    
    for country in countries:
        if country in article_words:
            international = True
            break
    
    if international:
        ok_id = coll_parsed.update({"link":article_link},{"$set":{"international":"Y"}})
        tot_intern +=1
        print "Total International: ",str(tot_intern)+" - "+article_link
