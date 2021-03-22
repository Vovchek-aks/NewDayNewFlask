import flask
from flask import jsonify

from . import db_session
from .job import Job

blueprint = flask.Blueprint(
    'del_jobs',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/del_job/<int:job_id>', methods=['DELETE'])
def delete_news(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})

