import json
from glob import glob
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
input_folder = os.path.join(dir_path, 'operations')
output_path = os.path.join(dir_path, 'graphFile.json')

operations = []
for op in glob(os.path.join(input_folder, '*.json')):
    with open(op, 'r') as f:
        operations.append(json.load(f))

for op in operations:
    op['inputs'] = []
    op['outputs'] = []
    fields = op[u'field_types']
    for f in fields:
        if f[u'role'] == u'input':
            op['inputs'].append(f)
        if f[u'role'] == u'output':
            op['outputs'].append(f)


nodes = []
node_to_group = {}
for i, op in enumerate(operations):
    node_to_group[op['name']] = i
    nodes.append(
    {
            'name': op['name'],
            'group': i
        }
    )

links = []
for op1 in operations:
    inputs = op1['inputs']
    for op2 in operations:
        outputs = op2['outputs']
        for i in inputs:
            for o in outputs:
                for it in i['object_types']:
                    for ot in o['object_types']:
                        if it == ot:
                            links.append(
                                {
                                    'source': node_to_group[op2['name']],
                                    'target': node_to_group[op1['name']],
                                    'weight': 1,
                                    'object_type': ot
                                })
data = {'nodes': nodes, 'links': links}
json.dump(data, open(output_path, 'w'))