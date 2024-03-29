from project import socketio, app
from project.model.subscriber.smart_tv_subscriber import SmartTvSubscriber
from project.model.publisher.smart_tv_publisher import SmartTvPublisher
from project.model.service.smart_tv_service import SmartTvService
from flask import request, jsonify
from time import sleep
import random
from datetime import datetime

tv_on = False


@app.route("/change_tv_status", methods=["POST"])
def change_status():
    
    command = request.json["lock"]
    block_tv(command)
    value = 'locked' if SmartTvService().last_record()['block'] else 'unlocked'
    SmartTvPublisher().start()
    return (
        jsonify(
            {"info": f"Tv's status is {value}"}
        ),
        200
    )

@socketio.on("tvConnect")
def tv_connect():
    global tv_on
    tv_on = True
    subscriber = SmartTvSubscriber()
    random.seed(datetime.now())
    SmartTvService().insert_data(dict(block=False))  # Set random here
    subscriber.start()
    while True:
        sleep(1)
        if not tv_on:
            subscriber.stop()
            break


@socketio.on("tvDisconnect")
def tv_disconnect():
    global tv_on
    tv_on = False


@socketio.on("tvBlock")
def block_tv(blocked):
    if blocked:
        info = {"info": "Tv is locked"}
        socketio.emit("TvInformation", info)
        socketio.emit("RedColor")
        SmartTvService().insert_data(dict(block=True))
    else:
        info = {"info": "Tv unlocked"}
        socketio.emit("TvInformation", info)
        socketio.emit("NormalColor")
        SmartTvService().insert_data(dict(block=False))
