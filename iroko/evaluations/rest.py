# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

# Pasos para completar una NUEVA evaluacion desde CERO

# 0- Nueva evaluacion     (/new)   
#     - REQUEST: el frontend solicita un objeto de evaluacion dado un PID 
#       (ISSN principio, para las revistas) (stept 1)
#     - RESPONSE: El backend crea un nuevo objeto evaluacion, con state: initial 
#           y lo devuelve al frontend,
#          el objeto de evaluacion tiene un UUID 
#          el usuario que pidio la evaluacion
# 1- Respuestas del usuario/ solicitud de recomendaciones (/process/:uuid) 
#     - REQUEST: el frontent envia el objeto de evaluacion con las respuestas del usuario
#       (en el campo data)... dado que es un objeto de evaluacion concreto
#        un argumento de este endpoint debe ser el uuid de la evaluacion (stept 2)
#     - RESPONSE: el backend devuelve el objeto de evaluacion con las recomendaciones
#       y state: processing 
#       el backend comprueba que el usuario qeu esta haciendo esta peticion
#       es el duenno de la evaluacion
#       el backend comprueba que el estado de la evaluacion es inicial      
# 2- Guardar evaluacion   (/save/:uuid)
#     - REQUEST: el frontend envia la sennal de guardar la evaluacion 
#     - RESPONSE: el backend pone la evaluacion en finished y devuelve ok. 
#       el backend comprueba que el usuario qeu esta haciendo esta peticion
#       es el duenno de la evaluacion
#

# Pasos para completar una NUEVA evaluacion desde otra ya realizada. 
 
# 0- Clonar evaluacion (/clone/:uuid)
#     Igual que el /new pero adicionando el uuid de la evaluacion que se clonna
#      lo otro pasos son iguales. 
# 

"""Iroko evaluations api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, request
from flask_login import current_user
from invenio_oauth2server import require_api_auth

from iroko.evaluations.api import Evaluations
from iroko.evaluations.marshmallow import evaluation_schema, evaluation_schema_many
from iroko.evaluations.models import Evaluation
from iroko.evaluations.permissions import evaluation_viewed_permission_factory
from iroko.utils import IrokoResponseStatus, iroko_json_response

api_blueprint = Blueprint(
    'iroko_api_evaluations',
    __name__,
    url_prefix='/evaluation'
    )


@api_blueprint.route('/list')
# @require_api_auth()
def get_evaluations():
    try:
        """
        List all evaluations.
        """
        count = int(request.args.get('size')) if request.args.get('size') else 10
        page = int(request.args.get('page')) if request.args.get('page') else 1

        if page < 1:
            page = 1
        offset = count * (page - 1)
        limit = offset + count

        result = Evaluation.query.all()
        total = len(result)

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            'ok', 'evaluations', \
            {
                'data': evaluation_schema_many.dump(result[offset:limit]),
                'total': total
                }
            )
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/<id>', methods=['GET'])
# @require_api_auth()
def get_evaluation(id):

    '''
        Get the evaluation with the given id.

        param1: The id of the evaluation.
    '''

    try:
        user = None

        msg, evaluation = Evaluations.get_evaluation(id)
        if not evaluation:
            raise Exception('Evaluation not found')

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            msg, 'evaluation', \
            evaluation_schema.dump(evaluation)
            )
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/reciever/<user_id>', methods=['GET'])
# @require_api_auth()
def get_user_evaluations(user_id):

    '''
        Get the evaluations corresponding with a specific user.

        param1: The id of the user.
    '''

    try:
        user = None

        msg, evaluation = Evaluations.get_user_evaluations(user_id)
        if not evaluation:
            raise Exception('Evaluation not found')

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            msg, 'evaluation', \
            evaluation_schema_many.dump(evaluation)
            )
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


# TODO: Need authentication
@api_blueprint.route('/new', methods=['POST'])
# @require_api_auth()
def new_evaluation():

    '''
        Create a new template for make a evaluation.
    '''

    # FIXME: get the user is trying to perform this action!!!!
    try:
        user = None

        #if not request.is_json:
        #    raise Exception('No JSON data provided')

        input_data = request.json
        evaluation = Evaluations.build_evaluation_object(input_data)

        if not evaluation:
            raise Exception("Error building the evaluation json")

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            'ok', 'evaluation', \
            evaluation
            )

    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
