from aiohttp import web
import os,time
import base64, json
import asyncio
import code
import sys
import io
import contextlib
import subprocess, threading

class WebSocketREPL:
    def __init__(self):
        self.console = code.InteractiveConsole()
        self.ws = None
        self.process = None

    async def send_output(self, output):
        if self.ws is not None and not self.ws.closed:
            await self.ws.send_str(output)

    async def handle(self, ws):
        self.ws = ws
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                code_out = io.StringIO()
                code_err = io.StringIO()

                with contextlib.redirect_stdout(code_out), contextlib.redirect_stderr(code_err):
                    result = self.console.push(msg.data)

                print(f"Code output: {code_out.getvalue()} Result: {result}")
                output = code_out.getvalue() + code_err.getvalue()
                if result:  # More input is needed
                    prompt = ">>> " if self.console.complete else "... "
                    await ws.send_str(output + prompt)
                else:  # Code block is complete
                    if not output:
                        await ws.send_str("\r\n>>> ")
                    else:
                        await ws.send_str(output+">>> ")
                code_out.close()
                code_err.close()
            elif msg.type == web.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
                break

    async def execute_file(self, file):
        print(f"Executing file {file}")
        if self.process is not None:
            self.process.terminate()
        env = os.environ.copy()
        self.process = subprocess.Popen(
            [sys.executable, '-u', file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        output_thread = threading.Thread(target=self.capture_output)
        output_thread.start()

    def capture_output(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while True:
            time.sleep(0.1)
            output = self.process.stdout.readline()
            if output:
                loop.run_until_complete(self.send_output(output))
            ret = self.process.poll()
            if ret is not None:
                loop.run_until_complete(self.send_output(f"\nProgram exited {ret}\n"))
                if ret != 0:
                    error = self.process.stderr.read()
                    print(f"Error: {error}")
                    loop.run_until_complete(self.send_output(error))
                loop.close()
                break

    async def terminate_process(self):
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            await self.send_output("\nProcess terminated\n")


repl = WebSocketREPL()

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print(f"Client connected: {request.remote}")
    await repl.handle(ws)
    return ws

async def upload_handler(request):
    body = await request.text()
    _json = json.loads(body)
    fileName = _json["fileName"]
    contentb64 = _json["content"]
    content = base64.b64decode(contentb64).decode("utf-8")
    with open(fileName, "w") as f:
        f.write(content)
    if fileName == "main.py":
        await repl.execute_file(fileName)
    return web.Response(text="OK")

app = web.Application()
app.router.add_route('GET', '/ws', websocket_handler)
app.router.add_route('POST', '/upload', upload_handler)
app.router.add_static('/', path='.', show_index=True)  # Serve static files from current directory

web.run_app(app, host='0.0.0.0', port=8601)
