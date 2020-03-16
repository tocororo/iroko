from iroko.harvester.html.issn import IssnHarvester
from flask import current_app


work_dir = current_app.config['HARVESTER_DATA_DIRECTORY']
issn_harvester = IssnHarvester(work_dir)