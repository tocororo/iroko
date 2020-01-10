

from iroko.harvester.base import Formater


class ISSN(Formater):

    def __init__(self):

        self.metadataPrefix ='issn.org'
        self.xmlns = ''


    def ProcessItem(self, xml:etree._Element):
        """given an html response from a search in issn, return the list of issns """


        
