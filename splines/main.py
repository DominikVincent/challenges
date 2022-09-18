import plotly.graph_objects as go
from scipy import interpolate
from matplotlib import cm
import numpy as np
np.random.seed(1)

import plotly.graph_objects as go

import numpy as np
np.random.seed(1)

import matplotlib.pyplot as plt

from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])

x1 = []
x2 = []
line, = ax.plot(x1, x2, "b-", markersize=15.0)
line_inter, = ax.plot(x1, x2, "r-", markersize=15.0)


# computes the linear distance along the line
def computeLineDistance(points):
    distance = np.cumsum( np.sqrt(np.sum( np.diff(points, axis=0)**2, axis=1 )) )
    distance = np.insert(distance, 0, 0)/distance[-1]
    
    return distance

def getSpline(x1, x2):
    steps = len(x1) * 10
    points = np.vstack((x1, x2)).T
    distance = computeLineDistance(points)
    print(distance)

    alpha = np.linspace(0, 1, steps)
    print(points.shape)
    interpolator =  interpolate.CubicSpline(distance, points, bc_type="periodic", axis=0)
    
    spline_points = interpolator(alpha)
    spline_points_1 = interpolator(alpha, 1)
    spline_points_2 = interpolator(alpha, 2)
    
    curvature = np.zeros(steps)
    for i in range(steps):
        curvature[i] = spline_points_1[i,0]*spline_points_2[i,1]-spline_points_1[i,1]*spline_points_2[i,0]
        curvature[i] /= np.power(np.linalg.norm(spline_points_1[i]), 3)
    # print(spline_points)
    return spline_points, curvature

cb = None

def onclick(event):
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.button, event.x, event.y, event.xdata, event.ydata))
    x1.append(event.xdata)
    x2.append(event.ydata)
    

    
    if (len(x1) > 3):
        global cb
        ax.clear()
        # try:
        #     cb = plt.colorbar() 
        #     print(cb)
        #     cb.remove()
        # except:
        #     pass
        if cb is not None:
            cb.remove() 

        spline, curv = getSpline(x1+[x1[0]], x2+[x2[0]])
        x_data = spline[:, 0]
        y_data = spline[:, 1]

        points = np.array([x_data, y_data]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        norm = plt.Normalize(curv.min(), curv.max())
        lc = LineCollection(segments, cmap='inferno', norm=norm)
        lc.set_array(curv)
        lc.set_linewidth(4)
        line = ax.add_collection(lc)
        ax.set_xlim([0, 10])
        ax.set_ylim([0, 10])
        cb = fig.colorbar(line, ax=ax)


        # color_map = cm.hot(curv)

        # ax.plot(x_data, y_data, c=color_map)
        # line_inter.set_xdata(x_data)
        # line_inter.set_ydata(y_data)
        # line_inter.set_color(cm.hot(curv))
    

    # ax.plot(x1, x2, "-", markersize=15.0)
    fig.canvas.draw()
    fig.canvas.flush_events()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
