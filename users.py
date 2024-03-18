from flask import Blueprint, jsonify, abort, request
from ..models import User, db, Tweet, likes_table
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

@bp.route('', methods=['GET'])  
def index():
    users = user.query.all()  
    result = []
    for u in tweets:
        result.append(t.serialize())  
    return jsonify(result)  

    @bp.route('/<int:id>/liked_tweets', methods=['GET'])
def liked_tweets(id):
    user = User.query.get_or_404(id)
    liked_tweets = user.liked_tweets

    serialized_tweets = [tweet.serialize() for tweet in liked_tweets]

    return jsonify(serialized_tweets)