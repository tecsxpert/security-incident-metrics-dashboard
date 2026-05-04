# ai-service/middleware/helpers.py

import logging
from middleware.sanitiser import sanitise_input

logger = logging.getLogger(__name__)

#  Constants
REQUIRED_FIELDS = [
    "title",
    "incident_type",
    "severity",
    "affected_system",
    "description"
]

VALID_SEVERITIES = ["Low", "Medium", "High", "Critical"]

FIELDS_TO_SANITISE = [
    "title",
    "incident_type",
    "affected_system",
    "description"
]


#  Validate required fields
def validate_input(data: dict) -> dict:
    for field in REQUIRED_FIELDS:
        if field not in data:
            return {
                "valid":  False,
                "reason": f"Missing required field: '{field}'"
            }
        if not str(data[field]).strip():
            return {
                "valid":  False,
                "reason": f"Field '{field}' cannot be empty"
            }

    if data["severity"] not in VALID_SEVERITIES:
        return {
            "valid":  False,
            "reason": f"Invalid severity. Must be one of: {VALID_SEVERITIES}"
        }

    return {"valid": True, "reason": None}


# Sanitise all fields
def sanitise_all_fields(data: dict) -> dict:

    sanitised = {}

    for field in FIELDS_TO_SANITISE:
        result = sanitise_input(str(data[field]))
        if not result["safe"]:
            logger.warning(
                f"Sanitisation failed on '{field}': {result['reason']}"
            )
            return {
                "safe":      False,
                "sanitised": {},
                "reason":    f"Field '{field}': {result['reason']}"
            }
        sanitised[field] = result["cleaned"]

    # severity does not need sanitising — already validated
    sanitised["severity"] = data["severity"]

    return {
        "safe":      True,
        "sanitised": sanitised,
        "reason":    None
    }


# Parse and validate JSON body
def parse_json_body(request) -> dict:

    data = request.get_json(silent=True)
    if not data:
        return {
            "valid":  False,
            "data":   {},
            "reason": "Request body must be valid JSON"
        }
    return {
        "valid":  True,
        "data":   data,
        "reason": None
    }