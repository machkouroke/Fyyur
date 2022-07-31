from datetime import datetime

from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import func

from config import app, TIME_FORMAT, HOME_PAGE, db, multidict_to_dict
from forms import ArtistForm
from models import Artist, Show


@app.route('/artists')
def artists():
    data = [
        {
            "id": artist[0],
            "name": artist[1],

        }
        for artist in Artist.query.with_entities(Artist.id, Artist.name)
    ]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    """
        Search case-insensitive in venues
    """
    artists = Artist.query \
        .filter(func.lower(Artist.name)
                .like(f"%{request.form.get('search_term', '').lower()}%")) \
        .all()
    response = {
        "count": len(artists),
        "data": [{"id": artist.id, "name": artist.name, "num_upcoming_shows": len({x.venue_id for x in artist.shows})}
                 for artist in artists]
    }

    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    """shows the artist page with the given artist_id"""
    artist = Artist.query.get(artist_id)

    past_shows = [{
        "venue_id": x.artist_id,
        "venue_name": x.artist.name,
        "venue_image_link": x.artist.image_link,
        "start_time": x.start_time.strftime(TIME_FORMAT)
    } for x in Show.query.filter(Show.artist_id == artist_id, Show.start_time < datetime.now()).all()]

    upcoming_shows = [{
        "venue_id": x.artist_id,
        "venue_name": x.artist.name,
        "venue_image_link": x.artist.image_link,
        "start_time": x.start_time.strftime(TIME_FORMAT)
    } for x in Show.query.filter(Show.artist_id == artist_id, Show.start_time > datetime.now()).all()]

    shows = {"past_shows": past_shows, "upcoming_shows": upcoming_shows, "past_shows_count": len(past_shows),
             "upcoming_shows_count": len(upcoming_shows)}
    return render_template('pages/show_artist.html', artist={**artist.asdict(), **shows})


@app.route('/artists/<artist_id>/delete', methods=["GET", "POST", "DELETE"])
def delete_artist(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        db.session.delete(artist)
        db.session.commit()
        flash(f'Artist {artist.name} was successfully deleted!')
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred:{e} Artist {Artist.query.get(artist_id).name} could not be deleted.")
    finally:
        db.session.close()
    return render_template(HOME_PAGE)


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id).asdict()
    form = ArtistForm(**artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        data_from_form = multidict_to_dict(request.form)
        data_from_form['seeking_venue'] = data_from_form.get('seeking_venue', "n") == 'y'
        artist = Artist(**data_from_form)
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred:{e}\n Artist {request.form['name']} could not be listed.")
    finally:
        db.session.close()
    return render_template(HOME_PAGE)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        data_from_form = multidict_to_dict(request.form)
        data_from_form['seeking_venue'] = data_from_form.get('seeking_venue', 'n') == 'y'
        db.session.query(Artist).filter_by(id=artist_id).update(data_from_form)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        flash(f"An error occurred: {e} Artist {request.form['name']} could not be updated.")
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))
