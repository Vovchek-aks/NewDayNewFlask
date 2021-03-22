import flask
from flask import jsonify

from . import db_session
from .job import Job

blueprint = flask.Blueprint(
    'get_jobs',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/get_jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(
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
                 for item in jobs]
        }
    )


