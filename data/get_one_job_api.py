import flask
from flask import jsonify, abort

from . import db_session
from .job import Job

blueprint = flask.Blueprint(
    'get_job',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/get_job/<int:job_id>')
def get_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == job_id).first()
    if job:
        return jsonify(
            {
                'job':
                    job.to_dict(
                        only=(
                            'id',
                            'creater_id',
                            'politryk_id',
                            'name',
                            'plan',
                            'ids_tovarishei',
                            'start_of_piatiletka',
                            'end_of_piatiletka',
                            'result_of_plan'
                              ))
            }
        )
    else:
        return jsonify({'error': 'Invalid id'})

