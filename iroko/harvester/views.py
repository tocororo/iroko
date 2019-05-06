
"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, request, render_template

from flask_login import login_required

from iroko.sources.models import Sources, HarvestType
from iroko.sources.marshmallow import sources_schema, sources_schema_full, source_schema_full

from .tasks import test_task

from os import listdir, path

blueprint = Blueprint(
    'iroko_harvester',
    __name__,
    template_folder='templates'
)

@blueprint.route('/sources')
@login_required
def view_sources():
    page = request.args.get('page')
    if not page or int(page) < 0:
        page=0
    limit = 10
    offset = int(page) * limit
    result = Sources.query.filter_by(harvest_type=HarvestType.OAI).limit(limit).offset(offset).all()
    sources = sources_schema.dump(result)

    prev_page = int(page) - 1
    next_page = int(page) + 1
    if prev_page < 0:
        prev_page=0
    if len(sources.data) < limit:
        next_page=int(page)

    return render_template('list-sources.html', sources=sources.data, prev_page= prev_page, next_page= next_page)

@blueprint.route('/sources/id/<id>')
@login_required
def view_source_id(id):
    src = Sources.query.filter_by(id=id).first()
    source = source_schema_full.dump(src)
    return render_template('source.html', source=source.data)

@blueprint.route('/harvest')
def harvest_task():
    source = {'id':"1", 'havest_endpoint': "http://192.168.56.6/index.php/cfores/oai"}
    job = test_task.delay(source)
    return render_template('harvest_task.html', jid=job.id)

@blueprint.route('/progress')
def task_progress():

    harvest_dir = path.join("data/harvester", "1")
    items = listdir(harvest_dir)
    result=[]  
    
    for item in items:
        idir=path.join(harvest_dir, item)
        if path.isdir(idir):
            result.append({'name':item, 'files':listdir(idir)})
    return render_template('task_progress.html',items=result, count=len(result))
