
"""Dublin Core /elements/1.1/ namespace processor"""

from iroko.modules.harvester.ext import Formater



class DubliCoreElements(Formater):

     def __init__(self):
          self.metadataPrefix ='oai_dc'

     """given an item return a Record"""
     def ProcessRecord(self, item):
          # return a record... 
          return item
