def validate(actual, expected, validation_type):
    validation_type = str(validation_type).strip().upper()
    if actual != expected:
        raise AssertionError(
            f"{validation_type} failed | Actual={actual} | Expected={expected}"
        )
