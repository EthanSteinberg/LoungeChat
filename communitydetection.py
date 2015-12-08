import json
import numpy as np
import numpy.linalg
import math

input_text = open('out2.data', 'r').read()
data = json.loads(input_text)

index_func = {}
next_id = 0

invert = {}

switch_func = .15

def add_to_index(name):
	global next_id
	if name not in index_func:
		index_func[name] = next_id
		invert[next_id] = name
		next_id += 1
	
last_length = 0

for source in data:
		data[source] = {i:data[source][i] for i in data[source] if data[source][i] > 20}

while last_length != len(data):
	print(data)
	last_length = len(data)
	for source in data:
		data[source] = {i:data[source][i] for i in data[source] if i in data}

	data = {i:data[i] for i in data if len(data[i]) != 0}

for source in data:
	add_to_index(source)

#print(data)

matrix = np.empty([next_id, next_id])
matrix.fill(switch_func/next_id)

better = np.zeros([next_id, next_id])

for source in data:
	total_weight = sum(data[source].values())
	for destination in data[source]:
		data[source][destination] = (data[source][destination]/total_weight)
		better[index_func[source]][index_func[destination]] = data[source][destination]

		matrix[index_func[destination]][index_func[source]] += (1-switch_func)*data[source][destination]

matrix = matrix - np.identity(next_id)

for i in range(next_id):
	matrix[0][i] = 1


target = np.zeros(next_id)
target[0] = 1

steady_state = np.linalg.solve(matrix, target)

print(steady_state)



def compute_leave(items_in_module):
	return (switch_func * (next_id - len(items_in_module))/(next_id - 1) * sum(steady_state[a] for a in items_in_module) +
		(1- switch_func)*sum(steady_state[a] * sum(better[a][b] for b in range(next_id) if b not in items_in_module) for a in items_in_module))

def last_term(modules_map, leaves):
	total = 0
	for leave, items in zip(leaves, modules_map):
		temp = leave + sum(steady_state[i] for i in items)
		total += temp * math.log(temp)

	return total


def total_score(modules_map, leaves):
	total_leaves = sum(leaves)

	last = last_term(modules_map, leaves)

	return total_leaves*math.log(total_leaves) - 2 * sum(leave * math.log(leave) for leave in leaves) + last

modules_map = [[i] for i in range(next_id)]
leaves = [compute_leave(items) for items in modules_map]

while len(modules_map) > 2:
	print(len(modules_map))
	best_score = total_score(modules_map, leaves)
	best_map = modules_map
	best_leaves = leaves

	for i in range(len(modules_map)):
		for j in range(len(modules_map)):
			new_modules_map = list(modules_map)
			new_leaves = list(leaves)

			new_modules_map[i] = new_modules_map[i] + new_modules_map[j]
			new_leaves[i] = compute_leave(new_modules_map[i])

			del new_modules_map[j]
			del new_leaves[j]

			#print (new_modules_map)
			score = total_score(new_modules_map, new_leaves)

			if score < best_score:
				best_score = score
				best_map = new_modules_map
				best_leaves = new_leaves

	if best_map is modules_map:
		break

	modules_map = best_map
	leaves = best_leaves

mapped = [[invert[i] for i in m] for m in modules_map]

print (mapped)
		

