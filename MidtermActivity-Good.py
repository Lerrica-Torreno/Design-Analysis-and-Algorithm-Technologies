# TORRENO, Lerrica Jeremy S. (BSCS-DS 2nd yr)
# Midterm Machine Problem 1 - Algorithm Implementation and Data Visualization
# Ford-Fulkerson Algorithm
# user prompt for saving graph, graph is present 

#Import libraries to process data, visualize flow network, network graph, BFS
import pandas as pd  
import networkx as nx 
import matplotlib.pyplot as plt 
from collections import defaultdict, deque  

class Edge:  # tracks connections between teams and assignments
    def __init__(self, to, rev, capacity):
        self.to = to  # stores which node the edge connects
        self.rev = rev  # stores position of reverse edge, used for adjusting flow in residual graph
        self.capacity = capacity  # remaining flow that can pass by the edge
        self.original_capacity = capacity  # stores original capacity for flow calculations

class FordFulkerson:  # finds maximum flow in network
    def __init__(self):  # creates empty graph using dictionary
        # stores edges as list for each node (easy adding and managing connections)
        self.graph = defaultdict(list)

    # Adds forward and reverse edge to the residual graph
    def add_edge(self, fr, to, capacity):
        forward = Edge(to, len(self.graph[to]), capacity) # creates forward edge, stores position to reverse edge
        backward = Edge(fr, len(self.graph[fr]), 0) # creates backward edge, capacity at 0 
        # saves both edge in list 
        self.graph[fr].append(forward)
        self.graph[to].append(backward)

    # Finds max flow from source to sink using BFS to find augmenting paths
    def max_flow(self, source, sink):
        flow = 0 # stores total max flow 
        while True: # stores path, keeps track of visited, starts BFS, keeps track if found a valid path
            parent = {}
            visited = set()
            queue = deque([source])
            visited.add(source)
            found = False

            # BFS to find augmenting path
            while queue:
                node = queue.popleft() # get next node from queue
                if node == sink:
                    found = True
                    break # sink is reached, stop BFS 
                for i, edge in enumerate(self.graph[node]): # loops all edges from node
                    if edge.capacity > 0 and edge.to not in visited: # check for available capacity and if visited
                        visited.add(edge.to) # marks edge as visited
                        parent[edge.to] = (node, i) # store parent node to reconstruct path later 
                        queue.append(edge.to)

            if not found:
                break  # No augmenting path found

            # Tracks smallest capacity in the path (bottleneck), and backtracks from sink to source 
            # each step checks the smallest available capacity  
            path_flow = float('inf')
            v = sink
            while v != source:
                u, i = parent[v]
                path_flow = min(path_flow, self.graph[u][i].capacity)
                v = u

            # Update residual capacities, moves backward from sink to source, reduces capacity of forward edge
            # increases capacity of reverse edge (allows backtracking)
            v = sink
            while v != source:
                u, i = parent[v]
                self.graph[u][i].capacity -= path_flow
                self.graph[v][self.graph[u][i].rev].capacity += path_flow
                v = u
            
            # add found path's flow to total max flow
            flow += path_flow
        return flow

def load_data(file_path):
    try:
        df = pd.read_csv(file_path, dtype=str)  # Read all data as strings first for validation

        # Ensure required columns exist
        required_columns = ['Student_ID', 'First_Name', 'Study_Hours_per_Week', 'Department']
        for col in required_columns:
            if col not in df.columns:
                print(f"Error: Missing required column '{col}' in CSV file.")
                return None

        # Track invalid rows for error messages
        invalid_rows = []

        # Iterate through rows to check validity
        for index, row in df.iterrows():
            student_id, first_name, study_hours, department = row['Student_ID'], row['First_Name'], row['Study_Hours_per_Week'], row['Department']
            # Check if any field is empty
            if pd.isna(student_id) or pd.isna(first_name) or pd.isna(study_hours) or pd.isna(department):
                invalid_rows.append((index + 2, "Contains blank values"))  # +2 for correct row number in the CSV
                continue
            # Check if First_Name and Department contain only letters
            if not first_name.replace(" ", "").isalpha():
                invalid_rows.append((index + 2, "Invalid First_Name (must contain only letters)"))
                continue
            if not department.replace(" ", "").isalpha():
                invalid_rows.append((index + 2, "Invalid Department (must contain only letters)"))
                continue
            # Check if Study_Hours_per_Week contains only numbers (integers or decimals)
            try:
                float(study_hours)  # Convert to float to check validity
            except ValueError:
                invalid_rows.append((index + 2, "Invalid Study_Hours_per_Week (must be a number)"))
                continue

        # If there are invalid rows, print error messages and remove them
        if invalid_rows:
            print("\n  Errors found in the following rows:")
            for row_num, error_msg in invalid_rows:
                print(f"  - Row {row_num}: {error_msg}")

            # Remove invalid rows
            df = df.drop([row[0] - 2 for row in invalid_rows]).reset_index(drop=True)
            print("\n Proceeding with valid data...\n")

        # Convert Study_Hours_per_Week to numeric after validation
        df['Study_Hours_per_Week'] = df['Study_Hours_per_Week'].astype(float)

        return df if not df.empty else None  # Return None if all rows are invalid

    except Exception as e:
        print(f"Error loading file: {e}")
        return None

