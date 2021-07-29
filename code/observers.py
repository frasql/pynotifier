import os
from collections import deque
import re
import datetime
from .events import Event
from .utils import convert_datetime, convert_time

    
    
class Observer(object):
    """
    Generic observer object, each observer inherit from it
    :param name: unique name for each class instance allows to differentiate the observer
    :param log_dir: directory where the files are located
    :param dst: destination of notifications
    """
    intance_names = set()
    
    def __init__(self, name: str, log_dir: str, dst: str = None) -> None:

        # only unique instance names are allowed
        if not isinstance(name, str):
            raise TypeError("Param name must be a string")
        
        if name in Observer.intance_names:
            raise Exception("Only different names for each instance of a generic Observer object are allowed")
        
        self.name = name
        # add name of the instance to set class attribute
        Observer.intance_names.add(name)
        # directory with logs / text
        self.log_dir = log_dir
        # observer destination name
        if dst is None:
            self.dst = "missing"
        else:
            self.dst = dst
        
    def search(self):
        raise NotImplementedError
    
        
class TextObserver(Observer):
    """
    Object that allows user to find regular expressions in multiple files, and store the search result in a json file
    :param name: unique name for each class instance allows to differentiate the observer
    :param log_dir: directory where the files are located
    :param dst: destination of notifications
    :param word_to_search: allows to search a specific word in multiple files
    :param regex: allows user to write his regular expression. You can modify this property with a Pattern type expression --> self.regex = re.compile(r'your regex')  
    :param send_notification: allows external object to know if a notification is present
    """
    
    def __init__(self, name: str, log_dir: str, dst: str = None, word_to_search: str = None, regex: str = None) -> None:
        super().__init__(name, log_dir, dst)
        assert regex is not None or word_to_search is not None

        
        if word_to_search is not None:
            self._re = re.compile(".*({}).*".format(word_to_search))
            
        if regex is not None:
            self._re = regex

        # handle notification state
        self.send_notification = False
        
        # list that contains Event objects
        self.events = self.search()
        
        
    def __str__(self) -> str:
        return f"<TextObserver(name={self.name}, log_dir={self.log_dir}, regex={self._re}, events={self.events}, dst={self.dst})"
        
        
    """
    search selected regex in multiple files and create a deque of events of Event object --> Event(file_contains_event=file, event_n_row=row, event_desrciption=description, dst=destination) 
    store the whole row where the event is happened   
    set send_notification to True if the queue events is not empty
    """
    def search(self) -> deque:
        if self._re is None:
            raise Exception("Without an initial word to search you must change the value of the regex attribute manually")
        # store each event for this TextObserver
        events = deque()
        for file in os.listdir(self.log_dir):
            with open(os.path.join(self.log_dir, file), "r") as f_log:
                data = f_log.readlines()
                for row, description in enumerate(data):   
                    if self._re.search(description):
                        event = Event(file=file, n_row=row, description=description) # create an event
                        events.append(event)
                if len(events) != 0:
                    self.send_notification = True
                    
        return events
 
    
class DateTimeObserver(Observer):
    def __init__(self, name: str, log_dir: str, dst: str = None, datetime_to_search: datetime = None) -> None:
        super().__init__(name, log_dir, dst)
        assert datetime_to_search is not None
        
        if isinstance(datetime_to_search, datetime.datetime):
            self.datetime_to_search = convert_datetime(datetime_to_search)
            self._re_datetime = re.compile(".*({}).*".format(self.datetime_to_search))
        else:
            raise TypeError("Only datetime.datetime objects are allowed")
        

        # handle notification state
        self.send_notification = False
        
        # list that contains Event objects
        self.events = self.search()
        
        
    def __str__(self) -> str:
        return f"<DatetimeObserver(name={self.name}, log_dir={self.log_dir}, datetime_to_search={self.datetime_to_search}, events={self.events}, dst={self.dst})"
        
        
    """
    search selected regex in multiple files and create a deque of events of Event object --> Event(file_contains_event=file, event_n_row=row, event_desrciption=description, dst=destination) 
    store the whole row where the event is happened   
    set send_notification to True if the queue events is not empty
    """
    def search(self) -> deque:
        # store each event for this DatetimeObserver
        events = deque()
        for file in os.listdir(self.log_dir):
            with open(os.path.join(self.log_dir, file), "r") as f_log:
                data = f_log.readlines()
                for row, description in enumerate(data):   
                    if self._re_datetime.search(description):
                        event = Event(file=file, n_row=row, description=description) # create an event
                        events.append(event)
                if len(events) != 0:
                    self.send_notification = True
                    
        return events


class DateObserver(Observer):
    def __init__(self, name: str, log_dir: str, dst: str = None, date_to_search: datetime = None) -> None:
        super().__init__(name, log_dir, dst)
        assert date_to_search is not None
        
        if isinstance(date_to_search, datetime.date):
            self.date_to_search = date_to_search.strftime("%Y-%m-%d")
            self._re_date = re.compile(".*({}).*".format(self.date_to_search))
    

        # handle notification state
        self.send_notification = False
        
        # list that contains Event objects
        self.events = self.search()
        
        
    def __str__(self) -> str:
        return f"<DateObserver(name={self.name}, log_dir={self.log_dir}, date_to_search={self.date_to_search}, events={self.events}, dst={self.dst})"
        
        
    """
    search selected regex in multiple files and create a deque of events of Event object --> Event(file_contains_event=file, event_n_row=row, event_desrciption=description, dst=destination) 
    store the whole row where the event is happened   
    set send_notification to True if the queue events is not empty
    """
    def search(self) -> deque:
        # store each event for this DateObserver
        events = deque()
        for file in os.listdir(self.log_dir):
            with open(os.path.join(self.log_dir, file), "r") as f_log:
                data = f_log.readlines()
                for row, description in enumerate(data):   
                    if self._re_date.search(description):
                        event = Event(file=file, n_row=row, description=description) # create an event
                        events.append(event)
                if len(events) != 0:
                    self.send_notification = True
                    
        return events

 
 
class TimeObserver(Observer):
    def __init__(self, name: str, log_dir: str, dst: str = None,  time_to_search: datetime = None) -> None:
        super().__init__(name, log_dir, dst)
        assert time_to_search is not None
        
        
        if isinstance(time_to_search, datetime.time):
            self.time_to_search = convert_time(time_to_search)
            self._re_time = re.compile(".*({}).*".format(self.time_to_search))   
    

        # handle notification state
        self.send_notification = False
        
        # list that contains Event objects
        self.events = self.search()
        
        
    def __str__(self) -> str:
        return f"<TimeObserver(name={self.name}, log_dir={self.log_dir}, time_to_search={self.time_to_search}, events={self.events}, dst={self.dst})"
        
        
    """
    search selected regex in multiple files and create a deque of events of Event object --> Event(file_contains_event=file, event_n_row=row, event_desrciption=description, dst=destination) 
    store the whole row where the event is happened   
    set send_notification to True if the queue events is not empty
    """
    def search(self) -> deque:
        # store each event for this TimeObserver
        events = deque()
        for file in os.listdir(self.log_dir):
            with open(os.path.join(self.log_dir, file), "r") as f_log:
                data = f_log.readlines()
                for row, description in enumerate(data):   
                    if self._re_time.search(description):
                        event = Event(file=file, n_row=row, description=description) # create an event
                        events.append(event)
                if len(events) != 0:
                    self.send_notification = True
                    
        return events
  
        
    

                
                
                
