from src.api import countries, friends, ping, posts, users
from src.api.auth import auth

all_routers = (
    auth.router,
    countries.router,
    posts.router,
    ping.router,
    users.router,
    friends.router
)
