from .. import db
import datetime

class BlacklistToken(db.Model):
    __tablename__='blacklist_tokens'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    token=db.Column(db.String(500), unique=True, nullable=False)
    blaklisted_on=db.Column(db.DateTime, nullable=False)

    def __init__(self,token):
        self.token=token
        self.blaklisted_on=datetime.datetime.utcnow()

    def __repr__(self):
        return '<id: token : {}'.format(self.token)

    @staticmethod
    def check_authtoken(authtoken):
        res=BlacklistToken.query.filter_by(token=authtoken).first()
        if res:
            return True
        else:
            return False
