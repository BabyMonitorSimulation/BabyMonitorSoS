from project.model.subscriber.baby_monitor_subscriber import BabyMonitorSubscriber
from project.model.subscriber.smartphone_subscriber import SmartphoneSubscriber
from project.model.subscriber.smart_tv_subscriber import SmartTvSubscriber
from multiprocessing import Process
from time import sleep

subscriber_list = []
subscriber_list.append(BabyMonitorSubscriber())
subscriber_list.append(SmartphoneSubscriber('babymonitor'))
subscriber_list.append(SmartphoneSubscriber('smart_tv'))
subscriber_list.append(SmartTvSubscriber())

# execute
process_list = []
for sub in subscriber_list:
    process = Process(target=sub.run)
    process.start()
    process_list.append(process)

sleep(1)
