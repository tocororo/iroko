from lxml import etree
from iroko.records import ContributorRole 

class IrokoPerson:

    @staticmethod
    def get_person_dict_from_nlm(contrib: etree._Element):
        """get a IrokoPerson from {http://dtd.nlm.nih.gov/publishing/2.3}contrib 
        etree._Element"""

        person = dict()
        xmlns = '{http://dtd.nlm.nih.gov/publishing/2.3}'
        surname = contrib.find(xmlns+'name/'+xmlns+'surname')
        given_names = contrib.find(xmlns+'name/'+xmlns+'given-names')
        aff = contrib.find(xmlns+'aff')
        email = contrib.find(xmlns+'email')
        if given_names is not None and surname is not None\
            and given_names.text is not None and surname.text is not None:
            person['name']=given_names.text + surname.text
        else:
            # FIXME if a person dont have surname and given name, then is not a person.... this should be an exception?
            return None
        if aff is not None:
            person['affiliations'] = []
            person['affiliations'].append(aff.text)
        if email is not None:
            person['email'] = email.text
        person['roles'] = []
        if 'corresp' in contrib.attrib:
            if contrib.attrib['corresp'] == "yes":
                person['roles'].append(ContributorRole.ContactPerson.value)
        if 'contrib-type' in contrib.attrib:
            ctype = contrib.attrib['contrib-type']
            if ctype == "author":
                person['roles'].append(ContributorRole.Author.value)
            if ctype == "editor":
                person['roles'].append(ContributorRole.Editor.value)
            if ctype == "jmanager":
                person['roles'].append(ContributorRole.JournalManager.value)
        return person


        