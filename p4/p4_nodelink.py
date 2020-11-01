from bokeh.models import Panel, Tabs, Slider
from bokeh.layouts import gridplot, column, layout
from bokeh.plotting import figure, show, output_file
import bokeh.sampledata
import networkx as nx
import json
import networkx as nx
from bokeh.io import show, output_file, curdoc
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool, LegendItem, Legend, \
    NodesAndLinkedEdges, EdgesAndLinkedNodes, ColumnDataSource, StaticLayoutProvider, LabelSet, Button
from bokeh.plotting import from_networkx
from bokeh.palettes import Colorblind4
from networkx.drawing.nx_agraph import graphviz_layout
from numpy import mean

filename = "flare.json"
with open(filename, 'r') as f:
    dataset = json.loads(f.read())

dataset['children'][2]['name'] = ' data '
G=nx.Graph()


def traverseNode(name, children, depth):
    G.add_node(name, value=0, depth=depth)
    for c in children:

        try:
            G.add_node(c['name'], value=c['value'],depth=depth+1)
        except:
            #G.add_node(c['name'], value=0)
            traverseNode(c['name'], c['children'],depth+1)
            #print(c['name'])
            #print(c['value'])
        G.add_edge(name, c['name'])
    return

layer = dataset
currentName = layer['name']
currentChildren = layer['children']

traverseNode(currentName,currentChildren, 0)


pos = graphviz_layout(G, prog="dot", args="")


newplot = figure(title="Node Link-radial", x_range=(-10, 1000), y_range=(-10, 1000))
plot = figure(title="Node Link",x_range=(0,15), y_range=(-5,120),plot_width=1500, plot_height=450,
              tools=['pan','wheel_zoom'])

graph_renderer = from_networkx(G, nx.spring_layout, scale=2, center=(0,0))
modified_pos = {}
name_label=[]
for key in pos.keys():
    name_label.append(key)
    modified_pos[key] = (-pos[key][1]/100.0 + 5, pos[key][0]/100.0)

value_list = []
label_list =[]
for n in G.nodes:
    label_list.append(n)
    value_list.append(G.nodes[n]['value'])

allcolor = Colorblind4
color_list= []
size_list=[]
width_list =[]

for v in value_list:
    size_list.append(9)
    if v > 10000:
        color_list.append(allcolor[1])
    elif v > 5000:
        color_list.append(allcolor[2])
    elif v > 0:
        color_list.append(allcolor[3])
    else:
        color_list.append(allcolor[1])


for e in G.edges:
    width_list.append(1)


print(mean(value_list))
fixed_layout_provider = StaticLayoutProvider(graph_layout=modified_pos)
graph_renderer.layout_provider = fixed_layout_provider
graph_renderer.node_renderer.glyph = Circle(size='size', fill_color='colors')
graph_renderer.edge_renderer.glyph = MultiLine(line_color="purple", line_alpha='width', line_width=1)
x,y=zip(*graph_renderer.layout_provider.graph_layout.values())
graph_renderer.node_renderer.data_source.data['x']=x
graph_renderer.node_renderer.data_source.data['y']=y
graph_renderer.node_renderer.data_source.data['colors']=color_list
graph_renderer.node_renderer.data_source.data['label']=label_list
graph_renderer.node_renderer.data_source.data['size']=size_list
graph_renderer.edge_renderer.data_source.data['width']=width_list

event_radius_dummy_1 = plot.circle(1,1,radius=0,fill_alpha=1.0, fill_color=allcolor[3],name='event_radius_dummy_1')
event_legend1 = Legend(items=[LegendItem(label='value <= 5000', renderers=[event_radius_dummy_1])],location=(20,154), label_standoff=0)
event_radius_dummy_2 = plot.circle(1,1,radius=0,fill_alpha=1.0, fill_color=allcolor[2],name='event_radius_dummy_2')
event_legend2 = Legend(items=[LegendItem(label='value > 5000', renderers=[event_radius_dummy_2])],location=(20,130), label_standoff=0)
event_radius_dummy_3 = plot.circle(1,1,radius=0,fill_alpha=1.0, fill_color=allcolor[1],name='event_radius_dummy_3')
event_legend3 = Legend(items=[LegendItem(label='value > 10000', renderers=[event_radius_dummy_3])],location=(20,106), label_standoff=0)

