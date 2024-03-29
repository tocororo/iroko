import datetime
import os
from typing import List
from unicodedata import normalize

from pandas import DataFrame, read_csv

from iroko.records.api import IrokoRecord
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

def _is_university_affiliation(affiliation: str):
    fix_words = ['universidad', 'university']
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
    universities = dict()
    for hit in search.scan():
        record = IrokoRecord.get_record_by_pid_value(hit.id)
        authors = get_cuban_authors_from_record(record)
        for aut in authors:
            if 'name' in aut and aut['name'] not in cubans:
                cubans[aut['name']] = aut
                for aff in aut['affiliations']:
                    if _is_university_affiliation(aff):
                        universities[aut['name']] = aut
    return cubans, universities

def _tmp_func():
    search = IrokoRecordSearch()
    last:str = '2022-12-31'
    universities = dict()
    for hit in search.scan():
        record = IrokoRecord.get_record_by_pid_value(hit.id)
        cur = record['publication_date']
        if last > cur:
            last = cur
            print('---------------------')
            print('---------------------')
            print(last)
            print(record)
            print('---------------------')
            print('---------------------')
#Helpers for file uploads
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'csv', 'json'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_ext(filename):
    return filename.rsplit('.', 1)[1].lower()

def csv_to_json(file):
    filename=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file.save(os.path.join('./data',filename+'.'+get_ext(file.filename)))
    df= read_csv(os.path.join('./data')+'/'+filename+'.'+get_ext(file.filename))
    DataFrame.to_json(df,path_or_buf=os.path.join('./data',filename+'.json'),orient='records')
    return os.path.join('./data',filename+'.json')
