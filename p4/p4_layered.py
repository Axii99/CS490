import matplotlib.pyplot as plt
import squarify
import json
import numpy as np
from bokeh.palettes import Viridis4
from matplotlib.lines import Line2D
from matplotlib.widgets import Slider, Button

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


rects_dict = {}
def setRects(name, children, parent):
    if name == 'flare':
        rects_dict[name] = [0, 0, 40, 500]
    else:
        parent_rect = rects_dict[parent]
        ratio = value_dict[name] / value_dict[parent]
        d = depth_dict[name]
        dy = parent_rect[3] - parent_rect[1]
        rects_dict[name] = [d*40, base_dict[parent]+parent_rect[1], (d+1)*40, base_dict[parent]+ ratio * dy+parent_rect[1]]
        base_dict[parent] += ratio * dy
    for c in children:
        try:
            v = c['value']
            parent_rect = rects_dict[name]
            ratio = v / value_dict[name]
            d = depth_dict[c['name']]
            dy = parent_rect[3] - parent_rect[1]
            rects_dict[c['name']] = [d * 40, base_dict[name]+ parent_rect[1], (d + 1) * 40, base_dict[name] + ratio * dy+parent_rect[1]]
            base_dict[name] += ratio * dy
        except:
            setRects(c['name'], c['children'], name)
    return

layer = dataset
currentName = layer['name']
currentChildren = layer['children']

traverseNode(currentName,currentChildren, 0)
base_dict = {}
for n in name_list:
    base_dict[n] = 0.0

setRects(currentName,currentChildren, currentName)


allcolor = Viridis4
color_list= []
label_list=[]
size_list = []
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

x = [rect[0] for rect in rects_dict.values()]
y = [rect[1] for rect in rects_dict.values()]
dx = [rect[2]-rect[0] for rect in rects_dict.values()]
dy = [rect[3]-rect[1] for rect in rects_dict.values()]

fig = plt.figure("Flare")
ax = fig.gca()
ax.bar(x, dy, width=dx, bottom=y,align="edge",label=label_list, color=color_list)
for key in rects_dict.keys():
    x, y = rects_dict[key][0], rects_dict[key][3]
    ax.text(x, y , key,va='top', ha="left")

axcolor = 'lightgoldenrodyellow'
axamp = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
samp = Slider(axamp, 'Depth', 0, 5, valinit=5, valstep=1)
isRadial = False


def sunburst(nodes, total=np.pi * 2, offset=0, level=0, ax=None, limit=0):
    if level >= limit:
        return
    ax = ax or plt.subplot(111, projection='polar')

    if level == 0 and len(nodes) == 1:
        ax.clear()
        label, value, subnodes = nodes[0]
        ax.bar([0], [0.5], [np.pi * 2])
        ax.text(0, 0, label, ha='center', va='center')
        sunburst(subnodes, total=value, level=level + 1, ax=ax,limit=limit)
    elif nodes:
        d = np.pi * 2 / total
        labels = []
        widths = []
        local_offset = offset
        for label, value, subnodes in nodes:
            labels.append(label)
            widths.append(value * d)
            sunburst(subnodes, total=total, offset=local_offset,
                     level=level + 1, ax=ax,limit=limit)
            local_offset += value
        values = np.cumsum([offset * d] + widths[:-1])
        heights = [1] * len(nodes)
        bottoms = np.zeros(len(nodes)) + level - 0.5
        rects = ax.bar(values, heights, widths, bottoms, linewidth=1,
                       edgecolor='white', align='edge')
        for rect, label in zip(rects, labels):
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + rect.get_height() / 2
            rotation = (90 + (360 - np.degrees(x) % 180)) % 360
            ax.text(x, y, label, rotation=rotation, ha='center', va='center')

    if level == 0:
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location('N')
        ax.set_axis_off()
    return ax

sunburstData=[]
def setSunburst(current):
    if 'value' in current.keys():
        return (current['name'], value_dict[current['name']], [])
    else:
        list = []
        for c in current['children']:
            list.append(setSunburst(c))
        return (current['name'],value_dict[current['name']], list)

sunburstData=[setSunburst(layer)]

legend_elements = [Line2D([0], [0], marker='o', color=allcolor[1], label='value > 10000',
                          markersize=15),
                   Line2D([0], [0], marker='o', color=allcolor[2], label='value > 5000',
                           markersize=15),
                   Line2D([0], [0], marker='o', color=allcolor[3], label='value <= 5000',
                           markersize=15),
                   ]
ax.legend(handles=legend_elements, loc='upper left')
sax=ax


def update(val):
    sax.clear()
    plt.axis('off')
    if not isRadial:
        tempx=[]
        tempy=[]
        tempdx=[]
        tempdy=[]
        tempcolor=[]
        i = 0
        for n in name_list:
            if (depth_dict[n] < val):
                tempx.append(rects_dict[n][0])
                tempy.append(rects_dict[n][1])
                tempdx.append(rects_dict[n][2]-rects_dict[n][0])
                tempdy.append(rects_dict[n][3]-rects_dict[n][1])
                tempcolor.append(color_list[i])
                ax.text(rects_dict[n][0], rects_dict[n][3], n, va='top', ha="left")
            i += 1
        sax.bar(tempx, tempdy, width=tempdx, bottom=tempy, align="edge", label=label_list, color=tempcolor)
        sax.legend(handles=legend_elements, loc='upper left')
        plt.axis('off')
        #plt.draw()
    else:
        sax.clear()
        sunburst(sunburstData, limit=val)
        plt.axis('off')
        return

samp.on_changed(update)
axnext = plt.axes([0.3, 0.015, 0.65, 0.03])
bnext = Button(axnext, 'Horizontal/Radial')

class Index:
    ind = 0
    rax=plt.subplot()
    def next(self, event):
        global isRadial
        global rax
        global sax
        if isRadial:

            rax.clear()
            isRadial = False
            samp.reset()
            sax.bar(x, dy, width=dx, bottom=y, align="edge", label=label_list, color=color_list)
            plt.draw()
        else:
            ax.clear()
            rax=sunburst(sunburstData, limit=5)
            isRadial = True
            samp.reset()
        plt.axis('off')


callback = Index()

bnext.on_clicked(callback.next)

plt.axis('off')
plt.show()