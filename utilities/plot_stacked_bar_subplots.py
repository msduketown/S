# Execute me with python3!
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

if len(sys.argv) < 2:
    print ("Tell me the file name please")
    sys.exit()

with open(sys.argv[1]) as f:
    content = [x.strip() for x in f.readlines()]

fileprefix = os.path.splitext(sys.argv[1])[0]

num_sub_plots=len(content)-8

headline=content[7].split()

scheds=headline[2:]

c_1_colors = ['0.45', '0.85']
c_1_labels = ['Interfered avg throughput',
                  'Interferers avg total throughput']

ind = np.arange(len(scheds))
width = 0.5

# works only with at least two subplots
f, ax = plt.subplots(1, num_sub_plots, sharey=True, sharex=True)

f.subplots_adjust(bottom=0.2) #make room for the legend

#plt.yticks(np.arange(0,18,2))
plt.xticks(ind+width/2., scheds)

plt.suptitle(content[0].replace('# ', ''))

def autolabel(rects, axis, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        axis.text(rect.get_x() + rect.get_width()*offset[xpos],
                      rect.get_y() + rect.get_height() / 2.,
                      '{}'.format(height), ha=ha[xpos], va='bottom',
                      size=8)


p = [] # list of bar properties
def create_subplot(matrix, colors, axis, title):
    bar_renderers = []
    ind = np.arange(matrix.shape[1])

    bottoms = np.cumsum(np.vstack((np.zeros(matrix.shape[1]), matrix)), axis=0)[:-1]

    for i, row in enumerate(matrix):
        r = axis.bar(ind, row, width=0.5, color=colors[i], bottom=bottoms[i],
                         align='edge')
        autolabel(r, axis)
        bar_renderers.append(r)
    axis.set_title(title)
    axis.text(0.5, -0.13, "policy-scheduler", ha="center", transform=axis.transAxes)
    return bar_renderers

i = 0
max_tot_throughput = 0
for line in content[8:]:
    line_elems = line.split()
    numbers = line_elems[1:]

    first_row = np.asarray(numbers[::2]).astype(np.float)
    second_row = np.asarray(numbers[1::2]).astype(np.float)

    mat = np.array([first_row, second_row])
    p.extend(create_subplot(mat, c_1_colors, ax[i], line_elems[0].replace('_', ' ')))

    tot_throughput = np.amax(mat.sum(axis=0))

    max_tot_throughput = max(max_tot_throughput, tot_throughput)
    i += 1


ax[0].set_ylabel('Interfered, interferers and total throughput') # add left y label
ax[0].set_ybound(0, max_tot_throughput * 1.1) # add buffer at the top of the bars

f.legend(((x[0] for x in p)), # bar properties
         (c_1_labels),
         bbox_to_anchor=(0.5, 0),
         loc='lower center',
         ncol=4)
plt.savefig(fileprefix + '.eps')
plt.show()
