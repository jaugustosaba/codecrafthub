# CodeCraftHub

CodeCraftHub is a beginner-friendly Flask REST API for tracking courses that developers want to learn.

The application stores course information in a local `courses.json` file instead of using a database. It demonstrates the basic REST API operations:

- Create a course
- Read one or more courses
- Update a course
- Delete a course

This project is designed for developers learning how HTTP requests, JSON, REST endpoints, and Flask work together.

---

## Features

- Built with Python and Flask
- RESTful API endpoints
- Create, read, update, and delete courses
- Stores data in a JSON text file
- Automatically creates `courses.json` if it does not exist
- Automatically generates course IDs
- Automatically records the course creation timestamp
- Validates required fields
- Validates target dates using the `YYYY-MM-DD` format
- Validates course status values
- Returns JSON responses
- Provides useful error messages
- No database required
- No authentication or user management required

### Valid course statuses

A course status must be one of these exact values:

```text
Not Started
In Progress
Completed
```

---

## Course Fields

Each course contains the following fields:

| Field | Description | Example |
|---|---|---|
| `id` | Automatically generated unique identifier | `1` |
| `name` | Course name; required | `"REST API Fundamentals"` |
| `description` | Course description; required | `"Learn HTTP methods and REST design."` |
| `target_date` | Planned completion date; required | `"2026-12-15"` |
| `status` | Current course status; required | `"Not Started"` |
| `created_at` | Automatically generated UTC timestamp | `"2026-11-18T14:30:00+00:00"` |

---

## Technology Used

- Python 3.9 or newer
- Flask
- JSON file storage
- `curl` for testing API requests

---

## Project Structure

A simple project structure is recommended:

```text
codecrafthub/
├── app.py
├── courses.json
├── requirements.txt
└── README.md
```

### `app.py`

Contains the Flask application, API routes, validation logic, and JSON file operations.

### `courses.json`

Stores all courses as a JSON list.

Example:

```json
[
  {
    "id": 1,
    "name": "REST API Fundamentals",
    "description": "Learn HTTP methods, status codes, JSON, and REST API design.",
    "target_date": "2026-12-15",
    "status": "Not Started",
    "created_at": "2026-11-18T14:30:00+00:00"
  }
]
```

If this file does not exist, the application creates it automatically with the following content:

```json
[]
```

### `requirements.txt`

Lists the Python packages required by the application.

Example:

```text
Flask==3.0.0
```

### `README.md`

Contains project documentation and usage instructions.

---

# Installation

## 1. Install Python

Check whether Python is installed:

```bash
python --version
```

On some systems, use:

```bash
python3 --version
```

You should have Python 3.9 or newer.

If Python is not installed, download it from:

