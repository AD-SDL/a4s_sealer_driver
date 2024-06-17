"""REST-based node for A4S Sealer device"""

from pathlib import Path

from a4s_sealer_driver import A4S_SEALER_DRIVER
from fastapi.datastructures import State
from wei.modules.rest_module import RESTModule
from wei.utils import extract_version

rest_module = RESTModule(
    name="sealer_node",
    version=extract_version(Path(__file__).parent.parent / "pyproject.toml"),
    description="A node to control the A4S Sealer device",
    model="A4S Sealer",
)
rest_module.arg_parser.add_argument(
    "--device",
    type=str,
    default="/dev/ttyUSB2",
    help="Serial device for communicating with the device",
)


@rest_module.startup()
def sealer(state: State):
    """Sealer startup handler."""
    state.sealer = A4S_SEALER_DRIVER(state.device)
    print("Sealer online")


if __name__ == "__main__":
    rest_module.start()
