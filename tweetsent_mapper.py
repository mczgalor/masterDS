#/usr/bin/env python2.7


##Importacion de librerias necesarias

import json, string, sys
import re

##Construccion de diccionario como se indica en la practica

scores = {"key":"value"}

def dic_sentimientos():

    file = open("AFINN-111.txt") ## caso de tweets en ingles
    for line in file:
        term, score = line.split("\t") 
        scores[term] = int(score) 


## definicion del principal

def main():

 dic_sentimientos()
## carga de los datos descargados en un fichero .json y filtramos por lenguaje y pais
 
 for line in sys.stdin:
    ## Eliminamos espacios en blanco
    line = line.strip()

    ## filtrar datos por pais y lenguaje
    data = ''
    try:
         data = json.loads(line)
    except ValueError as detail:
         sys.stderr.write(detail.__str__() + "\n")
         continue

    if 'text' in data and data['lang'] is not None and data['lang'] == "en" and data['place'] is not None and data['place']['country_code'] == "US":

        ## extraer texto del tweet en minusculas y extraer region 
       text = data['text'].lower()
       region = data['place']['full_name']
        ## decodificar en el formato adecuado, eliminar puntuacion e ignorar los signos raros
       text = text.encode('utf-8')
       text   = text.translate( string.maketrans(string.punctuation, ' ' * len(string.punctuation)) )
       text= unicode(text, errors='ignore')

       ## Busqueda de las palabras de los tweets en el diccionario, asignacion de valor de sentimiento, suma de valores en cada tweet y division por numero de palabras en la suma. Antes de la suma, se seleccionan los tweets con informacion de estado. Como hay tweets donde la informacion de 'place' te da lugar y estado  pero otros dan estado y pais o solo lugar, etc, se selecionan solo aquellos donde la informacion del estado (en el codigo correspondiente) se encuentra en la lista.  

       ## establecimiento a cero de los contadores 
       punt = 0
       num_pal = 0
       twestado = region.split()
       ##codigo de estados
       estaname=['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
      
       if twestado[1] in estaname:
        for palabra in text.split():
       ## asignacion valor y suma
          if palabra in scores:
            punt = punt + scores[palabra]
            num_pal = num_pal + 1
       ## normalizacion por numero de palabras usada en la suma
          if num_pal > 0:
            punt_total = int(punt/num_pal)
       ## salida, se imprime por cada tweet la region y el valor de la puntuacion de sentimiento  
            print "\t".join([twestado[1], str(punt_total)])


if __name__ == '__main__':
    main()



