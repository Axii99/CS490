from math import floor

from bokeh.layouts import gridplot, column, widgetbox
from bokeh.plotting import figure, show, output_file
import bokeh.sampledata
import networkx as nx
import json
bokeh.sampledata.download()
from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.us_states import data as states
from bokeh.sampledata.unemployment import data as unemployment
import networkx as nx
from bokeh.io import show, output_file, curdoc
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool, LegendItem, Legend, \
    NodesAndLinkedEdges, EdgesAndLinkedNodes, ColumnDataSource, Slider, StaticLayoutProvider
from bokeh.plotting import from_networkx
from bokeh.palettes import Spectral9
import us

# del states["HI"]
# del states["AK"]

EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]

# =[counties[code]["lons"] for code in counties if counties[code]["state"] not in EXCLUDED]
# county_ys=[counties[code]["lats"] for code in counties if counties[code]["state"] not in EXCLUDED]
county_xs = [counties[code]["lons"] for code in counties]
county_ys = [counties[code]["lats"] for code in counties]

colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

county_colors = []
for county_id in counties:
    # if counties[county_id]["state"] in EXCLUDED:
    # continue
    try:
        rate = unemployment[county_id]
        idx = int(rate / 6)
        county_colors.append(colors[idx])
    except KeyError:
        county_colors.append("black")

p = figure(title="US Air", toolbar_location="left", tools=["pan", 'wheel_zoom'],
           plot_width=1500, plot_height=450)

p.patches(state_xs, state_ys, fill_alpha=0.0,
          line_color="#884444", line_width=2, line_alpha=0.3)

filename = "USAir97v2.json"
with open(filename, 'r') as f:
    dataset = json.loads(f.read())

graph = nx.Graph()
poslist = []
x = []
y = []
degreelist = [0] * 335
for edges in dataset['links']:
    degreelist[edges['source']] += 1
    degreelist[edges['target']] += 1

for nodes in dataset['nodes']:
    # print(nodes['id'])
    graph.add_node(nodes['id'], name=nodes['name'], state=nodes['state'], degree=degreelist[nodes['id']])
    x.append(nodes['longitude'])
    y.append(nodes['latitude'])

a = 0
for edges in dataset['links']:
    graph.add_edge(edges['source'], edges['target'], weight=edges['value'],
                                  source=dataset['nodes'][edges['source'] - 1]['name'],
                                  target=dataset['nodes'][edges['target'] - 1]['name'])


node_indices= list(range(1,323))
graph_layout = dict(zip(node_indices, zip(x, y)))
graph_renderer = from_networkx(graph, graph_layout, scale=1, center=(0, 0))

color_dict = {}
timezonelist = []
for state in us.states.STATES:
    if (str(state.time_zones[0]) not in timezonelist):
        timezonelist.append(str(state.time_zones[0]))

colorlist = []
for nodes in dataset['nodes']:
    try:
        tz = us.states.lookup(nodes['state']).time_zones[0]
        colorlist.append(Spectral9[timezonelist.index(tz)])
    except:
        colorlist.append(Spectral9[8])

# print(colorlist)
# print(Spectral9[8])

node_number = len(colorlist)
edge_number = len(dataset['links'])

edge_width = []  # 0.0009 -- 0.5326
node_impactor = [0] * node_number


edgelist = graph.edges
for edge in edgelist:
    edge_width.append(graph.edges[edge[0],edge[1]]['weight'])
    node_impactor[edge[0] - 1] += graph.edges[edge[0],edge[1]]['weight']
    node_impactor[edge[1] - 1] += graph.edges[edge[0],edge[1]]['weight']



print(min(edge_width))
print(max(edge_width))

# map width
edge_width = [floor((e / 0.6 * 0.8 + 0.2) * 3) * 0.5 + 0.5 for e in edge_width]

# map alpha
edge_alpha = [(e - 0.5) / 1.2 + 0.2 for e in edge_width]

# map impactor
node_impactor = [int(i / 12.0 * 4.0) * 2 + 7 for i in node_impactor]

graph_renderer.node_renderer.data_source.data['colors'] = colorlist
graph_renderer.node_renderer.data_source.data['size'] = node_impactor
graph_renderer.edge_renderer.data_source.data['widths'] = edge_width
graph_renderer.edge_renderer.data_source.data['alpha'] = edge_alpha


fixed_layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
graph_renderer.layout_provider = fixed_layout_provider
graph_renderer.node_renderer.glyph = Circle(size='size', fill_color='colors')
graph_renderer.edge_renderer.glyph = MultiLine(line_color="purple", line_alpha='alpha', line_width='widths')

# add legends

event_radius_dummy_1 = p.circle(
    1, 1,
    radius=0,
    fill_alpha=0.0, line_color='black',
    name='event_radius_dummy_1'
)

event_legend1 = Legend(items=[
    LegendItem(label='0<= Weight Sum < 3', renderers=[event_radius_dummy_1])],
    location=(20, 154), label_standoff=0)

event_legend2 = Legend(items=[
    LegendItem(label='3 <= Weight Sum < 6', renderers=[event_radius_dummy_1])],
    location=(18, 132), label_standoff=0)

