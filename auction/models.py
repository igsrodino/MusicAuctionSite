# Models file 
from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    # Intialise the name of the table
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    # Create the columns for this table
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index = True, unique = True, nullable = False)
    email_address = db.Column(db.String(100), index = True, nullable = False)
    phone_number = db.Column(db.Integer, index = True, nullable = False)
    mail_address = db.Column(db.String(255), index = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)

    # Relationships
    listings = db.relationship('Listing', backref='user')
    watchlist = db.relationship("Watchlist", backref="user")
    bids = db.relationship("Bid", backref="user")


class Instrument(db.Model):
    # Intialise the name of the table
    __tablename__ = "instruments"

    # Create the columns for this table
    id = db.Column(db.Integer, primary_key=True)
    instrument = db.Column(db.String(50))
    category = db.Column(db.String(20))
    model = db.Column(db.String(20))
    brand = db.Column(db.String(20))
    year = db.Column(db.String(4))
    colour = db.Column(db.String(20))
    description = db.Column(db.String(250))
    image = db.Column(db.String(400))

    # Relationship
    listings = db.relationship('Listing', backref ='instrument')


class Listing(db.Model):
    # Intialise the name of the table
    __tablename__ = 'listings'

    # Create the columns for this table
    id = db.Column(db.Integer, primary_key=True)
    listTitle = db.Column(db.String(50))
    listingDate = db.Column(db.DateTime, default=datetime.now())
    startBid = db.Column(db.Integer)
    highestBid = db.Column(db.Integer)
    totalNumberOfBids = db.Column(db.Integer)
    auctionStatus = db.Column(db.Boolean, nullable=False)

    # Relationship
    watchlist = db.relationship('Watchlist', backref ='listing')

    #add the foreign keys
    instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Bid(db.Model):
    # Intialise the name of the table
    __tablename__ = "bid"

    # Create the columns for this table
    id = db.Column(db.Integer, primary_key=True)
    bidAmount = db.Column(db.Integer)
    bidDate = db.Column(db.DateTime, default=datetime.now())

    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    listing_id = db.Column(db.Integer, db.ForeignKey("listings.id"))


class Watchlist(db.Model):
    # Intialise the name of the table
    __tablename__ = "watchlist"

    # Create the columns for this table
    id = db.Column(db.Integer, primary_key=True)
    addedToWatchlistDate = db.Column(db.DateTime, default=datetime.now())

    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    listing_id = db.Column(db.Integer, db.ForeignKey("listings.id"))

 






