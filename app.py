"""
CodeCraftHub - Course Tracking REST API

This Flask application provides CRUD operations for courses and stores
course data in a local JSON file named courses.json.

Run the application with:

    python app.py
"""

from datetime import date, datetime, timezone
import json
from pathlib import Path

from flask import Flask, jsonify, request


# Create the Flask application
app = Flask(__name__)


# Store courses.json in the same directory as this app.py file.
# This prevents the file location from depending on where the command
# is executed.
DATA_FILE = Path(__file__).parent / "courses.json"


# These are the only valid course status values.
VALID_STATUSES = {
    "Not Started",
    "In Progress",
    "Completed",
}


class StorageError(Exception):
    """Raised when there is a problem reading or writing courses.json."""


def ensure_data_file():
    """
    Create courses.json automatically if it does not already exist.

    The initial content is an empty JSON list because courses will be
    stored as a list of course objects.
    """
    try:
        if not DATA_FILE.exists():
            DATA_FILE.write_text("[]", encoding="utf-8")
    except OSError as error:
        raise StorageError(
            f"Could not create data file: {error}"
        ) from error


def read_courses():
    """
    Read and return all courses from courses.json.

    Returns:
        list: A list of course dictionaries.

    Raises:
        StorageError: If the file cannot be read or contains invalid JSON.
    """
    ensure_data_file()

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            courses = json.load(file)
    except OSError as error:
        raise StorageError(
            f"Could not read courses.json: {error}"
        ) from error
    except json.JSONDecodeError as error:
        raise StorageError(
            f"courses.json contains invalid JSON: {error}"
        ) from error

    # The JSON file should contain a list, not an object or another type.
    if not isinstance(courses, list):
        raise StorageError(
            "courses.json must contain a JSON list."
        )

    return courses


def write_courses(courses):
    """
    Save all courses to courses.json.

    Args:
        courses (list): The list of course dictionaries to save.

    Raises:
        StorageError: If the file cannot be written.
    """
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(courses, file, indent=2)
            file.write("\n")
    except OSError as error:
        raise StorageError(
            f"Could not write to courses.json: {error}"
        ) from error


def get_next_course_id(courses):
    """
    Generate the next course ID.

    IDs start at 1. If there are no courses, the next ID is 1.
    Otherwise, the next ID is one greater than the highest existing ID.
    """
    if not courses:
        return 1

    return max(course.get("id", 0) for course in courses) + 1


def find_course(courses, course_id):
    """
    Find a course by its ID.

    Returns:
        dict or None: The matching course, or None if not found.
    """
    for course in courses:
        if course.get("id") == course_id:
            return course

    return None


def validate_course_data(data):
    """
    Validate the fields required for creating or updating a course.

    Required fields:
        - name
        - description
        - target_date
        - status

    Returns:
        str or None: An error message, or None if the data is valid.
    """
    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    required_fields = [
        "name",
        "description",
        "target_date",
        "status",
    ]

    # Check whether any required fields are missing.
    missing_fields = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return (
            "Missing required field(s): "
            + ", ".join(missing_fields)
        )

    # Name must be a non-empty string.
    if not isinstance(data["name"], str) or not data["name"].strip():
        return "name must be a non-empty string."

    # Description must be a non-empty string.
    if (
        not isinstance(data["description"], str)
        or not data["description"].strip()
    ):
        return "description must be a non-empty string."

    # Validate the target date.
    target_date = data["target_date"]

    if not isinstance(target_date, str):
        return "target_date must be a string in YYYY-MM-DD format."

    try:
        parsed_date = date.fromisoformat(target_date)

        # This additional check ensures that values such as
        # 2026-1-2 are rejected and must be written as 2026-01-02.
        if parsed_date.strftime("%Y-%m-%d") != target_date:
            return "target_date must use YYYY-MM-DD format."

    except ValueError:
        return "target_date must use YYYY-MM-DD format."

    # Validate the status.
    if data["status"] not in VALID_STATUSES:
        return (
            "Invalid status. Status must be one of: "
            '"Not Started", "In Progress", or "Completed".'
        )

    return None


def get_json_request_body():
    """
    Get JSON data from the incoming request.

    Returns:
        dict: The parsed request body.

    Raises:
        ValueError: If the request body is missing or invalid.
    """
    if not request.is_json:
        raise ValueError(
            "Request must use the 'application/json' content type."
        )

    data = request.get_json(silent=True)

    if data is None:
        raise ValueError(
            "Request body must contain valid JSON."
        )

    return data


@app.errorhandler(StorageError)
def handle_storage_error(error):
    """
    Return a helpful response when courses.json cannot be read or written.
    """
    return jsonify({
        "error": "File storage error",
        "message": str(error),
    }), 500


@app.route("/api/courses", methods=["POST"])
def create_course():
    """
    Add a new course.

    Endpoint:
        POST /api/courses
    """
    try:
        data = get_json_request_body()
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    # Read the current courses before adding the new course.
    courses = read_courses()

    new_course = {
        "id": get_next_course_id(courses),
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "target_date": data["target_date"],
        "status": data["status"],
        # Store a UTC timestamp in ISO 8601 format.
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    courses.append(new_course)
    write_courses(courses)

    return jsonify(new_course), 201


@app.route("/api/courses", methods=["GET"])
def get_courses():
    """
    Get all courses.

    Endpoint:
        GET /api/courses
    """
    courses = read_courses()

    return jsonify(courses), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """
    Get one course by ID.

    Endpoint:
        GET /api/courses/<id>
    """
    courses = read_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """
    Replace all editable fields of an existing course.

    Endpoint:
        PUT /api/courses/<id>

    PUT requires all course fields except id and created_at.
    The original id and created_at values are preserved.
    """
    try:
        data = get_json_request_body()
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    courses = read_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    # Keep the automatically generated id and creation timestamp.
    course["name"] = data["name"].strip()
    course["description"] = data["description"].strip()
    course["target_date"] = data["target_date"]
    course["status"] = data["status"]

    write_courses(courses)

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """
    Delete a course by ID.

    Endpoint:
        DELETE /api/courses/<id>
    """
    courses = read_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    courses.remove(course)
    write_courses(courses)

    return jsonify({
        "message": f"Course with ID {course_id} was deleted successfully."
    }), 200


@app.route("/api/courses/stats", methods=["GET"])
def get_course_stats():
    """
    Return statistics about all courses.

    Endpoint:
        GET /api/courses/stats

    The response includes:
        - Total number of courses
        - Number of courses in each status
    """
    courses = read_courses()

    # Count courses based on their status.
    status_counts = {
        "Not Started": 0,
        "In Progress": 0,
        "Completed": 0,
    }

    for course in courses:
        status = course.get("status")

        # Only count recognized statuses.
        if status in status_counts:
            status_counts[status] += 1

    return jsonify({
        "total_courses": len(courses),
        "courses_by_status": status_counts,
    }), 200


if __name__ == "__main__":
    # Create courses.json when the application starts if needed.
    # Any file-related problems are reported when an API request is made.
    try:
        ensure_data_file()
    except StorageError as error:
        print(f"Warning: {error}")

    # debug=True is useful while learning and developing.
    # Do not use debug mode in production.
    app.run(debug=True)