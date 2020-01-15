from flask import request, jsonify

from db import init_db, Quiz, db, app, Question

app = app


@app.route("/api/quiz/<quiz_id>", methods=["GET"])
def get_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if quiz:
        return jsonify(quiz.to_dict())
    else:
        return "", 404


@app.route("/api/quiz/", methods=["POST"])
def post_quiz():
    try:
        data = request.get_json()
        quiz = Quiz()
        quiz.name = data['name']
        quiz.description = data['description']
        db.session.add(quiz)
        db.session.commit()
        return jsonify(quiz.to_dict()), 201
    except:
        response = {
            "status": "failure",
            "reason": "Failed to add in DB"
        }
        return jsonify(response), 400


@app.route("/api/questions/<question_id>", methods=["GET"])
def get_question(question_id):
    question = Question.query.get(question_id)
    if question:
        return jsonify(question.to_dict())
    else:
        return "", 404


@app.route("/api/questions/", methods=["POST"])
def post_question():
    try:
        data = request.get_json()
        question = Question()
        question.name = data['name']
        question.options = data['options']
        question.correct_option = data['correct_option']
        question.quiz = int(data['quiz'])
        question.points = int(data['points'])
        db.session.add(question)
        db.session.commit()
        return jsonify(question.to_dict()), 201
    except:
        response = {
            "status": "failure",
            "reason": "Failed to add in DB"
        }
        return jsonify(response), 400


@app.route("/api/quiz-questions/<quiz_id>", methods=["GET"])
def get_quiz_questions(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return "", 404
    data = quiz.to_dict()
    questions = Question.query.filter_by(quiz=quiz_id).all()
    data['questions'] = []
    data.pop('id')
    for q in questions:
        data['questions'].append(q.to_dict())
    return jsonify(data), 200


if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=8080)
