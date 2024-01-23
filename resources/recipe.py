from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connention import get_connection
from mysql.connector import Error


# resources 폴더 안에 만드는 파일에는,
# API를 만들기 위한 클래스를 작성한다.

#  API를 만들기 위해서는 flask_restful 라이브러라의 
# Resource 클래스를 상속해서 만들어야 한다

class RecipeListResource(Resource) :

    # JWT 토큰이 헤어데 필수로 있어야 한다는 뜻.
    # 토큰이 없으면, 이 API는 실행이 안된다.
    @jwt_required()
    def get(self) :

        

        # 1. 클라이언트로부터 데이터를 받아온다
        # 받아올 데이터 없음.

        # 2. DB에 저장된 데이터를 가져온다.

        try :
            connection = get_connection()

            query = ''' select *
                            from posting; '''
            
            # 중요!!
            # select 문에서 커서를 만들 때에는 
            # 파라미터 dictionary = True 로 해준다
            # 왜? 리스트와 딕셔너리 형태로 가져오기 때문에
            # 클라이언트에게 json 형식으로 보내줄 수 있다.
            
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query)

            result_list = cursor.fetchall()


            # datetime 은 파이썬에서 사용하는 데이터타입 이므로
            #  json 형식이 아니다. 따라서
            #  json은 문자열이나 숫자만 가능하므로
            #  datetime을 문자열로 바꿔줘야 한다.

            i = 0
            for row in result_list :
                result_list[i]['createdAt']= row['createdAt'].isoformat()
                result_list[i]['updatedAt']= row['updatedAt'].isoformat()
                i = i + 1

            print()
            print(result_list)
            print()


            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail" , "error" : str(e)}, 500


        return {"result" : "success" , 
                "items" : result_list,
                "count" : len(result_list)} , 200

class RecipeResource(Resource) :


    #  Path (경로)에 숫자나 문자가 바뀌면서 처리되는 경우에는
    #  해당 변수를, 파라미터에 꼭 써줘야 한다.
    #  이 변수는, app.py 파일의 addResource 함수에서 사용한 변수다!
    def get(self, recipe_id ) :
        print(recipe_id)

        # 1. 클라이언트로부터 데이터를 받아온다.
        #    이미 경로에 들어있는, 레시피 아이디를 받아왔다.
        #    위의 recipe_id 라는 변수에 이미 있다.

        # 2. DB에서 recipe_id에 해당하는 레시피 1개를 가져온다.
        try :
            connection = get_connection()
            
            query = '''select *
                        from recipe
                        where id = %s; '''
            
            recode = (recipe_id , )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,recode)

            #  fetchall 함수는 항상 결과를 리스트로 리턴한다.
            result_list = cursor.fetchall()
            print('DB에서 실행')
            print(result_list)

            i = 0
            for row in result_list :
                result_list[0]['createdAt']= row['createdAt'].isoformat()
                result_list[0]['updatedAt']= row['updatedAt'].isoformat()
                i = i + 1


            cursor.close()
            connection.close()


        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail", "error" : str(e)} , 500
        
        #  여기서 리스트에 데이터가 있는 경우와 없는 경우로 체크하여
        #  클라이언트에게 데이터를 보낸다
        
        if len(result_list) == 0 :
            return {"result" : "fail", "message" : "데이터를 찾을 수 없습니다"}, 400
        else :
              return {"result" : "success",
                "items" : result_list[0]} , 200

class RecipeDetail(Resource) :
    
        
    #  Path (경로)에 숫자나 문자가 바뀌면서 처리되는 경우에는
    #  해당 변수를, 파라미터에 꼭 써줘야 한다.
    #  이 변수는, app.py 파일의 addResource 함수에서 사용한 변수다!
    def get(self, posting_id ) :
        print(posting_id)

        # 1. 클라이언트로부터 데이터를 받아온다.
        #    이미 경로에 들어있는, 레시피 아이디를 받아왔다.
        #    위의 recipe_id 라는 변수에 이미 있다.

        # 2. DB에서 recipe_id에 해당하는 레시피 1개를 가져온다.
        try :
            connection = get_connection()
            
            query = '''select u.nickname,
 p.id postingId, p.userId userId, p.title, p.content, p.imageURL, p.ingredients, p.recipe, p.createdAt,p.updatedAt,
r.rating, r.content
from posting p
join user u
on u.id = p.userId
left join review r
on p.id = r.postingId
where p.id = %s; '''
            
            recode = (posting_id , )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,recode)

            #  fetchall 함수는 항상 결과를 리스트로 리턴한다.
            result_list = cursor.fetchall()
            print('DB에서 실행')
            print(result_list)

            i = 0
            for row in result_list :
                result_list[0]['createdAt']= row['createdAt'].isoformat()
                result_list[0]['updatedAt']= row['updatedAt'].isoformat()
                i = i + 1


            cursor.close()
            connection.close()


        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail", "error" : str(e)} , 500
        
        #  여기서 리스트에 데이터가 있는 경우와 없는 경우로 체크하여
        #  클라이언트에게 데이터를 보낸다
        
        if len(result_list) == 0 :
            return {"result" : "fail", "message" : "데이터를 찾을 수 없습니다"}, 400
        else :
              return {"result" : "success",
                "items" : result_list[0]} , 200            
 
class RecipeMeResource(Resource) :


    @jwt_required()
    def get(self) :

        user_id = get_jwt_identity()

        print()
        print(user_id)


        try :
            connection = get_connection()
            query = '''select *
                        from posting
                        where userId = %s;'''
            
            record = (user_id , )

            cursor = connection.cursor(dictionary= True)
            cursor.execute(query,record)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {'result' : 'fail', 'error' : str(e)} , 400
        print()
        print(result_list)

        i = 0
        for row in result_list :
                result_list[i]['createdAt']= row['createdAt'].isoformat()
                result_list[i]['updatedAt']= row['updatedAt'].isoformat()
                i = i + 1


    


        return {'result' : 'success',
                'items' : result_list,
                'count' : len(result_list)
                  } , 200
    
class RecipeFollow(Resource) :
    
    @jwt_required()
    def get(self) :

        user_id = get_jwt_identity()

        print()
        print(user_id)

        

        # 1. 클라이언트로부터 데이터를 받아온다
        # 받아올 데이터 없음.

        # 2. DB에 저장된 데이터를 가져온다.

        try :
            connection = get_connection()

            query = ''' select u.id userId, p.id postingId,
                                    p.title, u.nickname ,
                                    p.imageURL,r.rating,
                                    p.createdAt
                                    from follow f
                                    join user u
                                    on f.followeeId = u.id
                                    join posting p
                                    on u.id = p.userId
                                    left join review r
                                    on u.id = r.userId 
                                    where followerId = %s;'''
            record = (user_id , )
            
            # 중요!!
            # select 문에서 커서를 만들 때에는 
            # 파라미터 dictionary = True 로 해준다
            # 왜? 리스트와 딕셔너리 형태로 가져오기 때문에
            # 클라이언트에게 json 형식으로 보내줄 수 있다.
            
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,record)

            result_list = cursor.fetchall()


            # datetime 은 파이썬에서 사용하는 데이터타입 이므로
            #  json 형식이 아니다. 따라서
            #  json은 문자열이나 숫자만 가능하므로
            #  datetime을 문자열로 바꿔줘야 한다.

            i = 0
            for row in result_list :
                result_list[i]['createdAt']= row['createdAt'].isoformat()
                
                i = i + 1

            print()
            print(result_list)
            print()


            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail" , "error" : str(e)}, 500


        return {"result" : "success" , 
                "items" : result_list,
                "count" : len(result_list)} , 200
