


from database.engine import getSession,userName
from models.user import User


class UserDataService:
    """ User Data Services"""

    def getUser():
        with getSession() as session:
            user = (
                session.query(User)
                .filter(User.user_name == userName)
            )
            if user is None:
                raise Exception("User not found")
            return user
        
    def createUser(self, data):
        with getSession() as session:
            user = User(
                user_name = userName,
                email_from = data.get("email_from"),
                email_to = data.get("email_to"),
                email_cc = data.get("email_cc")
            )
            session.add(user)
            session.commit()
            return user 