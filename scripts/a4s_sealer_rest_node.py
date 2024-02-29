"""The server that takes incoming WEI flow requests from the experiment application"""

import json
from argparse import ArgumentParser
from contextlib import asynccontextmanager
import time
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
from wei.core.data_classes import (
    ModuleAbout,
    ModuleAction,
    ModuleActionArg,
    ModuleStatus,
    StepResponse,
    StepStatus,
)
from wei.helpers import extract_version

from a4s_sealer_driver.a4s_sealer_driver import (
    A4S_SEALER_DRIVER,
)


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
args = parser.parse_args()

global sealer, state, device

device = args.device


@asynccontextmanager
async def lifespan(app: FastAPI):
    global sealer, state, device
    """Initial run function for the app, parses the worcell argument
        Parameters
        ----------
        app : FastApi
           The REST API app being initialized

        Returns
        -------
        None"""
    try:
        sealer = A4S_SEALER_DRIVER(device)
        state = "IDLE"
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
    global sealer, state
    if state != "BUSY":
        sealer.get_status()
        if sealer.status_msg == 3:
            state = "ERROR"

        elif sealer.status_msg == 0:
            state = "IDLE"

    return JSONResponse(content={"State": state})  # sealer.get_status() })


@app.get("/about")
async def about() -> JSONResponse:
    """Returns a description of the actions and resources the module supports"""
    global sealer, state
    about = ModuleAbout(
        name="Sealer Robot",
        description="Sealer is a robot module that can seal plates.",
        interface="wei_rest_node",
        version=extract_version(Path(__file__).parent.parent / "pyproject.toml"),
        actions=[
            ModuleAction(
                name="seal",
                description="This action seals a plate that is currenly in the sealer robot.",
                args=[
                    ModuleActionArg(
                        name="time",
                        description="The amount of time for sealing a plate.",
                        type="int",
                        required=True,
                    ),
                    ModuleActionArg(
                        name="temperature",
                        description="The temperature to heat the plate to when sealing it.",
                        type="int",
                        required=True,
                    ),
                ],
            )
        ],
        resource_pools=[],
    )
    return JSONResponse(content=about.model_dump(mode="json"))


@app.get("/resources")
async def resources():
    global sealer, state
    return JSONResponse(content={"State": state})  # sealer.get_status() })


@app.post("/action")
def do_action(
    action_handle: str,
    action_vars: str,
):
    global sealer, state
    state = "BUSY"
    if action_handle == "seal":
        # self.sealer.set_time(3)
        # self.sealer.set_temp(175)
        try:
            sealer.seal()
            time.sleep(15)
            response_content = {
                "action_msg": "Sealing successful",
                "action_response": "succeeded",
                "action_log": "",
            }
            state = "IDLE"
            return JSONResponse(content=response_content)
        except Exception as e:
            response_content = {
                "action_msg": "",
                "action_response": "failed",
                "action_log": str(e),
            }
            state = "IDLE"
            return JSONResponse(content=response_content)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "a4s_sealer_rest_node:app",
        host=args.host,
        port=args.port,
        reload=True,
    )