# Builds the flow network graph based on student data
def build_flow_network(df):
    ff = FordFulkerson() # for max flow
    source = "Source" # study hours start
    sink = "Sink" # study hours end, assignments completed 

    assignments = ["Math", "Science", "English", "History"] # can add more

    # Groups students by their departments, sums up total study hrs per week for each dept
    # converts to dictonary, and extract departments names into list of teams 
    team_hours = df.groupby("Department")["Study_Hours_per_Week"].sum().to_dict() # determines study hours per dept
    teams = list(team_hours.keys())

    # connects "Source" to each dept (team)
    # capacity of each edge is equal to he ttal study hours of that team
    for team, total_hours in team_hours.items():
        ff.add_edge(source, team, total_hours) # connects team to source with available study hours

        # each team distributes its study hours evenly across n assignments
        per_task = total_hours / len(assignments)
        for task in assignments:
            ff.add_edge(team, task, per_task) # split each team's study hours among 4 assignments

    # sums all students' study houurs, distribted equally to assignments
    # connects each assignment to sink 
    total_hours_all = df['Study_Hours_per_Week'].sum()
    per_assignment = total_hours_all / len(assignments)
    for task in assignments:
        ff.add_edge(task, sink, per_assignment)
    # flow network, starting point, endpoint, list of dept names, list of assignment names
    return ff, source, sink, teams, assignments

# Calculates the node positions for visualization
def get_layered_positions(teams, assignments):
    pos = {} # empty dictionary to store coordinates of each node
    pos["Source"] = (0, 0) # position of node
    # x-axis (1 for dept, 2 for assigments)
    # y-axis based on position in the list
    for i, team in enumerate(teams): 
        pos[team] = (1, i) # teams placed at (1, i) i - position in teams list
    for j, assignment in enumerate(assignments):
        pos[assignment] = (2, j)  # assignments placed at (2, j) j - position in assignments list
    pos["Sink"] = (3, 0)
    return pos

