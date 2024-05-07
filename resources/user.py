from flask.views import MethodView

from flask_smorest import Blueprint,abort

from schema import RegisterUser,UpdateUserDetails,UpdatePassword,ShowUserData,LoginUser

from models.user import UserModel

# lets import hashing mechanism fom passlib
from passlib.hash import pbkdf2_sha256

from datetime import datetime,timedelta

import os

# lets import blocklist to add logged out token to blocklist
from blocklist import Blocklist

# lets add Blurprint
blp = Blueprint("users",__name__,description="Operation on users",url_prefix="/users")


# lets add security by genrating access token and refersh token during user registration and user login. 
# also we need to delete thos access and refresh tokens to blocklist.
# lets use flsk_jwt_extended

from flask_jwt_extended import (
    create_access_token, # creates access token
    create_refresh_token, # creates refresh token
    jwt_required, # ask for jwt token everytime when accessing endpoint.
    get_jwt, # 
    get_jwt_identity # 
)

# lets add route for getting all users
@blp.route("/")
class Users(MethodView):
    # lets get response
    # user should not be accessible to everyine only to admin.
    @jwt_required() # ask for jwt_token everytime when asking for all users from database.
    @blp.response(200,ShowUserData)
    def get(self):
        # get all users
        
        users = UserModel.find_all()
        
        if not users:
            abort(400,message="can not find users from database.")
        
        return [user.json() for user in users]
    
