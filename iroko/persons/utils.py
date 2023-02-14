

from lxml import etree

from iroko.records import ContributorRole

def get_people_from_nlm(metadata: etree._Element):
    """get a PersonRecord from {http://dtd.nlm.nih.gov/publishing/2.3}contrib
    etree._Element
    return creators, contribs dics, """

    xmlns = '{http://dtd.nlm.nih.gov/publishing/2.3}'
    contribs_xml = metadata.findall('.//' + xmlns + 'contrib')

    contributors = {}

    for contrib in contribs_xml:
        person = dict()

        surname = contrib.find(xmlns + 'name/' + xmlns + 'surname')
        given_names = contrib.find(xmlns + 'name/' + xmlns + 'given-names')
        aff = contrib.find(xmlns + 'aff')
        email = contrib.find(xmlns + 'email')
        if given_names is None and surname is None:
            # FIXME if a person dont have surname or given name, then is not a person....
            #  even if there is an email?
            continue
        else:
            name = ""
            if given_names is not None and given_names.text is not None:
                name += given_names.text
            if surname is not None and surname.text is not None:
                name += ' ' + surname.text
            person['name'] = name
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
            if person['name'] in contributors.keys():
                contributors[person['name']]['roles'].extend(person['roles'])
            else:
                contributors[person['name']] = person
    creators = []
    contribs = []
    for name in contributors:
        person = contributors[name]
        if ContributorRole.Author.value in person['roles']:
            creators.append(person)
        else:
            contribs.append(person)
    return creators, contribs
