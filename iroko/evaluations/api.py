#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from typing import Dict

from invenio_access.models import ActionUsers
from invenio_accounts.models import User
from invenio_db import db

from iroko.evaluations.marshmallow import evaluation_schema
from iroko.evaluations.models import Evaluation
import yaml
import json


class Evaluations:
    '''Manage Evaluations'''

    @classmethod
    def get_evaluation(cls, id) -> Dict[str, Evaluation]:

        '''
            Obtain an evaluation from an id

            param1: The id of the evaluation

            return: The evaluation that matches with the given id
        '''

        eval = Evaluation.query.filter_by(id=id).first()
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

        evaluations = Evaluation.query.filter_by(user_id = user_id).all()

        if evaluations:
            return 'ok', evaluations

        else:
            msg = 'User {0} does not have any evaluation'
            return msg, None

    def get_question(cls, id: str):
        
        '''
            Obtain an specific methodology question.

            param1: The id of the question.

            return: A dictionary that contains the question info 

        '''

        with open("methodologies/journal/questions.es.yml", 'r') as stream:
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

        with open("methodologies/journal/recomendations.es.yml", 'r') as stream:
            recomendations = yaml.safe_load(stream)
            for recomendation in recomendations:
                if id == recomendation['id']:
                    return recomendation

    @classmethod
    def build_evaluation_object(cls, journal_id: str, user_id: str):

        '''
            Create a formulary for an evaluation.

            param1: The id of the journal to evaluate.
            param2: The id of the user that makes the evaluation.

            return: the json that represent the formulary data
        '''

        result = dict()
        with open("methodologies/journal/methodology.es.yml", 'r') as stream:
            result = yaml.safe_load(stream)
            result['user'] = user_id
            # TODO: fill global fields 
            for section in result['sections']:
                for category in section['categories']:
                    new_questions = []
                    for question in category['questions']:
                        print(question['id'])
                        q = cls.get_question(question['id'])
                        q['answer'] = ''
                        new_questions.append(q)
                    category['questionsOrRecoms'] = new_questions
                    del category['questions']
        json_object = json.dumps(result, indent = 4) 
        print(json_object)


    # @classmethod
    # def edit_evaluation(cls, id, data) -> Dict[str, Evaluation]:

    #     msg, notif = cls.get_evaluation(id)
    #     if notif:
    #         valid_data = evaluation_schema.load(data)
    #         if valid_data:
    #             notif.classification = valid_data['classification']
    #             notif.description = valid_data['description']
    #             notif.emiter = valid_data['emiter']
    #             notif.data = valid_data['data']
# 
    #             if not notif.receiver_id == valid_data['receiver_id']:
    #                 # deny al que estaba notif.receiver_id
    #                 cls.deny_evaluation_viewed_permission(notif.receiver_id, notif.id)
    #                 # grant al nuevo valid_data['receiver_id']
    #                 cls.grant_evaluation_viewed_permission(valid_data['receiver_id'], notif.id)
    #             notif.receiver_id = valid_data['receiver_id']
    #             db.session.commit()
    #             msg = 'New Evaluation UPDATED classification={0}'.format(notif.classification)
    #         else:
    #             msg = 'errors'
    #             notif = None
    #     return msg, notif

    @classmethod
    def new_evaluation(cls, data) -> Dict[str, Evaluation]:

        '''
            Create a new instace of Evaluation

            param1: A json with the data to fill the Evaluation fields

            return The create instance and the status of the process
        '''

        eval_data = evaluation_schema.load(data)

        if eval_data:

            evaluation = Evaluation()
            evaluation.data = eval_data['data']
            evaluation.datetime = eval_data['datetime']
            evaluation.notes = eval_data['notes']
            evaluation.state = eval_data['state']
            evaluation.user_id = eval_data['user_id']

            # TODO save the new evaluation instance
        
        else:
            msg = 'Invalid data'
            evaluation = None

        return msg, evaluation

    # @classmethod
    # def new_evaluation(cls, data) -> Dict[str, Evaluation]:

    #     notif_data = evaluation_schema.load(data)
    #     if notif_data:
    #         notif = Evaluation()
    #         notif.classification = notif_data['classification']
    #         notif.description = notif_data['description']
    #         notif.receiver_id = notif_data['receiver_id']
    #         notif.emiter = notif_data['emiter']
    #         notif.data = notif_data['data']
    #         db.session.add(notif)

    #         db.session.flush()
    #         cls.grant_evaluation_viewed_permission(notif.receiver_id, notif.id)
    #         db.session.commit()

    #         msg = 'New Evaluation CREATED classification={0}'.format(notif.classification)
    #     else:
    #         msg = 'Invalid data'
    #         notif = None
    #     return msg, notif

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
