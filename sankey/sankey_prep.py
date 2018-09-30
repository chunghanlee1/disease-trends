import pandas as pd
import floweaver as fl

filepath = '../data_extraction/research/'
df = pd.read_csv(filepath + 'ncomms5212-s4.txt', sep='\t')

####################################
# TODO
# How many symptoms to show
# Which diseases to show
# How to link up with final visualization: store a json for each mapping or execute this script every-time?
####################################

# only look at one disease
one_disease = 'HIV Infections' ### EDIT
df = df[df['MeSH Disease Term'] == one_disease]

# keep top 10 symptoms
valueCol = 'PubMed occurrence' ### EDIT
df.sort_values(by=valueCol, inplace=True, ascending=False)
df.loc[df[valueCol] < df[valueCol].nlargest(10).min(), 'MeSH Symptom Term'] = 'Other' ### EDIT

# Categories for source and target nodes of Sankey chart
target_cats = list(df['MeSH Symptom Term'].unique().astype(str))
source_cats = list(df['MeSH Disease Term'].unique().astype(str))
extent = ['MeSH Disease Term', 'MeSH Symptom Term']

# define params
source_point = 0
target_point = 1
palette = None #{'cat': extent[2], 'colors': , 'waypoint': False}
if_waypoints = False

# define nodes
nodes = {extent[0]: fl.ProcessGroup(source_cats), 
         extent[1]: fl.ProcessGroup(target_cats)}

# define endpoints
source = extent[source_point]
target = extent[target_point]

# define params
ordering = [[extent[0]], [extent[1]]]
bundles = [fl.Bundle(source, target)]

# endpoint partitions
part_source = fl.Partition.Simple("process", source_cats)
part_target = fl.Partition.Simple("process", target_cats)

# add to nodes
nodes[extent[source_point]].partition = part_source
nodes[extent[target_point]].partition = part_target

# define the sankey
sdd = fl.SankeyDefinition(nodes, bundles, ordering)

# weave it
sankey_data = fl.weave(sdd, df[extent + [valueCol]]
     .rename(columns={source:'source', target:'target', valueCol: 'value'}))

# sankey_data.to_widget(**dict(width=800, height=1000))
# save as json for input to d3
sJson = sankey_data.to_json()
import json
with open('sankey_json.json', 'w') as f:
    json.dump(sJson, f)