[https://www.python.org/downloads/](https://www.python.org/downloads/)

On Windows, enable the **Add Python to PATH** option during installation.

---

## 2. Create the Project Directory

```bash
mkdir codecrafthub
cd codecrafthub
```

Place the following files in this directory:

```text
app.py
requirements.txt
README.md
```

You do not need to create `courses.json` manually. The application creates it automatically.

---

## 3. Create a Virtual Environment

A virtual environment keeps this project's packages separate from other Python projects.

### macOS and Linux

```bash
python3 -m venv venv
```

### Windows

```bash
python -m venv venv
```

---

## 4. Activate the Virtual Environment

### macOS and Linux

```bash
source venv/bin/activate
```

### Windows Command Prompt

```bash
venv\Scripts\activate
```

### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

After activation, your terminal may show `(venv)` at the beginning of the command prompt.

---

## 5. Install Dependencies

Create a `requirements.txt` file containing:

```text
Flask==3.0.0
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

You can confirm Flask is installed with:

```bash
pip show Flask
```

---

# Running the Application

Start the Flask development server:

```bash
python app.py
```

On some macOS or Linux systems, use:

```bash
python3 app.py
```

You should see output similar to:

```text
* Running on http://127.0.0.1:5000
```

The API is now available at:

```text
http://127.0.0.1:5000
```

The application automatically creates:

```text
courses.json
```

when it starts or when the first API request is made.

To stop the server, press:

```text
Ctrl+C
```

---

# REST API Basics

REST APIs allow applications to communicate using HTTP requests.

The main HTTP methods used by CodeCraftHub are:

| HTTP method | Purpose |
|---|---|
| `POST` | Create a new resource |
| `GET` | Read or retrieve resources |
| `PUT` | Update an existing resource |
| `DELETE` | Delete a resource |

The API uses JSON for both request and response data.

For example, this request creates a course:

```http
POST /api/courses
```

with this JSON body:

```json
{
  "name": "Learn Flask",
  "description": "Build REST APIs with Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
```

---

# API Endpoints

## API Base URL

```text
http://127.0.0.1:5000
```

## Endpoint Summary

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/courses` | Add a new course |
| `GET` | `/api/courses` | Get all courses |
| `GET` | `/api/courses/<id>` | Get one course |
| `PUT` | `/api/courses/<id>` | Update a course |
| `DELETE` | `/api/courses/<id>` | Delete a course |

The `<id>` value must be replaced with a real course ID, such as `1`.

---

## 1. Create a Course

### Request

```http
POST /api/courses
```

### Required JSON fields

- `name`
- `description`
- `target_date`
- `status`

### Example request using curl

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "REST API Fundamentals",
    "description": "Learn HTTP methods, status codes, JSON, and REST API design.",
    "target_date": "2026-12-15",
    "status": "Not Started"
  }'
```

### Successful response

HTTP status:

```text
201 Created
```

Response:

```json
{
  "id": 1,
  "name": "REST API Fundamentals",
  "description": "Learn HTTP methods, status codes, JSON, and REST API design.",
  "target_date": "2026-12-15",
  "status": "Not Started",
  "created_at": "2026-11-18T14:30:00.123456+00:00"
}
```

The `id` and `created_at` fields are generated by the application.

---

## 2. Get All Courses

### Request

```http
GET /api/courses
```

### Example request

```bash
curl http://127.0.0.1:5000/api/courses
```

### Successful response

HTTP status:

```text
200 OK
```

Response:

```json
[
  {
    "id": 1,
    "name": "REST API Fundamentals",
    "description": "Learn HTTP methods, status codes, JSON, and REST API design.",
    "target_date": "2026-12-15",
    "status": "Not Started",
    "created_at": "2026-11-18T14:30:00.123456+00:00"
  }
]
```

If there are no courses, the response is:

```json
[]
```

---

## 3. Get a Specific Course

### Request

```http
GET /api/courses/<id>
```

For example:

```http
GET /api/courses/1
```

### Example request

```bash
curl http://127.0.0.1:5000/api/courses/1
```

### Successful response

HTTP status:

```text
200 OK
```

Response:

```json
{
  "id": 1,
  "name": "REST API Fundamentals",
  "description": "Learn HTTP methods, status codes, JSON, and REST API design.",
  "target_date": "2026-12-15",
  "status": "Not Started",
  "created_at": "2026-11-18T14:30:00.123456+00:00"
}
```

---

## 4. Update a Course

The `PUT` endpoint updates all editable fields of a course.

The request must include:

- `name`
- `description`
- `target_date`
- `status`

The existing `id` and `created_at` values are preserved.

### Request

```http
PUT /api/courses/<id>
```

### Example request

```bash
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Advanced REST API Fundamentals",
    "description": "Learn advanced REST API design, validation, errors, and security concepts.",
    "target_date": "2027-01-10",
    "status": "In Progress"
  }'
```

### Successful response

HTTP status:

```text
200 OK
```

Response:

```json
{
  "id": 1,
  "name": "Advanced REST API Fundamentals",
  "description": "Learn advanced REST API design, validation, errors, and security concepts.",
  "target_date": "2027-01-10",
  "status": "In Progress",
  "created_at": "2026-11-18T14:30:00.123456+00:00"
}
```

---

## 5. Delete a Course

### Request

```http
DELETE /api/courses/<id>
```

### Example request

```bash
curl -X DELETE http://127.0.0.1:5000/api/courses/1
```

### Successful response

HTTP status:

```text
200 OK
```

Response:

```json
{
  "message": "Course with ID 1 was deleted successfully."
}
```

---

# Validation Rules

## Required fields

Every `POST` and `PUT` request must include:

```json
{
  "name": "...",
  "description": "...",
  "target_date": "...",
  "status": "..."
}
```

## Valid dates

The `target_date` must use this format:

```text
YYYY-MM-DD
```

Valid example:

```text
2026-12-15
```

Invalid examples:

```text
12-15-2026
2026/12/15
December 15, 2026
2026-2-5
```

## Valid statuses

The status must exactly match one of these values:

```text
Not Started
In Progress
Completed
```

These values are case-sensitive.

For example, this is invalid:

```text
completed
```

The correct value is:

```text
Completed
```

---

# Error Responses

The API returns JSON error messages when a request cannot be completed.

## Missing required fields

Request:

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Incomplete Course",
    "target_date": "2027-01-01"
  }'
```

