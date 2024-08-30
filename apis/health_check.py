from flask import jsonify


def health_check():
    """
    This function handles the '/health-check' endpoint, which accepts a GET request.
    It returns a JSON response indicating that the server is running and ready to answer questions.

    Returns:
    dict: A JSON response indicating the server's status.
    """
    return jsonify({"status": "Server is running."}), 200