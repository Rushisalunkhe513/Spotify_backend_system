# admin related schema
from schema import UpdateAdminDetails,ShowAdminDetails,AdminLogin,UpdateAdminPassword

# admin model/table
from models.admin import AdminModel

# db 
from db import db

# Blueprint and abort
from flask_smorest import abort,Blueprint

# flask Methidviews
from flask.views import MethodView

from datetime import datetime,timedelta

from blocklist import Blocklist

import os

# lets get create_access_token,create_refresh_token,get_jwt,get_jwt_identity,jwt_required.
from flask_jwt_extended import get_jwt,create_access_token,create_refresh_token,get_jwt_identity,jwt_required

# for encrypting password and decrypting password.
from passlib.hash import pbkdf2_sha256

# lets create admin_blueprint
blp = Blueprint("admins",__name__,description="Operation on Admin",url_prefix="/admin")



# we need admin_login
# sim with user, for admin login create access and refresh tokens.
@blp.route("/login")
class Login(MethodView):
    # lets write post HTTP method
    @blp.response(204) # 204 means server have succesfully completed request.
    @blp.arguments(AdminLogin)
    def post(self,login_data):
        # lets check for admin_existence.
        existing_admin = AdminModel.get_admin_data_by_name(login_data["name"])
        
        if not existing_admin:
            abort(404,message="admin not found.")
            
        if existing_admin.name == login_data["name"] and pbkdf2_sha256.verify(login_data["password"],existing_admin.password):
            admin_access_token = create_access_token(identity=existing_admin.mobile_number,role="admin",token_type="access",expires_delta=datetime.now()+timedelta(hours=os.getenv("jwt_admin_access_token_exp")),fresh=True)
            admin_refresh_token = create_refresh_token(identity=existing_admin.mobile_number,role="admin",token_type="refresh",expires_delta=datetime.now()+timedelta(hours=os.getenv("jwt_admin_refresh_token_exp")))
            
            return {
                "status":"succesful",
                "message":"admin logged in succesfully.",
                "access_token":admin_access_token,
                "refresh_token":admin_refresh_token
            }
        
        else:
            return {
                "staus":"failed",
                "message":"admin username or password is wrong. please correct password."
            },400
            
# we need admin refresh for genrating new tokens.
@blp.route("/refresh")
class RefreshTokens(MethodView):
    # lets get new tokens
    @jwt_required(refresh=True)
    @blp.response(204)
    def post(self):
        # lets get jwt payload
        jwt_data = get_jwt()
        
        # lets see if token is refresh and role is admin
        if jwt_data["token_type"] != "refresh" or jwt_data["role"] != "admin":
            abort(400,message="wrong token is provided.")
        
        # now lets see iif admin exisit or not in database.
        exist_admin = AdminModel.get_admin_by_mobile_number(jwt_data["identity"])
        
        if not exist_admin:
            abort(400,message="admin do not exist.")
        
            
        # lets create new access and refresh tokens
        new_admin_access_token = create_access_token(identity=exist_admin.mobile_number,token_type="access",role="admin",fresh=True,expires_delta=datetime.now() + timedelta(hours=os.getenv("jwt_admin_access_token_exp")))
        new_admin_refresh_token = create_refresh_token(identity=exist_admin.mobile_number,token_type="refresh",role="admin",expires_delta=datetime.now()+timedelta(hours=os.getenv("jwt_admin_refresh_token_exp")))

        return {
            "admin_access_token":new_admin_access_token,
            "admin_refresh_token":new_admin_refresh_token,
            "message":"new token for admin are genrated.",
            "status":"success"
        }
        
        
        
# we need admin update data
@blp.route("/update_admin_details/<string:name>")
class UpdateAdminDetails(MethodView):
    # we will be needing put method to update admin _details
    @jwt_required(fresh=True)
    @blp.arguments(UpdateAdminDetails)
    @blp.response(201,ShowAdminDetails)
    def put(self,name,update_admin_data):
        
        # need jwt and its payload
        jwt_payload = get_jwt()
        
        if jwt_payload["token_type"] != "access" or jwt_payload["role"] != "admin":
            abort(400,message="wrong token is provided.")
        
        # lets check if admin-exist
        existing_admin = AdminModel.get_admin_data_by_name(name)
        
        if not existing_admin:
            abort(400,message="admin do not exist.")
        
        if update_admin_data["name"]:
            existing_admin.name = update_admin_data["name"]
            
        if update_admin_data["mobile_number"]:
            existing_admin.mobile_number = update_admin_data["mobile_number"]
            
        if update_admin_data["new_password"]:
            existing_admin.password = pbkdf2_sha256.hash(update_admin_data["new_password"])
        
        # now lets add newly added data to database
        db.session.add(existing_admin)
        db.session.commit()
        db.session.close()

        return existing_admin.json()

# we need admin reset password
@blp.route("/update_password/<string:name>")
class UpdateAdminPassword(MethodView):
    # lets write put method
    @jwt_required(fresh=True)
    @blp.arguments(UpdateAdminPassword)
    @blp.response(204)
    def put(self,name,update_password_data):
        
        jwt_payload = get_jwt()
        
        if jwt_payload["token_type"] != "access" or jwt_payload["role"] != "admin":
            abort(400,message="wrong token is provided.")
            
        # lets check if useer exist or not first
        existing_admin = AdminModel.get_admin_data_by_name(name)
        
        # if not existing user
        if not existing_admin:
            abort(400,message=f"admin with name {name} do not exist.")
        
        if update_password_data["new_password"] == update_password_data["verify_password"]:
            existing_admin.password = pbkdf2_sha256.hash(update_password_data["new_password"])
        
        else:
            abort(400,message="password do not match.")
        
        db.session.add(existing_admin)
        db.session.commit()
        
        return {
            "status":"success",
            "message":"updated admin password."
        }
        
        
# lets write logout endpoint for admin
@blp.route("/logout")
class AdminLogout(MethodView):
    # add response 
    # add jwt_required decorator
    @jwt_required(fresh=True)
    @blp.response(204)
    def post(self):
        # lets get jwt_payload data
        jwt_data = get_jwt()
        
        # lets see if token is refresh and role is admin
        if jwt_data["token_type"] != "refresh" or jwt_data["role"] != "admin":
            abort(400,message="wrong token is provided.")
            
        # lets see admin exist in database
        exist_admin = AdminModel.get_admin_by_mobile_number(jwt_data["identity"])
        
        if not exist_admin:
            abort(400,message="admin do not exist.")
            
        # now lets add ["jti"] in Blocklist
        
        jwt_jti_data = jwt_data["jti"]
        Blocklist.add(jwt_jti_data)
        
        # added token to blocklist
        return {
            "status":"success",
            "message":"admin logged out succesfully."
        }
        