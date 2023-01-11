import re
import subprocess
import time

template = "create\nadd {} vertices\nbuild {} {} {} 36\nbin 0 164 9\nbin 1 148 5\nbin 2 128 3\nbin 3 70 2\nbin 4 66 2\nbin 5 54 2\nbin 6 28 2\nbin 7 20 3\nbin 8 32 1\nbin 9 24 2\ncommit"



def get_graph_statistics(output, runtime):
    output_list = output.split("\n")
    match_average_degree = re.compile("The average degree of the graph ")
    match_needed_vertices = re.compile("total number of vertices needed by ")
    match_graph_size = re.compile("The graph has .* vertices and .* active edges")
    average_degree = list(filter(match_average_degree.match, output_list))[0].split(":")[-1]
    needed_vertices = list(filter(match_needed_vertices.match, output_list))[0].split(":")[-1]
    graph_size = list(filter(match_graph_size.match, output_list))[0]
    number_vertices = graph_size.split(" ")[3]
    number_edges = graph_size.split(" ")[6]
    return [runtime, float(number_vertices), float(number_edges), float(average_degree), float(needed_vertices), float(number_edges) / runtime]


def time_dygraph_from_script(number_of_vertices, exponent, scaling_factor, max_deg):
    write_commands_file(number_of_vertices, exponent, scaling_factor, max_deg)
    start_time = time.time()
    output = subprocess.run(['./dyGraph_gen'], capture_output=True, text=True, input="2")
    end_time = time.time()
    statistics = get_graph_statistics(output.stdout, end_time - start_time)
    ## TODO Extract Average Degree and Total Vertices needed
    ## TODo also extract actually number of nodes and edges created
    return statistics


def get_maximal_degree(number_of_vertices):
    return int(number_of_vertices * 0.5)


def write_commands_file(number_of_vertices, exponent, scaling_factor, max_deg):
    commands = template.format(number_of_vertices, exponent, scaling_factor, max_deg)
    f = open("commands.txt", "w")
    f.write(commands)
    f.close()
