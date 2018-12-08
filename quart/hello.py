from quart import Quart, render_template, websocket
app = Quart(__name__)

@app.route('/quart/')
async def hello():
    return await render_template('index.html')

@app.route('/quart/1/')
async def hello1():
    return await render_template('1.html')

app.run(port=5001)