# Draws the graph and shows assigned study hours on the side
# flow network object (stores nodes & connections), title, filename, list of teams, list of assignments
def visualize_graph(ff, title="Task Assignment and Workload Balancing",
                    save_path="workload_balancing.png",
                    students=None, assignments=None, should_save=False):  # added should_save parameter
    import matplotlib.patches as mpatches # for adding legend to the graph 
    import matplotlib.pyplot as plt # for drawing the graph 
    import networkx as nx # for creating and visualizing the flow network 
    plt.close('all') # prevents overlap
    G = nx.DiGraph() # ensures edges have direction 

    # Reconstruct flow used in each edge for visualization
    # loop each node in network
    for node, edges in ff.graph.items():
        G.add_node(node) # add each node to graph after each loop
        for edge in edges:
            if edge.original_capacity > 0: # checks if edge originally had capacity
                flow_used = edge.original_capacity - edge.capacity # calculates how much flow was used
                if flow_used > 0:
                    G.add_edge(node, edge.to, flow=flow_used)     # if flow was used, will be added the edge to graph 

    # Use layered layout or spring layout if undefined
    if students is not None and assignments is not None: # if students nd assignments are provided
        pos = get_layered_positions(students, assignments) # keeps nodes arranged in layers (left-right) for readability
    else:
        pos = nx.spring_layout(G, seed=42) # if positions are not defined, automatically spaces out nodes (avoid overlap)

    plt.figure(figsize=(15, 6))

    source_sink = ["Source", "Sink"] # start and end points
    team_nodes = [n for n in students if n not in source_sink] # teams (departments)
    assignment_nodes = assignments 

    # Draw node types with different colors
    nx.draw_networkx_nodes(G, pos, nodelist=["Source", "Sink"],
                           node_color="white", edgecolors="black", node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=team_nodes,
                           node_color="lightgreen", edgecolors="black", node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=assignment_nodes,
                           node_color="skyblue", edgecolors="black", node_size=3000)

    nx.draw_networkx_labels(G, pos, font_size=9)
    nx.draw_networkx_edges(G, pos, arrows=True)

    # Group edge flows into categories for display
    source_flows = [] # source - teams
    team_flows = [] # teams - assignments
    sink_flows = [] # assignments - sink

    for (u, v, d) in G.edges(data=True):
        if "flow" in d:
            flow_str = f"{u} → {v}: {d['flow']:.1f}"
            if u == "Source":
                source_flows.append(flow_str)
            elif v == "Sink":
                sink_flows.append(flow_str)
            else:
                team_flows.append(flow_str)

    edge_flows = (
        ["Source to Team:"] + source_flows +
        ["", "Team to Assignment:"] + team_flows +
        ["", "Assignment to Sink:"] + sink_flows
    )

    # displays assigned study hours on the right side of graph
    # plt.figtext() to print flow values
    flow_text = "\n".join(edge_flows)
    plt.figtext(1.02, 0.95, "Assigned Study Hours", fontsize=10, fontweight='bold', ha='left')
    plt.figtext(1.02, 0.93, "(Grouped by Flow)", fontsize=9, ha='left')
    plt.figtext(1.02, 0.91, flow_text, fontsize=8, ha='left', va='top', linespacing=1.2)

    # Node color legend for explanation
    legend_elements = [
        mpatches.Patch(facecolor='lightgreen', edgecolor='black', label='Team (Department)'),
        mpatches.Patch(facecolor='skyblue', edgecolor='black', label='Assignment'),
        mpatches.Patch(facecolor='white', edgecolor='black', label='Source / Sink'),
    ]
    plt.legend(handles=legend_elements, loc='lower center', ncol=3, frameon=True)

    plt.title(title)
    plt.tight_layout()

    # Conditionally save the figure
    if should_save:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print("Graph saved as 'workload_balancing.png'.")
    plt.show()  # Show the graph

# Outputs final team-to-assignment flows to CSV
def export_assignment_details(ff, output_csv="assignment_distribution.csv"):
    assignment_data = [] # list of assignment details that will be converted to table
    for node, edges in ff.graph.items(): # loops through all nodes in network
        if node not in ["Source", "Sink"]: # processes department nodes (teams)
            for edge in edges: # processes all team-to-assignment connections
                if edge.original_capacity > 0: # filters unnecessary edges 
                    flow_used = edge.original_capacity - edge.capacity # calculates actual assigned study hours
                    if flow_used > 0 and edge.to not in ["Source", "Sink"]: # filers invalid/0 hour assignments
                        assignment_data.append({
                            "Team": node,
                            "Assignment": edge.to,
                            "Hours_Assigned": flow_used
                        })

    df_assignments = pd.DataFrame(assignment_data) # creates pandas dataframe (prep data for saving & printing)
    if not df_assignments.empty: # prevents saving an empty file
        df_assignments.to_csv(output_csv, index=False)
        print("\n--- Assignment Distribution ---")
        print(df_assignments.to_string(index=False))
        print(f"\nSaved assignment distribution to: {output_csv}")
    else:
        print("\nNo assignment flows found.") # error handling if empty file

# Entry point: load data, build graph, compute max flow, visualize and export
def main():
    file_path = "Students_Grading_Dataset.csv"
    df = load_data(file_path)
    if df is not None and not df.empty:
        ff, source, sink, teams, assignments = build_flow_network(df)
        max_flow_value = ff.max_flow(source, sink)
        print(f"Maximum Study Hours Assigned: {max_flow_value}")

        # Ask user if they want to save the graph
        save_graph = input("Do you want to save the graph? Type Y for yes, and N for No: ").strip().upper()
        should_save = (save_graph == 'Y')

        # Visualize the graph and conditionally save it
        visualize_graph(ff,
                        title="Task Assignment and Workload Balancing by Team",
                        students=teams,
                        assignments=assignments,
                        should_save=should_save)

        export_assignment_details(ff)
    else:
        print("DataFrame is empty or None. Please check your CSV file.")

if __name__ == "__main__":
    main()
