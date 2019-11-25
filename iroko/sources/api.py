

from sqlalchemy import and_, or_, not_
from iroko.sources.models import Source, TermSources, SourceStatus, SourceType, SourceVersion
from iroko.taxonomy.models import Term
from iroko.sources.marshmallow import source_schema_many, source_schema_full_many, SourceSchema
from invenio_db import db
from datetime import datetime

from iroko.sources.utils import issn_is_in_data, field_is_in_data, _no_params, _load_terms_tree, __load_term_children_id, _filter_data_args, _filter_repo_args


class Sources:
    """API for manipulation of Sources
    Considering SourceVersion: meanining this class use Source and SourceVersion model.
    """

    # Listar todas las fuentes dado un status...
    # Listar una fuente con sus versiones
    # saber si de una version con un status determinado tiene una nueva version que no es "current"

    @classmethod
    def get_sources(cls, and_op, terms, data_args, repo_args):
        """return Source array"""

        result = []
        all_terms = _load_terms_tree(terms)
        filter_terms = len(all_terms) > 0
        if filter_terms:
            sources = TermSources.query.filter(TermSources.term_id.in_(all_terms)).all()
        else:
            sources = Source.query.order_by('name').all()

        # TODO: esto se puede hacer mas eficientemente...
        for item in sources:
            source = item.source if filter_terms else item
            in_data = _filter_data_args(source, data_args, and_op)
            in_repo = _filter_repo_args(source, repo_args, and_op)
            if and_op and in_data and in_repo:
                result.append(source)
            else:
                if in_data or in_repo:
                    result.append(source)
        return result

    @classmethod
    def get_source_by_id(cls, id=None, uuid= None):
        if id is not None:
            return Source.query.filter_by(id=id).first()
        if uuid is not None:
            return Source.query.filter_by(uuid=uuid).first()

    @classmethod
    def count_sources(cls):
        return Source.query.count()

    @classmethod
    def check_source_exist(cls, data):
        """ comprobar que no exista otro Title,ISSN, RNPS o URL igual

            :returns: boolean, Source
        """
        title = data['title'] if 'title' is in data else ''
        issn = data['issn'] if 'issn' is in data else ''
        rnps = data['rnps'] if 'rnps' is in data else ''
        url = data['url'] if 'url' is in data else ''

        source = Source.query.filter_by(name=title).first()
        if source:
            return True, source

        result = []
        sources = Source.query.all()

        for item in sources:
            if not issn_is_in_data(item.data, issn, True):
                if not field_is_in_data(item.data, 'rnps', rnps, True):
                    if field_is_in_data(item.data, 'url', url, True):
                        return True, item
                else:
                    return True, item
            else:
                return True, item

        return False, None

    @classmethod
    def insert_new_source(cls, user, json_data, source_type=SourceType.JOURNAL, source_status=SourceStatus.TO_REVIEW):
        """Insert new Source and an associated SourceVersion
        """

        #FIXME
        user_id = 1

        msg = ''

        exist, source = cls.check_source_exist(json_data)

        if exist:
            msg = 'Source already exist id={0}'.format(source.id)
            return msg, None
        else:
            new_source = Source()
            new_source.name = json_data["title"] if "title" in json_data else ""
            new_source.source_type = source_type
            new_source.source_status = source_status
            new_source.data = json_data
            #print(new_source)
            db.session.add(new_source)
            db.session.flush()

            # user_id, source_id, comment, data, created_at, is_current
            new_source_version = SourceVersion()
            new_source_version.data = json_data
            new_source_version.created_at = datetime.now()
            new_source_version.is_current = True
            new_source_version.source_id = new_source.id
            new_source_version.comment = json_data["comment"] if "comment" in json_data else ""
            new_source_version.user_id = user_id

            db.session.add(new_source_version)
            db.session.commit()

            msg = 'New Source created id={0}'.format(new_source.id)
            return msg, new_source


    @classmethod
    def insert_new_source_version(cls, user, json_data, source_id, is_current:bool):
        """Insert new Source and an associated SourceVersion
        """

        #FIXME
        user_id = 1

        msg = ''

        source = Source.query.filter_by(id=source_id).first()

        if not source:
            msg = 'Source not exist'
            return msg, None
        else:
            # user_id, source_id, comment, data, created_at, is_current
            new_source_version = SourceVersion()
            new_source_version.data = json_data
            new_source_version.created_at = datetime.now()
            new_source_version.is_current = is_current
            new_source_version.source_id = source.id
            new_source_version.comment = json_data["comment"] if "comment" in json_data else ""
            new_source_version.user_id = user_id

            db.session.add(new_source_version)
            db.session.commit()

            msg = 'New SourceVersion created id={0}'.format(new_source_version.id)
            return msg, new_source_version





