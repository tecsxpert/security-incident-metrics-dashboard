from datetime import datetime

def success_response(data):
    return {
        "success": True,
        "data": data,
        "error": None,
        "meta": {
            "generated_at": datetime.utcnow().isoformat()
        }
    }

def error_response(code, message):
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message
        },
        "meta": {
            "generated_at": datetime.utcnow().isoformat()
        }
    }