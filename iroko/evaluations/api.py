#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

import os
from copy import deepcopy
from datetime import datetime
from typing import Dict

import yaml
from flask import current_app
from invenio_db import db

from iroko.evaluations.models import Evaluation, EvaluationState
from iroko.evaluations.rules import evaluate_journal


# TODO comprobar que el usuario sea el autor de la evaluacion en cada operacion

class Evaluations:
    '''Manage Evaluations'''

    @classmethod
    def get_evaluation(cls, id):

        '''
            Obtain an evaluation from an id

            param1: The id of the evaluation

            return: The evaluation that matches with the given id
        '''
        eval = Evaluation.query.filter_by(uuid=id).first()
        if eval:
            return 'ok', eval
        else:
            msg = 'Evaluation not exist id={0}'.format(id)
            return msg, None

    @classmethod
    def get_user_evaluations(cls, user_id):

        '''
            Obtain the evaluations from an user

            param1: The id of the user

            return: The evaluation from the given user
        '''

        evaluations = Evaluation.query.filter(Evaluation.user_id == user_id,
                                              Evaluation.entity_id_value != '').all()

        if evaluations:
            return 'ok', evaluations

        else:
            msg = 'User {0} does not have any evaluation'
            return msg, None

    @classmethod
    def clone_evaluation(cls, uuid, user_id):

        original_evaluation = Evaluation.query.filter_by(uuid=uuid).first()

        if original_evaluation:

            new_evaluation = Evaluation()
            temp = deepcopy(original_evaluation.data)
            new_evaluation.data = temp
            new_evaluation.datetime = datetime.now()
            new_evaluation.state = EvaluationState.START
            new_evaluation.user_id = user_id

            db.session.add(new_evaluation)
            db.session.flush()
            db.session.commit()

            return 'ok', new_evaluation
        else:
            msg = 'Evaluation not exist id={0}'.format(id)
            return msg, None

    def get_question(cls, id: str):

        '''
            Obtain an specific methodology question.

            param1: The id of the question.

            return: A dictionary that contains the question info

        '''

        file_path = os.path.join(
            current_app.config["IROKO_METHODOLOGIES_DIR"],\
            "journal/questions.es.yml")
        with open(file_path, 'r') as stream:
            questions = yaml.safe_load(stream)
            for question in questions:
                if id == question['id']:
                    return question

    def get_recomendation(cls, id: str):

        '''
            Obtain an specific methodology recomendation.

            param1: The id of the recomendation.

            return: A dictionary that contains the recomendation info

        '''
        file_path = os.path.join(
            current_app.config["IROKO_METHODOLOGIES_DIR"],\
            "journal/recomendations.es.yml")
        with open(file_path, 'r') as stream:
            recomendations = yaml.safe_load(stream)
            for recomendation in recomendations:
                if id == recomendation['id']:
                    return recomendation

    @classmethod
    def build_evaluation_object(cls, user_id):

        '''
            Create a formulary for an evaluation.

            param1: Json with the data needed: the journal_id, user_id (language?)

            return: the json that represent the formulary data
        '''
        result = dict()
        file_path = os.path.join(
            current_app.config["IROKO_METHODOLOGIES_DIR"],
            "journal/methodology.es.yml")
        print("------", file_path)
        with open(file_path, 'r') as stream:

            result = yaml.safe_load(stream)
            result['user'] = user_id

            result['journalData'] = result['entity']
            result['journalData']['id'] = None
            result['journalData']['name'] = None
            result['journalData']['issn'] = None
            result['journalData']['url'] = None
            del result['entity']

            for section in result['sections']:
                for category in section['categories']:
                    new_questions = []
                    for question in category['questions']:
                        q = cls.get_question(cls, question['id'])
                        # q['answer'] = None
                        new_questions.append(q)
                    category['questionsOrRecoms'] = new_questions
                    del category['questions']
        #json_object = json.dumps(result, indent = 4)

        return result

    @classmethod
    def new_evaluation(cls, data, user_id) -> Dict[str, Evaluation]:

        '''
            Create a new instace of Evaluation

            param1: A json with the data to fill the Evaluation fields

            return The create instance and the status of the process
        '''

        if data:

            evaluation = Evaluation()
            evaluation.data = data
            evaluation.datetime = datetime.now()
            evaluation.state = EvaluationState.START
            evaluation.user_id = user_id

            # TODO ver bien como llenar estos campos, de momento vacios
            evaluation.entity_name = ""
            evaluation.entity_type = ""
            evaluation.entity_id_type = ""
            evaluation.entity_id_value = ""

            evaluation.methodology_name = ""
            evaluation.methodology_schema = ""

            db.session.add(evaluation)
            db.session.flush()
            db.session.commit()

            msg = "New Evaluation Created"

        else:
            msg = 'Invalid data'
            evaluation = None

        return msg, evaluation

    @classmethod
    def make_recoms(cls):

        result = dict()

        file_path = os.path.join(
            current_app.config["IROKO_METHODOLOGIES_DIR"], \
            "journal/results.es.yml")
        with open(file_path, 'r') as stream:
            result = yaml.safe_load(stream)

        return result

    @classmethod
    def build_recoms(cls, json_data):

        result = dict()
        file_path = os.path.join(
            current_app.config["IROKO_METHODOLOGIES_DIR"], \
            "journal/results.es.yml")
        with open(file_path, 'r') as stream:
            result = yaml.safe_load(stream)
            # result['user'] = json_data['user_id']

            values = []
            for sec in json_data['sections']:
                for category in sec['categories']:
                    for question in category['questionsOrRecoms']:

                        values.append(question['answer'])

            evaluate_journal(result, values)

        return result

    @classmethod
    def fillInitialInfo(cls, data):

        evaluation = None

        if data:

            try:
                msg, evaluation = cls.get_evaluation(data['uuid'])

                temp = deepcopy(evaluation.data)
                temp['journalData']['issn'] = data['issn']
                temp['journalData']['name'] = data['name']
                temp['journalData']['url'] = data['url']
                evaluation.entity_name = data['name']
                # TODO en un futuro esta info se obtendria de otra forma
                evaluation.entity_id_value = data['issn']
                evaluation.entity_type = "Journal"
                evaluation.state = EvaluationState.INITIAL
                evaluation.data = temp

                db.session.commit()

            except Exception as e:
                msg = str(e)

        else:
            msg = 'Invalid Data'
            evaluation = None

        return msg, evaluation

    @classmethod
    def process_evalaution(cls, data, user_id):

        if data:
            try:
                msg, evaluation = cls.get_evaluation(data['uuid'])
                if evaluation is None:
                    msg = "The evaluation does not exist"
                    return msg, None

                if evaluation.state != EvaluationState.INITIAL and evaluation.state != EvaluationState.PROCESSING:

                    msg = "Is not an Initial or Processing Evalaution"
                    return msg, evaluation

                if evaluation.user_id != user_id:

                    msg = "The current user is not the author of the evaluation"
                    return msg, evaluation

                evaluation.state = EvaluationState.PROCESSING

                for sec in evaluation.data['sections']:
                    for category in sec['categories']:
                        for question in category['questionsOrRecoms']:
                            question['answer'] = data['sections'][question['id']]

                recom = cls.build_recoms(evaluation.data)
                temp = deepcopy(evaluation.data)
                temp['resultAndRecoms']= recom

                # TODO en un futuro esta info se obtendria de otra forma
                evaluation.methodology_name = "sceiba-journal"


                evaluation.data = temp
                db.session.commit()

            except Exception as e:
                msg = str(e)

        else:
            msg = 'Invalid Data'
            evaluation = None

        return msg, evaluation

    @classmethod
    def complete_evaluation(cls, uuid, user_id):

        msg, evaluation = cls.get_evaluation(uuid)
        print(user_id)
        print(evaluation.user_id)

        if evaluation.user_id != user_id:

            msg = "The current user is not the author of the evaluation"
            return msg, evaluation

        if evaluation.state != EvaluationState.PROCESSING:

            msg = "Is not a processing evaluation"
            return msg, evaluation

        evaluation.state = EvaluationState.FINISH

        db.session.flush()
        db.session.commit()

        return "ok", evaluation

    # @classmethod
    # def grant_evaluation_editor_permission(cls, user_id, evaluation_id) -> Dict[str, bool]:
    #     done = False
    #     msg = ''
    #     try:
    #         evaluation = Evaluation.query.filter_by(id=evaluation_id).first()
    #         user = User.query.filter_by(id=user_id)
    #         if not evaluation:
    #             msg = 'Evaluation not found'
    #         elif not user:
    #             msg = 'User not found'
    #         else:
    #             db.session.add(ActionUsers.allow(ObjectEvaluationEditor(evaluation.id),
    #             user=user))
    #             if not evaluation.data:
    #                 evaluation.data = {'editor':[user.id]}
    #             else:
    #                 evaluation.data['editor'].append(user.id)

    #             db.session.commit()
    #             msg = 'Editor Permission granted over {0}'.format(evaluation.name)
    #             done = True

    #     except Exception as e:
    #         msg = str(e)
    #         # print(str(e))

    #     return msg, done

    # @classmethod
    # def deny_evaluation_viewed_permission(user_id, evaluation_id) -> Dict[str, bool]:
    #     done = False
    #     msg = ''
    #     try:
    #         evaluation = Evaluation.query.filter_by(id=evaluation_id).first()
    #         user = User.query.filter_by(id=user_id)
    #         if not evaluation:
    #             msg = 'Evaluation not found'
    #         elif not user:
    #             msg = 'User not found'
    #         else:
    #             db.session.add(
    #                 ActionUsers.deny(ObjectEvaluationEditor(evaluation.id), user=user)
    #                 )

    #             db.session.commit()
    #             msg = 'Mark as viewed Permission granted '
    #             done = True

    #     except Exception as e:
    #         # print(str(e))
    #         msg = str(e)

    #     return msg, done

    # @classmethod
    # def check_user_evaluation_editor_permission(user_id, evaluation_id)-> Dict[str, bool]:
    #     done = False
    #     msg = ''
    #     try:
    #         evaluation = Evaluation.query.filter_by(id=evaluation_id).first()
    #         user = User.query.filter_by(id=user_id)
    #         user_identity = get_identity(user)
    #         permission = Permission(ObjectEvaluationEditor(evaluation.id))
    #         done = permission.allows(user_identity)
    #     except Exception as e:
    #         msg = str(e)
    #         # print(str(e))

    #     return msg, done

    # @classmethod
    # def grant_evaluation_viewed_permission(cls, user_id, evaluation_id, is_flush=True) -> Dict[
    #     str, bool]:
    #     done = False
    #     msg = ''
    #     try:
    #         user = User.query.filter_by(id=user_id)
    #         if not user:
    #             msg = 'User not found'
    #         else:
    #             db.session.add(
    #                 ActionUsers.allow(ObjectEvaluationEditor(evaluation_id), user=user)
    #                 )
    #             if is_flush:
    #                 db.session.flush()
    #             else:
    #                 db.session.commit()
    #             msg = 'Evaluation marking viewed Permission granted '
    #             done = True

    #     except Exception as e:
    #         msg = str(e)
    #         # print(str(e))

    #     return msg, done
