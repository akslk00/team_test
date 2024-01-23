from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from config import Config
from mysql_connention import get_connection
from mysql.connector import Error


# 댓글작성
class ReviewResource(Resource):

    @jwt_required()
    def post(self,postingId):

        data = request.get_json()
        user_id = get_jwt_identity()

        if int(data['rating']) < 1 or int(data['rating']) > 5:
            return {'error': '별점은 1부터 5까지만 가능합니다.'}, 400
        
        try :
            connection = get_connection()

            query = '''insert into review
                        (postingId,userId,content,rating)
                        values
                        (%s,%s,%s,%s);'''
            record = (postingId,user_id,data['content'],data['rating'])

            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)}, 500

        return {'result' : 'success'}, 200
    

class MyReviewResource(Resource):
    # 수정
    @jwt_required()
    def put(self,postingId,reviewId):

        user_id=get_jwt_identity()
        data = request.get_json()

        if int(data['rating']) < 1 or int(data['rating']) > 5:
            return {'error': '별점은 1부터 5까지만 가능합니다.'}, 400

        
        try:
            connection = get_connection()

            query = '''update review
                        set content=%s,
                            rating = %s
                        where id=%s and postingId=%s and userId=%s;'''
            record =(data['content'],data['rating'],reviewId,postingId,user_id)

            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)},500
            
        return{'result':'success'},200
        
    # 삭제
    @jwt_required()
    def delete(self,postingId,reviewId):
        
        user_id=get_jwt_identity()
        try:
            connection = get_connection()
            query = '''delete from review
                        where id=%s and postingId=%s and userId=%s;'''
            record = (reviewId,postingId,user_id)

            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error':str(e)},500
        
        return {'result':'success'},200

