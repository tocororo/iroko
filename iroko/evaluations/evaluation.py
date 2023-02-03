
import yaml
import json 


def get_question(id: str):
    
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

def get_recomendation(id: str):
    
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


def build_evaluation_object(journal_id: str, user_id: str):

    '''
        Create a formulary for an evaluation.

        param1: The id of the journal to evaluate.
        param2: The id of the user that makes the evaluation.
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
                    q = get_question(question['id'])
                    q['answer'] = ''
                    new_questions.append(q)
                category['questionsOrRecoms'] = new_questions
                del category['questions']
    json_object = json.dumps(result, indent = 4) 
    print(json_object)


def apply_rules(json_formulary : json):
    # TODO aplicar todas las reglas necesarias y devolver el json con las recomendaciones
    pass




build_evaluation_object("333333", "44444444")


