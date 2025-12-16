from flask import Blueprint, request, jsonify        # Flask Blueprint for routes, request for input, jsonify for JSON responses
from models import db, User                           # Import database and User model
from datetime import datetime                         # For handling date fields

# Create Blueprint for users routes; all routes start with /users
users_bp = Blueprint("users", __name__, url_prefix="/users")

# --------------------------
# GET ALL USERS
# --------------------------
@users_bp.get("/")                                    # GET /users → fetch all users
def get_all_users():
    users = User.query.all()                         # Query all users from the database
    return jsonify([u.to_dict() for u in users]), 200 # Return JSON list of users, HTTP 200 OK

# --------------------------
# GET SINGLE USER
# --------------------------
@users_bp.get("/<int:user_id>")                      # GET /users/<id> → fetch a specific user by ID
def get_user(user_id):
    user = User.query.get(user_id)                   # Query user by primary key
    if not user:                                     # If user does not exist
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200              # Return JSON of user, HTTP 200 OK

# --------------------------
# GET USER BY USERNAME
# --------------------------
@users_bp.get("/name/<string:username>")            # GET /users/name/<username> → fetch user by username
def get_user_by_name(username):
    user = User.query.filter_by(username=username).first()  # Query first user matching the username
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

# --------------------------
# CREATE NEW USER
# --------------------------
@users_bp.post("/")                                  # POST /users → create a new user
def create_user():
    data = request.get_json()                        # Get JSON data from request

    required = ["username", "name", "dob", "email"] # Required fields
    for field in required:                           # Check for missing fields
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    dob = datetime.strptime(data["dob"], "%Y-%m-%d").date()  # Convert DOB string to date object

    new_user = User(
        username=data["username"],
        name=data["name"],
        dob=dob,
        email=data["email"],
        job=data.get("job")                          # Optional field
    )

    db.session.add(new_user)                         # Add new user to DB session
    db.session.commit()                              # Commit changes to DB

    return jsonify(new_user.to_dict()), 201          # Return created user, HTTP 201 Created

# --------------------------
# UPDATE USER
# --------------------------
@users_bp.put("/<int:user_id>")                      # PUT /users/<id> → update an existing user
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    if "dob" in data:                               # Update DOB only if provided
        try:
            user.dob = datetime.strptime(data["dob"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid dob format. Use YYYY-MM-DD"}), 400

    if "username" in data:                          # Update username if provided
        user.username = data["username"]
    if "name" in data:                              # Update name if provided
        user.name = data["name"]
    if "email" in data:                             # Update email if provided
        user.email = data["email"]
    if "job" in data:                               # Update job if provided
        user.job = data["job"]

    db.session.commit()                              # Commit updates to DB

    return jsonify(user.to_dict()), 200             # Return updated user, HTTP 200 OK

# --------------------------
# DELETE USER
# --------------------------
@users_bp.delete("/<int:user_id>")                  # DELETE /users/<id> → delete a user
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)                          # Remove user from DB
    db.session.commit()                              # Commit deletion

    return jsonify({"message": "User deleted"}), 200 # Return success message


# from flask import Blueprint, request, jsonify
# from models import db, User
# from datetime import datetime

# # IMPORTANT → add url_prefix
# users_bp = Blueprint("users", __name__, url_prefix="/users") #creates the blueprint andprefix it as /users


# # --------------------------
# # GET ALL USERS
# # --------------------------
# @users_bp.get("/")#get all users
# def get_all_users():
#     users = User.query.all()# query all to users
#     return jsonify([u.to_dict() for u in users]), 200# return jsoniy



# # --------------------------
# # GET SINGLE USER
# # --------------------------
# @users_bp.get("/<int:user_id>")
# def get_user(user_id):
#     user = User.query.get(user_id)

#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     return jsonify(user.to_dict()), 200

# # GET user by name (new route)


# @users_bp.get("/name/<string:username>")
# def get_user_by_name(username):
#     user = User.query.filter_by(username=username).first()
#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     return jsonify(user.to_dict()), 200
# # --------------------------
# # CREATE NEW USER
# # --------------------------


# @users_bp.post("/")
# def create_user():
#     data = request.get_json()

#     required = ["username", "name", "dob", "email"]
#     for field in required:
#         if field not in data:
#             return jsonify({"error": f"Missing field: {field}"}), 400

#     dob = datetime.strptime(data["dob"], "%Y-%m-%d").date()

#     new_user = User(
#         username=data["username"],
#         name=data["name"],
#         dob=dob,
#         email=data["email"],
#         job=data.get("job")  # optional
#     )

#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify(new_user.to_dict()), 201


# # --------------------------
# # UPDATE USER
# # --------------------------
# @users_bp.put("/<int:user_id>")
# def update_user(user_id):
#     user = User.query.get(user_id)

#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     data = request.get_json()

#     # Handle dob ONLY IF provided
#     if "dob" in data:
#         try:
#             user.dob = datetime.strptime(data["dob"], "%Y-%m-%d").date()
#         except ValueError:
#             return jsonify({"error": "Invalid dob format. Use YYYY-MM-DD"}), 400

#     # Update other fields
#     if "username" in data:
#         user.username = data["username"]

#     if "name" in data:
#         user.name = data["name"]

#     if "email" in data:
#         user.email = data["email"]

#     if "job" in data:
#         user.job = data["job"]

#     db.session.commit()

#     return jsonify(user.to_dict()), 200

# # --------------------------
# # DELETE USER
# # --------------------------
# @users_bp.delete("/<int:user_id>")
# def delete_user(user_id):
#     user = User.query.get(user_id)

#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     db.session.delete(user)
#     db.session.commit()

#     return jsonify({"message": "User deleted"}), 200
