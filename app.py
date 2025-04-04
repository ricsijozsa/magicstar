import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import base64

from pulp_megoldas import get_pulp_solution, c1, c2, c3, c4
from itertools_megoldas_0323 import get_brute_force_solution

# hatter beolvasasa
def load_bg_base64(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# kep betoltese
bg_base64 = load_bg_base64("image.png")

# css stilus
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    html, body, .block-container {{
        background-color: rgba(0, 0, 0, 0.6);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }}
    h1 {{
        text-align: center;
        color: #00cfff;
        font-size: 3em;
        text-shadow: 2px 2px 8px black;
    }}
    .stButton>button {{
        background-color: #ae00ff;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        font-size: 16px;
        border: none;
        box-shadow: 0 0 15px #ff7b00;
    }}
    .stButton>button:hover {{
        background-color: #ff7b00;
        transform: scale(1.05);
    }}
    </style>
""", unsafe_allow_html=True)

# cim
st.markdown("<h1>Mágikus Csillag Megoldó</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; font-size: 18px;'>Válassz módszert és nézd meg az eredményt</div>", unsafe_allow_html=True)

# modszer valasztas
method = st.radio("Módszer:", ["Pulp", "Brute Force"], horizontal=True)

# inditas gomb
if st.button("Indítás"):

    # brute force figyelmeztetes
    if method == "Brute Force":
        info = "Számolás folyamatban... lehet hogy több perc lesz (mivel  kb 50 000 permutacio / mp)"
    else:
        info = "Számítás folyamatban..."

    with st.spinner(info):
        solution = get_pulp_solution() if method == "Pulp" else get_brute_force_solution()

    if solution:
        st.success("Megoldás megtalálva")

        # csomopont ertekek
        nodes = {
            0: solution[0], 1: solution[1], 2: solution[2], 3: solution[3],
            4: solution[4], 5: solution[5], 6: solution[6], 7: solution[7],
            8: c1, 9: c2, 10: solution[8], 11: solution[9],
            12: c3, 13: solution[10], 14: c4, 15: solution[11],
        }

        # graf letrehozasa
        G = nx.Graph()
        inner = list(range(8))
        outer = list(range(8, 16))
        G.add_nodes_from(inner + outer)

        # elek
        for i in range(8):
            G.add_edge(inner[i], inner[(i + 1) % 8])
            G.add_edge(inner[i], outer[i])

        # poziciok
        pos = {}
        for i in range(8):
            angle = 2 * np.pi * i / 8
            pos[inner[i]] = (1.2 * np.cos(angle), 1.2 * np.sin(angle))
            pos[outer[i]] = (2.0 * np.cos(angle), 2.0 * np.sin(angle))

        # kiemelt utak
        highlight_paths = [(8, 0, 1, 9), (10, 2, 3, 11), (12, 4, 5, 13), (14, 6, 7, 15)]

        # rajz
        fig, ax = plt.subplots(figsize=(7, 7))
        nx.draw_networkx_nodes(G, pos, node_color='#fff8dc', edgecolors='black', node_size=800)
        nx.draw_networkx_labels(G, pos, labels=nodes, font_size=12, font_weight='bold')
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='#888888', width=2)

        for path in highlight_paths:
            edge_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color='#ff7b00', width=6)

        plt.axis('off')
        st.pyplot(fig)

        # tabla
        with st.expander("Megoldás részletei"):
            values = [nodes[i] for i in range(16)]
            st.dataframe({f"Csomópont {i}": [v] for i, v in enumerate(values)})

    else:
        st.error("Nincs megoldás")
