from RESTAPI_ import db, session, Base

class Company(Base):
    __tablename__ = 'Company_data'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name_ = db.Column(db.String(250), nullable=False)
    Date_ = db.Column(db.Date, nullable=False)
    Open_ = db.Column(db.Float, nullable=False)
    High = db.Column(db.Float, nullable=False)
    Low = db.Column(db.Float, nullable=False)
    Close_ = db.Column(db.Float, nullable=False)
    Adj_Close = db.Column(db.Float, nullable=False)
    Volume = db.Column(db.Integer, nullable=False)
