import re
from typing import Callable
from app import request, response


class Router:
    route_map: dict[str, Callable[[request.Request], bytes]] = {}

    def add_route(self, path: str, handler: Callable[[request.Request], bytes]):
        self.route_map[path] = handler

    def run(self, request: request.Request) -> bytes:
        for path, handler in self.route_map.items():
            match = re.search(path, request.resource)
            if match:
                request.params = match.groupdict()
                return handler(request)
        # none path matched
        return response.response_builder(404, "Not Found").encode()
