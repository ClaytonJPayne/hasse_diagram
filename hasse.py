import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_edges(df):
    """Identifies shortest-step pairs in partial order"""

    short_steps = []

    # Iterate through every pair x R y
    for lab1, row1 in df.iterrows():
        # Ignore self-relation
        if row1['x'] == row1['y']:
            continue
        else: 
            x, y = row1['x'], row1['y']

            # Find potential intermediate steps
            same_x = df[df['x'] == x]
            same_y = df[df['y'] == y]

            smallsteptest = True

            for lab2, row2 in same_x.iterrows():
                # Ignore self-relation
                if row2['x'] == row2['y']:
                    continue
                else:
                    for lab3, row3 in same_y.iterrows():
                        if row3['x'] == row3['y']:
                            continue
                        # If y of same_x matches x of same_y:
                        # Small step test false, move on to next pair
                        elif row3['x'] == row2['y']:
                            smallsteptest = False
                            break
                        else:
                            smallsteptest = True
                    if smallsteptest == False:
                        break
    
            if smallsteptest == True:
                short_steps += [(x, y)]
            else:
                continue
    
    print("\nPartial order relation:\n")
    print(df)
    print("\nPairs to be directly connected in Hasse Diagram:\n")
    print(str(short_steps) + "\n")

    return short_steps

def get_coordinates(edges):
    """Determines location of points on Hasse"""

    points = {}
    
    for pair1 in edges:
        if pair1[0] not in points:
            points[pair1[0]] = (100, 100)
        if pair1[1] not in points:
            points[pair1[1]] = (100, 100)

    points_df = pd.DataFrame(points)
    points_df = pd.DataFrame.transpose(points_df)

    # Increase height of second point until it's higher than first
    iterations = range(len(points))

    for pair2 in edges:
        while ( points_df.loc[pair2[1], 1] <= points_df.loc[pair2[0], 1] ):
            points_df.loc[pair2[1], 1] += 50

    # If two vertices at same height, spread them out
    for lab2, row2 in points_df.iterrows():
        for lab3, row3 in points_df.iterrows():
            if lab2 == lab3:
                continue
            elif ( (row2[0]==row3[0]) and (row2[1] == row3[1]) ):
                row3[0] += 50
            else:
                continue

    print(points_df)
    return points_df

def graph_Hasse(order):
    """Graphs Hasse"""

    order_df = pd.read_csv(order)
    short_steps = get_edges(order_df)
    points = get_coordinates(short_steps)

    xmin = min(points[0]) - 10
    xmax = max(points[0]) + 10
    ymin = min(points[1]) - 10
    ymax = max(points[1]) + 10
    
    plt.scatter(points[0], points[1], s=30, c='black')
    plt.axis([xmin, xmax, ymin, ymax])
    plt.axis('off')

    for lab, row in points.iterrows():
        plt.annotate(str(lab), xy=(row[0]-7, row[1]-2), fontsize=15)

    for edges in short_steps:
        plt.annotate(text = None,
                     xy = ( points.loc[edges[1], 0], points.loc[edges[1], 1] ),
                     xytext = ( points.loc[edges[0], 0], points.loc[edges[0], 1] ),
                     arrowprops = {'width':0.2, 'headwidth':0.2}
                     )
    
    plt.show()

graph_Hasse('partial_order_1.csv')
graph_Hasse('partial_order_2.csv')
graph_Hasse('partial_order_3.csv')
graph_Hasse('partial_order_4.csv')


            
                
            


            
        

