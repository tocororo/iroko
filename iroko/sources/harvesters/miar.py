import json
import os
import time
from random import randint

import requests
from flask import current_app
from invenio_db import db
from lxml import html

from iroko.harvester.base import BaseHarvester
from iroko.harvester.utils import get_iroko_harvester_agent
from iroko.sources.api import SourceRecord, IrokoSourceVersions
from iroko.sources.models import Issn, SourceType, SourceStatus
from iroko.utils import IrokoVocabularyIdentifiers, get_default_user
from iroko.vocabularies.models import Term, Vocabulary


# TODO:
# 1- tratar de arreglar el lio del encoding
# 2- la sincronizacion de las revistas tiene que tener en cuenta que una revista puede tener mas de un issn.


class MiarHarvester(BaseHarvester):
    """
    TODO: Document this!!!!
    """

    @classmethod
    def collect_databases(cls, recheck=True):
        work_dir = current_app.config['IROKO_DATA_DIRECTORY']
        if not recheck:
            harvester = MiarHarvester(work_dir, True)
        else:
            # print('recheck is True')
            harvester = MiarHarvester(work_dir, False)
            harvester.get_info_database_recheck()

    @classmethod
    def sync_databases(cls, recheck=True):
        work_dir = current_app.config['IROKO_DATA_DIRECTORY']
        indexes = Vocabulary.query.filter_by(identifier=IrokoVocabularyIdentifiers.INDEXES.value).first()
        if not indexes:
            indexes = Vocabulary()
            indexes.identifier = IrokoVocabularyIdentifiers.INDEXES.value
            indexes.human_name = 'Indices, Bases de Datos'
            db.session.add(indexes)
            db.session.commit()
        miar_harvester = MiarHarvester(work_dir)
        miar_harvester.syncronize_miar_databases()

    @classmethod
    def collect_journals(cls):
        work_dir = current_app.config['IROKO_DATA_DIRECTORY']
        miar_harvester = MiarHarvester(work_dir)
        miar_harvester.collect_miar_info()

    @classmethod
    def sync_journals(cls):
        work_dir = current_app.config['IROKO_DATA_DIRECTORY']
        miar_harvester = MiarHarvester(work_dir)
        miar_harvester.syncronize_miar_journals()

    def __init__(self, work_dir, load_remote=False):
        self.work_dir = os.path.join(work_dir, 'miar')
        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)

        self.miar_dbs_file = os.path.join(self.work_dir, 'dbs.json')
        self.issn_info_file = os.path.join(self.work_dir, 'issn.info.cuba.json')

        self.issn_info_miar_dir = os.path.join(self.work_dir, 'miar_info')
        if not os.path.exists(self.issn_info_miar_dir):
            os.mkdir(self.issn_info_miar_dir)
        self.issn_info_miar = os.path.join(self.work_dir, 'issn.info.miar.json')
        self.miar_journals_file = os.path.join(self.work_dir, 'miar.journals.json')
        self.miar_types_vocab_name = 'miar_types'
        self.miar_database_vocab_name = 'miar_databases'
        if load_remote:
            self.miar_groups = [
                {
                    'name': 'WoS / Scopus',
                    'url':  'http://miar.ub.edu/databases/GRUPO/G'
                },
                {
                    'name': 'Bases de datos multidisciplinares',
                    'url':  'http://miar.ub.edu/databases/GRUPO/S'
                },
                {
                    'name': 'Bases de datos especializadas',
                    'url':  'http://miar.ub.edu/databases/GRUPO/E'
                },
                {
                    'name': 'Sistemas de evaluación',
                    'url':  'http://miar.ub.edu/databases/GRUPO/M'
                }
            ]
            self.get_url_db()
            self.get_info_databases()
        else:
            with open(self.miar_dbs_file, 'r') as file_db:
                self.miar_groups = json.load(file_db)

    def get_url_db(self):
        sess = requests.Session()
        sess.headers.update(get_iroko_harvester_agent())
        for group in self.miar_groups:
            # print('getting group {0}'.format(group['name']))
            group['dbs'] = self.get_db_group(sess, group['url'])

    def get_db_group(self, sess, url):
        result = []

        sleep_time = randint(3, 9)
        time.sleep(sleep_time)
        response = sess.get(url)
        doc1 = html.fromstring(response.text)
        element = doc1.xpath('.//span[@id="total_registros"]')
        count_db = element[0].text.split()[0]
        if int(count_db) > 25:
            self.post_database_miar(url, result, sess, count_db)
        else:
            element_db = doc1.xpath('.//div[@class="table-responsive"]//a')
            for e in element_db:
                result.append({'name': e.text, 'url': e.get('href')})

        return result

    def post_database_miar(self, url: str, result, sess: requests.Session, count):
        value_ini = 0
        value_content_length = 35
        headers = {
            'Accept':                    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept-Encoding':           "gzip, deflate",
            'Accept-Language':           "en-US,en;q=0.5",
            'Connection':                "keep-alive",
            'Content-Length':            str(value_content_length),
            'Content-Type':              "application/x-www-form-urlencoded",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent':                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",
            'Cache-Control':             "max-age=0",
        }

        while int(count) >= int(value_ini):
            if value_ini > 0:
                value_content_length = 36
            payload = 'directorio=miar&letra=&ini=' + str(value_ini) + '&rgs=25'
            headers['Content-Length'] = str(value_content_length)
            sleep_time = randint(3, 9)
            time.sleep(sleep_time)
            resp = sess.post(url, data=payload, headers=headers)

            if resp.status_code == 200:
                doc1 = html.fromstring(resp.text)
                element_db = doc1.xpath('.//div[@class="table-responsive"]//a')
                for e in element_db:
                    result.append({'name': e.text, 'url': e.get('href')})
            else:
                # print('ERROR ' + str(resp.status_code) + ' en ' + url)
                pass

            value_ini = value_ini + 25

    def get_info_db(self, url):

        sess = requests.Session()
        sess.headers.update(get_iroko_harvester_agent())
        timeout = 30
        dictionary = {}
        response = sess.get(url, timeout=timeout)
        doc1 = html.fromstring(response.text)
        element = doc1.xpath('.//div[@id="gtb_div_base"]//div[@style="display:table-row-group"]')

        for e in element:
            element1 = e.xpath('.//div//div')
            if (element1[1].xpath('.//a')):
                a = element1[1].xpath('.//a')
                dictionary[element1[0].text_content()] = a[0].get('href')
            else:
                dictionary[element1[0].text_content()] = element1[1].text_content().split(sep='\n')[1]
            # sleep_time = randint(3, 9)
            # time.sleep(sleep_time)

        return dictionary

    def get_info_databases(self):
        with open(self.miar_dbs_file, 'w') as file_db:
            for group in self.miar_groups:
                for db in group['dbs']:
                    if 'url' in db:
                        try:
                            # print('getting info of {0}'.format(db['url']))
                            db['info'] = self.get_info_db(db['url'])
                        except Exception as ex:
                            # print('ERROR, getting {0}'.format(db['url']))
                            db['info'] = 'ERROR'
                        else:
                            # print('ok, saving to file')
                            if file_db:
                                file_db.seek(0)
                                json.dump(self.miar_groups, file_db, ensure_ascii=False)
                        finally:
                            sleep_time = randint(3, 9)
                            # print('finally, sleep {0} seconds'.format(sleep_time))
                            time.sleep(sleep_time)

    def get_info_database_recheck(self):
        # print(self.miar_groups)
        for group in self.miar_groups:
            for db in group['dbs']:
                if 'url' in db and (
                    (not 'info' in db) or ('info' in db and db['info'] == 'ERROR')
                ):
                    try:
                        # print('getting info of {0}'.format(db['url']))
                        db['info'] = self.get_info_db(db['url'])
                    except Exception as ex:
                        # print('ERROR, getting {0}'.format(db['url']))
                        db['info'] = 'ERROR'
                    # else:
                    #     # print('ok, saving to file')
                    #     if file_db:
                    #         # This is an error
                    #         file_db.seek(0)

                    finally:
                        sleep_time = randint(3, 9)
                        # print('finally, sleep {0} seconds'.format(sleep_time))
                        time.sleep(sleep_time)
        with open(self.miar_dbs_file, 'w+', encoding=('UTF-8')) as file_db:
            # print('writing to file {0}'.format(self.miar_dbs_file))
            json.dump(self.miar_groups, file_db, ensure_ascii=False)

    def get_info_from_journals(self, issn_path):
        # TODO: dado la lista de issns en un archivo llamar a get_info_journal y guargar todo en el fichero
        # self.miar_journals_file
        dbs = open(self.miar_dbs_file, 'w')
        # print(dbs)
        pass

    def get_info_journal(self, issn: str):

        url = 'http://miar.ub.edu/issn/' + issn

        # print('request: {0}'.format(url))

        sess = requests.Session()
        sess.headers.update(get_iroko_harvester_agent())
        timeout = 60
        dictionary = {}
        response = sess.get(url, timeout=timeout)
        # print('request finish: {0}'.format(url))

        sleep_time = randint(10, 20)
        # print('sleep: {0}'.format(sleep_time))
        time.sleep(sleep_time)

        html_text = response.text

        doc1 = html.fromstring(response.text)
        element_not_found = doc1.xpath('.//div[@class="alert alert-danger"]')
        element = doc1.xpath('.//div[@id="gtb_div_Revista"]//div[@style="display:table-row-group"]')
        element_history = doc1.xpath('.//div[@id="mod_versiones"]//a')

        if len(element_not_found) > 0:
            return element_not_found[0].text, html_text

        # Info ISSN in actual year
        for e in element:
            element1 = e.xpath('.//div//div')
            label = element1[0].text_content()

            if (element1[1].xpath('.//a') and len(element1[1].xpath('.//a')) > 0):
                arr = []
                for elem in element1[1].xpath('.//a'):
                    url = elem.get('href')
                    if 'indizadaen' in url:
                        try:
                            arr.append(url.split('/' + issn + '/')[1])
                        except Exception:
                            pass
                    else:
                        arr.append(elem.text)
                dictionary[label] = arr
            #     a = element1[1].xpath('.//a')
            #     dictionary[element1[0].text_content()] = a[0].text
            # elif(count(element1[1].xpath('.//a')) > 1)
            #     for elem in element1[1].xpath('.//a'):
            #         dictionary[element1[0].text_content()] = elem[0].text
            else:
                dictionary[label] = element1[1].text_content().split(sep='\n')[1]

        # Info ISSN in past years
        for e_h in element_history:
            element_history1 = e_h.xpath('.//img/@alt')
            url_history = e_h.get('href')
            icds_year = element_history1[0]

            self.get_info_icds(url_history, dictionary, sess, icds_year)

            sleep_time = randint(10, 20)
            # print('sleep: {0}'.format(sleep_time))
            time.sleep(sleep_time)

        return dictionary, html_text

    def get_info_icds(self, url: str, dictionary: dict, sess: requests.Session, icds_year: str):

        timeout = 120
        response = sess.get(url, timeout=timeout)
        doc1 = html.fromstring(response.text)
        element = doc1.xpath('.//div[@id="sp_icds"]')
        if len(element) > 0:
            dictionary[str(icds_year)] = element[0].text
            # print(dictionary[str(icds_year)])

    def collect_miar_info(self):
        """
        el fichero issn_list_path debe tener la forma ['issn1', 'issn2', ...]
        crear un nuevo fichero donde:
        por cada issn en el fichero de entrada se guarde:
            { issn : get_info_journal }
        """

        issn_list = Issn.query.all()
        if issn_list:
            for issn in issn_list:
                # print('getting miar info of: {0}'.format(issn.code))

                if not os.path.exists(self.issn_info_miar_dir + '/' + issn.code):
                    res, text = self.get_info_journal(issn.code)
                    with open(os.path.join(self.issn_info_miar_dir, issn.code), 'w+', encoding=('UTF-8')) as file_issn:
                        json.dump(res, file_issn, ensure_ascii=False)
                    with open(os.path.join(self.issn_info_miar_dir, issn.code + '-html'), 'w+',
                              encoding=('UTF-8')) as file_issn:
                        file_issn.write(text)

            #     result[archive] =
            # with open(self.issn_info_miar, 'w+',  encoding=('UTF-8')) as file_issn:
            #     # print('writing to file {0}'.format(self.issn_info_miar))
            #     json.dump(result, file_issn, ensure_ascii=False)
        else:
            return 'danger'

        return 'success'

    def syncronize_miar_databases(self):
        """
        sincroniza lo que  hay en self.miar_dbs_file con la base de datos de iroko
        con los Term y Vocabulary
        TODO: document this !!!!,
        TODO: hacer que la sincronizacion no se pare si ya existe el termino.
        """

        with open(self.miar_dbs_file, 'r') as file_dbs:
            archive = json.load(file_dbs)

        if archive:
            for archive_dbs in archive:
                miar_db_type_term = Term.query.filter_by(identifier=archive_dbs['name']).first()
                if not miar_db_type_term:
                    miar_types = Term()
                    miar_types.identifier = archive_dbs['url']
                    miar_types.vocabulary_id = IrokoVocabularyIdentifiers.INDEXES.value
                    miar_types.description = archive_dbs['name']
                    db.session.add(miar_types)
                    db.session.flush()
                    miar_db_type_term = miar_types
                for archive_dbs_info in archive_dbs['dbs']:
                    try:
                        name = archive_dbs_info['url'].split('/ID/')[1]
                        description = archive_dbs_info['name']
                        miar_db_term = Term.query.filter_by(identifier=name).first()
                        if not miar_db_term:
                            miar_dbs = Term()
                            miar_dbs.identifier = name
                            miar_dbs.vocabulary_id = IrokoVocabularyIdentifiers.INDEXES.value
                            miar_dbs.description = description
                            miar_dbs.data = archive_dbs_info
                            miar_dbs.parent_id = miar_db_type_term.id
                            db.session.add(miar_dbs)
                        else:
                            miar_db_term.name = name
                            miar_db_term.vocabulary_id = IrokoVocabularyIdentifiers.INDEXES.value
                            miar_db_term.description = description
                            miar_db_term.data = archive_dbs_info
                            miar_db_term.parent_id = miar_db_type_term.id

                        db.session.commit()
                    except Exception:
                        pass

                        # db.session.flush()

                        # miar_classification = TermClasification()
                        # miar_classification.term_class_id = miar_db_type_term.id
                        # miar_classification.term_clasified_id = miar_dbs.id
                        # db.session.add(miar_classification)

            return 'success'
        else:
            return 'error'

    def _get_source_by_issn(self, issnModel: Issn) -> SourceRecord:
        """
        get the source by the issn
        si el issn no esta en ningun Source, crea uno nuevo, usando la informacion de el modelo ISSN
        """

        issn = issnModel.code
        data = issnModel.data
        # print("buscando el issn {0}".format(issn))
        pid, source = SourceRecord.get_source_by_pid(issn)
        if source:
            return source
        # print("no existe, creando source {0}".format(issn))
        for item in data["@graph"]:
            if item['@id'] == 'resource/ISSN/' + issn + '#KeyTitle':
                title = item["value"]
                # print(title)
                data = dict()
                data['source_type'] = SourceType.JOURNAL.value
                data['name'] = title
                data['source_status'] = SourceStatus.UNOFFICIAL.value
                data['title'] = title
                data['identifiers'] = [{'idtype': 'pissn', 'value': issn}]
                user = get_default_user()
                msg, source = SourceRecord.new_source(data, user.id)
                if source:
                    return source
        return None

    def syncronize_miar_journals(self):
        """
        sincronizar lo que hay en el info de miar con el modelo TermSource donde
        Source es el source dado el issn
        Term, es el Tems con el nombre de la base de datos en cuestion
        Source es el que tenga el issn que se recolecto.
        Si no existe el Source, se debe crear uno nuevo utilizando la informacion que hay en el model ISSN
        """
        issncount = 0
        sourcecount = 0
        issn_list = Issn.query.all()
        if issn_list:
            try:
                for issn in issn_list:

                    issncount = issncount + 1
                    with open(os.path.join(self.issn_info_miar_dir, issn.code), 'r') as file_issn_miar:
                        archive_issn_miar = json.load(file_issn_miar)
                        try:
                            # atribute = archive_issn_miar['Indexed\xa0in:']
                            if archive_issn_miar != issn.code + ' IS NOT LISTED IN MIAR DATABASE':
                                dbs_split = []
                                # print('---------------------------')
                                # print(archive_issn_miar)
                                # TODO: este es un error que tiene que ver con la forma en que se habren los json
                                keys = [
                                    'Indexed\xa0in:',
                                    'Indexed\u00a0in:',
                                    'Evaluated\xa0in:',
                                    'Evaluated\u00a0in:'
                                ]
                                for key in keys:
                                    if key in archive_issn_miar:
                                        dbs_split.append(str(archive_issn_miar[key]))

                                # print(dbs_split)
                                source = self._get_source_by_issn(issn)
                                # print(type(source), source)
                                sourcecount = sourcecount + 1
                                to_add = []
                                for dbs in dbs_split:
                                    miar_db_type_terms = Term.query.filter_by(
                                        vocabulary_id=IrokoVocabularyIdentifiers.INDEXES.value).all()

                                    for miar in miar_db_type_terms:
                                        if miar.identifier.lower().strip() == dbs.lower().strip():
                                            # print("add {0}".format(dbs))
                                            to_add.append(miar)
                                for t in to_add:
                                    # print("----------- !! ADD a Clasfication {0}-{1}-{2}-{3}".format(t.uuid, t.description, t.vocabulary_id, t.parent_id))
                                    source.add_term(
                                        str(t.uuid),
                                        t.description,
                                        t.vocabulary_id,
                                        dict(
                                            url='', initial_cover='', end_cover=''
                                        )
                                    )
                                    # add also the parent, meaning the miar_groups
                                    if t.parent_id and t.parent_id != 0:
                                        parent = Term.query.filter_by(id=t.parent_id).first()
                                        # print("----------- !! ADD a parent {0}- {1}".format(parent.uuid, parent.description))
                                        source.add_term(
                                            str(parent.uuid),
                                            parent.description,
                                            parent.vocabulary_id,
                                            dict()
                                        )

                                # print('***********',source.model.json['classifications'])
                                source.update(data=source.model.json, dbcommit=True, reindex=True)
                                IrokoSourceVersions.new_version(
                                    source.id,
                                    source.model.json,
                                    user_id=get_default_user().id,
                                    comment='MIAR Classifications Update',
                                    is_current=True
                                )
                                # source.commit()

                        except Exception:
                            # print("issncount={0}".format(issncount))
                            # print("sourcecount={0}".format(sourcecount))
                            # print(traceback.format_exc())
                            continue
            except Exception as e:
                # print("issncount={0}".format(issncount))
                # print("sourcecount={0}".format(sourcecount))
                # print(traceback.format_exc())
                return None
            # print("issncount={0}".format(issncount))
            # print("sourcecount={0}".format(sourcecount))

        return 'success'

# {"title": "Agrotecnia de Cuba",
# "description":
# "Contiene art\u00edculos, editoriales, metodolog\u00eda, res\u00famenes de tesis y rese\u00f1as de los resultados de investigaciones cient\u00edficas y aplicadas en los campos de la sanidad vegetal y ciencias afines, con \u00e9nfasis en las tecnolog\u00edas que est\u00e1n listas para su generalizaci\u00f3n en la pr\u00e1ctica agraria.",
#     "url": "http://www.actaf.co.cu/agrotecnia-de-cuba.html",
#     "rnps": "2120",
#     "seriadas_cubanas": "http://www.seriadascubanas.cult.cu/publicaci%C3%B3n-seriada/agrotecnia-de-cuba-2",
#     "issn": {"p": "1816-8604"},
#     "terms": [{"id": 171, "data": null}, {"id": 1128, "data": null}, {"id": 1127, "data": null}, {"id": 270, "data": null}, {"id": 873, "data": {"url": "http://www.latindex.unam.mx/latindex/ficha?folio=20272"}}]}
