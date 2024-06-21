from typemallow2 import generate_ts

from server.auth import *
from server.api import *

generate_ts("frontend/src/app/types.ts")
