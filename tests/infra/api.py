from dataclasses import dataclass
from tests.infra.endpoints import Posts
from tests.infra.endpoints import Post


@dataclass
class API:
    post = Post()
    posts = Posts()
