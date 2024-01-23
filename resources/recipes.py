from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from config import Config
from mysql_connention import get_connection
from mysql.connector import Error

from datetime import datetime

import boto3

# 레시피 업로드
class RecipeResource(Resource):
        
    @jwt_required()
    def post(self) :

        file = request.files.get('photo')
        title = request.form.get('title')
        subTitle = request.form.get('subTitle')
        ingredients = request.form.get('ingredients')
        recipe = request.form.get('recipe')
    
        user_id = get_jwt_identity()

        if file is None :
            return {'error' : '파일을 업로드 하세요'}, 400
        

        current_time = datetime.now()

        new_file_name = current_time.isoformat().replace(':', '_') + str(user_id) + '.jpg'  
 
        file.filename = new_file_name

        s3 = boto3.client('s3',
                    aws_access_key_id = Config.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY )

        try :
            s3.upload_fileobj(file, 
                              Config.S3_BUCKET,
                              file.filename,
                              ExtraArgs = {'ACL' : 'public-read' , 
                                           'ContentType' : 'image/jpeg'} )
        except Exception as e :
            print(e)
            return {'error' : str(e)}, 500
        
        try :
            connection = get_connection()

            query = '''insert into posting
                        (userId, title,subTitle, imageURL, ingredients,recipe)
                        values
                        (%s,%s,%s,%s,%s,%s);'''
            record = (user_id,title,subTitle,
                      Config.S3_LOCATION+new_file_name,ingredients,recipe,
                      )
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
    
# 레시피 수정, 삭제
class MyRecipeResource(Resource):

    # 수정
    @jwt_required()
    def put(self,Myrecipes_id):

        file = request.files.get('photo')
        title = request.form.get('title')
        subTitle = request.form.get('subTitle')
        ingredients = request.form.get('ingredients')
        recipe = request.form.get('recipe')

        user_id=get_jwt_identity()

        current_time = datetime.now()

        new_file_name = current_time.isoformat().replace(':', '_') + str(user_id) + '.jpg'  
 
        file.filename = new_file_name

        s3 = boto3.client('s3',
                    aws_access_key_id = Config.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY )

        try :
            s3.upload_fileobj(file, 
                              Config.S3_BUCKET,
                              file.filename,
                              ExtraArgs = {'ACL' : 'public-read' , 
                                           'ContentType' : 'image/jpeg'} )
        except Exception as e :
            print(e)
            return {'error' : str(e)}, 500

        try:
            connection = get_connection()
            query = '''update posting
                        set title=%s,
                            subTitle = %s,
                            imageURL = %s,
                            ingredients = %s,
                            recipe = %s
                        where id=%s and userId=%s;'''
            record =(title,subTitle,Config.S3_LOCATION+new_file_name,ingredients,recipe,Myrecipes_id,user_id)

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
    def delete(self,Myrecipes_id):
        
        user_id=get_jwt_identity()
        try:
            connection = get_connection()
            query = '''delete from posting
                        where id = %s and userId = %s;'''
            record = (Myrecipes_id,user_id)

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
