from code.observers import DateTimeObserver, TextObserver
from code.filestorage import ObserverToJson
from code.notifier import Notifier
import datetime
                

datetime_to_search = datetime.datetime(2021,7,27,19,54,21,411)
                
time = DateTimeObserver("time", "logs", datetime_to_search=datetime_to_search)
info = TextObserver("info", "logs", word_to_search="INFO", dst="fra.squillace@gmail.com")



notifier = Notifier([time, info])


info_destination = notifier.destination("info")
info_events = notifier.events("info")

print(info_events)
print(info_destination)