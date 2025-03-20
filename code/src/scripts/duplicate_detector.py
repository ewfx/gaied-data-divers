from fuzzywuzzy import fuzz
import json

previous_requests = []

def is_duplicate(new_request):
    for prev in previous_requests:
        similarity = fuzz.ratio(json.dumps(prev), json.dumps(new_request))
        if similarity > 90:
            return True
    return False
