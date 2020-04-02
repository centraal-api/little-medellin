from typing import List

class Person(object):
    def __init__(self, name, status = 's'):
        self.name   = name
        self.status  = status
        self.occupation  =  ''
        self.contacts : List[Contact] = []
        self.vector = ''
    
    def meet(self, someone, timeevent):
        self.contacts.append(Contact(someone, timeevent))

    def showme_your_id(self):
        print(self.name, self.status)

    def list_my_contacts(self):
       for c in self.contacts:
          print(c.someone.name, c.someone.status)
        
    def contacts_infected(self):
        for c in self.contacts:
          if (c.someone.status == 'i'):
              print("take care you were in contact with:")
              print(c.someone.name)

    def update_vector(self, vector_name: str, timeevent):
        self.vector = (vector_name, timeevent)

class Contact(object):
    def __init__(self, someone : Person, timeevent):
        self.someone = someone
        self.timeevent = timeevent



