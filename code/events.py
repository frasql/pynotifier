from typing import Union
import uuid


class Event(object):
    def __init__(self, file: str, n_row: Union[str, int], description: str) -> None:
        self._id = uuid.uuid4().hex
        self.file = file
        self.n_row = n_row
        self.description = description
        
    def __str__(self) -> str:
        return f"<Event(file={self.file}, n_row={self.n_row}, event={self.event})>"
    
    def to_dict(self):
        return vars(self)
    
    def to_text(self):
        text = f"Attenzione, all'interno del file {self.file} alla riga {self.n_row} si è verificato il seguente evento: {self.description}"
        return text
    

class RegexEvent(Event):
    def __init__(self, file: str, n_row: Union[str, int], description: str) -> None:
        super().__init__(file, n_row, description)
        
    def __str__(self) -> str:
        return f"<RegexEvent(file={self.file}, n_row={self.n_row}, event={self.event})>"
    
    def to_dict(self):
        return vars(self)
    
    def to_text(self):
        text = f"Attenzione, all'interno del file {self.file} alla riga {self.n_row} si è verificato il seguente evento: {self.description}"
        return text
    
class DateTimeEvent(Event):
    def __init__(self, file: str, n_row: Union[str, int], description: str, datetime_obj: str) -> None:
        super().__init__(file, n_row, description)
        self.datetime_obj = datetime_obj

    def to_dict(self):
        return vars(self)
    
    def to_text(self):
        text = f"Attenzione, all'interno del file {self.file} alla riga {self.n_row} si è verificato il seguente evento: {self.description}"
        return text
        
        
