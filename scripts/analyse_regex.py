import json, sys
from rfixer_utils import run_rfixer, generate_RFixer_input



def dump_to_ndjson(data, file_name="temp/.temp_sols.ndjson"):
    with open(file_name, 'w') as file:
        if isinstance(data, dict):
            for key, value in data.items():
                json_object = json.dumps({key: value})
                file.write(json_object + '\n')
        elif isinstance(data, list):
            for json_obj in data:
                file.write(json.dumps(json_obj) + '\n')
        else:
            raise ValueError("Data must be either a dictionary or a list of dictionaries")

def load_data(file_path: str):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    positive_inputs = []
    negative_inputs = []
    data = []

    for id, line in enumerate(lines):
        entry = json.loads(line)
        positive_len = len(entry['positive_inputs'])
        negative_len = len(entry['negative_inputs'])
        positive_inputs.append((id, positive_len))
        negative_inputs.append((id, negative_len))
        entry['id'] = id  # Add an ID field
        data.append(entry)

    return positive_inputs, negative_inputs, data


def filter_entries(positive_inputs, negative_inputs, data, upper_bound=100, lower_bound=5):
    positive_dict = {id: length for id, length in positive_inputs}
    negative_dict = {id: length for id, length in negative_inputs}

    filtered_positive_inputs = []
    filtered_negative_inputs = []
    filtered_data = []

    for entry in data:
        id = entry['id']
        pos_len = positive_dict.get(id, 0)
        neg_len = negative_dict.get(id, 0)
        if (lower_bound < pos_len < upper_bound) and (lower_bound < neg_len < upper_bound):
            filtered_data.append(entry)
            filtered_positive_inputs.append((id, pos_len))
            filtered_negative_inputs.append((id, neg_len))

    return filtered_positive_inputs, filtered_negative_inputs, filtered_data


def load_ndjson_as_dict(file_path):
    data_dict = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    json_obj = json.loads(line)
                    key = list(json_obj.keys())[0]
                    data_dict[key] = json_obj[key]
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse line as JSON: {line}")
                except KeyError:
                    print(f"Warning: Key not found in line: {line}")
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error: {e}")

    return data_dict

INFILE = sys.argv[1] if len(sys.argv) > 1 else '../temp/.regexes.ndjson'
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else '../temp/rfixer_output'
UPPER_BOUND = float ('inf')
LOWER_BOUND = 2

positive_lengths, negative_lengths, data = load_data(INFILE)
filtered_positive_inputs, filtered_negative_inputs, filtered_data = filter_entries(positive_lengths, negative_lengths, data, UPPER_BOUND, LOWER_BOUND)

print (f'Total Packages {len (filtered_data)}')

generate_RFixer_input(filtered_data, OUTDIR)
solutions = run_rfixer(OUTDIR, True, timeout=60)

for id, solution in solutions.items():
    data [int(id)]['RFixer-Solution'] = solution

dump_to_ndjson (data, "temp/rfixer_solutions.ndjson")
