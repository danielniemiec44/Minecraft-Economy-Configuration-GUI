import os
import pandas as pd
import yaml
from collections import OrderedDict

page_size = 29

def convert_to_int_or_default(value):
    if pd.isna(value) or pd.to_numeric(value) <= 0:
        return int(-1)
    return float(value)

# Custom representer for OrderedDict
def represent_ordereddict(dumper, data):
    return dumper.represent_dict(data.items())

# Register custom representer with the default Dumper
yaml.add_representer(OrderedDict, represent_ordereddict, Dumper=yaml.Dumper)

# Directory containing CSV files
csv_directory = 'csv'
output_directory = 'output'

# If directory does not exist, create it
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Iterate over all CSV files in the directory
for csv_file in os.listdir(csv_directory):
    if csv_file.endswith('.csv'):
        # Read CSV file into DataFrame
        df = pd.read_csv(os.path.join(csv_directory, csv_file), delimiter=';', header=0)

        # Convert column names to lowercase
        df.columns = df.columns.str.lower()

        # Replace commas with dots and remove dollar signs
        df = df.replace({',': '.', r'\$': ''}, regex=True)

        # Convert buy and sell columns to floats
        # df['buy'] = pd.to_numeric(df['buy'], errors='raise')
        # df['sell'] = pd.to_numeric(df['sell'], errors='raise')

        df['buy'] = df['buy'].apply(convert_to_int_or_default)
        df['sell'] = df['sell'].apply(convert_to_int_or_default)

        # Ensure buy and sell prices are -1 if they are 0 or less
        # df.loc[df['buy'] <= 0, 'buy'] = -1
        # df.loc[df['sell'] <= 0, 'sell'] = -1

        # Create ordered dictionary structure for YAML
        pages = OrderedDict()
        items = OrderedDict()
        page_number = 1
        item_count = 0

        for index, row in df.iterrows():
            items[item_count % page_size] = OrderedDict({
                'material': '_'.join(row['material'].strip().split()).upper(),
                'buy': row['buy'],
                'sell': row['sell']
            })
            item_count += 1

            if item_count % page_size == 0 or index == len(df) - 1:
                pages[f'page{page_number}'] = OrderedDict({'items': items})
                items = OrderedDict()
                page_number += 1

        yaml_data = OrderedDict({'pages': pages})

        # Create YAML file name in the output directory
        yaml_file = os.path.join(output_directory, csv_file.replace('.csv', '.yml'))

        # Write ordered dictionary to YAML file
        with open(yaml_file, 'w') as file:
            yaml.dump(yaml_data, file, default_flow_style=False, Dumper=yaml.Dumper)