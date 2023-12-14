import os
from talon import actions

# Constants
TRANSPARENT = "#00000000"

from enum import Enum
class ZoneType(Enum):
    SIMPLE=1
    TRIGGER=2
class TriggerType(Enum):
    HOVER=1
    CLICK=2

# Functions
def verify_home_dir()->str:
    dirname = os.path.join(os.path.dirname(os.path.abspath(__file__)),"InteractionZones")
    HOME_DIRECTORY = dirname
    if not os.path.exists(HOME_DIRECTORY):
        os.makedirs(HOME_DIRECTORY)
    return HOME_DIRECTORY
    
def rgba2hex(r, g, b,a) -> str:
    return '#{:02x}{:02x}{:02x}{:02x}'.format(r, g, b,a)

def is_float(s) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False