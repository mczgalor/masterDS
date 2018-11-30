import networkx as nx
from networkx.readwrite import json_graph
import json
import operator
import io
import community


def detect_communities(g):
    print('Buscando comunidades...')
    partition = community.best_partition(g)
    print('Proceso finalizado')
    size = float(len(set(partition.values())))
    if (len(g.nodes()) <= 50 and size < 4) or (len(g.nodes()) > 50):
        print('Numero comunidades en la componente: ', size)
        count = 0.
        dicc = {}
        for com in set(partition.values()):
            count = count + 1.
            list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
            # print('Comunidad', count, 'tiene tamaño', len(list_nodes))
            for id in list_nodes:
                dicc[id] = int(count)
        nx.set_node_attributes(g, 'comunidad', dicc)
        print('Atributo comunidad añadido al grafo')


def unir_comps(comp1, comp2):
    # comp1 comp2 son ficheros json
    f = io.open(comp1, "r")
    h = io.open(comp2, "r")
    json1 = json.load(f)
    json2 = json.load(h)

    comp1 = json_graph.node_link_graph(json1, directed=False)
    comp2 = json_graph.node_link_graph(json2, directed=False)
    g = nx.compose(comp1, comp2)
    print('Grafo final: ', nx.info(g))
    with open('total.json', 'w') as f:
        json.dump(comp, f, indent=1)
    print('Grafo guardado en total.json')


def eliminar_bbcero(g, bb=0.0):
    # Eliminar recursivamente todos los nodos con grado menor que 2
    print('Eliminando recursivamente todos los nodos con betweenness 0.0:')
    eliminados = 0

    for nodo in nx.get_node_attributes(g, 'betweenness'):
        # Dividimos entre 515 que es el grado max de la comp2
        if g.node[nodo]['betweenness'] <= bb:
            g.remove_node(nodo)
            eliminados += 1

    print('Numero de nodos eliminados: ', eliminados)


def eliminar_gradobajo(g):
    # Eliminar recursivamente todos los nodos con grado menor que 2
    print('Eliminando recursivamente con degreeCent menor que 0.001')
    eliminados = 0

    for nodo in nx.get_node_attributes(g, 'degreeCent'):
        # Dividimos entre 515 que es el grado max de la comp2
        if g.node[nodo]['degreeCent'] < 0.001:
            g.remove_node(nodo)
            eliminados += 1

    print('Numero de nodos eliminados: ', eliminados)


if __name__ == '__main__':
    f = io.open("g_json.json", "r")
    json_data = json.load(f)
    g = json_graph.node_link_graph(json_data, directed=False)

    print('Informacion sobre el grafo de entrada: ', nx.info(g))
    print("\nCOMPONENTES CONEXAS")
    i = 0

    for comp in nx.connected_component_subgraphs(g):
        i += 1
        print('Comp ', i, ': ')
        # for node, atts in comp.nodes(data=True):
        # print(atts['name'], '\t')
        print('\tEl tamano de la componente', i, ' es ', len(comp.nodes()))
        if len(comp.nodes()) > 1:
            # degree_w es el grado con pesos para saber cantantes que ha colaborado más con otros
            # degreeCent para saber con cuantos colaboradores distintos ha interactuado
            degree_w = nx.degree(comp, weight='freq')
            nx.set_node_attributes(comp, 'degree_weight', degree_w)
            max_degree_w = max(degree_w.items(), key=operator.itemgetter(1))
            print("\t\tEl cantante o grupo con mayor numero de colaboraciones: ", comp.node[max_degree_w[0]]['name'])

            degreeCent = nx.degree_centrality(comp)
            nx.set_node_attributes(comp, 'degreeCent', degreeCent)
            maxs_d = max(degreeCent.items(), key=operator.itemgetter(1))
            print("\t\tEl cantante o grupo con mayor numero de colaboraciones con cantantes distintos: ",
                  comp.node[maxs_d[0]]['name'])
            del degreeCent[maxs_d[0]]
            second_maxs_d = max(degreeCent)
            print("\t\tEl segundo cantante o grupo con mayor numero de colaboraciones con cantantes distintos: ",
                  comp.node[second_maxs_d]['name'])

            closeness = nx.closeness_centrality(comp)
            nx.set_node_attributes(comp, 'closeness', closeness)
            maxs_cl = max(closeness.items(), key=operator.itemgetter(1))
            print("\t\tEl cantante con mas impacto en la red de colaboraciones: ", comp.node[maxs_cl[0]]['name'])

            betweenness = nx.betweenness_centrality(comp)
            nx.set_node_attributes(comp, 'betweenness', betweenness)
            maxs_b = max(betweenness.items(), key=operator.itemgetter(1))
            print(
                "\t\tEl cantante o grupo que muestra un abanico mas amplio de colaboraciones, esto es, el que colabora con cantantes de tematica mas diversa: ",
                comp.node[maxs_b[0]]['name'])
            vecinos = comp.neighbors(maxs_b[0])
            vec = [comp.node[ven]['name'] for ven in vecinos]
            print("\tColaboradores: ", vec)
            del betweenness[maxs_b[0]]
            second_maxs_b = max(betweenness.items(), key=operator.itemgetter(1))
            vecinos2 = comp.neighbors(second_maxs_b[0])
            print("\t\tEl segundo cantante o grupo con colaboraciones de tematicas diversas: ",
                  comp.node[second_maxs_b[0]]['name'])
            vec2 = [comp.node[ven2]['name'] for ven2 in vecinos2]
            print("\tColaboradores: ", vec2)

            pagerank = nx.pagerank(comp)
            nx.set_node_attributes(comp, 'pagerank', pagerank)
            maxs_p = max(pagerank.items(), key=operator.itemgetter(1))
            print("\t\tEl cantante con mas posibilidades de ser solicitado para colaborar: ", comp.node[maxs_p[0]]['name'])

            # Modificacion para visualizacion
            if len(comp.nodes()) > 50:
                eliminar_gradobajo(comp)
                eliminar_bbcero(comp)

            # Deteccion de comunidades en cada componente
            detect_communities(comp)

            comp = json_graph.node_link_data(comp)
            with open('grafo%s.json' % i, 'w') as f:
                json.dump(comp, f, indent=1)
            print('Componente guardada en grafo%s.json' % i)

    unir_comps('grafo1.json', 'grafo2.json')
    dg1_dg2_path = nx.shortest_path(g, source="spotify:artist:5sUrlPAHlS9NEirDB8SEbF",
                                    target="spotify:artist:56n1NeXsTOOxjX3Z4lVMTJ")

    print("Cuantos grados de conexion hay entre Alejandro Sanz y SFDK: ", len(dg1_dg2_path) - 1)
