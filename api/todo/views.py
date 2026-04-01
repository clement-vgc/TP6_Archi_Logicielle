from flask import jsonify, abort, make_response, request, url_for, redirect
from .app import app
from .models import (
    get_all_questionnaires, get_questionnaire_by_id, 
    create_questionnaire, delete_questionnaire
)


@app.route('/')
def api_root_redirect():
    return redirect(url_for('get_questionnaires'))

def make_public_questionnaire(quiz):
    new_quiz = {}
    quiz_data = quiz.to_json()
    for field in quiz_data:
        if field == 'id':
            new_quiz['id'] = quiz_data['id']
            new_quiz['uri'] = url_for('get_one_questionnaire', qid=quiz_data['id'], _external=True)
        else:
            new_quiz[field] = quiz_data[field]
    return new_quiz


def build_question_payload(data):
    question_type = data.get('type')
    if question_type not in ('ouverte', 'qcm'):
        return None

    payload = {
        'question_type': question_type,
        'bonnes_reponses': data.get('bonnes_reponses', []),
        'propositions': data.get('propositions', []),
    }

    if question_type == 'ouverte':
        if not isinstance(payload['bonnes_reponses'], list):
            return None
        if any(not isinstance(answer, str) for answer in payload['bonnes_reponses']):
            return None

    if question_type == 'qcm':
        if not isinstance(payload['propositions'], list):
            return None
        for prop in payload['propositions']:
            if not isinstance(prop, dict):
                return None
            if not isinstance(prop.get('text'), str):
                return None
            if not isinstance(prop.get('is_correct'), bool):
                return None

    return payload


def sanitize_open_answers(answers):
    return [a.strip() for a in answers if isinstance(a, str) and a.strip()]


def sanitize_qcm_choices(choices):
    clean_choices = []
    for choice in choices:
        text = choice.get('text', '').strip()
        if not text:
            continue
        clean_choices.append({
            'text': text,
            'is_correct': bool(choice.get('is_correct', False)),
        })
    return clean_choices


def validate_question_update_payload(question, data):
    update = {}

    if 'title' in data:
        if not isinstance(data['title'], str):
            return None
        update['title'] = data['title']

    if question.type == 'ouverte' and 'bonnes_reponses' in data:
        if not isinstance(data['bonnes_reponses'], list):
            return None
        if any(not isinstance(answer, str) for answer in data['bonnes_reponses']):
            return None
        update['bonnes_reponses'] = sanitize_open_answers(data['bonnes_reponses'])

    if question.type == 'qcm' and 'propositions' in data:
        if not isinstance(data['propositions'], list):
            return None
        for prop in data['propositions']:
            if not isinstance(prop, dict):
                return None
            if not isinstance(prop.get('text'), str):
                return None
            if not isinstance(prop.get('is_correct'), bool):
                return None
        update['propositions'] = sanitize_qcm_choices(data['propositions'])

    return update


def find_question_in_quiz(quiz, question_id):
    for index, question in enumerate(quiz.questions):
        if question.id == question_id:
            return index, question
    return None, None

@app.route('/quiz/api/v1.0/questionnaires', methods=['GET'])
def get_questionnaires():
    return jsonify({'questionnaires': [make_public_questionnaire(q) for q in get_all_questionnaires()]})

@app.route('/quiz/api/v1.0/questionnaires/<int:qid>', methods=['GET'])
def get_one_questionnaire(qid):
    q = get_questionnaire_by_id(qid)
    if q is None:
        abort(404)
    return jsonify({'questionnaire': make_public_questionnaire(q)})

@app.route('/quiz/api/v1.0/questionnaires', methods=['POST'])
def add_questionnaire():
    if not request.json or 'name' not in request.json:
        abort(400)
    new_q = create_questionnaire(request.json['name'])
    if new_q is None:
        return make_response(jsonify({'error': 'Ce nom de questionnaire existe déjà'}), 409)
    return jsonify({'questionnaire': make_public_questionnaire(new_q)}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/quiz/api/v1.0/questionnaires/<int:qid>', methods=['PUT'])
def update_questionnaire(qid):
    q = get_questionnaire_by_id(qid)
    if q is None:
        abort(404)
        
    if not request.json:
        abort(400)
        
    if 'name' in request.json and not isinstance(request.json['name'], str):
        abort(400)
        
    q.name = request.json.get('name', q.name)
    return jsonify({'questionnaire': make_public_questionnaire(q)})

@app.route('/quiz/api/v1.0/questionnaires/<int:qid>', methods=['DELETE'])
def remove_questionnaire(qid):
    q = get_questionnaire_by_id(qid)
    if q is None:
        abort(404)
    delete_questionnaire(qid)
    return jsonify({'status': 'deleted'})

@app.route('/quiz/api/v1.0/questionnaires/<int:qid>/questions', methods=['GET'])
def get_questions(qid):
    q = get_questionnaire_by_id(qid)
    if q is None:
        abort(404)
    return jsonify({'questions': [quest.to_json(i) for i, quest in enumerate(q.get_questions())]})

@app.route('/quiz/api/v1.0/questionnaires/<int:qid>/questions', methods=['POST'])
def add_question_to_quiz(qid):
    q = get_questionnaire_by_id(qid)
    if q is None:
        abort(404)
    if not request.json or 'title' not in request.json:
        abort(400)

    if not isinstance(request.json['title'], str):
        abort(400)

    payload = build_question_payload(request.json)
    if payload is None:
        abort(400)
    
    new_quest = q.add_question(
        request.json['title'],
        payload['question_type'],
        sanitize_open_answers(payload['bonnes_reponses']),
        sanitize_qcm_choices(payload['propositions']),
    )
    return jsonify({'question': new_quest.to_json(len(q.questions) - 1)}), 201


@app.route('/quiz/api/v1.0/questionnaires/<int:qid>/questions/<int:question_id>', methods=['GET'])
def get_one_question(qid, question_id):
    q = get_questionnaire_by_id(qid)
    if q is None:
        abort(404)

    index, question = find_question_in_quiz(q, question_id)
    if question is None:
        abort(404)

    return jsonify({'question': question.to_json(index)})


@app.route('/quiz/api/v1.0/questionnaires/<int:qid>/questions/<int:question_id>', methods=['PUT'])
def update_question(qid, question_id):
    q = get_questionnaire_by_id(qid)
    if q is None:
        abort(404)

    if not request.json:
        abort(400)

    index, question = find_question_in_quiz(q, question_id)
    if question is None:
        abort(404)

    update_data = validate_question_update_payload(question, request.json)
    if update_data is None:
        abort(400)

    if 'title' in update_data:
        question.title = update_data['title']

    if question.type == 'ouverte' and 'bonnes_reponses' in update_data:
        question.bonnes_reponses = update_data['bonnes_reponses']

    if question.type == 'qcm' and 'propositions' in update_data:
        question.propositions = update_data['propositions']

    return jsonify({'question': question.to_json(index)})

@app.route('/quiz/api/v1.0/questionnaires/<int:qid>/questions/<int:question_id>', methods=['DELETE'])
def remove_question(qid, question_id):
    q = get_questionnaire_by_id(qid)
    if q is None:
        abort(404)

    index, question = find_question_in_quiz(q, question_id)
    if question is None:
        abort(404)

    if q.delete_question(index) is None:
        abort(404)

    return jsonify({'status': 'deleted'})