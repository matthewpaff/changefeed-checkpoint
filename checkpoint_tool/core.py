"""Original bounded concept exercise with supplied synthetic data only."""


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or not value.keys() <= set(required) | set(optional):
        raise ValueError("Unexpected or missing object fields")


def integer(value, low=0, high=10**12):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("Integer outside the supported range")
    return value


def label(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 80 or any(ord(c) < 32 for c in value):
        raise ValueError("Expected a nonblank label of at most 80 characters")
    return value.strip()


def sequence(value, maximum):
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError("Expected a bounded list")
    return value

def evaluate(data):
    fields(data, ("start", "events"))
    next_offset = integer(data["start"])
    outcomes = []
    for event in sequence(data["events"], 1000):
        fields(event, ("offset", "ok"))
        offset = integer(event["offset"])
        if type(event["ok"]) is not bool:
            raise ValueError("ok must be boolean")
        if offset < next_offset:
            outcome = "duplicate"
        elif offset > next_offset:
            outcome = "gap"
        elif not event["ok"]:
            outcome = "failed"
        else:
            next_offset += 1
            outcome = "processed"
        outcomes.append(outcome)
    return {"next_offset": next_offset, "outcomes": outcomes}