event_legend_list = [event_legend1,event_legend2,event_legend3]
for legend in event_legend_list:
    plot.add_layout(legend)

for i in range(3):
    plot.legend[i].padding = 0
    plot.legend[i].margin = 0
    plot.legend[i].border_line_alpha = 0
    plot.legend[i].background_fill_alpha = 0

label=LabelSet(x='x', y='y', text='label',level='glyph', source=graph_renderer.node_renderer.data_source)
plot.renderers.append(graph_renderer)
plot.renderers.append(label)



temp_pos = graphviz_layout(G, prog="twopi", args="")
new_renderer = from_networkx(G, nx.spring_layout, scale=2, center=(0, 0))
temp_layout_provider = StaticLayoutProvider(graph_layout=temp_pos)
new_renderer.layout_provider = temp_layout_provider
new_renderer.node_renderer.glyph = Circle(size='size', fill_color='colors')
new_renderer.edge_renderer.glyph = MultiLine(line_color="purple", line_alpha='width', line_width=1)
tempx, tempy = zip(*new_renderer.layout_provider.graph_layout.values())
new_renderer.node_renderer.data_source.data['x'] = tempx
new_renderer.node_renderer.data_source.data['y'] = tempy
new_renderer.node_renderer.data_source.data['colors'] = color_list
new_renderer.node_renderer.data_source.data['label'] = label_list
new_renderer.node_renderer.data_source.data['size']=size_list
new_renderer.edge_renderer.data_source.data['width']=width_list
templabel = LabelSet(x='x', y='y', text='label', level='glyph', source=new_renderer.node_renderer.data_source)

event_radius_dummy_4 = newplot.circle(1,1,radius=0,fill_alpha=1.0, fill_color=allcolor[3],name='event_radius_dummy_4')
event_legend4 = Legend(items=[LegendItem(label='value > 10000', renderers=[event_radius_dummy_4])],location=(20,154), label_standoff=0)
event_radius_dummy_5 = newplot.circle(1,1,radius=0,fill_alpha=1.0, fill_color=allcolor[2],name='event_radius_dummy_5')
event_legend5 = Legend(items=[LegendItem(label='value > 5000', renderers=[event_radius_dummy_5])],location=(20,130), label_standoff=0)
event_radius_dummy_6 = newplot.circle(1,1,radius=0,fill_alpha=1.0, fill_color=allcolor[1],name='event_radius_dummy_6')
event_legend6 = Legend(items=[LegendItem(label='value <= 5000', renderers=[event_radius_dummy_6])],location=(20,106), label_standoff=0)

event_legend_list = [event_legend4,event_legend5,event_legend6]
for legend in event_legend_list:
    newplot.add_layout(legend)

for i in range(3):
    newplot.legend[i].padding = 0
    newplot.legend[i].margin = 0
    newplot.legend[i].border_line_alpha = 0
    newplot.legend[i].background_fill_alpha = 0

newplot.renderers.append(new_renderer)
newplot.renderers.append(templabel)
newplot.add_layout(legend)

tab1 = Panel(child=plot, title="Horizontal")
tab2 = Panel(child=newplot, title="Radial")


slider = Slider(start=0, end=5, value=0, step=1, title="Depth")
def slider_handler(attr, old, new):
    value = 5 - slider.value
    temp_size =[]
    temp_width =[]
    temp_label =[]
    for n in G.nodes:
        if (G.nodes[n]['depth'] >= value):
            temp_size.append(0)
            temp_label.append('')
        else:
            temp_size.append(9)
            temp_label.append(n)

    for e in G.edges:
        if (G.nodes[e[0]]['depth'] >= value or G.nodes[e[1]]['depth'] >= value):
            temp_width.append(0)
        else:
            temp_width.append(1)

    graph_renderer.node_renderer.data_source.data['size'] = temp_size
    new_renderer.node_renderer.data_source.data['size'] = temp_size
    graph_renderer.node_renderer.data_source.data['label'] = temp_label
    new_renderer.node_renderer.data_source.data['label'] = temp_label
    graph_renderer.edge_renderer.data_source.data['width'] = temp_width
    new_renderer.edge_renderer.data_source.data['width'] = temp_width

slider.on_change('value', slider_handler)


layout=column(Tabs(tabs=[tab1, tab2]), slider)
curdoc().add_root(layout)
