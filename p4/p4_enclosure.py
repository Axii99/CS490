import time
import squarify
import matplotlib.pyplot as plt
import networkx as nx
import json
import networkx as nx
from bokeh.io import show, output_file, curdoc
from bokeh.plotting import from_networkx
from bokeh.palettes import Colorblind4, Viridis4
from matplotlib.lines import Line2D
from matplotlib.widgets import Button, Slider
from networkx.drawing.nx_agraph import graphviz_layout
from numpy import mean


filename = "flare.json"
with open(filename, 'r') as f:
    dataset = json.loads(f.read())
dataset['children'][2]['name'] = ' data '
name_list =[]
value_dict ={}
depth_dict={}
def traverseNode(name, children, depth):
    name_list.append(name)
    depth_dict[name] = depth
    value_dict[name] = 0
    for c in children:
        try:
            v = c['value']
            name_list.append(c['name'])
            value_dict[name] += v
            value_dict[c['name']] = v
            depth_dict[c['name']] = depth + 1
        except:
            traverseNode(c['name'], c['children'], depth + 1)
            value_dict[name] += value_dict[c['name']]
    return


layer = dataset
currentName = layer['name']
currentChildren = layer['children']

traverseNode(currentName,currentChildren, 0)
label_list=[]
size_list = []

allcolor = Viridis4
color_list= []


for key in value_dict.keys():
    label_list.append(key)
    size_list.append(value_dict[key])
    if (value_dict[key] > 10000):
       color_list.append(allcolor[1])
    elif value_dict[key] > 5000:
        color_list.append(allcolor[2])
    elif value_dict[key] > 0:
        color_list.append(allcolor[3])
    else:
        color_list.append(allcolor[1])

#size_list.sort(reverse=True)
rects = squarify.padded_squarify(size_list,0,0, 1000, 800)



xs=[]
ys=[]

for r in rects:
    xs.append([r['x'],r['x'], r['x'] + r['dx'],r['x']+ r['dx']])
    ys.append([r['y'], r['y']+r['dy'],r['y'] +r['dy'],r['y']])


fig = plt.figure("Enclosure")
ax = fig.gca()
squarify.plot(sizes=size_list, alpha=1, ax=ax,color=color_list)
plt.axis('off')


legend_elements = [Line2D([0], [0], marker='o', color=allcolor[1], label='value > 10000',
                          markersize=15),
                   Line2D([0], [0], marker='o', color=allcolor[2], label='value > 5000',
                           markersize=15),
                   Line2D([0], [0], marker='o', color=allcolor[3], label='value <= 5000',
                           markersize=15),
                   ]
ax.legend(handles=legend_elements, loc='upper left')
axcolor = 'lightgoldenrodyellow'
axamp = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
samp = Slider(axamp, 'Depth', 0, 5, valinit=0, valstep=1)

def update(val):
    new_size=[]
    tempcolor=[]
    i = 0
    for n in name_list:
        if (depth_dict[n] < 5-val):
            new_size.append(value_dict[n])
            tempcolor.append(color_list[i])
        i += 1
    if len(new_size) > 0:
        plt.axis('off')
        squarify.plot(sizes=new_size, alpha=1, ax=ax,color=tempcolor)
        ax.legend(handles=legend_elements, loc='upper left')
    else:
        squarify.plot(sizes=[], alpha=0, ax=ax,color=tempcolor)
        ax.legend(handles=legend_elements, loc='upper left')

samp.on_changed(update)

plt.show()