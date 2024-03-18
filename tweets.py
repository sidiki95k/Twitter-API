from flask import Blueprint, jsonify, abort, request
from ..models import Tweet, User, db

bp = Blueprint('tweets', __name__, url_prefix='/tweets')

@bp.route('', methods=['GET'])  
def index():
    tweets = Tweet.query.all()  
    result = []
    for t in tweets:
        result.append(t.serialize())  
    return jsonify(result) 

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    t = Tweet.query.get_or_404(id)
    return jsonify(t.serialize())

@bp.route('', methods=['POST'])
def create():
    
    if 'user_id' not in request.json or 'content' not in request.json:
        return abort(400)

    
    User.query.get_or_404(request.json['user_id'])

   
    t = Tweet(
        user_id=request.json['user_id'],
        content=request.json['content']
    )

    db.session.add(t)  
    db.session.commit()  

    return jsonify(t.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    t = Tweet.query.get_or_404(id)
    try:
        db.session.delete(t) 
        db.session.commit()  
        return jsonify(True)
    except:
       
        return jsonify(False)


@bp.route('/users/<int:id>', methods=['PATCH', 'PUT'])
def update(id):
    user = User.query.get(id)
    if not user:
        abort(404, description="User not found")

   
    if 'username' not in request.json and 'password' not in request.json:
        abort(400, description="Username or password must be provided")

    
    if 'username' in request.json:
        username = request.json['username']
        if len(username) < 3:
            abort(400, description="Username must be at least 3 characters long")
        user.username = username

   
    if 'password' in request.json:
        password = request.json['password']
        if len(password) < 8:
            abort(400, description="Password must be at least 8 characters long")
        
        user.password = scramble(password)

    try:
        db.session.commit()
        return jsonify({'id': user.id, 'username': user.username}), 200
    except:
        return jsonify({'message': 'Update failed'}), 400


def scramble(password):
    
    pass


@bp.route('/<int:id>/liking_users', methods=['GET'])
def liking_users(id: int):
    t = Tweet.query.get_or_404(id)
    result = []
    for u in t.liking_users:
        result.append(u.serialize())
    return jsonify(result)