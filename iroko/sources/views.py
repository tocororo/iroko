
"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, current_app, jsonify, request, json, render_template, flash, url_for, redirect
from flask_login import login_required
from iroko.utils import iroko_json_response, IrokoResponseStatus
from iroko.sources.marshmallow import source_schema_full_many, source_schema_full, journal_schema, JournalSchema
from iroko.sources.models import Source, SourceVersion, SourcesType, SourceStatus
from marshmallow import ValidationError
from iroko.sources.api import Sources
from invenio_i18n.selectors import get_locale
from .forms import InclusionForm
from flask_babelex import lazy_gettext as _
import json
#from iroko.utils import mail
from flask_mail import Message
import unicodedata
import re
import random
from datetime import datetime


blueprint = Blueprint(
    'iroko_sources',
    __name__,
    url_prefix='/iroko-sources',
    template_folder='templates',
    static_folder='static',
)


api_blueprint = Blueprint(
    'iroko_api_sources',
    __name__,
)


@api_blueprint.route('/sources')
def get_sources():
    """List all sources with filters in parameters"""
    # TODO: document this!!!
    
    and_op = True if request.args.get('op') and request.args.get('op') == 'and' else False

    count = int(request.args.get('count')) if request.args.get('count') else 10
    page = int(request.args.get('page')) if request.args.get('page') else 0

    limit = count
    offset = count*page

    tids = request.args.get('terms')
    terms = []
    if tids:
        tids= tids.split(',')
        term_op = tids[0]
        if tids[0].lower() == 'and' or tids[0].lower() == 'or':
            del tids[0]
        terms = tids

    repo_args = {
        'harvest_type' : str(request.args.get('harvest_type')),
        'has_harvest_endpoint': str(request.args.get('has_harvest_endpoint')),
        'harvest_status': str(request.args.get('harvest_status'))
    }
    data_args = {
        'title' : str(request.args.get('title')),
        'description': str(request.args.get('description')),
        'url': str(request.args.get('url')),
        'issn': str(request.args.get('issn')),
        'rnps': str(request.args.get('rnps')),
        'year_start': str(request.args.get('year_start')),
        'year_end': str(request.args.get('year_end'))
    }

    result = Sources.get_sources(and_op, terms, data_args, repo_args)
    if result is not None:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': source_schema_full_many.dump(result[offset:offset+limit]).data,\
                         'count': len(result)})
    return iroko_json_response(IrokoResponseStatus.NOT_FOUND, 'Sources not found', None, {'count': 0})


@api_blueprint.route('/sources/count')
def get_sources_count():
    """return sources count"""

    result = Sources.count_sources()
    return iroko_json_response(IrokoResponseStatus.SUCCESS, 'ok','count', result)


@api_blueprint.route('/source/id/<id>')
def get_source_by_id(id):
    """Get a source by ID"""

    src = Sources.get_source_by_id(id=id)
    return jsonify_source(src)


@api_blueprint.route('/source/uuid/<uuid>')
def get_source_by_uuid(uuid):
    """Get a source by UUID"""

    src = Sources.get_source_by_id(uuid=uuid)
    return jsonify_source(src)


#TODO: Necesita autenticacion.
@api_blueprint.route('/source/new', methods=['POST'])
def source_new(id):

    created_at = datetime.now()
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    # json_data has several key: 
    #       token for user accounts managment, 
    #       data with field of the new source version
    #       type for the type of source: journal, repository
    #       comment for the version of the source
    # 
    if "type" not in json_data:
        return {"message": "Not source type provided"}, 412    

    if json_data["type"] is SourcesType.JOURNAL:
        try:
            data = journal_schema.loads(json_data["data"])
        except ValidationError as err:
            return err.messages, 422
        issn = rnps = url = None
        if "issn" in data: 
            issn = data["issn"]
        if "rnps" in data:
            rnps = data["rnps"]
        if "url" in data:
            url = data["url"]
        if not issn and not rnps and not url:
            return {"message": "Source need issn, or rnps, or url in order to identify it self"}, 412

        if len(Sources.sources_existences(issn, rnps, url)) > 0:
            return {"message": "Source already exist"}, 412  

        new_source = Source()
        new_source.name = data["title"] if "title" in data else ""
        new_source.source_type = SourcesType.JOURNAL
        new_source.source_status = SourceStatus.TO_REVIEW
        new_source.data = data
        #print(new_source)
        db.session.add(new_source)
        db.session.flush()

        # user_id, source_id, comment, data, created_at, is_current
        new_source_version = SourceVersion()
        new_source_version.data = data
        new_source_version.created_at = created_at
        new_source_version.is_current = True
        new_source_version.source_id = new_source.id
        new_source_version.comment = json_data["comment"] if "comment" in json_data else ""

        db.session.add(new_source_version)
        db.session.commit()

        return {"message": "Created source and sourve version"}, 201
    else:
        return {"message": "No journal type provided, other types are not implemented yet"}, 501

    # Crear un Source y un SourceVersion que tienen el mismo Data. 
    # comprobar que no exista otro ISSN, RNPS o URL igual, sino da error
    # source_status = REview
    # supuestamente en source.data.terms vienen los terminos relacionados y eso hay que reflejarlo en la tabla TermSources
    # Aqui no se trata la parte que tiene en ver con repo!!!!



#TODO: Necesita autenticacion.
@api_blueprint.route('/source/<id>/new-version', methods=['GET', 'POST'])
def source_new_version(id):
    
    # inserta un nuevo sourceVersion de un source que ya existe
    # hay que comprobar que el usuario que inserta, es quien creo el source (el que tiene el sourceversion mas antiguo) o un usuario con el role para crear cualquier tipo de versiones.
    src = Sources.get_source_by_id(id=id)
    created_at = datetime.now()


