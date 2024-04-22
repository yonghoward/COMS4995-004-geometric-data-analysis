import random
import networkx as nx
import matplotlib.pyplot as plt

def main():
    '''
    # Example 1 (Pure): 3 players, 2 strategies, 2 eq
    vertices = [(0,0,0), (1,0,0), (0,1,0), (1,1,0), (0,0,1), (1,0,1), (0,1,1), (1,1,1)]
    payouts = [
        (0.52, 0.7, 0.42), 
        (0.22, 0.64, 0.12), 
        (0.2, 0.7, 0.56), 
        (0.85, 0.77, 0.58), 
        (0.2, 0.54, 0.17), 
        (0.11, 0.57, 0.79), 
        (0.19, 0.09, 0.39), 
        (0.95, 0.53, 0.05)
    ]
    '''
    '''
    # Example 2 (Pure): 2 players, 2 strategies, 1 eq
    vertices = [(0,0), (0,1), (1, 0), (1, 1)]
    payouts = [
        (1,1),
        (1,-1),
        (-1,1),
        (0,0)
    ]
    '''
    '''
    # Example 3 (Pure): 2 players, 3 strategies, 0 eq
    vertices = [(0,0), (0,1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    payouts = [(0,0), (-2,2), (1,-1),
        (2,-2), (0,0), (-1,1),
        (-1,1), (1,-1), (0,0)
    ]
    '''
    vertices = [(0,0), (0,1), (1, 0), (1, 1)]
    payouts = [
        (3,3), (1,5), 
        (5,1), (0,0)
    ]


    G = nx.DiGraph()
    for i in range(len(vertices)):
        v = vertices[i]
        p = payouts[i]
        G.add_node(v, payout=p)

    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)):
            v1, v2 = vertices[i], vertices[j]
            if sum((a-b)**2 for a, b in zip(v1, v2)) == 1:
                curr_player = [a != b for a, b in zip(v1, v2)].index(True)
                p1, p2 = G.nodes[v1]['payout'][curr_player], G.nodes[v2]['payout'][curr_player]

                if p1 < p2:     # Weight edges by benefit in paylod by changing strategy
                    G.add_edge(v1, v2, weight=p2-p1)
                elif p1 > p2:
                    G.add_edge(v2, v1, weight=p1-p2)

    pr = nx.pagerank(G, alpha=0.85)
    for node in pr:
        print(node, pr[node])

    '''pos = nx.spring_layout(G)
    nx.draw(G, pos, node_size=100, node_color='lightblue', with_labels=True, font_size=10)
    plt.show()'''

    return
    

if __name__ == '__main__':
    main()