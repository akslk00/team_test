from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from resources.history import historyTop10
from resources.recipe import RecipeDetail, RecipeFollow, RecipeListMoreShowResource, RecipeListResource, RecipeMeResource, RecipeResource
from resources.user import UserDelete, jwt_blocklist
from config import Config
from resources.user import UserLoginResource, UserLogoutResource, UserRegisterResource

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header,jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blocklist

api = Api(app)

# api 작성

api.add_resource( UserRegisterResource, '/user/register')
api.add_resource( UserLoginResource ,'/user/login')
api.add_resource( UserLogoutResource,'/user/logout')
api.add_resource( UserDelete,'/user/delete')


api.add_resource(RecipeListResource, '/recipe')
api.add_resource(RecipeListMoreShowResource, '/recipemore')
api.add_resource( RecipeDetail , '/recipe/<int:posting_id>')
api.add_resource(RecipeMeResource, '/myrecipe')
api.add_resource(RecipeFollow, '/followrecipe')

api.add_resource(historyTop10, '/history')


# 댓글 작성
api.add_resource(ReviewResource,'/review/<int:postingId>')
# 댓글 수정, 삭제
api.add_resource(MyReviewResource,'/review/<int:postingId>/<int:reviewId>')

if __name__ == '__main__':
    app.run()
