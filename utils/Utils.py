from typing import List

def build_url(url: str, query_params: List[tuple[str, str]]) -> str:
    if len(query_params) > 0:
        # TODO: Convert to url encoded string.
        return url + '?' + '&'.join([f'{key}={value}' for key, value in query_params])
    else:
        return url