# lets write new endoint to register user
@blp.route("/register")
class RegisterUser(MethodView):
    # lets add new user to database by post method.
    @blp.response(201,ShowUserData)
    @blp.arguments(RegisterUser)
    def post(self,user_data):
        # lets first find user with email exist.
        
        existing_user = UserModel.find_user_by_email(user_data["email"])
        
        if existing_user:
            abort(400,message = "user already exist.")
            
        # we need to hide or encypt it.
        
        user = UserModel(
            name = user_data["name"],
            email = user_data["email"],
            mobile_number = user_data["mobile_number"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        
        """
        When user is added to the database user will automatically logged in to website. 
        so,we need to genrate jwt token and return that tokens to client.
        """
        """
        Here expires_delta means expiry time for token.
        fresh=True means that token is genrated recently.
        role = "user" means token belongs to user.
        """
        access_token = create_access_token(identity=user.mobile_number,role = "user",token_type="access",expires_delta=datetime.now()+timedelta(minutes=os.getenv("jwt_user_access_token_exp")),fresh=True)
        refresh_token = create_refresh_token(identity=user.mobile_number,role = "user",token_type="refresh",expires_delta=datetime.now()+timedelta(minutes=os.getenv("jwt_user_refresh_token_exp")))
        # now lets add new user data to database.
        user.save_data()
        
        # now lets return user data
        return {
            "access_token":access_token,
            "refresh_token":refresh_token,
            "user_data":user.json()
        }
    
    
# now lets write endpoint to do login
@blp.route("/login")
class LoginUser(MethodView):
    # lets login user by name(username) and password(by decrypting it passlib library.)
    @blp.arguments(LoginUser)
    @blp.response(200)
    def post(self,login_data):
        # lets see user login
        
        #  first lets see user with same email exist.
        existing_user = UserModel.find_user_by_email(login_data["email"])
        
        if not existing_user:
            abort(400,message = "user with email do not exist.")
        
        """
        when user logins he should get access token and refresh token.
        when we add fresh=True in token crestion it will add some sort of metadata in it which will in time of decoding 
        will be verified for token is fresh or not by this metadata.
        """
        access_token = create_access_token(identity=existing_user.mobile_number,role="user",token_type="access",expires_delta=datetime.now()+timedelta(minutes=os.getenv("jwt_user_access_token_exp")),fresh=True)
        refresh_token = create_refresh_token(identity=existing_user.mobile_number,role="user",token_type="refresh",expires_delta=datetime.now()+timedelta(minutes=os.getenv("jwt_user_access_token_exp")))
        
        # we need to verify password from database that is encrypted
        if existing_user and pbkdf2_sha256.verify(login_data["password"],existing_user.password):
            return {
                "status":"success",
                "message":"succesfully logged in.",
                "access_token":access_token,
                "refresh_token":refresh_token
            }
        else:
            abort(
                400,
                message="email or password is not correct."
            )
            

# lets write endpoint to update password.
@blp.route("/update_password")
class UpdateUserPassword(MethodView):
    # lets write HTTP put method to update user password
    @jwt_required(fresh=True)
    @blp.arguments(UpdatePassword)
    @blp.response(201)
    def put(self,user_password_data):
        
        # now lets see token is access token and role for token is user.
        jwt_data = get_jwt()
        
        if jwt_data["token_type"]=="refresh" or jwt_data["role"] !="user":
            abort(400,message="token provided is not access token.")
        
        # lets check use exist or not.
        existing_user = UserModel.find_user_by_email(user_password_data["email"])
        
        if not existing_user:
            abort(400,message = "user do not exist.")
            
        if user_password_data["password"] == user_password_data["re_enter_password"]:
            existing_user.password = pbkdf2_sha256.hash(user_password_data["password"])
        else:
            abort(400,message="password do not matches.")
            
        # lets add updated password to database.
        existing_user.save_data()
        
        # now lets return status and message
        return {
            "status":"success",
            "message":"updated password in database"
        }
        
# now lets update user details and delete user by email.
@blp.route("/<string:email>")
class UpdateUserDetails(MethodView):
    # lets get response from updating user data
    # lets get arguments from user.
    @jwt_required(fresh=True) # will check token is fresh or not.
    @blp.response(201,ShowUserData)
    @blp.arguments(UpdateUserDetails)
    def put(self,email,updated_user_data):
        
        jwt_data=get_jwt()
        
        if jwt_data["token_type"]=="refresh" or jwt_data["role"] !="user":
            abort(400,message="wrong jwt token given.")
            
        # lets check if user exist or not
        existing_user = UserModel.find_user_by_email(email)
        
        if not  existing_user:
            abort(400,message = f"user with {email} do not exist.")
            
        if updated_user_data["email"]:
            existing_user.email = updated_user_data["email"]
        
        if updated_user_data["mobile_number"]:
            existing_user.mobile_number = updated_user_data["mobile_number"]
            
        if updated_user_data["name"]:
            existing_user.name = updated_user_data["name"]
            
        # now lets add updated user data
        existing_user.save_data()
        
        # now lets return user_details
        return existing_user.json()
    
    # lets delete user by email
    @jwt_required(fresh=True)
    @blp.response(204)
    def delete(self,email):
        jwt_data = get_jwt()
        if jwt_data["token_type"]=="refresh" or  jwt_data["role"] !="user":
            abort(400,message="wrong jwt token given.")
            
        # lets check user with same email exist.
        existing_user = UserModel.find_user_by_email(email)
        
        if not existing_user:
            abort(400,message=f"user with {email} do not exist.")
        
        existing_user.delete_data()
        
        return {
            "status":"success",
            "message":"user_dt is deleted succesfully."
        }
        

# lets write logout endpoint for user.
@blp.route("/logout")
class UserLogout(MethodView):
    # server will be nedding user access token when he tries to logout. 
    # no additonal data
    @jwt_required(fresh=True)
    @blp.response(204)
    def post(self):
        # lets get jwt_data from the token
        
        jwt_data = get_jwt()
        
        if jwt_data["token_type"]=="refresh" or jwt_data["role"] !="user":
            abort(400,message="wrong jwt token given.")
            
        # lets check user exist in database.
        user_exist = UserModel.query.filter(UserModel.mobile_number == jwt_data["identity"]).first() # will check for user exist ot not.
        
        if not user_exist:
            abort(400,message="user do not exist.")
        
        
        # now lets get ["jti"].
        # jti is unique id uuid which is used to make token unique.
        # we get this from jwt token payload and add to blocklist.
        # when user take this token and the same jti is found in blocklist and token then token will be revoked or wrong token error will be given.
        
        jti_unique = jwt_data["jti"]
        
        # lets add jti to Blocklist
        Blocklist.add(jti_unique)
        
        return  {
            "status":"success",
            "message":"user logged out succesfully."
        }
        

# lets write /refresh endpoint to genrate new pair of access and refresh tokens.
@blp.route("/refresh")
class RefreshUser(MethodView):
    # lets write post method to genrate new access and refresh tokens.
    @jwt_required(refresh=True)
    @blp.response(204)
    def post(self):
        # check for user in database.
        jwt_data = get_jwt()
        
        # lets see user exist in database.
        exist_user = UserModel.get_user_by_mobile_number(jwt_data["identity"])
        
        if not exist_user:
            abort(400,message="user do not exist.")
        
         # if user then check provided token is refrresh token and it is ofuser token 
        if jwt_data["token_type"] != "refresh" or jwt_data["role"] != "user":
            abort(400,message="wrong token is being used for refresh endpoint.")
        
        # then give a access token and refresh token.
        new_access_token = create_access_token(identity=exist_user.mobile_number,role="user",expires_delta=datetime.now()+timedelta(minutes=os.getenv("jwt_user_access_token_exp")),token_type="access",fresh=True)
        new_refresh_token = create_refresh_token(identity=exist_user.mobile_number,role="user",token_type="refresh",expires_delta=datetime.now()+timedelta(minutes=os.getenv("jwt_user_refresh_token_exp")))
        return {
            "access_token":new_access_token,
            "refresh_token":new_refresh_token,
            "status":"success",
            "message":"new access and refresh token are genrated."
        }
            
        
            