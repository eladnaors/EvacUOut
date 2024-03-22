import igraph as ig
'''creates weight vertex graph'''
def buildplotgraph(g):
    
    # 0
    g.add_vertex('NW0')
    g.add_vertex('NE0')
    g.add_vertex('SW0')
    g.add_vertex('SE0')
    g.add_vertex('NW1')
    g.add_vertex('NE1')
    g.add_vertex('SW1')
    g.add_vertex('SE1')
    g.add_vertex('NW2')
    g.add_vertex('NE2')
    g.add_vertex('SW2')
    g.add_vertex('SE2')
    g.add_vertex('NW3')
    g.add_vertex('NE3')
    g.add_vertex('SW3')
    g.add_vertex('SE3')

    g.vs["Motion"] = [False, False, False, False, False, False, False, False,
                      False, False, False, False, False, False, False, False]
    g.vs["index"] = [0, 1, 2, 3, 4, 5, 6, 7,
                   8, 9, 10, 11, 12, 13, 14, 15]

    g.add_edge('NW0', 'NE0')
    g.add_edge('NE0', 'SW0')
    g.add_edge('SW0', 'SE0')
    g.add_edge('SE0', 'NW0')
    # 1
    g.add_edge('NW0', 'NW1')
    g.add_edge('NE0', 'NE1')
    g.add_edge('SW0', 'SW1')
    g.add_edge('SE0', 'SE1')
    g.add_edge('NW1', 'NE1')
    g.add_edge('NE1', 'SW1')
    g.add_edge('SW1', 'SE1')
    g.add_edge('SE1', 'NW1')
    # 2
    g.add_edge('NW1', 'NW2')
    g.add_edge('NE1', 'NE2')
    g.add_edge('SW1', 'SW2')
    g.add_edge('SE1', 'SE2')
    g.add_edge('NW2', 'NE2')
    g.add_edge('NE2', 'SW2')
    g.add_edge('SW2', 'SE2')
    g.add_edge('SE2', 'NW2')
    # 3
    g.add_edge('NW2', 'NW3')
    g.add_edge('NE2', 'NE3')
    g.add_edge('SW2', 'SW3')
    g.add_edge('SE2', 'SE3')
    g.add_edge('NW3', 'NE3')
    g.add_edge('NE3', 'SW3')
    g.add_edge('SW3', 'SE3')
    g.add_edge('SE3', 'NW3')
    g['edge_label']="ssssss"
    
    for i in range(0,28):
        g.es[i]['edge_color']='black'
        g.es[i]['weight']=1.0
        g.es[i]['edge_label']="ssssss"
        g.es[i]['edge_background']="red"
     
   