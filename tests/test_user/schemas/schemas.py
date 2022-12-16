valid_schema = {
    "type": "object",
    "properties": {
        "access_token": {"type": "string"},
        "refresh_token": {"type": "string"},
    },
    "required": ["access_token", "refresh_token"]
}

empty_schema = {
    "type": "object",
    "properties": {
            "error": {"type": "string"},
        },
}

already_exists_schema = {
    "type": "object",
    "properties": {
            "error": {"type": "string"},
        },
}

invalid_schema = {
    "type": "object",
    "properties": {
            "error": {"type": "string"},
        },
}

invalid_field_schema = {
    "type": "object",
    "properties": {
            "error": {"type": "string"},
        },
}

email_verification_valid_schema = {
    "type": "object",
    "properties": {
            "Message": {"type": "string"},
            "url": {"type": "string"}
        },
}

email_verification_invalid_schema = {
    "type": "object",
    "properties": {
            "Message": {"type": "string"},
        },
}

email_confirmation_valid_schema = {
    "type": "object",
    "properties": {
            "Message": {"type": "string"},
        },
}

email_confirmation_invalid_schema = {
    "type": "object",
    "properties": {
            "error": {"type": "string"},
        },
}

reset_password_valid_schema = {
    "type": "object",
    "properties": {
            "Message": {"type": "string"},
        },
}

reset_password_invalid_schema = {
    "type": "object",
    "properties": {
            "error": {"type": "string"},
        },
}

