import traceback
import locale
import string
import time
import random
import asyncio
import json
import os
import sys
import re
import io
import binascii
import signal
import base64
from urllib.parse import unquote
from copy import copy
from multiprocessing import Process, freeze_support

import websockets
from gevent import monkey

monkey.patch_all()
import bottle
from bottle import static_file, get, request, template, response

from assembler import parse as ASMparser
from bytecodeinterpreter import BCInterpreter

from translation import dictionary

translate = dictionary.create_main_dict()

from native_app import start_app
from stateManager import StateManager

appState = StateManager()

UPDATE_THROTTLE_SEC = 0.3

interpreters = {}
connected = set()


async def producer(ws, data_list):
    """
    Sends the data in the list to the client in json string form

    Parameters:
        web_socket(ws):Connected client
        data_list(data_list):Data waiting to be sent
    """

    while True:
        if ws not in connected:
            break
        if data_list:
            out = []
            while True:
                try:
                    out.append(data_list.pop(0))
                except IndexError:
                    break
            return json.dumps(out)
        await asyncio.sleep(0.05)


async def run_instance(ws):
    """
    Checks if the waiting time from two steps has surpassed and if the user didn't ask to stop

    Parameters:
        web_socket(ws):Connected client
    """
    while True:
        if ws not in connected:
            break
        if ws in interpreters:
            interp = interpreters[ws]
            if (interp.user_asked_stop__ == False) and (
                time.time() > interp.last_step__ + interp.animate_speed__
            ):
                return
        await asyncio.sleep(0.05)


async def update_ui(ws, to_send):
    """
    Checks if the expected time has passed and if one or more instructions have been executed

    Parameters:
        web_socket(ws):Connected client
    """
    while True:
        if ws not in connected:
            break
        if ws in interpreters:
            interp = interpreters[ws]
            if interp.next_report__ < time.time() and interp.num_exec__ > 0:
                return
        await asyncio.sleep(0.02)


def get_cookie(cookie_str, cookie_name):
    """
    Get the cookie from the cookie string

    Parameters:
        cookie_name(cookie_name):Name of the cookie to search for
        cookie_string(cookie_str):String with cookies
    """
    pattern = f"{cookie_name}=([^;]+)"
    match = re.search(pattern, cookie_str)
    if match:
        return match.group(1)
    return None


async def handler(websocket):
    """
    Handles the connection of the client

    Parameters:
        web_socket(websocket):Client to connect
    """
    print("User {} connected.".format(websocket))
    connected.add(websocket)

    to_send = []
    received = []
    ui_update_queue = []

    try:
        listener_task = asyncio.ensure_future(websocket.recv())
        producer_task = asyncio.ensure_future(producer(websocket, to_send))
        to_run_task = asyncio.ensure_future(run_instance(websocket))
        update_ui_task = asyncio.ensure_future(update_ui(websocket, to_send))

        while True:
            if websocket.state != True:  # not websocket.open:
                break

            done, pending = await asyncio.wait(
                [listener_task, producer_task, to_run_task, update_ui_task],
                timeout=3600,
                return_when=asyncio.FIRST_COMPLETED,
            )

            if len(done) == 0:
                print("{} timeout!".format(websocket))
                listener_task.cancel()
                producer_task.cancel()
                to_run_task.cancel()
                break

            if listener_task in done:
                try:
                    message = listener_task.result()
                except websockets.exceptions.ConnectionClosed:
                    break

                if message:
                    received.append(message)

                data = process(websocket, received)
                if data:
                    to_send.extend(data)

                listener_task = asyncio.ensure_future(websocket.recv())

            if producer_task in done:
                message = producer_task.result()
                await websocket.send(message)
                producer_task = asyncio.ensure_future(producer(websocket, to_send))

            if websocket not in interpreters:
                await asyncio.sleep(0.05)
                continue

            # Continue executions of "run", "step out" and "step forward"
            if to_run_task in done:
                if interpreters[websocket].animate_speed__:
                    interpreters[websocket].step()
                    interpreters[websocket].last_step__ = time.time()
                    interpreters[websocket].num_exec__ += 1
                    if interpreters[websocket].shouldStop:
                        interpreters[websocket].user_asked_stop__ = True
                    ui_update_queue.extend(updateDisplay(interpreters[websocket]))

                else:
                    interpreters[websocket].num_exec__ -= interpreters[
                        websocket
                    ].getCycleCount()
                    interpreters[websocket].execute()
                    interpreters[websocket].last_step__ = time.time()
                    interpreters[websocket].num_exec__ += interpreters[
                        websocket
                    ].getCycleCount()
                    interpreters[websocket].num_exec__ = max(
                        interpreters[websocket].num_exec__, 1
                    )
                    interpreters[websocket].user_asked_stop__ = True
                    ui_update_queue.extend(updateDisplay(interpreters[websocket]))

                to_run_task = asyncio.ensure_future(run_instance(websocket))

            if update_ui_task in done:
                interpreters[websocket].num_exec__ = 0

                interpreters[websocket].next_report__ = (
                    time.time() + UPDATE_THROTTLE_SEC
                )

                to_send.extend(ui_update_queue)
                ui_update_queue = []
                update_ui_task = asyncio.ensure_future(update_ui(websocket, to_send))

    except Exception as e:
        ex = traceback.format_exc()
        if not isinstance(e, websockets.exceptions.ConnectionClosed):
            print("Simulator crashed:\n{}".format(ex))
            try:
                code = interpreters[websocket].code__
            except (KeyError, AttributeError):
                code = ""
    finally:
        if websocket in interpreters:
            del interpreters[websocket]
        connected.remove(websocket)
        print("User {} disconnected.".format(websocket))


