import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10



def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  app.config['DEBUG'] = True
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  #CORS(app, resources={"/": {"origins": "*"}})
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                           'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods',
                           'GET, PATCH, POST, DELETE, OPTIONS')
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    #get all the categories
    results = Category.query.all()
    categories = {}
    for category in results:
      categories[category.id] = category.type

    if len(results) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories
    }), 200

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
  def retrieve_questions():
    # fetch all questions
      questions = Question.query.order_by(Question.id).all()
    # get 10 per page  
      current_questions = paginate_questions(request, questions)
    # fetch all categories
      categories = Category.query.order_by(Category.type).all()

      if(len(current_questions)) == 0:
        abort(404)

      return jsonify({
        'questions': current_questions,
        'total_questions': len(questions),
        'categories': {category.id: category.type for category in categories},
        'current_category': None,
        'success': True
      }), 200

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_questions(question_id):
    try:
        question = Question.query.filter_by(id=question_id).one_or_none()
        question.delete()
        return jsonify({
          'success': True,
          'deleted': question_id,
          'total_questions': len(Question.query.all()),
        }), 200
    except:
        abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def addQuestion():
    #  to add questions
      body = request.get_json()

      try:
        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')

        if question=='' or answer =='' or category=='' or difficulty=='':
          abort(422)
      except:
        abort(422)
      try:
        new_question = Question(question=question, answer=answer,
                                category=category, difficulty=difficulty)

        new_question.insert()
        new_quest = (new_question.format())
        id = new_quest.get("id", "")
      
        return jsonify({
           'success': True,
           'created': id,
           'total_questions': len(Question.query.all())
        }), 200
      except:
          abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    #search related question with input string
    data = request.get_json()
    search_term = data.get('searchTerm', None)

    if (search_term.isspace() == True or search_term == ''):
       abort(404)

    try:   
       related_questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
       output = paginate_questions(request, related_questions)
       return jsonify({
          'success': True,
          'questions': output,
          'total_questions': len(related_questions),
       })
    except:   
      abort(404)
  
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_question_by_category(id):
    category = Category.query.get(id)
    if (category is None):
      abort(404)

    try:
      questions = Question.query.filter_by(category=category.id).all()
      
      current_questions = paginate_questions(request, questions)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'current_category': category.type,
        'total_questions': len(questions)
      })
    except:
      abort(404)
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
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
        try:
            body = request.get_json()
            if not ('quiz_category' in body and 'previous_questions' in body and body.get('quiz_category') != '' and body.get('previous_questions') != ''):
                abort(422)

            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            if category['type'] == 'click':
                available_questions = Question.query.filter(
                    ~Question.id.in_(previous_questions)).all()
            else:
                available_questions = Question.query.filter_by(
                    category=category['id']).filter(~Question.id.in_(previous_questions)).all()

            new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(available_questions) > 0 else None

            return jsonify({
                'success': True,
                'question': new_question
            })

        except Exception as e:
            abort(422)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422
  
  return app    