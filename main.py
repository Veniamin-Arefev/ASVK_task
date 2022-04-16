import os
from argparse import ArgumentParser, FileType, ArgumentError
from math import cos, sin, atan2, pi, sqrt
import networkx
import traceback
import matplotlib.pyplot


def parse_file(file_object):
    file_extension = os.path.splitext(file_object.name)[-1]
    if (file_extension.lower() == ".gml"):
        return networkx.Graph(networkx.parse_gml(file_object, label='id'))
    elif (file_extension.lower() == ".graphml"):
        wrong_labels_graph = networkx.Graph(networkx.read_graphml(file_object))  # change 'id' to id
        mapping = {str(i): i for i in range(len(wrong_labels_graph.nodes))}
        return networkx.relabel_nodes(wrong_labels_graph, mapping)
    else:  # invalid file extension
        raise ValueError("Invalid file extension")


def geo_to_kilometers(lat1, lon1, lat2, lon2):  # Haversine_formula
    earth_radius = 6378.137  # Radius of earth in KM
    a = cos(lat1 * pi / 180) * cos(lat2 * pi / 180) * sin((lon2 - lon1) * pi / 360) ** 2 \
        + sin((lat2 - lat1) * pi / 360) ** 2
    return 2 * earth_radius * atan2(sqrt(a), sqrt(1 - a))


def calculate_distance_and_delay(my_graph_object):
    for it_edge in list(graph_object.edges(data=True)):
        node1 = my_graph_object.nodes()[it_edge[0]]
        node2 = my_graph_object.nodes()[it_edge[1]]
        graph_object[it_edge[0]][it_edge[1]]['distance'] = \
            geo_to_kilometers(lat1=node1['Latitude'], lon1=node1['Longitude'],
                              lat2=node2['Latitude'], lon2=node2['Longitude'])

    for it_edge in list(graph_object.edges(data=True)):
        graph_object[it_edge[0]][it_edge[1]]['delay'] = graph_object[it_edge[0]][it_edge[1]]['distance'] * 4.8
    pass


def criteria_1(old_graph_object):
    new_graph_object = networkx.Graph()
    new_graph_object.graph.update(old_graph_object.graph)

    nodes_list = list(old_graph_object.nodes)
    nodes_list.sort()

    total_delay = [0 for i in nodes_list]
    for i in nodes_list:
        used_list = [False for i in nodes_list]
        path_delay_list = [float('+inf') for i in nodes_list]
        path_delay_list[i] = 0.0
        used_list[i] = True
        nodes_to_go = [i]
        while (len(nodes_to_go) > 0):
            min_node = nodes_to_go[0]
            for j in nodes_to_go:  # get node by min delay
                if (path_delay_list[j] < path_delay_list[min_node]):
                    min_node = j
            for j in graph_object[min_node]:  # all adjacent nodes
                if (not used_list[j]):
                    new_delay = path_delay_list[min_node] + graph_object[min_node][j]['delay']
                    if (new_delay < path_delay_list[j]):
                        path_delay_list[j] = new_delay
                    nodes_to_go.append(j)
            used_list[min_node] = True
            nodes_to_go.remove(min_node)
        total_delay[i] = sum(path_delay_list)
    used_list = [False for i in nodes_list]
    path_delay_list = [float('+inf') for i in nodes_list]
    source_node = [-1 for i in nodes_list]
    controller_node = total_delay.index(min(total_delay))
    new_graph_object.graph['controller_node_id'] = controller_node
    path_delay_list[controller_node] = 0.0
    used_list[controller_node] = True
    nodes_to_go = [controller_node]
    while (len(nodes_to_go) > 0):
        min_node = nodes_to_go[0]
        for j in nodes_to_go:  # get node by min delay
            if (path_delay_list[j] < path_delay_list[min_node]):
                min_node = j
        for j in graph_object[min_node]:  # all adjacent nodes
            if (not used_list[j]):
                new_delay = path_delay_list[min_node] + graph_object[min_node][j]['delay']
                if (new_delay < path_delay_list[j]):
                    source_node[j] = min_node
                    path_delay_list[j] = new_delay
                nodes_to_go.append(j)
        used_list[min_node] = True
        nodes_to_go.remove(min_node)
    new_graph_object.add_nodes_from(old_graph_object)
    for i in range(len(path_delay_list)):
        new_graph_object.nodes[i]['path_delay'] = path_delay_list[i]

    for i in range(len(source_node)):
        if (source_node[i] != -1):
            new_graph_object.add_edge(i, source_node[i])  # add specific edge
            new_graph_object[i][source_node[i]].update(old_graph_object[i][source_node[i]])  # add specific edge data
            new_graph_object.nodes[i]['source'] = source_node[i]

    return new_graph_object


