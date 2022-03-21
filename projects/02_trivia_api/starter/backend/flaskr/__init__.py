import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request):
    page = request.args.get("page", 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = Question.query.order_by(Question.id).all()
    formatted_questions = [question.format() for question in questions]
    question_list = formatted_questions[start:end]

    return question_list



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*":{"origins":"*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add(
          'Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS'
      )
      response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type'
      )

      return response

  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
      categories = Category.query.order_by(Category.id).all()
      category_dict = {}

      for category in categories:
          category_dict[category.id] = category.type


      return jsonify({
        "success" : True,
        "categories" : category_dict
      })

  '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
  @app.route('/questions')
  def get_paginated_questions():
      # Paginate questions
      question_list = paginate_questions(request)

      # Trigger an error when page argument is out of range
      if question_list == []:
          abort(404)

      # Get dictionary of categories
      categories = Category.query.order_by(Category.id).all()
      category_dict = {}

      for category in categories:
          category_dict[category.id] = category.type

      return jsonify({
        "success" : True,
        "questions" : question_list,
        "total_questions" : len(question_list),
        "categories" : category_dict,
        "current_category" : None
      })

  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''


  '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

  '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.

  '''

  '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_categorized_questions(category_id):
      category = Category.query.filter(Category.id == category_id).one_or_none()

      if category is None:
          abort(404)

      questions = Question.query.filter(Question.category == category_id).order_by(
                    Question.id).all()

      formatted_questions = [question.format() for question in questions]


      return jsonify({
        "success" : True,
        "questions" : formatted_questions,
        "total_questions" : len(Question.query.all()),
        "current_category" : category.type
      })


  '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(404)
  def resource_not_found(error):
      return jsonify({
        "success" : False,
        "error" : 404,
        "message" : "Resource cannot be found"
      }), 404


  return app
