"""Original case templates with independently supplied expected results."""
import copy
import re

TEMPLATES = [('advance the checkpoint after successful processing', {'start': '@i+1', 'events': [{'offset': '@i+1', 'ok': True}]}, {'next_offset': '@i+2', 'outcomes': ['processed']}), ('retain the checkpoint after a failed record', {'start': '@i+1', 'events': [{'offset': '@i+1', 'ok': False}]}, {'next_offset': '@i+1', 'outcomes': ['failed']}), ('distinguish duplicate records from offset gaps', {'start': '@i+2', 'events': [{'offset': '@i+1', 'ok': True}, {'offset': '@i+3', 'ok': True}]}, {'next_offset': '@i+2', 'outcomes': ['duplicate', 'gap']}), ('reject boolean offsets', {'start': True, 'events': []}, None), ('require boolean processing outcomes', {'start': 0, 'events': [{'offset': 0, 'ok': 1}]}, None)]


def make_case(index):
    description, source, expected = copy.deepcopy(TEMPLATES[index % len(TEMPLATES)])
    def fill(value):
        if isinstance(value, str):
            if re.fullmatch(r"@i[+]\d+", value):
                return index + int(value[3:])
            return value.replace("{n}", str(index))
        if isinstance(value, list):
            return [fill(item) for item in value]
        if isinstance(value, dict):
            return {fill(key): fill(item) for key, item in value.items()}
        return value
    case = {"id": "checkpoint-{:04d}".format(index), "description": description, "input": fill(source)}
    case.update({"expected_error": True} if expected is None else {"expected": fill(expected)})
    return case
