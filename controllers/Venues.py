from datetime import datetime

from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import func

from config import app, TIME_FORMAT, db, HOME_PAGE, multidict_to_dict
from forms import VenueForm
from models import Venue, Show


@app.route('/venues')
def venues():
    """
    List all venues
    """
    data = [
        {
            "city": location[0],
            "state": location[1],
            "venues": [
                {
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": len({x.artist_id for x in venue.shows})
                }
                for venue in Venue.query.filter(Venue.city == location[0], Venue.state == location[1]).all()
            ]
        }
        for location in Venue.query.with_entities(Venue.city, Venue.state).distinct()
    ]

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    """
    Search case-insensitive in venues
    """
    venues = Venue.query \
        .filter(func.lower(Venue.name)
                .like(f"%{request.form.get('search_term', '').lower()}%")) \
        .all()
    response = {
        "count": len(venues),
        "data": [{"id": venue.id, "name": venue.name, "num_upcoming_shows": len({x.artist_id for x in venue.shows})}
                 for venue in venues]
    }

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    """
    shows the venue page with the given venue_id
    """

    venue = Venue.query.get(venue_id)

    past_shows = [{
        "artist_id": x.artist_id,
        "artist_name": x.artist.name,
        "artist_image_link": x.artist.image_link,
        "start_time": x.start_time.strftime(TIME_FORMAT)
    } for x in Show.query.filter(Show.venue_id == venue_id, Show.start_time < datetime.now()).all()]

    upcoming_shows = [{
        "artist_id": x.artist_id,
        "artist_name": x.artist.name,
        "artist_image_link": x.artist.image_link,
        "start_time": x.start_time.strftime(TIME_FORMAT)
    } for x in Show.query.filter(Show.venue_id == venue_id, Show.start_time > datetime.now()).all()]

    shows = {"past_shows": past_shows, "upcoming_shows": upcoming_shows, "past_shows_count": len(past_shows),
             "upcoming_shows_count": len(upcoming_shows)}

    return render_template('pages/show_venue.html', venue={**venue.asdict(), **shows})


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        venue = Venue(name=request.form['name'], city=request.form['city'], state=request.form['state'],
                      address=request.form['address'], phone=request.form.get('phone', None),
                      genres=request.form.getlist('genres'),
                      image_link=request.form.get('image_link', None),
                      facebook_link=request.form.get('facebook_link', None),
                      website=request.form.get('website', None),
                      seeking_talent=request.form.get('seeking_talent', None) == 'y',
                      seeking_description=request.form.get('seeking_description', None))
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred:{e}\n Venue {request.form['name']} could not be listed.")
    finally:
        db.session.close()
    return render_template(HOME_PAGE)


@app.route('/venues/<venue_id>/delete', methods=["GET", "POST", "DELETE"])
def delete_venue(venue_id):
    print("venue", venue_id)
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash(f'Venue {venue.name} was successfully deleted!')
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred:{e} Venue {Venue.query.get(venue_id).name} could not be deleted.")
    finally:
        db.session.close()
    return render_template(HOME_PAGE)


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id).asdict()
    print(venue)
    form = VenueForm(**venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        data_from_form = multidict_to_dict(request.form)
        data_from_form['seeking_talent'] = data_from_form.get('seeking_talent', "n") == 'y'
        db.session.query(Venue).filter_by(id=venue_id).update(data_from_form)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e} Venue {request.form['name']} could not be updated.")
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))