def generateUpdate(inter):
    """
    Parameters:
        interpreter(inter):
    Return:
        A structured list of the interpreter status with flags and registers
    """
    retval = []

    # Breakpoints
    bpm = inter.getBreakpointsMem()
    retval.extend(
        [
            ["membp_r", ["0x{:08x}".format(x) for x in bpm["r"]]],
            ["membp_w", ["0x{:08x}".format(x) for x in bpm["w"]]],
            ["membp_rw", ["0x{:08x}".format(x) for x in bpm["rw"]]],
            ["membp_e", ["0x{:08x}".format(x) for x in bpm["e"]]],
        ]
    )

    # Memory View
    mem = inter.getMemoryFormatted()
    mem_addrs = range(0, len(mem), 16)
    chunks = [mem[x : x + 16] for x in mem_addrs]
    vallist = []
    for i, line in enumerate(chunks):
        cols = {"c{}".format(j): char for j, char in enumerate(line)}
        cols["ch"] = "0x{:08x}".format(mem_addrs[i])
        # web interface is 1-indexed in this case
        vallist.append({"id": i + 1, "values": cols})
    retval.append(["mem", vallist])

    # Registers
    registers_types = inter.getRegisters()
    retval.extend(
        tuple(
            {
                "r{}".format(k): "{:08x}".format(v)
                for k, v in registers_types["User"].items()
            }.items()
        )
    )
    retval.extend(
        tuple(
            {
                "FIQ_r{}".format(k): "{:08x}".format(v)
                for k, v in registers_types["FIQ"].items()
            }.items()
        )
    )
    retval.extend(
        tuple(
            {
                "IRQ_r{}".format(k): "{:08x}".format(v)
                for k, v in registers_types["IRQ"].items()
            }.items()
        )
    )
    retval.extend(
        tuple(
            {
                "SVC_r{}".format(k): "{:08x}".format(v)
                for k, v in registers_types["SVC"].items()
            }.items()
        )
    )

    # Flags
    retval.extend(inter.getFlagsFormatted())

    # Breakpoints
    retval.append(["asm_breakpoints", inter.getBreakpointInstr()])

    # Errors
    retval.extend(inter.getErrorsFormatted())

    return retval


