#/usr/bin/env python2.7

##Importacion de librerias necesarias

import sys

## definicion del principal

def main():

    ## establecimiento a cero de los contadores y el nombre de la region
     
    char_region  = None
    cuentatotal = 0
    num_cuentas = 0

    ## carga de los datos salida del mapper 
    for line in sys.stdin:
        ## Eliminacion de espacios en blanco
        line = line.strip()
        region, puntuacion = line.split('\t')
        
        ## suma de puntuaciones por cada region 
        try:
            puntuacion = float(puntuacion)
        except ValueError:
            continue 

        if char_region == region:      
               cuentatotal =  cuentatotal + puntuacion
               num_cuentas = num_cuentas + 1
        ## toma unico valor si solo hay un valor en la region
        else:   
           if char_region:
                 print '%s\t%s' % (char_region, cuentatotal/num_cuentas)
           cuentatotal = puntuacion
           char_region  = region
           num_cuentas = 1
    ## impresion de salida, region y numero de puntuacion calculada como la suma de puntuaciones de los tweets de cada region por el numero de tweets sumados en dicha region

    if char_region == region:
        print '%s\t%s' % (char_region, cuentatotal/num_cuentas)
 
if __name__ == '__main__':
    main()

