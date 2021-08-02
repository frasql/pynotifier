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
    
    def to_html(self, div_style: str = None, p_style = None):
        # create open / closed div
        if div_style is None:
            builder = HtmlElement.create('div style="display: flex; justify-content: center; align-items: center; border: 1px solid lightgrey;"')
        else:
            builder = HtmlElement.create('div style="{}"'.format(div_style))
            
        # create html element to chain
        if p_style is None:
            builder.add_child_chain('h4 style="display: flex; justify-content: center; align-items: center"', f"Attenzione! Notifica numero: {self._id}").add_child_chain('h5 style="display: flex; justify-content: center; align-items: center"', f"All'interno del file: {self.file} si è verificto il seguente evento: ")
            builder.add_child_chain('h5 style="display: flex; justify-content: center; align-items: center"', f"Riga numero {self.n_row}, descrizione: {self.description}")
        else:
            builder.add_child_chain('p style="{}"'.format(p_style), f"Attenzione! Notifica numero: {self._id}").add_child_chain('p style="{}"'.format(p_style), f"All'interno del file: {self.file} si è verificto il seguente evento: ")
            builder.add_child_chain('p style="{}"'.format(p_style), f"Riga numero {self.n_row}, descrizione: {self.description}")            
        
        return str(builder)
