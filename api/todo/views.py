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
    
    new_quest = q.add_question(request.json['title'])
    return jsonify({'question': new_quest.to_json(len(q.questions) - 1)}), 201

@app.route('/quiz/api/v1.0/questionnaires/<int:qid>/questions/<int:index>', methods=['DELETE'])
def remove_question(qid, index):
    q = get_questionnaire_by_id(qid)
    if q is None:
        abort(404)
    if q.delete_question(index) is None:
        abort(404)
    return jsonify({'status': 'deleted'})