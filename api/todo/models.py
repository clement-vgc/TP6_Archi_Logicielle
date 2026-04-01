questionnaires = []
next_questionnaire_id = 1
next_question_id = 1


class Question:
    def __init__(self, title):
        global next_question_id
        self.id = next_question_id
        self.title = title
        next_question_id += 1

    def to_json(self, index):
        return {
            'id': self.id,
            'number': index,
            'title': self.title,
            'type': self.type,
        }


class QuestionOuverte(Question):
    def __init__(self, title, bonnes_reponses=None):
        super().__init__(title)
        self.type = "ouverte"
        self.bonnes_reponses = bonnes_reponses or []

    def to_json(self, index):
        json_data = super().to_json(index)
        json_data['bonnes_reponses'] = self.bonnes_reponses
        return json_data


class QuestionQCM(Question):
    def __init__(self, title, propositions=None):
        super().__init__(title)
        self.type = "qcm"
        self.propositions = propositions or []

    def to_json(self, index):
        json_data = super().to_json(index)
        json_data['propositions'] = self.propositions
        return json_data


class Questionnaire:
    def __init__(self, name):
        global next_questionnaire_id
        self.id = next_questionnaire_id
        self.name = name
        self.questions = []
        next_questionnaire_id += 1

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'questions': [q.to_json(i) for i, q in enumerate(self.questions)],
        }

    def add_question(
        self,
        title,
        question_type="ouverte",
        bonnes_reponses=None,
        propositions=None,
    ):
        if question_type == "ouverte":
            new_q = QuestionOuverte(title, bonnes_reponses)
        elif question_type == "qcm":
            new_q = QuestionQCM(title, propositions)
        else:
            return None

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