def updateDisplay(interp, force_all=False):
    """
    Parameters:
        interpreter(interp):
    Return:
        A structured list of the interpreter status with current line of debugging
    """
    retval = []

    currentLine = interp.getCurrentLine()
    if currentLine:
        retval.append(["debugline", currentLine])
        retval.extend(interp.getCurrentInfos())
    else:
        retval.append(["debugline", -1])
        retval.append(["nextline", -1])
        retval.append(["disassembly", appState.getT(0)])

    try:
        instr_addr = interp.getCurrentInstructionAddress()
        retval.append(
            [
                "debuginstrmem",
                ["0x{:08x}".format(x) for x in range(instr_addr, instr_addr + 4)],
            ]
        )
    except Exception as e:
        retval.append(["debuginstrmem", -1])
        retval.append(["error", str(e)])

    if force_all:
        retval.extend(generateUpdate(interp))
        retval.append(["banking", interp.getProcessorMode()])
    else:
        retval.extend(interp.getChangesFormatted(setCheckpoint=True))

    diff_bp = interp.getBreakpointInstr(diff=True)
    if diff_bp:
        retval.append(["asm_breakpoints", interp.getBreakpointInstr()])
        bpm = interp.getBreakpointsMem()
        retval.extend(
            [["membp_e", ["0x{:08x}".format(x) for x in bpm["e"]]], ["mempartial", []]]
        )

    retval.append(["cycles_count", interp.getCycleCount()])

    return retval


