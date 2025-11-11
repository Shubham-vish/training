import os
import sys
# Add path for imports if needed
PARENT_DIR = os.path.abspath(os.path.dirname(__file__))


# Get absolute path two levels up
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)


paths = [
    os.path.abspath(os.path.join(PARENT_DIR, "")),
    os.path.abspath(os.path.join(PARENT_DIR, "../..")),
    os.path.abspath(os.path.join(PARENT_DIR, "../../..")),
    os.path.abspath(os.path.join(PARENT_DIR, "CustomGraph")),
    os.path.abspath(os.path.join(PARENT_DIR, "services"))]

paths

sys.path.extend(paths)
sys.path
