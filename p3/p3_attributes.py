from math import floor

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
import bokeh.sampledata
import networkx as nx
import json
#bokeh.sampledata.download()
from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.us_states import data as states
from bokeh.sampledata.unemployment import data as unemployment
import networkx as nx
from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool, LegendItem, Legend
from bokeh.plotting import from_networkx
from bokeh.palettes import Spectral9
import us

#del states["HI"]
#del states["AK"]

EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]

#=[counties[code]["lons"] for code in counties if counties[code]["state"] not in EXCLUDED]
#county_ys=[counties[code]["lats"] for code in counties if counties[code]["state"] not in EXCLUDED]
county_xs=[counties[code]["lons"] for code in counties ]
county_ys=[counties[code]["lats"] for code in counties ]


colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

county_colors = []
for county_id in counties:
    #if counties[county_id]["state"] in EXCLUDED:
        #continue
    try:
        rate = unemployment[county_id]
        idx = int(rate/6)
        county_colors.append(colors[idx])
    except KeyError:
        county_colors.append("black")

p = figure(title="US Air", toolbar_location="left", tools=["pan",'wheel_zoom'],
           plot_width=1500, plot_height=450)

p.patches(state_xs, state_ys, fill_alpha=0.0,
          line_color="#884444", line_width=2, line_alpha=0.3)

filename = "USAir97v2.json"
with open(filename, 'r') as f:
    dataset = json.loads(f.read())

graph = nx.Graph()
poslist =[]
x = []
y = []
for nodes in dataset['nodes']:
    #print(nodes['id'])
    graph.add_node(nodes['id'])
    x.append(nodes['longitude'])
    y.append(nodes['latitude'])


for edges in dataset['links']:
    graph.add_weighted_edges_from([(edges['source'],edges['target'],edges['value'])])


node_indices= list(range(1,323))
graph_layout = dict(zip(node_indices, zip(x, y)))
graph_renderer = from_networkx(graph, graph_layout, scale=1, center=(0, 0))


color_dict = {}
timezonelist =[]
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

#print(colorlist)
#print(Spectral9[8])

node_number = len(colorlist)
edge_number = len(dataset['links'])

edge_width = [] #0.0009 -- 0.5326
node_impactor = [0]*edge_number


for edge in dataset['links']:
    edge_width.append(edge['value'])
    node_impactor[edge['source']-1] += edge['value']
    node_impactor[edge['target'] - 1] += edge['value']

print(min(edge_width))
print(max(edge_width))

#map width
edge_width = [floor((e/0.6 * 0.8 + 0.2)* 3)*0.5 +0.5 for e in edge_width]



#map alpha
edge_alpha = [(e-0.5)/1.2 + 0.2 for e in edge_width]
print(set(edge_alpha))
print(min(edge_alpha))
print(max(edge_alpha))
#map impactor
node_impactor = [int(i/12.0 * 4.0)*2 + 7 for i in node_impactor]



graph_renderer.node_renderer.data_source.data['colors'] =colorlist
graph_renderer.node_renderer.data_source.data['size'] =node_impactor
graph_renderer.edge_renderer.data_source.data['widths'] =edge_width
graph_renderer.edge_renderer.data_source.data['alpha'] =edge_alpha

graph_renderer.node_renderer.glyph = Circle(size='size', fill_color='colors')
graph_renderer.edge_renderer.glyph = MultiLine(line_color="purple", line_alpha='alpha', line_width='widths')



#add legends

event_radius_dummy_1 = p.circle(
    1,1,
    radius=0,
    fill_alpha=0.0, line_color='black',
    name='event_radius_dummy_1'
    )

event_legend1 = Legend(items=[
    LegendItem(label='0<= Weight Sum < 3', renderers=[event_radius_dummy_1])],
    location=(20,154), label_standoff=0)

event_legend2 = Legend(items=[
    LegendItem(label='3 <= Weight Sum < 6', renderers=[event_radius_dummy_1])],
    location=(18,132), label_standoff=0)

event_legend3 = Legend(items=[
    LegendItem(label='6 <= Weight Sum < 9', renderers=[event_radius_dummy_1])],
    location=(16,107), label_standoff=0)

event_legend4 = Legend(items=[
    LegendItem(label='9 <= Weight Sum < 12', renderers=[event_radius_dummy_1])],
    location=(14,79), label_standoff=0)

event_legend_list = [event_legend1,event_legend2,event_legend3,event_legend4]
for legend in event_legend_list:
    p.add_layout(legend)



size_list = [15, 20, 25, 30]
index_list = [0,1,2,3]

for index, size in zip(index_list, size_list):
    p.legend[index].glyph_height = size
    p.legend[index].glyph_width = size
    p.legend[index].padding = 0
    p.legend[index].margin = 0
    p.legend[index].border_line_alpha = 0
    p.legend[index].background_fill_alpha = 0



tempx = [5, 5]
tempy = [0, 0]
event_line_dummy_1 = p.line(tempx, tempy, line_alpha= 0.3, line_width=0.5)
event_line_dummy_2 = p.line(tempx, tempy, line_alpha= 0.6, line_width=1)
event_line_dummy_3 = p.line(tempx, tempy, line_alpha= 1, line_width=1.5)
event_legend5 = Legend(items=[
    LegendItem(label='0<= weight < 0.2', renderers=[event_line_dummy_1])],
    location=(14,200), label_standoff=0)
event_legend6 = Legend(items=[
    LegendItem(label='0.2 <= weight < 0.4', renderers=[event_line_dummy_2])],
    location=(14,250), label_standoff=0)
event_legend7 = Legend(items=[
    LegendItem(label='0.4 <= weight < 0.6', renderers=[event_line_dummy_3])],
    location=(14,300), label_standoff=0)
p.add_layout(event_legend5)
p.add_layout(event_legend6)
p.add_layout(event_legend7)



p.renderers.append(graph_renderer)


show(p)
