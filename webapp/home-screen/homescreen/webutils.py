def get_content_type(response):
    CONTENT_TYPES = ['Content-Type', 'content-type']
    content_type = None
    for ct in CONTENT_TYPES:
        if not content_type:
            content_type = response.headers.get(ct)
    return content_type