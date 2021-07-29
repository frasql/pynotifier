 
# Pynotifier

## About


* Python application that allows to create text / logging observers, store events in json fomat and send email notification in plain text or html


## Requirements

* Python 3.3+.
* The application doesn't need external modules

## Usage

* Create a logger with setup_logger function (logger.py) 
* An Observer object allows to create multiple events based on a regular expression or a datetime object
* Store events for each observers in json format with ObserverToJson object
* Send a notification in plain text or html format with Notifier object


### Example (run.py)

* A basic example: 

```
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
```

### Future Implementation

* Async Pynotifier




