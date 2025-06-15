import asyncio
import hypercorn
import hypercorn.utils
from quart import Quart, render_template, websocket
from lib.forest.gen import generateForest
from lib.forest.felling import simulateFelling
from lib.forest.database import loadForest

app = Quart(__name__)

async def testFunc():
    forest = await loadForest()
    if forest:
        print(forest[0].to_csv())
    else:
        print("Unable to load forest!")

@app.route("/")
async def hello():
    return await render_template("index.html")

@app.route("/api")
async def json():
    app.add_background_task(testFunc)
    return {"hello": "world"}

@app.websocket("/forest/generate")
async def wsGenerateForest():
    pollingDuration = 1
    keepAliveDuration = 30

    # Do not change
    keepAliveTimer = 0

    app.add_background_task(generateForest)
    await websocket.send_json({"type": "connect"})
    while True:
        try:
            if keepAliveTimer >= keepAliveDuration:
                keepAliveTimer = 0
                await websocket.send_json({"type": "keep-alive"})
            else:
                keepAliveTimer += pollingDuration
            await asyncio.sleep(pollingDuration)
        except hypercorn.utils.UnexpectedMessageError:
            break
