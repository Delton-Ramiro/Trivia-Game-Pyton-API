# API Development and Documentation Final Project

# Getting started #

## Pre-requisites and Local Development ##
If you plan to use this project, you must have a machine with Python3, pip, and node installed.

### Backend ###
From the backend folder run:
    pip install requirements.txt

This will install all the packages required for the frontend in your local machine.

If you have errors with depracated versions of package installation write manualy:
<br />

pip install --upgrade <package_name> for all the packages<br />


To run the application, go to /backend directory and run the following commands:
export FLASK_APP=flaskr<br />
export FLASK_DEBUG=1<br />
flask run<br />

These commands will put the application in development and directs our application to use the __init__.py file inside our flaskr folder.

Open the link provided in your terminal: 
http://127.0.0.1:<application_port_number>/


### Frontend ###

From the frontend folder run:
    npm install 

This will install all the dependencies for the frontend in your local machine.

If you run into problems related to socket timeout, please consider changing timeouts. 
A possible timeout is
npm config set fetch-retry-mintimeout 20000<br />
npm config set fetch-retry-maxtimeout 120000<br />

To start the application run:
    npm start
By default the app will run on port 3000


### API Reference ###
Base URL: this api is hosted locally and its base url is the same provided when you ran 
    flask run
http://127.0.0.1:<application_port_number>/

#### Error handling ####
Errors are returned as JSON objects following this format:<br />
    {<br />
        "success": False,<br />
        "error": 404,<br />
        "message": "resource not found"<br />
    }

In case of failure, the API will return any of these errors: 
    422 - Unprocessable
    402 - Resource not found

#### Endpoints ####

`GET '/categories'`

- Fetches a dictionary of categories. The keys are ids and the values are the categories.
- Request Arguments: None
- Returns: A JSON object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
<br />
`{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}`


---


`GET '/questions?page=${integer}'`

- Fetches a paginated list of dictionaries of questions, a total number of questions, all categories and current category.
- Request Arguments: `page` - integer
- Returns: A JSON object with 10 paginated questions, total questions, object including all categories, and current category string

{<br />
  "questions": [<br />
    {<br />
      "id": 1,<br />
      "question": "This is a question",<br />
      "answer": "This is an answer",<br />
      "difficulty": 5,<br />
      "category": 2<br />
    }<br />
  ],
  "totalQuestions": 100,<br />
  "categories": {<br />
    "1": "Science",<br />
    "2": "Art",<br />
    "3": "Geography",<br />
    "4": "History",<br />
    "5": "Entertainment",<br />
    "6": "Sports"<br />
  },<br />
  "currentCategory": "History"<br />
}


---


`GET '/categories/${id}/questions'`

- Fetches questions for a given category specified by its id
- Request Arguments: `id` - integer
- Returns: A JSON object containing the list of questions, total questions and current category


{<br />
  "questions": [<br />
    {<br />
      "id": 1,<br />
      "question": "This is a question",<br />
      "answer": "This is an answer",
      "difficulty": 5,<br />
      "category": 4<br />
    }<br />
  ],<br />
  "totalQuestions": 100,<br />
  "currentCategory": "History"<br />
}


---


`DELETE '/questions/${id}'`

- Deletes a question by its id
- Request Arguments: `id` - integer
- Returns: A JSON object containing the success state and the id of the deleted question


{<br />
    "success": True, <br />
    "deleted_id": question_id<br />
}


---


`POST '/quizzes'`

- Sends a post request to get the next question belonging the current category and non seen question
- Request Body:

```json
{<br />
    'previous_questions': [1, 4, 20, 15]<br />
    quiz_category': 'current category'<br />
 }
```

- Returns: A JSON object of the single new question object


{<br />
  "question": {<br />
    "id": 1,<br />
    "question": "This is a question",<br />
    "answer": "This is an answer",<br />
    "difficulty": 5,<br />
    "category": 4<br />
  }<br />
}


---


`POST '/questions'`

- Sends a post request to add a new question
- Request Body:

```json
{<br />
  "question": "Heres a new question string",<br />
  "answer": "Heres a new answer string",<br />
  "difficulty": 1,<br />
  "category": 3<br />
}
```

- Returns: A JSON object containing the success state and the id of the created question
{<br />
    "success": True, <br />
    "created_id": new_question.id<br />
}


---


`POST '/questions'`

- Sends a post request to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "term the user looks for"
}
```

- Returns: A JSON object containing a list of questions, a number of totalQuestions meeting the search term and the current category


{<br />
  "questions": [<br />
    {<br />
      "id": 1,<br />
      "question": "This is a question",<br />
      "answer": "This is an answer",<br />
      "difficulty": 5,<br />
      "category": 5<br />
    }<br />
  ],<br />
  "totalQuestions": 100,<br />
  "currentCategory": "Entertainment"<br />
}<br />
