"""REST-based node for A4S Sealer device"""

import traceback
from pathlib import Path

from a4s_sealer_driver import A4S_SEALER_DRIVER
from fastapi.datastructures import State
from wei.modules.rest_module import RESTModule
from wei.types.module_types import ModuleStatus
from wei.utils import extract_version

rest_module = RESTModule(
    name="ur_node",
    version=extract_version(Path(__file__).parent.parent / "pyproject.toml"),
    description="A node to control the ur plate moving robot",
    model="ur",
)
rest_module.arg_parser.add_argument(
    "--device",
    type=str,
    default="/dev/ttyUSB2",
    help="Serial device for communicating with the device",
)


@rest_module.startup()
def ur_startup(state: State):
    """UR startup handler."""
    try:
        state.sealer = None
        state.sealer = A4S_SEALER_DRIVER(state.device)
        state.status = ModuleStatus.IDLE
    except Exception:
        state.status = ModuleStatus.ERROR
        traceback.print_exc()
        print("CONNECTION FAILED")
    else:
        print("Sealer online")
