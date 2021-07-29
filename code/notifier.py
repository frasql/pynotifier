from typing import List, Any, Tuple
from .observers import Observer


class Singleton(type):
    _instances = {}
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
        else:
            raise Exception("Notifier object is a singleton. You must create only one instance!")
            # cls._instances[cls].__init__(*args, **kwargs) -> return None for replicated instance 



class Notifier(metaclass=Singleton):
    """
    Events notifier is a singleton, only one instance can be created
    :param oservers: list of observer objects
    """
    def __init__(self, observers: List["Observer"]) -> None:
        assert isinstance(observers, list)
        for obj in observers:
            if not issubclass(type(obj), Observer):
                raise TypeError("Only a list of observers are allowed")
        
        self.observers = observers
        # store TextObserver objects if they have some notification result
        self.wait_dict = {}
        
        # find notification for each observer when the notifier is instantiated
        self._find_events()
            
    def __str__(self) -> str:
        return f"<Notifier(observers={self.observers})>"
    
    # register events for each observer and store them in a dict(observer_name=observer)
    def _find_events(self) -> None:
        for observer in self.observers:
            if observer.send_notification is True:
                self.wait_dict[observer.name] = (observer.events, observer.dst)
            else:
                print("No events")
                
    # get each notification stored in wait_dict
    def _get_events(self, name_event: str) -> Tuple:
        return self.wait_dict[name_event]
    
    # events for an observer
    def events(self, name_event: str):
        obs_events = self._get_events(name_event)
        return obs_events[0]
    
    # destination (owner) of the observer
    def destination(self, name_event: str):
        obs_events = self._get_events(name_event)
        return obs_events[1]
    
    
    def send_email_notification(self):
        if len(self.wait_dict) != 0:
            for name in self.wait_dict:
                obs_events = self.get_events(name)
                if obs_events[1] != "missing":
                    for event in obs_events[0]:
                        print(event.to_text())
                    
    
    