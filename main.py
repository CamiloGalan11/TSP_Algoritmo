import random
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from copy import deepcopy

# =====================
# PARÁMETROS DE CONFIGURACIÓN
# =====================
MAX_ITER = 500  # Número máximo de iteraciones
TABU_TENURE = 10  # Tenencia Tabú
ASPIRATION_CRITERIA = True  # Permitir soluciones mejores aunque estén en la lista tabú
MOVE_TYPE = "swap"  # Tipo de movimiento (intercambio de nodos)

# =====================
# MATRIZ DE DISTANCIAS
# =====================
distancias = {
    'Ocaña':     {'Cúcuta': 200, 'Pamplona': 240, 'Tibú': 150, 'Ábrego': 50},
    'Cúcuta':    {'Ocaña': 200, 'Pamplona': 75,  'Tibú': 120, 'Ábrego': 230},
    'Pamplona':  {'Ocaña': 240, 'Cúcuta': 75,  'Tibú': 190, 'Ábrego': 270},
    'Tibú':      {'Ocaña': 150, 'Cúcuta': 120, 'Pamplona': 190, 'Ábrego': 170},
    'Ábrego':    {'Ocaña': 50,  'Cúcuta': 230, 'Pamplona': 270, 'Tibú': 170},
}

# Crear grafo
G = nx.Graph()
for o, destinos in distancias.items():
    for d, w in destinos.items():
        G.add_edge(o, d, weight=w)

# Lista de ciudades
ciudades = list(G.nodes)
n = len(ciudades)

# Función para calcular la distancia total de una solución
def calcular_distancia(solucion):
    return sum(G[solucion[i]][solucion[i+1]]['weight'] for i in range(len(solucion) - 1)) + G[solucion[-1]][solucion[0]]['weight']

# Generar solución inicial
def generar_solucion_inicial():
    sol = ciudades[:]
    random.shuffle(sol)
    return sol

# Movimiento: intercambio de dos ciudades
def generar_vecinos(solucion):
    vecinos = []
    for i in range(len(solucion)):
        for j in range(i+1, len(solucion)):
            nuevo = solucion[:]
            nuevo[i], nuevo[j] = nuevo[j], nuevo[i]
            vecinos.append((nuevo, (i, j)))
    return vecinos

# =====================
# ALGORITMO TABU SEARCH
# =====================
sol_actual = generar_solucion_inicial()
mejor_sol = deepcopy(sol_actual)
mejor_dist = calcular_distancia(mejor_sol)
tabu_list = {}

for iteracion in range(MAX_ITER):
    vecinos = generar_vecinos(sol_actual)
    vecinos_validos = []

    for vecino, movimiento in vecinos:
        if movimiento not in tabu_list or (ASPIRATION_CRITERIA and calcular_distancia(vecino) < mejor_dist):
            vecinos_validos.append((vecino, movimiento))

    if not vecinos_validos:
        break

    vecino_seleccionado, movimiento = min(vecinos_validos, key=lambda x: calcular_distancia(x[0]))
    sol_actual = vecino_seleccionado
    dist_actual = calcular_distancia(sol_actual)

    if dist_actual < mejor_dist:
        mejor_sol = deepcopy(sol_actual)
        mejor_dist = dist_actual

    # Actualizar lista tabú
    tabu_list[movimiento] = TABU_TENURE
    for move in list(tabu_list.keys()):
        tabu_list[move] -= 1
        if tabu_list[move] <= 0:
            del tabu_list[move]

# =====================
# VISUALIZACIÓN
# =====================
# Dibujar el grafo
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

# Dibujar la mejor solución encontrada
path = mejor_sol + [mejor_sol[0]]
path_edges = list(zip(path, path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

# Ventana con resultados
recorrido_str = " → ".join(path)
info_str = f"Recorrido óptimo:\n{recorrido_str}\n\nDistancia total: {mejor_dist} km"
root = tk.Tk()
root.withdraw()
messagebox.showinfo("Resultado Búsqueda Tabú", info_str)

fig = plt.gcf()
fig.canvas.manager.set_window_title("TSP - Tabu Search")
plt.title("Recorrido del TSP con Búsqueda Tabú")
plt.show()
