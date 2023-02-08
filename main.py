#importation des modules
import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import random as rd
import random

#définition de la class node
class Node:
    def __init__(self, id, Energy):
        self.id = id
        self.status = 0
        self.Energy = Energy
        self.En_max = Energy

#la list des noudes à representer 
nodes_list = []

#initialisation de l'interface 
root = tk.Tk()

#les fonctions d'affichages des graphs
Frame2 = Frame(root, borderwidth=2, relief=GROOVE, width= 300, height= 300)
Frame2.grid(padx=5, pady=5, row=0, column=3, rowspan=5)


############################## la graphe de l'énergie ##################################
def update_graph(canvas, ax):
    for node in nodes_list:
        node.Energy = random.randint(0, int(node.Energy))
    data = [node.Energy for node in nodes_list]
    ax.clear()
    ax.bar(range(len(data)), data)
    canvas.draw()

def energy_graph():
    figure = Figure(figsize=(6, 4), dpi=100)
    ax = figure.add_subplot(111)
    figure.set_size_inches(3, 3)
    canvas = FigureCanvasTkAgg(figure, Frame2)
    canvas.get_tk_widget().grid(padx=5, pady=5, row=0, column=3, rowspan=5)
    update_graph(canvas, ax)

########################################################################################   

############################## la graphe des nodes ##################################
def show_nodes(ch):
    nodes = []
    for node in nodes_list:
        if(node.id!=ch.id):
            nodes.append((node.id, ch.id))
    G = nx.DiGraph(
        nodes
    )

    for layer, nodes in enumerate(nx.topological_generations(G)):
        for node in nodes:
            G.nodes[node]["layer"] = rd.randint(0, 5)
            
    pos = nx.multipartite_layout(G, subset_key="layer")
    fig, ax = plt.subplots()
    
    nx.draw_networkx(G, pos=pos, ax=ax,)
    ax.set_title("LEACH PROTOCOL")
    fig = plt.gcf()
    fig.set_size_inches(3, 3)
    canvas_graph = FigureCanvasTkAgg(fig, master=Frame1)
    canvas_graph.draw()
    canvas_graph.get_tk_widget().grid(padx=5, pady=5, row=0, column=2, rowspan=9)

######################################################################################## 

#les paramétres
N, r, P, En_max, En_current = 0, 0, 0, 0, 0

###############################les entrées et les buttons ###############################
Label(root, text="N : ").grid(row=0, column=0, )
entree1 = Entry(root, width=15)
entree1.grid(row=0, column=1,)

Label(root, text="r : ").grid(row=1, column=0,)
entree2 = Entry(root, textvariable=r, width=15)
entree2.grid(row=1, column=1,)

Label(root, text="P : ").grid(row=2, column=0,)
entree3 = Entry(root,  width=15,)
entree3.grid(row=2, column=1,)

Label(root, text="En_max : ").grid(row=3, column=0,)
entree4 = Entry(root,  width=15,)
entree4.grid(row=3, column=1,)

#les deux interfaces pour l'affichage des graphs 
Frame1 = Frame(root, borderwidth=2, relief=GROOVE, width= 300, height= 300)
Frame1.grid(padx=5, pady=5, row=0, column=2, rowspan=5)

Canvas(Frame1, width=300, height=300, bg='ivory').grid(padx=5, pady=5, row=0, column=2, rowspan=5)
Canvas(Frame2, width=300, height=300, bg='ivory').grid(padx=5, pady=5, row=0, column=3, rowspan=5)

###############################################################################################


# choix du noudes qui va étre CH
def set_CH(P, r):
    n = nodes_list[0]
    for node in nodes_list:
        node.status = 0
        a = P/(1 - (r % (1/P)))
        e = node.Energy * node.En_max
        t = a/e
        rnd = random.uniform(0, 1)
        if rnd<t: 
            node.status = 1
            n = node
            i = nodes_list.index(n)
            nodes_list[i].status=1
    return n

#Submite 
def show_graphs():
    global nodes_list 
    nodes_list = []
    N = int(entree1.get())
    r = int(entree1.get())
    P = int(entree1.get())
    En_max = int(entree1.get())
    for i in range(N):
        node = Node(i, En_max)
        nodes_list.append(node)
    n = set_CH(P, r)
    show_nodes(n)
    energy_graph()

Button(root, text ='Submite', command= show_graphs, width= 25).grid(padx=5, pady=5, row=4, column=0, columnspan=2)


root.mainloop()