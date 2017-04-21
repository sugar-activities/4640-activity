from ConfigParser import SafeConfigParser


def parsear(listaSecciones):

    parser = SafeConfigParser()
    parser.read('config.ini')
    nro_items = parser.getint('initialize','items')
    etiqueta = 'seccion'
    #listaSecciones = []
    for i in range(nro_items):
        etiqueta = etiqueta + str(i)      
        #print parser.get(etiqueta, 'info')
        list_seccion=[]
        list_seccion.insert(0, parser.get(etiqueta, 'name'))
        list_seccion.insert(1, parser.get(etiqueta, 'info'))
        list_seccion.insert(2, parser.get(etiqueta, 'image'))
        listaSecciones.insert(i,list_seccion)
        etiqueta = 'seccion'


