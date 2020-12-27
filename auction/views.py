from flask import Blueprint, render_template, request
from .models import Listing, Instrument, Watchlist, Bid
from flask_login import login_required, current_user


# All url_for's from this .py file will use this namespace
bp = Blueprint('main', __name__)


# Index/landing page
@bp.route('/', methods = ['GET', 'POST'])
def index():
    # For the carousel slides on the index page. Grab only listings that are currently
    # up for auction, and show the most recent listings
    listings = Listing.query.order_by(Listing.id.desc()).all()
    return render_template('index.html', listings = listings)


# Browse/browse by category page
@bp.route('/browse/<category>', methods = ['GET', 'POST'])
def browse(category):
    listings = Listing.query.all() # Get all listings
    lengthOfAllListings = len(listings) # Get number of total listings
    listOfResultLengths = list() # Create an empty list to append to
    listOfResultLengths.append(lengthOfAllListings) # Add total listing num as first list item
    allCategories = ["Acoustic Guitar", "Electric/Rock Guitar", "Bass Guitar", "Piano/Keyboard", "Drums & Percussion", 
             "Electronic/MIDI/Synth", "Orchestra/Strings", "Jazz/Woodwind", "Studio Hardware/Recording", "DJ Mixers/CDJ's", "Other"] 
    

    for thisCategory in allCategories:
        filteredCategory = Instrument.query.filter_by(category = thisCategory).all() # Get the chosen category
        lengthOfFilteredResult = len(filteredCategory) # Get the length of said category
        listOfResultLengths.append(lengthOfFilteredResult) # Append all categories total length to list
    
    return render_template('browse_all.html', listings = listings, category = category, 
                            listOfResultLengths = listOfResultLengths, allCategories = allCategories)

    
# My watchlist page
@bp.route('/watchlist')
@login_required
def watchlist():
    watchlist = Watchlist.query.filter_by(user_id = current_user.get_id())
    return render_template('watchlist.html', watchlist = watchlist)