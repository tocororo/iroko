from typing import Any, List

from iroko.records.api import IrokoRecord

from unicodedata import normalize

from iroko.records.search import IrokoRecordSearch


def _is_cuban_affiliation(affiliation: str):
    fix_words = ['cuba', 'pinar del rio', 'artemisa'
                , 'mayabeque', 'matanzas', 'habana'
                , 'cienfuegos', 'villa clara', 'santa clara'
                , 'santi spiritus', 'ciego de avila'
                , 'camaguey', 'las tunas', 'bayamo', 'holguin'
                , 'santiago de cuba', 'guantanamo']
    af = normalize('NFC', affiliation.lower())
    for word in fix_words:
        if word in af:
            return True
    return False


def _creator_is_cuban(creator):
    if 'affiliations' in creator:
        for aff in creator['affiliations']:
            if _is_cuban_affiliation(aff):
                return True
    return False


def _creator_is_author(creator):
    if 'roles' in creator:
        for role in creator['roles']:
            if role == 'Author':
                return True
    return False


def get_cuban_authors_from_record(rec: IrokoRecord):
    authors: List[dict] = []
    if 'creators' in rec:
        for creator in rec['creators']:
            if _creator_is_author(creator) and _creator_is_cuban(creator):
                authors.append(creator)
    return authors


def get_all_cubans_authors_from_records():
    search = IrokoRecordSearch()
    cubans = dict()
    for hit in search.scan():
        record = IrokoRecord.get_record_by_pid_value(hit.id)
        authors = get_cuban_authors_from_record(record)
        for aut in authors:
            if 'name' in aut and aut['name'] not in cubans:
                cubans[aut['name']] = aut
    return cubans

