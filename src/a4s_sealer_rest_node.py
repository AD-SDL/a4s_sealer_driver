"""The server that takes incoming WEI flow requests from the experiment application"""

import time
from argparse import ArgumentParser, Namespace
from contextlib import asynccontextmanager
from pathlib import Path

from a4s_sealer_driver import (
    A4S_SEALER_DRIVER,
)
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from wei.core.data_classes import (
    ModuleAbout,
    ModuleAction,
    ModuleStatus,
    StepResponse,
    StepStatus,
)
from wei.helpers import extract_version


def parse_args() -> Namespace:
    """Parses CLI args for the REST server"""
    parser = ArgumentParser()
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Hostname that the REST API will be accessible on",
    )
    parser.add_argument("--port", type=int, default=3001)
    parser.add_argument(
        "--device",
        type=str,
        default="/dev/ttyUSB2",
        help="Serial device for communicating with the device",
    )
    return parser.parse_args()


global sealer, state


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the REST server"""
    global sealer, state
    try:
        args = parse_args()
        sealer = A4S_SEALER_DRIVER(args.device)
        state = ModuleStatus.IDLE
    except Exception as err:
        print(err)
        state = "ERROR"

    # Yield control to the application
    yield

    # Do any cleanup here
    pass


app = FastAPI(
    lifespan=lifespan,
)


@app.get("/state")
def get_state():
    """Returns the current status of the module"""
    global sealer, state
    if state != ModuleStatus.BUSY:
        try:
            sealer.get_status()
            if sealer.status_msg == 3:
                state = ModuleStatus.ERROR
            elif sealer.status_msg == 0:
                state = ModuleStatus.IDLE
        except Exception:
            state = ModuleStatus.ERROR

    return JSONResponse(content={"State": state})


@app.get("/about")
async def about() -> ModuleAbout:
    """Returns a description of the actions and resources the module supports"""
    global sealer, state
    return ModuleAbout(
        name="Sealer Robot",
        description="Sealer is a robot module that can seal plates.",
        interface="wei_rest_node",
        version=extract_version(Path(__file__).parent.parent / "pyproject.toml"),
        actions=[
            ModuleAction(
                name="seal",
                description="This action seals a plate that is currently in the sealer robot.",
                args=[],
            )
        ],
        resource_pools=[],
    )


@app.get("/resources", status_code=501)
async def resources():
    """Returns information about the resources managed by this module"""
    pass


@app.post("/action")
def do_action(
    action_handle: str,
    action_vars: str,
) -> StepResponse:
    """Performs the action specified by 'action_handle' on the instrument, with the args specified in 'action_vars'"""
    global sealer, state
    state = ModuleStatus.BUSY
    if action_handle == "seal":
        try:
            sealer.seal()
            time.sleep(15)
            state = ModuleStatus.IDLE
            return StepResponse(
                action_msg="Sealing successful", action_response=StepStatus.SUCCEEDED
            )
        except Exception as e:
            state = ModuleStatus.IDLE
            return StepResponse(
                action_msg="Sealing failed",
                action_response=StepStatus.FAILED,
                action_log=str(e),
            )


if __name__ == "__main__":
    import uvicorn

    args = parse_args()

    uvicorn.run(
        "a4s_sealer_rest_node:app",
        host=args.host,
        port=args.port,
        reload=True,
    )
