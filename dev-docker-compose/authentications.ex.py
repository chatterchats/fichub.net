SESSION: str = "redacted"  # the api session cookie

AX_USER: str = "redacted"
AX_PASS: str = "redacted"
AX_API_KEY: str = "redacted"
AX_API_PREFIX: str = "http://ax:8000/v0"  # base url for ax api
AX_STATUS_ENDPOINT: str = f"{AX_API_PREFIX}/status"
AX_LOOKUP_ENDPOINT: str = f"{AX_API_PREFIX}/lookup"
AX_FIC_ENDPOINT: str = f"{AX_API_PREFIX}/fic"

ELASTICSEARCH_HOSTS: list[str] = ["http://elastic:espass@es:9200"]