Response status:

```text
400 Bad Request
```

Response:

```json
{
  "error": "Missing required field(s): description, status"
}
```

## Invalid status

Response status:

```text
400 Bad Request
```

Response:

```json
{
  "error": "Invalid status. Status must be one of: \"Not Started\", \"In Progress\", or \"Completed\"."
}
```

## Invalid date

Response status:

```text
400 Bad Request
```

Response:

```json
{
  "error": "target_date must use YYYY-MM-DD format."
}
```

## Course not found

Request:

```bash
curl http://127.0.0.1:5000/api/courses/9999
```

Response status:

```text
404 Not Found
```

Response:

```json
{
  "error": "Course with ID 9999 was not found."
}
```

## File storage error

If the application cannot read or write `courses.json`, it returns:

HTTP status:

```text
500 Internal Server Error
```

Example response:

```json
{
  "error": "File storage error",
  "message": "..."
}
```

---

# Testing the API

## Prerequisites

Make sure:

1. The virtual environment is activated.
2. Flask is installed.
3. The application is running.
4. A terminal is available for sending requests.

Start the application:

```bash
python app.py
```

Keep that terminal open. Open a second terminal to run the tests.

---

## Test 1: Create a course

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python for Developers",
    "description": "Learn Python programming fundamentals.",
    "target_date": "2026-12-20",
    "status": "Not Started"
  }'
```

Expected status:

```text
201 Created
```

---

## Test 2: Retrieve all courses

```bash
curl http://127.0.0.1:5000/api/courses
```

Expected status:

```text
200 OK
```

---

## Test 3: Retrieve one course

```bash
curl http://127.0.0.1:5000/api/courses/1
```

Expected status:

```text
200 OK
```

---

## Test 4: Update a course

```bash
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python for Web Developers",
    "description": "Learn Python and prepare for web development.",
    "target_date": "2027-01-15",
    "status": "In Progress"
  }'
```

Expected status:

```text
200 OK
```

---

## Test 5: Delete a course

```bash
curl -X DELETE http://127.0.0.1:5000/api/courses/1
```

Expected status:

```text
200 OK
```

---

## Test 6: Confirm deletion

```bash
curl http://127.0.0.1:5000/api/courses/1
```

Expected status:

```text
404 Not Found
```

---

## Test 7: Test missing fields

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Missing Fields Course"
  }'
```

Expected status:

```text
400 Bad Request
```

---

## Test 8: Test an invalid status

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Status Course",
    "description": "This course uses an unsupported status.",
    "target_date": "2027-02-01",
    "status": "Started"
  }'
```

Expected status:

```text
400 Bad Request
```

---

## Test 9: Test an invalid date

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Date Course",
    "description": "This course uses an invalid date.",
    "target_date": "02-01-2027",
    "status": "Not Started"
  }'
```

Expected status:

```text
400 Bad Request
```

---

## Windows PowerShell Note

The examples above use Unix-style line continuation characters. In PowerShell, use the backtick character:

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/courses `
  -H "Content-Type: application/json" `
  -d '{
    "name": "REST API Fundamentals",
    "description": "Learn REST API basics.",
    "target_date": "2026-12-15",
    "status": "Not Started"
  }'
