from typing import TYPE_CHECKING, Any, cast
import hashlib

if TYPE_CHECKING:
    from pathlib import Path

import requests

import fichub_net.authentications as a


def hash_file(fname: Path) -> str:
    with fname.open("rb") as f:
        data: bytes = f.read()
        return hashlib.md5(data).hexdigest()


def req_json(link: str, retry_count: int = 5, timeout: float = 300.0) -> dict[Any, Any]:
    params: dict[str, str] = {"apiKey": a.AX_API_KEY}
    headers: dict[str, str] = {"User-Agent": "fichub.net/0.1.0"}
    r: requests.Response = requests.get(
        link,
        headers=headers,
        timeout=timeout,
        params=params,
        auth=(a.AX_USER, a.AX_PASS),
    )
    try:
        p: dict | Any = r.json()
    except ValueError:
        if retry_count < 1:
            return {
                "err": -1,
                "msg": f"req_json: received status code: {r.status_code!s}",
            }
        return req_json(link, retry_count - 1)
    return cast("dict[Any, Any]", p)
