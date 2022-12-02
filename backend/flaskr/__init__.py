import json
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)


    def paginate_questions(request, selection):
        """Get paginated questions for a specific page number"""
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    def get_game_categories():
        """Auxiliar method to get all game categories from the database"""
        categories = Category.query.all()
        return {category.id: category.type for category in categories}

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories", methods=["GET"])
    def get_categories():
        """Get all game categories"""
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)

        return jsonify({"success": True, "categories": get_game_categories()})

    @app.route("/questions", methods=["GET"])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "categories": get_game_categories(),
                "current_category": None,
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)
            question.delete()
            return jsonify({"success": True, "deleted_id": question_id})
        except:
            abort(422)

    @app.route("/questions", methods=["POST"])
    def post_question():
        body = request.get_json()

        if (
            "question" in body
            and "answer" in body
            and "category" in body
            and "difficulty" in body
        ):
            question = body.get("question")
            answer = body.get("answer")
            difficulty = body.get("difficulty")
            category = body.get("category")

            try:
                new_question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty,
                )
                new_question.insert()

                return jsonify({"success": True, "created_id": new_question.id})
            except:
                abort(422)
        else:
            abort(500)

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()
        search_term = body.get("searchTerm", None)

        if search_term:
            search_results = Question.query.filter(
                Question.question.ilike(f"%{search_term}%")
            ).all()
            return jsonify(
                {
                    "success": True,
                    "questions": [question.format() for question in search_results],
                    "total_questions": len(search_results),
                    "current_category": None,
                }
            )
        abort(404)

    @app.route("/categories/<int:category_id>/questions", methods=["POST"])
    def get_questions_by_category(category_id):
        try:
            categoryId = str(category_id)
            questions_by_category = Question.query.filter(
                Question.category == categoryId
            ).all()
            return jsonify(
                {
                    "success": True,
                    "questions": [
                        question.format() for question in questions_by_category
                    ],
                    "total_questions": len(questions_by_category),
                    "current_category": category_id,
                }
            )
        except:
            abort(404)

    @app.route("/quizzes", methods=["POST"])
    def get_questions_for_quizz():
        body = request.get_json()
        try:
            print("TargetBF")
            if "quiz_category" in body and "previous_questions" in body:
                category = body.get("quiz_category")
                print(category)
                previous_questions = body.get("previous_questions")
                print("TargetBQ" + str(category) + "  " +str(previous_questions))
                questions = (
                    Question.query.filter_by(category=category)
                    .filter(Question.id.notin_(previous_questions))
                    .all()
                )
                print("TargetBIF")
                questions_amount = len(questions)
                
                if questions_amount > 0:
                    random_question_number = random.randint(
                        0, questions_amount - 1)
                    new_question = questions[random_question_number]
                    print("TargetBR")
                    return jsonify(
                        {
                            "success": True,
                            "id": new_question.id,
                            "question": new_question.question,
                            "answer": new_question.answer,
                            "difficulty": new_question.difficulty,
                            "category": new_question.category,
                        }
                    )
                else:
                    return None
            else:
                abort(422)
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({"success": False, "error": 500,
                    "message": "internal server error"}),
            500,
        )

    return app