def criteria_2(old_graph_object):
    new_graph_object = networkx.Graph()
    new_graph_object.graph.update(old_graph_object.graph)  # copy graph info

    networkx.set_node_attributes(old_graph_object, False, 'used')

    new_graph_object.add_node(0)  # add init node
    new_graph_object.nodes[0].update(dict(old_graph_object.nodes(data=True)[0]))  # add init node data
    old_graph_object.nodes(data=True)[0]['used'] = True  # set it to used

    edges_list = list(old_graph_object.edges(data='delay'))  # get all edges
    available_edges_list = []

    new_available_edges_list = list(
        filter(lambda x: x[0] == 0 or x[1] == 0, edges_list))  # get all edges with init node

    for i in new_available_edges_list:
        edges_list.remove(i)
    available_edges_list.extend(new_available_edges_list)

    while len(new_graph_object.nodes) < len(old_graph_object.nodes):
        edge_to_add = 1
        delay = float("+inf")
        for i in available_edges_list:
            if (i[2] < delay):
                delay = i[2]
                edge_to_add = i
        new_node_number = 1
        if (old_graph_object.nodes[edge_to_add[0]]['used']):  # is True
            new_node_number = edge_to_add[1]
        else:
            new_node_number = edge_to_add[0]
        old_graph_object.nodes[new_node_number]['used'] = True

        new_graph_object.add_node(new_node_number)  # add specific node
        new_graph_object.nodes[new_node_number].update(dict(old_graph_object.nodes(data=True)[
                                                                new_node_number]))  # add specific node data
        new_graph_object.add_edge(edge_to_add[0], edge_to_add[1])  # add specific edge
        new_graph_object[edge_to_add[0]][edge_to_add[1]].update(
            old_graph_object[edge_to_add[0]][edge_to_add[1]])  # add specific edge data

        new_available_edges_list = list(
            filter(lambda x: x[0] == new_node_number or x[1] == new_node_number,
                   edges_list))  # get all edges with new_node_number node
        for i in new_available_edges_list:
            edges_list.remove(i)
        available_edges_list.extend(new_available_edges_list)
        junk_edges = list(
            filter(lambda x: old_graph_object.nodes[x[0]]['used'] and old_graph_object.nodes[x[1]]['used'],
                   available_edges_list))  # get all edges that creates loops
        for i in junk_edges:
            available_edges_list.remove(i)

    return new_graph_object


def create_topology_file(my_graph_object):
    file_name = my_graph_object.graph['label'] + "_topo.csv"
    try:
        output_file = open(file_name, "w")
        output_file.write("Node1 (id);Node1 (label);Node1 (latitude);Node1 (longitude);"
                          "Node2 (id);Node2 (label);Node2 (latitude);Node2 (longitude);"
                          "Distance (km);Delay (mks)\n")  # just table header
        nodes_list = list(my_graph_object.nodes)
        node_strings = []
        for i in nodes_list:
            node_strings.append(
                str(i) + ';' + my_graph_object.nodes[i]['label'] + ';'
                + str(my_graph_object.nodes(data=True)[i]['Latitude']) + ';'
                + str(my_graph_object.nodes(data=True)[i]['Longitude']) + ';'
            )
        for i in nodes_list:
            second_node = list(my_graph_object[i])
            second_node.sort()
            for j in second_node:
                output_file.write(node_strings[i] + node_strings[j] + str(round(my_graph_object[i][j]['distance'], 5))
                                  + ';' + str(round(my_graph_object[i][j]['delay'], 5)) + '\n')

        output_file.close()

    except OSError as e:
        print("Failed to create and open csv file")
        print(e)
    return


