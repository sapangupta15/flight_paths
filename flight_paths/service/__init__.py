import os
import json
import pandas as pd
import networkx as nx

# read flight routes and airline info into a data frame
resource_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../resources'))
data_df = pd.read_csv(os.path.join(resource_path, 'combined_data.csv'), header=0)

# read airport info
with open(os.path.join(resource_path, 'airport_columns.json'), 'r') as airport_file:
    airport_details = json.loads(airport_file.read())
airports_by_id = {airport['Airport_ID']: airport for airport in airport_details}

# create network of routes
route_network = nx.from_pandas_edgelist(data_df,
                                        'Source_airport_ID',
                                        'Destination_airport_ID',
                                        edge_attr='Distance',
                                        create_using=nx.DiGraph())
