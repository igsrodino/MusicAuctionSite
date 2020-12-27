from flask import Blueprint, flash, render_template, request, url_for, redirect, get_flashed_messages
from .models import Listing, Instrument, User, Watchlist, Bid
from flask_login import current_user, login_required
from .forms import CreateListingForm, AddToWatchlistForm, RemoveFromWatchlistForm, BidForm
from . import db
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy

#create a blueprint
bp = Blueprint('listing', __name__, url_prefix='/listings')
c = False


# Checks and saves listing's image to static/img folder
def check_upload_file(form):
    fp=form.image.data
    filename=fp.filename
    BASE_PATH=os.path.dirname(__file__)

    upload_path=os.path.join(BASE_PATH,'static/img',secure_filename(filename))
    db_upload_path='/static/img/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path

 
@bp.route('/<id>', methods = ['GET', 'POST'])
def show(id):
    # Forms
    wl_form = AddToWatchlistForm()
    del_form = RemoveFromWatchlistForm()  
    bid_form = BidForm()

    # Database querys
    listing = Listing.query.filter_by(id=id).first() 
    alreadyOnWatchlist = Watchlist.query.filter_by(user_id = current_user.get_id(), listing_id = id).first()
    bid = Bid(bidAmount = bid_form.bidField.data, user_id = current_user.get_id(), listing_id = id)
    bidWinner = Bid.query.filter_by(listing_id = id, user_id = Bid.user_id).order_by(Bid.bidAmount.desc()).first()
    startBid = Listing.query.filter_by(id = id).first()
    bidHistory = Bid.query.filter_by(user_id = Bid.user_id, listing_id = id)
    users = Bid.query.filter_by(listing_id = id).all()


    success = False
    
    # Query for finding if the current user is the user that listed the item, and if so, 
    # to display bidding history on page
    listingOwner = Listing.query.filter_by(id = id).all()
    
    # bidding add to db
    if request.method == "POST":
        if bid_form.bidSubmit.data and bid_form.validate_on_submit():
            # update highest bid amount in Listings table to the previous bid made
            if (bid.bidAmount > listing.highestBid) and (bid.bidAmount > listing.startBid):
                listing.highestBid = bid.bidAmount
                listing.totalNumberOfBids = listing.totalNumberOfBids + 1
                db.session.add(bid)
                db.session.commit()
                success = True
                flash('Bid successfully placed!', 'success')
            else:
                flash('Bid must be higher than', 'danger')
                     
            redirect(url_for("listing.show", id = id))
    
    # watchlist add to database
    if not alreadyOnWatchlist:
        if request.method == "POST":
            if wl_form.addToWatchlist.data and wl_form.validate_on_submit():
                watchlistAdd = Watchlist(user_id = current_user.get_id(), listing_id = id)
                db.session.add(watchlistAdd)
                db.session.commit() 
                redirect(url_for("listing.show", id = id))
                alreadyOnWatchlist = Watchlist.query.filter_by(user_id = current_user.get_id(), listing_id = id).first()
    else:
        if request.method == "POST":
            if del_form.removeFromWatchlist.data and del_form.validate_on_submit():
                watchlistDel = Watchlist.query.filter_by(user_id = current_user.get_id(), listing_id = id).first()
                db.session.delete(watchlistDel)
                db.session.commit() 
                redirect(url_for("listing.show", id = id))
                alreadyOnWatchlist = Watchlist.query.filter_by(user_id = current_user.get_id(), listing_id = id).first()

    # Show the given listing
    return render_template('listings/showListing.html', listing = listing, bid_form = bid_form, wl_form = wl_form, del_form = del_form, 
    alreadyOnWatchlist = alreadyOnWatchlist, bidWinner = bidWinner, bid = bid, users = users, bidHistory = bidHistory, listingOwner = listingOwner, success = success, startBid = startBid)

# Close Auction
@bp.route('/<id>/close_auction', methods = ['GET', 'POST'])
def close_auction(id):
    listing = Listing.query.filter_by(id=id).first() 
    
    if (current_user == listing.user):
        # Delete the record from any users watchlist
        deleteWatchlist = Watchlist.__table__.delete().where(Watchlist.listing_id == id)
        db.session.execute(deleteWatchlist)
        db.session.commit()

        # Set the auction status to false in the DB
        listing.auctionStatus = False
        db.session.commit()
        
    return redirect(url_for("listing.show", id = id))      
            
# Create a listing
@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
    form = CreateListingForm()
    
    # Add all listing details to the database
    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        listing = Listing(listTitle = form.title.data, startBid = round(form.startingBid.data, 2), highestBid = 0, totalNumberOfBids = 0,
                            auctionStatus = True, user_id = current_user.get_id(), instrument = Instrument(instrument = form.instrument.data, category = form.category.data, 
                            model = form.model.data, brand = form.brand.data, year = form.year.data, 
                            colour = form.colour.data, description = form.description.data, image = db_file_path))
        
        db.session.add(listing)
        db.session.commit()

        flash('Listing successfully created!', 'success')

        return redirect(url_for("listing.create"))  
    return render_template('listings/createListing.html', form = form)


# Gets bidding history on specific listings
@bp.route('/history', methods = ['GET', 'POST'])
@login_required
def history():
    history = Bid.query.all()
    return render_template('listings/showListing.html', getHistory= history)
