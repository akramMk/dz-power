import networkx as nx  
import os
# import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


def generate_aspartix(arguments, attacks):
    aspartix_str = ""

    # Generate argument atoms
    for arg in arguments:
        aspartix_str += f"arg({arg.name}).\n"

    # Generate attack atoms
    for attack in attacks:
        attacker, defender = attack
        aspartix_str += f"att({attacker.name},{defender.name}).\n"

    return aspartix_str

def generate_graph(all_arguments,all_defeats) :
    aspartix_output = generate_aspartix(all_arguments, all_defeats)
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes and edges to the graph
    for arg in all_arguments:
        G.add_node(arg.name)
    for a in all_defeats:
        G.add_edge(a[0].name, a[1].name)

    # Draw the graph
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')
    
    # Check if the image exists and delete it
    if os.path.exists('static/graph.png'):
        os.remove('static/graph.png')

    plt.title(f"Node Graph of {len(all_arguments)} Nodes")
    plt.subplots_adjust(top=0.5)

    # Save the graph image
    plt.savefig('static/graph.png',bbox_inches='tight')
    plt.close()

def generate_histogram(all_arguments, all_defeats):
    # Create a directed graph (if not already available)
    G = nx.DiGraph()
    for arg in all_arguments:
        G.add_node(arg.name)
    for a in all_defeats:
        G.add_edge(a[0].name, a[1].name)

    # Calculate in-degree for each node
    in_degrees = [G.in_degree(n) for n in G.nodes()]

    # Generate histogram data
    max_degree = max(in_degrees) + 1 if in_degrees else 1
    counts = [0] * max_degree
    for degree in in_degrees:
        counts[degree] += 1

    # Plot the histogram
    plt.figure()
    plt.bar(range(max_degree), counts, color='skyblue')
    plt.xlabel('Degree of Defeat (In-Degree)')
    plt.ylabel('Number of Arguments')
    plt.title('Histogram of Arguments by Degree of Defeat')

    # Save the histogram image
    plt.savefig('static/histogram.png')
    plt.close()