```

Alternatively, place the entire command on one line.

---

# Working with `courses.json`

Courses are saved as a JSON array.

Example:

```json
[
  {
    "id": 1,
    "name": "Flask REST APIs",
    "description": "Build REST APIs using Flask.",
    "target_date": "2027-01-20",
    "status": "In Progress",
    "created_at": "2026-11-18T14:30:00+00:00"
  }
]
```

The application performs these steps when changing data:

1. Opens `courses.json`.
2. Reads the JSON data into Python.
3. Adds, updates, or removes a course.
4. Writes the updated list back to `courses.json`.
5. Returns a JSON response.

Do not manually remove the square brackets from the file. Even one course must be stored inside a JSON list.

An empty file should contain:

```json
[]
```

---

# Troubleshooting

## Flask is not installed

Error:

```text
ModuleNotFoundError: No module named 'flask'
```

Solution:

Activate the virtual environment and install the dependencies:

```bash
pip install -r requirements.txt
```

---

## The `python` command is not found

Try:

```bash
python3 app.py
```

On Windows, reinstall Python and make sure **Add Python to PATH** is selected.

---

## The virtual environment will not activate

On Windows PowerShell, you may see an execution policy error. You can try:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
venv\Scripts\Activate.ps1
```

---

## Port 5000 is already in use

Another application may already be using port `5000`.

Stop the other application, or change the Flask port in `app.py`:

```python
app.run(debug=True, port=5001)
```

Then use:

```text
http://127.0.0.1:5001
```

for API requests.

---

## The API returns a connection error

Make sure the Flask application is running:

```bash
python app.py
```

You should see:

```text
Running on http://127.0.0.1:5000
```

Also confirm that the URL in your `curl` command matches the server URL.

---

## The API says the request must contain JSON

Make sure your request includes this header:

```bash
-H "Content-Type: application/json"
```

For example:

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"name":"Example"}'
```

---

## The API reports missing fields

Make sure your request contains all four required fields:

```json
{
  "name": "Course name",
  "description": "Course description",
  "target_date": "2026-12-15",
  "status": "Not Started"
}
```

---

## The API reports an invalid status

Use one of these exact values:

```text
Not Started
In Progress
Completed
```

Status values are case-sensitive.

---

## The API reports an invalid date

Use the exact format:

```text
YYYY-MM-DD
```

Example:

```text
2026-12-15
```

---

## `courses.json` contains invalid JSON

If you accidentally edit the file incorrectly, the application may be unable to read it.

A valid empty file is:

```json
[]
```

You can replace the contents with:

```json
[]
```

This removes all existing courses.

Before changing the file, you may want to create a backup:

```bash
cp courses.json courses-backup.json
```

On Windows:

```powershell
Copy-Item courses.json courses-backup.json
```

---

## File storage errors

The application needs permission to read and write `courses.json`.

Check that:

- The project directory exists.
- `courses.json` is not read-only.
- The application has permission to write to the project directory.
- The JSON file is not being edited by another program in a way that prevents access.

---

# Important Limitations

This project uses a JSON file to keep the application simple and beginner-friendly. It is suitable for learning and small personal projects, but it has limitations:

- It is not intended for many users.
- It does not provide authentication.
- It does not support multiple users.
- Simultaneous writes could overwrite each other.
- It does not provide database transactions.
- Searching and filtering are not implemented.
- The entire file is read and rewritten for each change.
- A large number of courses may make the application slower.

For a larger production application, the JSON file could later be replaced with a database such as SQLite or PostgreSQL.

The API design can remain mostly the same even if the storage system changes.

---

# Learning Concepts Demonstrated

This project introduces several important REST API concepts:

## Resources

A course is a resource identified by an ID:

```text
/api/courses/1
```

## HTTP methods

Different methods represent different actions:

```text
POST    Create
GET     Read
PUT     Update
DELETE  Delete
```

## JSON

JSON is used to send and receive structured data:

```json
{
  "name": "Learn Flask",
  "status": "Not Started"
}
```

## HTTP status codes

The API uses status codes to describe the result of each request:

| Status | Meaning |
|---:|---|
| `200` | Request succeeded |
| `201` | Resource was created |
| `400` | Request contains invalid data |
| `404` | Resource was not found |
| `500` | Server or file storage error |

---

# Future Improvements

Possible improvements for a future version include:

- Add a web-based frontend
- Add course filtering by status
- Add search by course name
- Add partial updates with `PATCH`
- Add automated unit tests
- Add SQLite or PostgreSQL storage
- Add user authentication
- Add course progress percentages
- Add reminders for target completion dates
- Add API documentation using Swagger or OpenAPI

---

# License

This project is intended for educational and personal use.
