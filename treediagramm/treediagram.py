import igraph
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px

def dfs_permuations(level, colors, permuations, position_x, v_poses, edges, depth):
    if level != 0:
        v_poses["x"].append(position_x)
        v_poses["y"].append(level)
        v_poses["color"].append(colors[level-1])

    if level == min(depth, len(colors)):
        permuations.append(colors.copy())
        return

    if level + 1 == len(colors):
        positions_x = [position_x]
    else:
        spacing_reg =  1 / (len(colors)**level)
        positions_x = np.linspace(position_x - spacing_reg, position_x + spacing_reg, len(colors) - level)
    print(positions_x)
    parent_id = len(v_poses["x"])
    for idx, i in enumerate(range(level, len(colors))):
        edges["from"].append(parent_id - 1)
        edges["to"].append(len(v_poses["x"]))
        edges["label"].append(colors[i])
        colors[level], colors[i] = colors[i], colors[level]
        dfs_permuations(level + 1, colors, permuations, positions_x[idx], v_poses, edges=edges, depth=depth)
        colors[level], colors[i] = colors[i], colors[level]

def dfs_all_premuations(level, colors, permuations, position_x, v_poses, edges, depth):
    if level != 0:
        v_poses["x"].append(position_x)
        v_poses["y"].append(level)
        v_poses["color"].append(colors[level-1])

    if level == min(depth, len(colors)):
        permuations.append(colors.copy())
        return

    spacing_reg =  3 / (len(colors)**level)
    positions_x = np.linspace(position_x - spacing_reg, position_x + spacing_reg, len(colors))
    print(positions_x)
    parent_id = len(v_poses["x"])
    for idx, i in enumerate(range(len(colors))):
        print("level: ", level, "i: ", i)
        edges["from"].append(parent_id - 1)
        edges["to"].append(len(v_poses["x"]))
        edges["label"].append(colors[i])
        colors[level], colors[i] = colors[i], colors[level]
        dfs_all_premuations(level + 1, colors, permuations, positions_x[idx], v_poses, edges=edges, depth=depth)
        colors[level], colors[i] = colors[i], colors[level]

def plot_custom_tree(points, edges):
    # get all unique color values from df points
    colors = points["color"].unique()
    color_discrete_map = {}
    for color in colors:
        color_discrete_map[color] = color

    # do a plotly scatter plot where each point has the color defined by the field "color"
    fig = px.scatter(points, x="x", y="y", color="color", color_discrete_map=color_discrete_map)
    fig.update_traces(marker=dict(size=12))

    # plot the lines
    Xe = []
    Ye = []
    for index, row in edges.iterrows():
        Xe+=[points.iloc[row["from"]]["x"], points.iloc[row["to"]]["x"], None]
        Ye+=[points.iloc[row["from"]]["y"], points.iloc[row["to"]]["y"], None]

    fig.add_trace(go.Scatter(x=Xe,
                    y=Ye,
                    mode='lines',
                    line=dict(color='rgb(210,210,210)', width=1),
                    hoverinfo='none'
                    ))
    fig.show()

def main():
    colors = ["red", "green", "blue", "orange", "purple"]
    v_poses = {"x": [0], "y": [0], "color": ["black"]}
    permuations = []
    edges = {"from": [], "to": [], "label": []}
    # dfs_permuations(0, colors, permuations, 0, v_poses, edges, depth=50)
    dfs_all_premuations(0, colors, permuations, 0, v_poses, edges, depth=3)
    # make a dataframe out of the dictionary v_poses
    v_poses = pd.DataFrame(v_poses)
    edges = pd.DataFrame(edges)
    print(v_poses.shape)

    # flip all the y values
    v_poses["y"] = v_poses["y"].apply(lambda x: -x)
    # add the minimum to the y values
    v_poses["y"] = v_poses["y"] + v_poses["y"].min()

    plot_custom_tree(v_poses, edges)


    # Xe, Ye, Xn, Yn, labels = get_tree_data()
    # fig = plot_tree(Xe, Ye, Xn, Yn, labels)
    # fig.show()
    
if __name__ == "__main__":
    main()