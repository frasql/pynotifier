from typing import Union
import uuid
from .html_builder import HtmlElement


class Event(object):
    def __init__(self, file: str, n_row: Union[str, int], description: str) -> None:
        self._id = uuid.uuid4().hex
        self.file = file
        self.n_row = n_row
        self.description = description.strip()
            
        
    def __str__(self) -> str:
        return f"<Event(file={self.file}, n_row={self.n_row}, description={self.description})>"
    
    def to_dict(self):
        return vars(self)
    
    def to_text(self):
        text = f"Attenzione, all'interno del file {self.file} alla riga {self.n_row} si è verificato il seguente evento: {self.description} \n\n"
        return text
    
    def to_html(self):
        # create open / closed div
        builder = HtmlElement.create('div')
        # create html element to chain
        builder.add_child_chain('h4', "Attenzione, notifica dall'aplicazione").add_child_chain('h5', f"All'interno del file: {self.file} si è verificto il seguente evento: ")
        builder.add_child_chain('h5', f"Riga numero {self.n_row}, descrizione: {self.description}")
        return builder


