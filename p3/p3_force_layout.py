import networkx as nx
import json
import matplotlib.pyplot as plt


filename = "USAir97v2.json"

with open(filename, 'r') as f:
    dataset = json.loads(f.read())

graph = nx.Graph()
poslist =[]
for nodes in dataset['nodes']:
    graph.add_node(nodes['id'])
    #graph.add_nodes_from([nodes['posx'], nodes['posy']])



for edges in dataset['links']:
    graph.add_weighted_edges_from([(edges['source'],edges['target'],edges['value'])])


nx.draw(graph,pos = nx.random_layout(graph),node_color = 'b',edge_color = 'black',with_labels = True,font_size =9,node_size =50,linewidths=0,width=0.1)
#nx.draw(graph,node_color = 'b',edge_color = 'black',with_labels = False,font_size =9,node_size =10,linewidths=0,width=0.1)
plt.show()
