from flask_wtf import FlaskForm
from wtforms.fields import FloatField, TextAreaField, SubmitField, StringField, PasswordField, SelectField, FileField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets.html5 import NumberInput


#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("Username:", validators=[InputRequired('Enter username')])
    password=PasswordField("Password:", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")


 # this is the registration form
class RegisterForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    email_id = StringField("Email Address:", validators=[Email("Please enter a valid email address!")])
    phone = IntegerField('Contact Number:', validators=[InputRequired("Please enter a valid phone number!")])
    address = StringField('Mailing Address:', validators=[InputRequired()])
    
    # add buyer/seller - check if it is a buyer or seller hint : Use RequiredIf field
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password:", validators=[InputRequired(), EqualTo('confirm', message="Passwords must match!")])
    confirm = PasswordField("Confirm Password:")

    # submit button
    submit = SubmitField("Register")


class CreateListingForm(FlaskForm):
    # Variables
    categories = ['Acoustic Guitar', 'Electric/Rock Guitar', 'Bass Guitar', 'Piano/Keyboard', 'Drums & Percussion', 'Electronic/MIDI/Synth', 'Orchestra/Strings', 'Jazz/Woodwind',  'Studio Hardware/Recording', "DJ Mixers/CDJ's", 'Other']
    categories_list = [(status, status) for status in categories]
    ALLOWED_FILE = {"png", "jpg", "jpeg", "JPG", "PNG"}

    # Objects
    title = StringField('Listing Title:', validators=[InputRequired("Please enter in the title of the listing."), Length(max=100)], render_kw={"placeholder": "*Enter title*"})
    startingBid = IntegerField("Starting minimum bid (minimum $1):", validators=[InputRequired("Please enter a valid starting bid price"), NumberRange(min=1, message="Please enter a valid starting price (minimum $1), rounded to a whole dollar")], render_kw={"placeholder": "$0"})   
    instrument = StringField('Instrument:', validators=[InputRequired("Please enter in the instrument."), Length(max=100, message = "You have exceed the character count (100).")], render_kw={"placeholder": "*Enter instrument (example: Nylon Guitar)*"})
    category = SelectField('Category:', choices=categories_list, default=1)
    model = StringField('Model:', validators=[InputRequired("Please enter in the model."), Length(max=100, message = "You have exceed the character count (100).")], render_kw={"placeholder": "*Insert the model/model number*"})
    brand = StringField('Brand:', validators=[InputRequired("Please enter in the brand."), Length(max=100, message = "You have exceed the character count (100).")], render_kw={"placeholder": "*Enter brand name*"})
    year = IntegerField('Year:', validators=[DataRequired(), NumberRange(min = 1000, max = 2020, message = "Please enter a valid year.")], render_kw={"placeholder": "*YYYY*"})
    colour = StringField('Colour:', validators=[InputRequired("Please enter in the colour(s)."), Length(min = 2, max = 100, message = "Please enter a valid colour.")], render_kw={"placeholder": "*Enter colour*"})
    description = TextAreaField("Description:", validators = [InputRequired("Please enter in a brief description"), Length(max=750, message = "You have exceeded your character count (750)")], render_kw={"placeholder": "*Insert any additional information about the listing here (up to 750 characters)*", "rows": "5"})
    image = FileField('Add image:', validators=[FileRequired(message='You must provide an image'), FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    submit = SubmitField("Create & Publish Listing")


 # this is the bidding form
class BidForm(FlaskForm):
    bidField = IntegerField("Bid Amount:", validators=[InputRequired("Please enter a valid bid price."), NumberRange(min=1, message="Please enter a valid bid as a rounded price (e.g, $20)")])

    # submit button
    bidSubmit = SubmitField("Bid")


# form to add a listing to user's watchlist
class AddToWatchlistForm(FlaskForm):
    addToWatchlist = SubmitField("Add to Watchlist")


# form to remove a listing from user's watchlist
class RemoveFromWatchlistForm(FlaskForm):
    removeFromWatchlist = SubmitField("Remove from Watchlist")