def process(ws, msg_in):
    if "changeLang" in msg_in[0]:
        newLang = msg_in[0].split(":")[1]
        appState.setLang(newLang)
        return

    """
    Parameters:
        websocket(ws): Connected client
        messages_in(msg_in): Messages to send
    Return:
        List of the status of the interpreter after the execution of the messages
    """
    force_update_all = False
    retval = []
    if ws in interpreters and not hasattr(interpreters[ws], "history__"):
        interpreters[ws].history__ = []

    try:
        for msg in msg_in:
            data = json.loads(msg)

            if ws in interpreters:
                interpreters[ws].history__.append(data)

            if data[0] != "assemble" and ws not in interpreters:
                if data[0] != "interrupt":
                    retval.append(
                        [
                            "error",
                            appState.getT(1),
                        ]
                    )
            elif data[0] == "assemble":
                code = "".join(
                    s for s in data[1].replace("\t", " ") if s in string.printable
                )

                if ws in interpreters:
                    del interpreters[ws]

                bytecode, bcinfos, line2addr, assertions, snippetMode, errors = (
                    ASMparser(code.splitlines())
                )

                if errors:
                    retval.extend(errors)
                    retval.append(["edit_mode"])
                else:
                    interpreters[ws] = BCInterpreter(
                        bytecode, bcinfos, assertions, snippetMode=snippetMode
                    )
                    force_update_all = True
                    interpreters[ws].code__ = copy(code)
                    interpreters[ws].last_step__ = time.time()
                    interpreters[ws].next_report__ = 0
                    interpreters[ws].animate_speed__ = 0.1
                    interpreters[ws].num_exec__ = 0
                    interpreters[ws].user_asked_stop__ = True
                    retval.append(["line2addr", line2addr])
            else:
                if data[0] == "stepback":
                    interpreters[ws].stepBack()
                    force_update_all = True
                elif data[0] == "stepinto":
                    interpreters[ws].execute("into")
                elif data[0] == "stepforward":
                    interpreters[ws].setStepMode("forward")
                    interpreters[ws].user_asked_stop__ = False
                    interpreters[ws].last_step__ = time.time()
                    try:
                        interpreters[ws].animate_speed__ = int(data[1]) / 1000
                    except (ValueError, TypeError):
                        interpreters[ws].animate_speed__ = 0
                        retval.append(
                            ["animate_speed", str(interpreters[ws].animate_speed__)]
                        )
                elif data[0] == "stepout":
                    interpreters[ws].setStepMode("out")
                    interpreters[ws].user_asked_stop__ = False
                    interpreters[ws].last_step__ = time.time()
                    try:
                        interpreters[ws].animate_speed__ = int(data[1]) / 1000
                    except (ValueError, TypeError):
                        interpreters[ws].animate_speed__ = 0
                        retval.append(
                            ["animate_speed", str(interpreters[ws].animate_speed__)]
                        )
                elif data[0] == "run":
                    if interpreters[ws].shouldStop == False and (
                        interpreters[ws].user_asked_stop__ == False
                    ):
                        interpreters[ws].user_asked_stop__ = True
                    else:
                        interpreters[ws].user_asked_stop__ = False
                        interpreters[ws].setStepMode("run")
                        interpreters[ws].last_step__ = time.time()
                        try:
                            anim_speed = int(data[1]) / 1000
                        except (ValueError, TypeError):
                            anim_speed = 0
                            retval.append(["animate_speed", str(anim_speed)])
                        interpreters[ws].animate_speed__ = anim_speed
                elif data[0] == "stop":
                    del interpreters[ws]
                elif data[0] == "reset":
                    interpreters[ws].reset()
                elif data[0] == "breakpointsinstr":
                    interpreters[ws].setBreakpointInstr(data[1])
                    force_update_all = True
                elif data[0] == "breakpointsmem":
                    try:
                        interpreters[ws].toggleBreakpointMem(int(data[1], 16), data[2])
                    except ValueError:
                        retval.append(["error", appState.getT(2)])
                    else:
                        bpm = interpreters[ws].getBreakpointsMem()
                        retval.extend(
                            [
                                ["membp_r", ["0x{:08x}".format(x) for x in bpm["r"]]],
                                ["membp_w", ["0x{:08x}".format(x) for x in bpm["w"]]],
                                ["membp_rw", ["0x{:08x}".format(x) for x in bpm["rw"]]],
                                ["membp_e", ["0x{:08x}".format(x) for x in bpm["e"]]],
                            ]
                        )
                elif data[0] == "update":
                    reg_update = re.findall(r"^(?:([A-Z]{3})_)?r(\d{1,2})", data[1])
                    if reg_update:
                        bank, reg_id = reg_update[0]
                        if not len(bank):
                            bank = "User"
                        try:
                            interpreters[ws].setRegisters(
                                bank, int(reg_id), int(data[2], 16)
                            )
                        except (ValueError, TypeError):
                            retval.append(
                                ["error", appState.getT(3).format(repr(data[2]))]
                            )
                    elif data[1].upper() in (
                        "N",
                        "Z",
                        "C",
                        "V",
                        "I",
                        "F",
                        "SN",
                        "SZ",
                        "SC",
                        "SV",
                        "SI",
                        "SF",
                    ):
                        flag_id = data[1].upper()
                        try:
                            val = not interpreters[ws].getFlags()[flag_id]
                        except KeyError:
                            pass
                        else:
                            interpreters[ws].setFlags(flag_id, val)
                    elif data[1][:2].upper() == "BP":
                        _, mode, bank, reg_id = data[1].split("_")
                        try:
                            reg_id = int(reg_id[1:])
                        except (ValueError, TypeError):
                            retval.append(
                                [
                                    "error",
                                    appState.getT(4).format(repr(reg_id[1:])),
                                ]
                            )
                        # bank, reg name, mode [r,w,rw]
                        interpreters[ws].setBreakpointRegister(
                            bank.lower(), reg_id, mode
                        )
                    force_update_all = True
                elif data[0] == "interrupt":
                    mode = ["FIQ", "IRQ"][data[2] == "IRQ"]  # FIQ/IRQ
                    try:
                        cycles_premier = int(data[4])
                    except (TypeError, ValueError):
                        cycles_premier = 50
                        retval.append(["interrupt_cycles_first", 50])
                    try:
                        cycles = int(data[3])
                    except (TypeError, ValueError):
                        cycles = 50
                        retval.append(["interrupt_cycles", 50])
                    try:
                        notactive = bool(data[1])
                    except (TypeError, ValueError):
                        notactive = 0
                        retval.append(["interrupt_active", 0])
                    interpreters[ws].setInterrupt(
                        mode, not notactive, cycles_premier, cycles, 0
                    )
                elif data[0] == "memchange":
                    try:
                        val = bytearray([int(data[2], 16)])
                    except (ValueError, TypeError):
                        retval.append(["error", appState.getT(5).format(repr(data[2]))])
                        val = interpreters[ws].getMemory(data[1])
                        retval.append(["mempartial", [[data[1], val]]])
                    else:
                        interpreters[ws].setMemory(data[1], val)
                else:
                    print("<{}> Unknown message: {}".format(ws, data))
    except Exception as e:
        traceback.print_exc()
        retval.append(["error", str(e)])

        ex = traceback.format_exc()
        print("Handling loop crashed:\n{}".format(ex))
        try:
            code = interpreters[ws].code__
        except (KeyError, AttributeError):
            code = ""
        try:
            hist = interpreters[ws].history__
        except (KeyError, AttributeError):
            hist = []
        try:
            cmd = msg
        except NameError:
            cmd = ""

    del msg_in[:]

    if ws in interpreters:
        retval.extend(updateDisplay(interpreters[ws], force_update_all))
    return retval


