import json
from .observers import Observer
import os
from typing import List
from concurrent.futures import ThreadPoolExecutor


class ObserverToJson(object):
    """
    Utils for save observer(s) in a specific file in json format
    Each method requires an observer object as parameter
    """ 
    # store each event of an Observer in a list
    @staticmethod
    def __observer_events_to_dict(observer):
        events = []
        for event in observer.events:
            events.append(event.to_dict())
        return events
    
    # create result folder and json file for an observer
    @staticmethod
    def __store_json(observer) -> None:
        # create json file if not exists
        folder = "results_observers"
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        filename = observer.name + ".json"

        with open(os.path.join(folder, filename), "w+", encoding="UTF-8") as fw:
            data = ObserverToJson.__observer_events_to_dict(observer)
            json.dump(data, fw, indent=4, ensure_ascii=False, default=str)

    # save observer events to json file 
    @staticmethod
    def save_json(observer) -> None:
        if observer.send_notification is True:
            ObserverToJson.__store_json(observer)
        else:
            raise Exception("Nothing to do...")
   
    # save multiple observers events to different json files
    @staticmethod
    def save_multiple_json(observers: List["Observer"]) -> None:
        assert isinstance(observers, list)
        for obj in observers:
            if not issubclass(type(obj), Observer):
                raise TypeError("Only a list of observers is allowed")
    
        with ThreadPoolExecutor() as executor:
            executor.map(ObserverToJson.save_json, observers)
            
            
            
    