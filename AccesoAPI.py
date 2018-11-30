import spotipy
from collections import deque
import spotipy.util as util
import networkx as nx
from networkx.readwrite import json_graph
import re
import time
import json


def crear_grafo(token, g, spotify, artista_ini, max_artistas=10):
    # Numero de Artistas a extraer
    print('Analizando ', max_artistas, ' artistas')

    # Inicializar el numero de requests y el tiempo de busqueda
    requests = 0
    start = time.time()

    # Comienzo de la busqueda y creacion del grafo
    results = spotify.search(q='artist:' + artista_ini, type='artist', limit=1)
    # Extraer solo la informacion util del artista
    artist = results['artists']['items'][0]
    print(artist)

    # Creamos una cola para ir metiendo artistas
    queue = deque()
    queue.append(artist['uri'])
    # Los nodos van a tener como atributos el nombre del artista y su popularidad
    g.add_node(artist['uri'], name=artist['name'], popularity=artist['popularity'])

    # Artistas que han sido examinados
    art_examinados = set()

    # Albunes que han sido examinados
    alb_examinados = set()

    # Crear grafo de forma iterativa
    while len(art_examinados) < max_artistas:
        print('Numero de artistas examinados:', len(art_examinados))
        artist_uri = queue.popleft()
        if artist_uri in art_examinados:
            continue

        # Anadimos al nodo el atributo "visitado" y el artista al grupo de examinados
        try:
            g.node[artist_uri]['visitado'] = True
        except KeyError:
            print("ERROR en marcar el artista " + artist_uri)
        art_examinados.add(artist_uri)

        # Obtener los albunes
        results = spotify.artist_albums(artist_uri, album_type='album,single', country='ES')
        albums = results['items']
        requests += 1
        while results['next']:  # next: URL de la proxima pagina de items. (null if none)
            # Depaginate
            results = spotify.next(results)
            albums.extend(results['items'])

        # Filtrar los albumes o singles unicos
        real_albums = dict()
        for album in albums:
            # Strip extraneous characters
            name = re.sub(r'\([^)]*\)|\[[^)]*\]', '', album['name'])  # Para borrar (Deluxe edition) y [Feat. asdf]
            name = re.sub(r'\W', '', name).lower().strip()  # Para borrar caracteres no alfanumericos
            if name not in real_albums:
                # print('Adding ' + name)
                real_albums[name] = album

        # Analizar los albumes del artista actual
        for album in real_albums:
            if album not in alb_examinados:
                # Marcar albun como analizado
                alb_examinados.add(album)
                # print('\t Examinando Album: ' + real_albums[album]['name'])

                # Obtener las canciones/pistas del album
                results = spotify.album_tracks(real_albums[album]['id'])
                requests += 1
                tracks = results['items']
                # print('Las pistas son: ', tracks)
                while results['next']:
                    results = spotify.next(results)
                    tracks.extend(results['items'])

                # Obtener los artistas colaboradores de cada album
                for track in tracks:
                    for artist in track['artists']:
                        if artist['uri'] != artist_uri:
                            # print('\t\t', artist)
                            queue.append(artist['uri'])
                            if artist['uri'] not in g:
                                # Obtener detalles de la descripcion del artista y crear nodo
                                artist = spotify.artist(artist['uri'])
                                print("\t\t", artist)
                                print("\t\t\t Adjuntando al grafo al artista: ", artist['name'])
                                g.add_node(artist['uri'], name=artist['name'], popularity=artist['popularity'])
                                # Si el artista tiene imagen cogerla, sino coger la de spotify
                                if len(artist['images']) > 0:
                                    g.node[artist['uri']]['image_url'] = artist['images'][0]['url']
                                else:
                                    g.node[artist['uri']][
                                        'image_url'] = "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg"
                            # Contar el numero de colaboraciones del artista
                            try:
                                g[artist['uri']][artist_uri]['freq'] += 1
                            except KeyError:
                                g.add_edge(artist['uri'], artist_uri, freq=1)

        print("Artista Analizado")

    # Mostras estadisticas
    print('Adjuntados ' + str(nx.number_of_nodes(g)) + ' nodos en ' + str(time.time() - start) + ' segundos con ' + str(
        requests) + ' solicitudes')
    print(str(len(art_examinados)) + ' artistas analizados')


if __name__ == '__main__':
    scope = 'user-library-read'
    username = 'David Córdoba Ruiz'
    token = util.prompt_for_user_token(username, scope)
    # Acceso a la API de Spotify y creacion del grafo
    spotify = spotipy.Spotify(auth=token)
    g = nx.Graph(name='Analisis Artistas Spotify')

    crear_grafo(token, g, spotify, 'Mago de Oz', 29)
    crear_grafo(token, g, spotify, 'Malú', 29)
    crear_grafo(token, g, spotify, 'Rosario Flores', 29)
    crear_grafo(token, g, spotify, 'Xuso Jones', 29)
    crear_grafo(token, g, spotify, 'SFDK', 29)
    crear_grafo(token, g, spotify, 'El Barrio', 29)
    # eliminar_gradobajo(g, 2)
    # eliminar_novisitados(g)
    print(nx.info(g))
    g_json = json_graph.node_link_data(g)
    with open('g_json.json', 'w') as f:
        json.dump(g_json, f, indent=1)
    print('Grafo guardado en g_json.json')
