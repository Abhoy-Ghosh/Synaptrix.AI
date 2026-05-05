import os
import ast
import networkx as nx
from pyvis.network import Network

# -----------------------------
# BASE PATH (project root)
# -----------------------------
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

# -----------------------------
# CONFIG (TUNE HERE)
# -----------------------------
IGNORE_FOLDERS = ["venv", "__pycache__"]
IMPORTANT_ONLY = True   # 🔥 show only meaningful modules

# -----------------------------
# GET FILES
# -----------------------------
def get_py_files():
    files = []
    for root, _, filenames in os.walk(BASE_PATH):
        if any(ignored in root for ignored in IGNORE_FOLDERS):
            continue

        for f in filenames:
            if f.endswith(".py"):
                files.append(os.path.join(root, f))
    return files


# -----------------------------
# EXTRACT IMPORTS
# -----------------------------
def get_imports(file_path):
    imports = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

    except Exception:
        pass

    return imports


# -----------------------------
# MODULE NAME
# -----------------------------
def get_module_name(path):
    return path.replace(BASE_PATH, "") \
        .replace("/", ".") \
        .replace("\\", ".") \
        .replace(".py", "") \
        .strip(".")


# -----------------------------
# FILTER IMPORTANT FILES
# -----------------------------
def is_important(module):
    if not IMPORTANT_ONLY:
        return True

    keywords = [
        "pipeline", "agents", "services",
        "retriever", "synthesizer",
        "llm", "vector", "cache"
    ]

    return any(k in module for k in keywords)


# -----------------------------
# LAYER DETECTION
# -----------------------------
def get_layer(module):
    if "pipeline" in module:
        return "core"
    elif "agents" in module:
        return "agents"
    elif "services" in module:
        return "services"
    elif "cache" in module or "vector" in module:
        return "storage"
    else:
        return "other"


# -----------------------------
# COLOR MAP
# -----------------------------
def get_color(layer):
    return {
        "core": "#ff4d4d",      # red
        "agents": "#4da6ff",    # blue
        "services": "#66cc66",  # green
        "storage": "#ffcc00",   # yellow
        "other": "#aaaaaa"
    }.get(layer, "#aaaaaa")


# -----------------------------
# BUILD GRAPH
# -----------------------------
def build_graph():
    G = nx.DiGraph()

    py_files = get_py_files()
    module_map = {}

    # map modules
    for f in py_files:
        mod = get_module_name(f)

        if is_important(mod):
            module_map[mod] = f
            G.add_node(mod)

    # build edges
    for f in py_files:
        src = get_module_name(f)

        if src not in module_map:
            continue

        imports = get_imports(f)

        for imp in imports:
            imp = imp.strip()

            for mod in module_map:
                # strong matching
                if mod.endswith(imp) or imp in mod.split("."):
                    if src != mod:
                        G.add_edge(src, mod)

    return G


# -----------------------------
# VISUALIZATION
# -----------------------------
def visualize_graph(output_file="codebase_graph.html"):
    G = build_graph()

    net = Network(height="1800px", width="100%", directed=True)
    net.barnes_hut()  # 🔥 clean layout

    for node in G.nodes:
        layer = get_layer(node)
        color = get_color(layer)

        size = 25
        if "pipeline" in node:
            size = 50  # highlight main brain

        net.add_node(
            node,
            label=node.split(".")[-1],
            color=color,
            size=size,
            title=f"{node}\nLayer: {layer}"
        )

    for src, dst in G.edges:
        net.add_edge(src, dst)

    net.write_html(output_file)

    print(f"✅ Graph generated → {output_file}")