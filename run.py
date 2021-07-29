from code.observers import DateTimeObserver, TextObserver
from code.notifier import Notifier
from code.filestorage import ObserverToJson
import datetime
                

datetime_to_search = datetime.datetime(2021,7,27,19,54,21,411)
    
# create observer objects           
time = DateTimeObserver("time", "logs", datetime_to_search=datetime_to_search)
info = TextObserver("info", "logs", word_to_search="INFO", dst="bob@gmail.com")


""" Store event in json example """

# instantiate the Observer to json object
# call save_json() method and save the events in a folder (results_observers) with filename = observer_name
store_info = ObserverToJson(info)
store_info.save_json()

store_time = ObserverToJson(time)
store_time.save_json()

""" Notification event example  """


# create a notifier with a list of observers
notifier = Notifier([info])

# retrieve the destination of an observer from the notifier
info_destination = notifier.obs_destination("info")
# retrieve the events of an observer from the notifier
info_events = notifier.obs_events("info")
# notify via email
notifier.send_email_notification("info", html=True)
