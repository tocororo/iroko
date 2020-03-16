from iroko.harvester.html.miar import MiarHarvester
from flask import current_app


work_dir = current_app.config['HARVESTER_DATA_DIRECTORY']
miar_harvester = MiarHarvester(work_dir)
