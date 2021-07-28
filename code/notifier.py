from typing import List, Any
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
                self.wait_dict[observer.name] = observer.events
            else:
                print("No events")
                
    # get each notification stored in wait_dict
    def get_events(self, name_event: str):
        return self.wait_dict[name_event]