from api.models import UserModel
import logging


class MyAuthBackend(object):
    def authenticate(self, username, password):
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except UserModel.DoesNotExist:
            logging.getLogger("error_logger").error(
                "user with login %s does not exists " % username)
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def get_user(self, id):
        try:
            user = UserModel.objects.get(id=id)
            if user:
                return user
            return None
        except UserModel.DoesNotExist:
            logging.getLogger("error_logger").error(
                "user with %(user_id)d not found")
            return None
