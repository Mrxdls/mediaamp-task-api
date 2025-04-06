from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request
from credentials import REDIS_URL


limiter = Limiter(
    get_remote_address,
    default_limits=["100 per hour"],
    storage_uri= REDIS_URL,
    storage_options={}
)