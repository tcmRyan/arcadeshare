from typemallow2 import generate_ts

from server.auth import *
from server.api import *

generate_ts("client/src/app/types.ts")