#TODO: Necesita autenticacion.
@api_blueprint.route('/source/<id>/current', methods=['GET', 'POST'])
def source_version_set_current(id):

    # pone un sourceVersion como current version en source y recibe tambien el estatus para el source
    # comprobar que el usuario tiene el role para hacer esto. 

    src = Sources.get_source_by_id(id=id)



def jsonify_source(src):
    if src:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','sources', \
                            {'data': source_schema_full.dump(src).data,\
                             'count': 1})
    return iroko_json_response(IrokoResponseStatus.NOT_FOUND, 'Sources not found', None, None)


@blueprint.route('/inclusions', methods=['GET', 'POST'])
@login_required
def inclusions():
    inclusions = {}
    with open(current_app.config['INIT_STATIC_JSON_PATH']+'/inclusions.json') as file:
        inclusions = json.load(file) 
    rejections = {}
    with open(current_app.config['INIT_STATIC_JSON_PATH']+'/rejected_inclusions.json') as file:
        rejections = json.load(file)  
    accepted = {}
    with open(current_app.config['INIT_STATIC_JSON_PATH']+'/accepted_inclusions.json') as file:
        accepted = json.load(file)  

    return render_template('inclusions.html', 
                            inclusions=inclusions, 
                            rejections=rejections,
                            accepted=accepted)


@blueprint.route('/inclusions/del/<string:key>', methods=['GET', 'POST'])
@login_required
def delete_inclusion(key):
    inclusions = {}
    with open(current_app.config['INIT_STATIC_JSON_PATH']+'/inclusions.json') as file:
        inclusions = json.load(file)  
    
    rejections = {}
    with open(current_app.config['INIT_STATIC_JSON_PATH']+'/rejected_inclusions.json') as file:
        rejections = json.load(file)     
    
    rejections[key] = inclusions[key]
    del inclusions[key]
    
    with open(current_app.config['INIT_STATIC_JSON_PATH']+'/inclusions.json', 'w') as file:
        json.dump(inclusions, file, indent=4)
    with open(current_app.config['INIT_STATIC_JSON_PATH']+'/rejected_inclusions.json', 'w') as file:
        json.dump(rejections, file, indent=4)

    return redirect(url_for('iroko_sources.inclusions'))



@blueprint.route('/inclusions/acept/<string:key>', methods=['GET', 'POST'])
@login_required
def acept_inclusion(key):
    inclusions = {}
    with open(current_app.config['INIT_STATIC_JSON_PATH']+'/inclusions.json') as file:
        inclusions = json.load(file)  
    
    accepted = {}
    with open(current_app.config['INIT_STATIC_JSON_PATH']+'/accepted_inclusions.json') as file:
        accepted = json.load(file)     
    
    accepted[key] = inclusions[key]
    del inclusions[key]
    
    with open(current_app.config['INIT_STATIC_JSON_PATH']+'/inclusions.json', 'w') as file:
        json.dump(inclusions, file, indent=4)
    with open(current_app.config['INIT_STATIC_JSON_PATH']+'/accepted_inclusions.json', 'w') as file:
        json.dump(accepted, file, indent=4)

    return redirect(url_for('iroko_sources.inclusions'))


@blueprint.route('/inclusions/new', methods=['GET', 'POST'])
@login_required
def new_inclusion():
    """The create view."""
    form = InclusionForm()
    # if the form is submitted and valid
    if form.validate_on_submit(): 
        body_text = form.source.data + ' ask for being part of Sceiba with OAI: ' + form.homepage_url.data
        body_text += ' Process started by ' + form.contact_name.data + ', Email: ' + form.contact_email.data
        
        # fichero=open(current_app.config['INIT_STATIC_JSON_PATH']+'/inclusions/'+form.source.data+'.txt','w')
        # fichero.write(body_text) 
        # fichero.close()

        inclusions = {}
        with open(current_app.config['INIT_STATIC_JSON_PATH']+'/inclusions.json') as file:
            inclusions = json.load(file)   

        if form.source.data in inclusions:       
            raise Exception(_('That source already have an entry for a new inclusion in Sceiba'))    

        requeriments = {}
        with open(current_app.config['INIT_STATIC_JSON_PATH']+'/'+get_locale()+ '/inclusion_requeriments.json') as file:
            requeriments = json.load(file)        

        data = {}
        data["source"] = form.source.data
        data["url"] = form.homepage_url.data
        data["contact"] = form.contact_name.data
        data["email"] = form.contact_email.data
        data["date"] = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")        
        data["requeriments"] = [] 
        for item in form.requeriments.data:
            data["requeriments"].append(requeriments[item])
        
        inclusions[form.source.data] = data

        with open(current_app.config['INIT_STATIC_JSON_PATH']+'/inclusions.json', 'w') as file:
            json.dump(inclusions, file, indent=4)

        # body_text += '\n' + _("Inclusion Requeriments: ") + '\n'
        # for item in form.requeriments.data:
        #     body_text += requeriments[item] + '\n' 
        # print(body_text)

        # msg = Message(_("Inclusion message"),
        #           sender=current_app.config["MAIL_DEFAULT_SENDER"],
        #           recipients=["eduardo.arencibia@upr.edu.cu", current_app.config["MAIL_DEFAULT_SENDER"]], 
        #           body=body_text)
        # current_app.extensions['mail'].send(msg)
        
        flash(_('Inclusion procees started'), 'info')
        return redirect(url_for('iroko_theme.index'))

    return render_template('new_inclusion.html', form=form)