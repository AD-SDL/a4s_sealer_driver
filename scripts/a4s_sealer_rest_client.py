"""The server that takes incoming WEI flow requests from the experiment application"""
import json
from argparse import ArgumentParser
from contextlib import asynccontextmanager
import time
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse

from a4s_sealer_driver.a4s_sealer_driver import (
    A4S_SEALER_DRIVER,
)

global sealer, state

parser = ArgumentParser()
parser.add_argument("--host", type=str, default="0.0.0.0", help="Hostname that the REST API will be accessible on")
parser.add_argument("--port", type=int, default=2000)
parser.add_argument("--device", type=str, default="/dev/ttyUSB1", help="Serial device for communicating with the device")
args = parser.parse_args()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global sealer, state
    """Initial run function for the app, parses the worcell argument
        Parameters
        ----------
        app : FastApi
           The REST API app being initialized

        Returns
        -------
        None"""
    try:
        sealer = A4S_SEALER_DRIVER(args.device)
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
            msg.data = "State: ERROR"
            state = "ERROR"

        elif sealer.status_msg == 0:
            state = "IDLE"

    return JSONResponse(content={"State": state})  # sealer.get_status() })


@app.get("/about")
async def about():
    global sealer, state
    return JSONResponse(
        content={
            "name": "sealer",
            "model": "a4s_sealer",
            "version": "0.0.1",
            "actions": {
                "seal": "config : %s",
            },
            "repo": "https://github.com/AD-SDL/a4s_sealer_rest_node/edit/main/a4s_sealer_client.py",
        }
    )  # sealer.get_status() })


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
        "a4s_sealer_rest_client:app",
        host=args.host,
        port=args.port,
        reload=False,
    )
