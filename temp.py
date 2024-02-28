import json, sys

def load_ndjson_as_dict(file_path):
    data_dict = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    json_obj = json.loads(line)
                    data_dict[json_obj["file_id"]] = json_obj["solution"]

                except json.JSONDecodeError:
                    print(f"Warning: Could not parse line as JSON: {line}")
                except KeyError:
                    print(f"Warning: Key not found in line: {line}")
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error: {e}")

    return data_dict


print (f"File Name: {sys.argv[1]}")

sols = load_ndjson_as_dict (sys.argv[1])
keys = list(sols.keys())


no_sol = 0
sol = 0
timed_out = 0

sol_keys = []

for key in keys:
    if sols[key] == "NO_SOL":
        no_sol += 1
    elif sols[key] == "TIMEOUT":
        timed_out += 1
    else:
        sol += 1
        sol_keys.append(key)
        


print (f"Total: {len(keys)}")
print (f"No Solution: {no_sol}")
print (f"Solution: {sol}")
print (f"Timed Out: {timed_out}")

print (f"Percenatge of Solution: {sol/len(keys)*100 : .2f}%")