default_code = """SECTION INTVEC

B main

SECTION CODE

main

end
B end

SECTION DATA
"""


def decodeWSGI(data):
    """
    @private
    """
    return "".join(chr((0xDC00 if x > 127 else 0) + x) for x in data)


def encodeWSGI(data):
    """
    @private
    """
    return bytes([(ord(x) % 0xDC00) for x in data]).decode("utf-8")


def encodeWSGIb(data):
    """
    @private
    """
    return bytes([(x % 0xDC00) for x in data]).decode("utf-8")


def readFileBrokenEncoding(filename):
    """
    Reads the content of a file, handling broken or missing locale encoding settings.
    On systems where `locale.getlocale()` returns `(None, None)`,

    Args:
        filename (str): The path to the file to be read.

    Returns:
        str: The file content as a string.

    Note:
        This function relies on the presence of `encodeWSGIb()` to decode the binary content when locale is not set.
    """

    if locale.getlocale() == (None, None):
        with open(filename, "rb") as fhdl:
            data = fhdl.read()
        data = encodeWSGIb(data)
    else:
        with io.open(filename, "r", encoding="utf-8") as fhdl:
            data = fhdl.read()
    return data


def get():
    """
    Creates and returns a Bottle web application with routes for a simulator interface.

    The application includes the following endpoints:

    - `/` (GET): Renders the main simulation interface using a predefined template.
    - `/static/<filename>` (GET): Serves static files (CSS, JS, images) from the `./interface/static/` directory.
    - `/download/` (POST): Accepts simulation data, decodes a filename, and returns the data as a downloadable text file.

    Returns:
        bottle.Bottle: A configured Bottle app instance ready to be run or served via WSGI.

    Notes:
        - The function relies on the following external variables and functions:
            - `default_code`: Default code to be shown in the simulator.
            - `simulator_template`: The template file to render the main page.
            - `encodeWSGI()`: A function that encodes string data for WSGI compliance.
        - The filename received in the `/download/` route is expected to be base64-encoded in the `sim` form field.
    """
    app = bottle.Bottle()
    appState.setLang(request.get_cookie("lang") or "en")

    @app.route("/")
    def index():
        code = default_code
        sections = {}

        this_template = "./interface/simulator.html"

        return template(
            this_template, code=code, sections=sections, rand=random.randint(0, 2**16)
        )

    @app.route("/static/<filename:path>")
    def static_serve(filename):
        return static_file(filename, root="./interface/static/")

    @app.post("/download/")
    def download():
        simParameter = unquote(request.forms.get("sim"))
        try:
            filename = base64.b64decode(simParameter).decode("utf-8")
            filename = os.path.splitext(os.path.basename(filename))[0]
        except binascii.Error:
            filename = "source"
        data = request.forms.get("data")
        data = encodeWSGI(data)
        response.headers["Content-Type"] = "text/plain; charset=UTF-8"
        response.headers["Content-Disposition"] = (
            'attachment; filename="%s.txt"' % filename
        )
        return data

    return app


def http_server():
    """
    Start in async mode the http server
    """
    bottle.run(
        app=get(),
        host="0.0.0.0",
        port=appState.getHttpPort(),
        server="gevent",
        debug=True,
    )


def display_amount_users():
    print("Number of clients:", len(connected))
    print(connected)
    print("Number of interpreters:", len(interpreters))
    print(interpreters)
    sys.stdout.flush()


async def async_webserver():
    """
    Start in async mode the web server
    """
    port = appState.getWebPort()
    print(f"Started WebSocket on port {port}")
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()


def web_server():
    """
    @private
    """
    asyncio.run(async_webserver())


def init_server(server_type):
    """
    Param:
        server_type(server_type): server function to initialize
    Return:
        Server initialized
    """
    p = Process(target=server_type)
    p.daemon = True
    p.start()
    return p


if hasattr(signal, "SIGUSR1"):
    signal.signal(signal.SIGUSR1, display_amount_users)

if __name__ == "__main__":
    freeze_support()

    http_server = init_server(http_server)
    web_server = init_server(web_server)

    start_app()
