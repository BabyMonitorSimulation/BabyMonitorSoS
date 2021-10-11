from project.util.config_broker import ConfigScenario
from project.util.construct_scenario import (
    exchange,
    queue_smartphone_bm,
    queue_smartphone_st,
    bm_info,
    st_msg,
    st_info,
)
from project.model.business.smartphone_business import (
    check_is_notification,
    forward_message_smart_tv,
    type_notification,
    check_user_confirm,
)
from project.model.smartphone import control, confirm_user, mutex_confirm
from project import socketio
from threading import Thread
from project.model.publisher.smartphone_publisher import SmartphonePublisher
import threading
import json
import time

forwarded = False
try_again = False
start_time = 0
time_waiting = 0


class SmartphoneSubscriber(ConfigScenario, Thread):
    def __init__(self, type_consume):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.channel.queue_delete(queue=queue_smartphone_bm)
        self.channel.queue_delete(queue=queue_smartphone_st)
        self._stop = threading.Event()
        self.type_consume = type_consume
        self.declare_exchange(exchange, "topic")
        self.declare_queue(queue_smartphone_bm)
        self.declare_queue(queue_smartphone_st)

    def run(self):
        if self.type_consume == "babymonitor":
            self.bind_exchange_queue(exchange, queue_smartphone_bm, bm_info)
            self.consume_message_baby_monitor()
        if self.type_consume == "smart_tv":
            self.bind_exchange_queue(exchange, queue_smartphone_st, st_info)
            self.consume_message_tv()

    def stop(self):
        if self.type_consume == "babymonitor":
            print("(Subscribe) SP|BM: Close")
            self._stop.set()
            self._stop.isSet()
        else:
            print("(Subscribe) SP|TV: Close")
            self._stop.set()
            self._stop.isSet()

    def consume_message_baby_monitor(self):
        print(
            " [*] Smartphone waiting for messages from Baby Monitor."
            + " To exit press CTRL+C"
        )
        self.channel.basic_consume(
            queue=queue_smartphone_bm,
            on_message_callback=self.callback_babymonitor_sm,
            auto_ack=False,
        )

        self.channel.start_consuming()

    def consume_message_tv(self):
        print(" [*] Smartphone waiting for messages from TV." + " To exit press CTRL+C")

        self.channel.basic_consume(
            queue=queue_smartphone_st,
            on_message_callback=self.callback_smart_tv,
            auto_ack=False,
        )

        self.channel.start_consuming()

    def callback_babymonitor_sm(self, ch, method, properties, body):
        global time_waiting, forwarded, start_time

        ch.basic_ack(delivery_tag=method.delivery_tag)
        body = body.decode("UTF-8")
        body = json.loads(body)
        notification = check_is_notification(body)
        socketio.emit("SmartphoneReceive", body)
        if notification:
            if start_time == 0:
                start_time = int(time.time())
            time_waiting = int(time.time()) - start_time
            info = type_notification(body)
            socketio.emit("SmartphoneInformation", {"info": info})
            if time_waiting > 10 and not forwarded:
                forwarded = True
                forward_message_smart_tv()
        else:
            start_time, time_waiting = 0, 0 
            socketio.emit("SmartphoneInformation", {"info": "Emma is fine."})

    def callback_smart_tv(self, ch, method, properties, body):
        global forwarded, try_again
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        body = body.decode("UTF-8")
        body = json.loads(body)
        socketio.emit("FromTv", body)
        time.sleep(1)
        confirm = check_user_confirm()
        if body["block"] and not confirm:
            try_again = True
            socketio.emit("FromTvInformation", {"info": "TV couldn't show message"})
        else:

            if try_again and not confirm:
                try_again = False
                forward_message_smart_tv()
            
            forwarded = False
            # send confirmation to BM
            SmartphonePublisher("confirmation").start()

            socketio.emit("FromTvInformation", {"info": "TV just showed the message"})

