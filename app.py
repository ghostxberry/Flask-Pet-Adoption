from flask import Flask, request, redirect, render_template, abort, flash, jsonify, url_for
from models import db, connect_db, Pet
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from forms import addPetForm, editPetForm

app = Flask(__name__)

app.debug = True

app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adopt.db'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


toolbar = DebugToolbarExtension(app)

connect_db(app)

migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


@app.route('/')
def root():
    return redirect("/pets")

@app.route('/pets')
def pets_index():
    "Show list of available pets"
    pets = Pet.query.order_by(Pet.name).all()
    return render_template('pets.html', pets = pets)


@app.route('/add', methods=["GET", "POST"])
def add_pet():
    "Add a pet"
    form = addPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()
        return redirect('/pets')
    else:
        return render_template('pet_add_form.html', form = form)


@app.route('/pets/<int:id>', methods=["GET", "POST"])
def pet_detail(id):
    "Show pet details and edit form"
    pet = Pet.query.get_or_404(id)
    form = editPetForm(obj=pet)
    
    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('pets_index'))  # Corrected route name

    return render_template('pet_detail.html', form=form, pet=pet)


        

if __name__ == '__main__':
     app.run()