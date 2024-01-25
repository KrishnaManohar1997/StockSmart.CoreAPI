def translate_serializer_errors(serializer_errors):
    return " ".join(
        [
            error_key + ":" + error_detail[0]
            for error_key, error_detail in serializer_errors.items()
        ]
    )
