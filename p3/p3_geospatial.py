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
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool
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
           plot_width=3100, plot_height=700)

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
print(graph_layout)
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
graph_renderer.node_renderer.data_source.data['colors'] =colorlist
graph_renderer.node_renderer.glyph = Circle(size=9, fill_color='colors')
graph_renderer.edge_renderer.glyph = MultiLine(line_color="black", line_alpha=0.5, line_width=0.5)
p.renderers.append(graph_renderer)

show(p)