def create_routes_file(my_graph_object):
    def get_way_by_source(source, destination):
        way = [destination]
        while destination != source:
            destination = my_graph_object.nodes(data=True)[destination]['source']
            way.append(destination)
        way.reverse()
        return way

    file_name = my_graph_object.graph['label'] + "_routes.csv"
    try:
        output_file = open(file_name, "w")
        output_file.write("Node1 (id);Node2 (id);Path type;Path;Delay (mks)\n")  # just table header
        nodes_list = list(my_graph_object.nodes)
        controller_node = my_graph_object.graph['controller_node_id']
        for i in nodes_list:
            if (i != controller_node):
                output_file.write(str(controller_node) + ';' + str(i) + ';main;' +
                                  str(get_way_by_source(destination=i, source=controller_node)) + ';' +
                                  str(round(my_graph_object.nodes(data=True)[i]['path_delay'], 5)) + '\n')

        output_file.close()

    except OSError as e:
        print("Failed to create and open csv file")
        print(e)
    return


arg_parser = ArgumentParser(exit_on_error=False)
# arg_parser = ArgumentParser()
arg_parser.add_argument("-t", "-topology", help="This is filename of topology", type=FileType('r'))
arg_parser.add_argument("-k", "-criteria", help="This is number of criteria, should we use k1(1) or k2+k1(2)",
                        type=int, default=2, choices=[1, 2])
arg_parser.add_argument("-st", "-save_top", help="Save built spanning tree to new_<name>.gml",
                        type=int, default=0, choices=[0, 1])
arg_parser.add_argument("-sp", "-save_pic", help="Save built SDN to <name>.png",
                        type=int, default=1, choices=[0, 1])

try:
    args = arg_parser.parse_args()
    text_file = vars(args).get('t')
    criteria = vars(args).get('k')
    save_top = vars(args).get('st')
    save_pic = vars(args).get('sp')
    if (text_file is None):
        print("Empty file. Please specify correct file")
        arg_parser.print_usage()
        exit(0)
    else:
        try:
            graph_object = parse_file(text_file)
            matplotlib.pyplot.figure(figsize=(12.80, 9.60))
            networkx.draw(graph_object, with_labels=True)
            matplotlib.pyplot.show()

            calculate_distance_and_delay(graph_object)
            create_topology_file(graph_object)
            if (criteria == 1):
                graph_object = criteria_1(graph_object)
            else:
                graph_object = criteria_2(graph_object)
                graph_object = criteria_1(graph_object)
            create_routes_file(graph_object)

            if (save_top):
                file_name = "new_" + graph_object.graph['label'] + ".gml"
                networkx.write_gml(graph_object, file_name)

            matplotlib.pyplot.figure(figsize=(12.80, 9.60))
            layout = networkx.spring_layout(graph_object)
            networkx.draw(graph_object, with_labels=True, pos=layout)
            networkx.draw_networkx_nodes(graph_object, nodelist={graph_object.graph['controller_node_id']},
                                         node_color='g', pos=layout)

            if (save_pic):
                file_name = graph_object.graph['label'] + ".png"
                matplotlib.pyplot.savefig(file_name)
            matplotlib.pyplot.show()

        except networkx.exception.NetworkXError as e:
            print("Error during file parsing: " + str(e))
            exit(0)
except (ArgumentError, ValueError) as e:
    print(e)
    arg_parser.print_usage()
    exit(0)

except BaseException as e:
    if (not (type(e) is SystemExit)):
        print("Critical error. Input file should be corrupted.")
        traceback.print_exc()
        exit(0)
