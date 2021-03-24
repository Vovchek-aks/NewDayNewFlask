import flask
from flask import jsonify, request

from . import db_session
from .job import Job

blueprint = flask.Blueprint(
    'add_jobs',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['politryk_id',
                  'creater_id',
                  'name',
                  'plan',
                  'ids_tovarishei',
                  'start_of_piatiletka',
                  'end_of_piatiletka',
                  'result_of_plan']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    job = Job(politryk_id=request.json['politryk_id'],
              creater_id=request.json['creater_id'],
              name=request.json['name'],
              plan=request.json['plan'],
              ids_tovarishei=request.json['ids_tovarishei'],
              start_of_piatiletka=request.json['start_of_piatiletka'],
              end_of_piatiletka=request.json['end_of_piatiletka'],
              result_of_plan=request.json['result_of_plan'])

    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})

