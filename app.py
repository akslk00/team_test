from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
<<<<<<< HEAD
from resources.recipe import RecipeDetail, RecipeFollow, RecipeListResource, RecipeMeResource, RecipeResource
=======
from resources.recipes import MyRecipeResource, RecipeResource
>>>>>>> 742c2b127ee2b11fc1d2ba492b361a682b3ef4d0
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


<<<<<<< HEAD
api.add_resource(RecipeListResource, '/recipe')
api.add_resource( RecipeDetail , '/recipe/<int:posting_id>')
api.add_resource(RecipeMeResource, '/myrecipe')
api.add_resource(RecipeFollow, '/followrecipe')

=======
api.add_resource(RecipeResource, '/recipes/add')
api.add_resource(MyRecipeResource,'/myrecipes/<int:Myrecipes_id>')
>>>>>>> 742c2b127ee2b11fc1d2ba492b361a682b3ef4d0


if __name__ == '__main__':
    app.run()
