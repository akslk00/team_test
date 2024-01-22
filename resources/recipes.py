from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connention import get_connection
from mysql.connector import Error

class RecipeResource(Resource):

    @jwt_required()
    def post(self):
   
        data = request.get_json()
      
        user_id=get_jwt_identity()

        print(data)

        try:
           
            connection = get_connection()

            query ='''insert into posting
                        (userId, title,content, imageURL, ingredients,recipe)
                        values
                        (%s,%s,%s,%s,%s,%s);'''
           
            record = (data['userId'],data['title'],data['content'],
                      data['imageURL'],data['ingredients'],user_id)
            
            cursor = connection.cursor()

            cursor.execute(query,record)

            connection.commit()

            cursor.close()
            connection.close()


        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {"result":"fail","error":str(e)}, 500
        
        return {"result":"success"}, 200