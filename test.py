from pprint import pprint
import requests


j = []

# j += [requests.get('http://127.0.0.1:5000/api/get_jobs').json()]
# j += [requests.get('http://127.0.0.1:5000/api/get_job/1').json()]
# j += [requests.get('http://127.0.0.1:5000/api/get_job/3').json()]
# j += [requests.get('http://127.0.0.1:5000/api/get_job/q').json()]

j += [requests.post('http://127.0.0.1:5000/api/jobs',
                    json={
                        'politryk_id': 1,
                        'creater_id': 1,
                        'name': 'ania loh',
                        'plan': 0,
                        'ids_tovarishei': '1',
                        'start_of_piatiletka': '1',
                        'end_of_piatiletka': '1',
                        'result_of_plan': True
                    })]

# j += [requests.delete('http://127.0.0.1:5000/api/del_job/3').json()]
# j += [requests.delete('http://127.0.0.1:5000/api/del_job/3').json()]
# j += [requests.delete('http://127.0.0.1:5000/api/del_job/щроца').json()]
pprint(j)
