from flask import render_template, request, flash

from config import app, TIME_FORMAT, db, HOME_PAGE
from forms import ShowForm
from models import Show


@app.route('/shows')
def shows():
    """displays list of shows at /shows"""

    data = [{**show.asdict(),
             **{"venue_name": show.venue.name},
             **{"artist_name": show.artist.name, "artist_image_link": show.artist.image_link}}
            for show in Show.query.all()]
    for show in data:
        show['start_time'] = show['start_time'].strftime(TIME_FORMAT)

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        show = Show(artist_id=request.form['artist_id'], venue_id=request.form['venue_id'],
                    start_time=request.form['start_time'])
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e} Show could not be listed.')
    finally:
        db.session.close()

    return render_template(HOME_PAGE)
