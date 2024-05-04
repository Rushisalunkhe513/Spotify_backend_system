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

# for encrypting password and decrypting password.
from passlib.hash import pbkdf2_sha256

# lets create admin_blueprint
blp = Blueprint("admins",__name__,description="Operation on Admin",url_prefix="/admin")



# we need admin_login
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
            return {
                "status":"succesful",
                "message":"admin logged in succesfully."
            }
        else:
            return {
                "staus":"failed",
                "message":"admin username or password is wrong. please correct password."
            },400
            
# we need admin refresh for genrating new tokens.
        # we will apply this last.
# we need admin update data
@blp.route("/update_admin-details/<string:name>")
class UpdateAdminDetails(MethodView):
    # we will be needing put method to update admin _details
    @blp.arguments(UpdateAdminDetails)
    @blp.response(201,ShowAdminDetails)
    def put(self,name,update_admin_data):
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
    @blp.arguments(UpdateAdminPassword)
    @blp.response(204)
    def put(self,name,update_password_data):
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