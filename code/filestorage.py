import json
from .observers import Observer
import os


class ObserverToJson(object):
    """
    Write the events of a generic Observer in a json file 
    :param observer: a generic Observer object 
    """
    def __init__(self, observer) -> None:
        assert issubclass(type(observer), Observer)
        self.observer = observer
        
    # store each event of an Observer in a list
    def observer_events_to_dict(self):
        events = []
        for event in self.observer.events:
            events.append(event.to_dict())
        return events
    
    def __str__(self) -> str:
        return f"<OnserverToJson(observer={self.observer})>"
    
    # store events in json files
    def _store_json(self) -> None:
        # create json file if not exists
        folder = "results_observers"
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        filename = self.observer.name + ".json"

        with open(os.path.join(folder, filename), "w+", encoding="UTF-8") as fw:
            data = self.observer_events_to_dict()
            json.dump(data, fw, indent=4, ensure_ascii=False, default=str)

    # register events per file and store them in a dedicated json file
    def save_json(self) -> None:
        if self.observer.send_notification is True:
            self._store_json()
        else:
            pass
                