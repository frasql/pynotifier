from typing import List, Any, Tuple
from .observers import Observer
from .utils import send_mail
import webbrowser
from pathlib import Path


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
    def obs_events(self, name_event: str):
        obs_events = self._get_events(name_event)
        return obs_events[0]
    
    # destination (owner) of the observer
    def obs_destination(self, name_event: str):
        obs_events = self._get_events(name_event)
        return obs_events[1]
    
    # send notification to email destination in plain text or html
    def send_email_notification(self, name_event: str, html=False) -> None:
        if len(self.wait_dict) != 0:
            destination = self.obs_destination(name_event)
            if html is True:
                events = [event.to_html() for event in self.obs_events(name_event)]
                for event in events:
                    try:
                        print(event)
                        # send_mail(text="Aplication Notification", subject="Notification", from_email="sender", to_emails=[destination], html=str(event))
                    except Exception as e:
                        raise Exception(f"Errore sending emails: {e}")
            else:
                events = [event.to_text() for event in self.obs_events(name_event)]
                for event in events:
                    try:
                        print(event)
                        # send_mail(text=event, subject="Notification", from_email="sender", to_emails=[destination])
                    except Exception as e:
                        raise Exception(f"Errore sending emails: {e}")
                    
                    
    # send notification events to an html page (locally or remote)
    def _events_to_html(self, name_event: str) -> List["str"]:
        if len(self.wait_dict) != 0:
            events = [event.to_html() for event in self.obs_events(name_event)]
        return events
    
    
    def save_to_html(self, name_event: str, html_filename) -> None:
        BASEDIR = Path(__file__).resolve().parent.parent
        HTML_PATH = Path.joinpath(BASEDIR, "templates")
        
        events = self._events_to_html(name_event)
        
        try:
            f = open(Path.joinpath(HTML_PATH, html_filename),'w+')
                
            message = ""
            for event in events:
                message += event
                
            f.write(message)
            f.close()
        except:
            raise Exception("Unable to write the html file")
    
                    
    # send notification events to an html page (locally or remote)
    def open_in_html(self, name_event: str, html_filename: str) -> None:
        BASEDIR = Path(__file__).resolve().parent.parent
        HTML_PATH = Path.joinpath(BASEDIR, "templates")
                
        try:
            self.save_to_html(name_event, html_filename)
        except Exception as e:
            raise Exception(f"{e}")
 
        try:   
            html_path_render = f"file:///{HTML_PATH}/{html_filename}"
            #Change path to reflect file location
            webbrowser.open_new_tab(html_path_render)
        except:
            raise Exception("Unable to render html file")


        
            
                
                
                
                    
    
    