event_legend3 = Legend(items=[
    LegendItem(label='6 <= Weight Sum < 9', renderers=[event_radius_dummy_1])],
    location=(16, 107), label_standoff=0)

event_legend4 = Legend(items=[
    LegendItem(label='9 <= Weight Sum < 12', renderers=[event_radius_dummy_1])],
    location=(14, 79), label_standoff=0)

event_legend_list = [event_legend1, event_legend2, event_legend3, event_legend4]
for legend in event_legend_list:
    p.add_layout(legend)

size_list = [15, 20, 25, 30]
index_list = [0, 1, 2, 3]

for index, size in zip(index_list, size_list):
    p.legend[index].glyph_height = size
    p.legend[index].glyph_width = size
    p.legend[index].padding = 0
    p.legend[index].margin = 0
    p.legend[index].border_line_alpha = 0
    p.legend[index].background_fill_alpha = 0

tempx = [5, 5]
tempy = [0, 0]
event_line_dummy_1 = p.line(tempx, tempy, line_alpha=0.3, line_width=0.5)
event_line_dummy_2 = p.line(tempx, tempy, line_alpha=0.6, line_width=1)
event_line_dummy_3 = p.line(tempx, tempy, line_alpha=1, line_width=1.5)
event_legend5 = Legend(items=[
    LegendItem(label='0<= weight < 0.2', renderers=[event_line_dummy_1])],
    location=(14, 200), label_standoff=0)
event_legend6 = Legend(items=[
    LegendItem(label='0.2 <= weight < 0.4', renderers=[event_line_dummy_2])],
    location=(14, 250), label_standoff=0)
event_legend7 = Legend(items=[
    LegendItem(label='0.4 <= weight < 0.6', renderers=[event_line_dummy_3])],
    location=(14, 300), label_standoff=0)
p.add_layout(event_legend5)
p.add_layout(event_legend6)
p.add_layout(event_legend7)

node_hover_tool = HoverTool(
    tooltips=[("index", "@index"), ("Name", "@name"), ("State", "@state"), ("Degree", "@degree")])
edge_hover_tool = HoverTool(tooltips=[("Source", "@source"), ("Target", "@target")])
p.add_tools(node_hover_tool)

minfactor = 0.0
minweight = 0.0
node_check = [1] * node_number


slider1 = Slider(start=0.0, end=12, value=0.0, step=1, title="Min Importance factor")
def slider_handler1(attr, old, new):

    temp_value=int(slider1.value / 12.0 * 4.0) * 2 + 7
    global minfactor
    minfactor = temp_value
    temp_list=[]
    for i in range(len(node_impactor)):
        if node_impactor[i] < temp_value or node_check[i] <= 0:
            temp_list.append(0)
        else:
            temp_list.append(node_impactor[i])

    temp_alpha=[0]*len(edge_alpha)
    i = 0
    for e in edgelist:
        if temp_list[e[0]-1] > 0 and temp_list[(e[1]-1)] > 0 and edge_width[i] > minweight:
                temp_alpha[i] = edge_width[i]
        i += 1

    graph_renderer.node_renderer.data_source.data['size'] = temp_list
    graph_renderer.edge_renderer.data_source.data['alpha'] = temp_alpha



slider1.on_change('value', slider_handler1)


edgelist = list(edgelist)

slider2 = Slider(start=0.0, end=0.6, value=0, step=0.1, title="Min Weight")
def slider_handler2(attr, old, new):
    global minweight
    global minfactor
    temp_value = floor((slider2.value / 0.6 * 0.8 + 0.2) * 3) * 0.5 + 0.5
    minweight = temp_value
    i = 0
    temp_width = []
    temp_alpha = []
    temp_node_check = [0] * node_number
    for w in edge_width:
        if w < temp_value:
           temp_width.append(0)
           temp_alpha.append(0)
        elif (node_impactor[edgelist[i][0]-1] > minfactor and node_impactor[edgelist[i][1]-1] >minfactor):
            temp_node_check[edgelist[i][0]-1] += 1
            temp_node_check[edgelist[i][1]-1] += 1
            temp_width.append(w)
            temp_alpha.append(edge_alpha[i])
        else:
            temp_width.append(0)
            temp_alpha.append(0)
        i += 1
    temp_size = []
    i = 0
    for c in temp_node_check:
        if c > 0 and node_impactor[i] > minfactor:
            temp_size.append(node_impactor[i])
        else:
            temp_size.append(0)
        i += 1

    global node_check
    node_check = temp_node_check
    graph_renderer.node_renderer.data_source.data['size'] = temp_size
    graph_renderer.edge_renderer.data_source.data['widths'] = temp_width
    #graph_renderer.edge_renderer.data_source.data['alpha'] = temp_alpha


    print(temp_value)

slider2.on_change('value', slider_handler2)

graph_renderer.selection_policy = NodesAndLinkedEdges()
graph_renderer.inspection_policy = NodesAndLinkedEdges()
p.renderers.append(graph_renderer)
curdoc().add_root(column(p,slider1,slider2))
