def valueError(missingValue = "<not implemented>"):
    response = {
        "error": "lowlevel_type_mismatch",
        "http_status_code": 400,
        "path": missingValue,
        "error_description": "Unexpected null value"
    }
    return (400, response, {})

def methodError(valid_methods = ["<not implemented>"]):
    response = {
        "error":"method_not_allowed",
        "http_status_code":405,
        "error_description":"An endpoint was found matching this HTTP request but the method was not allowed. Valid methods are {}".format(', '.join(valid_methods)),
        "data":{
            "valid_methods": valid_methods
            }
        }
    return (405, response, {})