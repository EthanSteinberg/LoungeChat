import json

input_text = open('out2.data', 'r').read()

def create_graph(data): 
	result =  "strict digraph {"
	
	for start_node in data.keys():
		for end_node in data[start_node].keys():
			weight = data[start_node][end_node]

			result += "\"{}\" -> \"{}\"[label=\"{}\"];".format(start_node.replace(" ", ""), end_node.replace(" ", ""), weight)

	return result + "}"

print(create_graph(json.loads(input_text)))