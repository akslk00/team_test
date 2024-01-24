from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from resources.favorites import FavoritesResource
from resources.follows import FollowResource
from resources.history import historyTop10
from resources.naver import NaverLogin

from resources.recipelist import RecipeDetail, RecipeFollow, RecipeListMoreShowResource, RecipeListResource, RecipeMeResource, RecipeResource

from resources.recipes import MyRecipeResource, RecipeResource

from resources.review import MyReviewResource, ReviewResource

from resources.user import UserDelete, UserPasswordUpdate, jwt_blocklist

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
api.add_resource( UserPasswordUpdate,'/user/passwordUpdate')

# 레시피 전체보기(간략히)
api.add_resource(RecipeListResource, '/recipe')
# 레시피 전체보기(더보기)
api.add_resource(RecipeListMoreShowResource, '/recipemore')
# 레시피 상세보기
api.add_resource( RecipeDetail , '/recipe/<int:posting_id>')
# 내 레시피 보기
api.add_resource(RecipeMeResource, '/myrecipe')
# 팔로워 레시피 보기
api.add_resource(RecipeFollow, '/followrecipe')
# 인기검색어 Top10
api.add_resource(historyTop10, '/history')
# 팔로우 
api.add_resource(  FollowResource , '/follow/<int:followee_id>')

# 즐겨찾기 
api.add_resource(FavoritesResource,'/favorites/<int:postingId>')

# 레시피 작성
api.add_resource(RecipeResource, '/recipes/add')
#레시피 수정,삭제
api.add_resource(MyRecipeResource,'/myrecipes/<int:Myrecipes_id>')

# 댓글 작성
api.add_resource(ReviewResource,'/review/<int:postingId>')
# 댓글 수정, 삭제
api.add_resource(MyReviewResource,'/review/<int:postingId>/<int:reviewId>')



# 네이버 로그인 API
api.add_resource(NaverLogin , '/naverLogin')
# api.add

if __name__ == '__main__':
    app.run()


