questionnaires = []
next_id = 1 

class Question:
    def __init__(self, title):
        self.title = title

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    
class Questionnaire:
    def __init__(self, name):
        global next_id
        self.id = next_id
        self.name = name
        self.questions = []
        next_id += 1

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'questions': [q.to_json(i) for i, q in enumerate(self.questions)] 
        }

    def add_question(self, title):
        new_q = Question(title)
        self.questions.append(new_q)
        return new_q

    def get_questions(self):
        return self.questions

    def delete_question(self, index):
        if 0 <= index < len(self.questions):
            return self.questions.pop(index)
        return None


def get_all_questionnaires():
    return questionnaires

def get_questionnaire_by_id(qid):
    for q in questionnaires:
        if q.id == qid:
            return q
    return None

def get_questionnaires_by_name(name):
    for q in questionnaires:
        if q.name.lower() == name.lower():
            return q
    return None

def create_questionnaire(name):
    if get_questionnaires_by_name(name):
        return None
        
    new_q = Questionnaire(name)
    questionnaires.append(new_q)
    return new_q

def delete_questionnaire(qid):
    global questionnaires
    questionnaires = [q for q in questionnaires if q.id != qid]

create_questionnaire("français")
create_questionnaire("géo")