from pprint import pprint
import requests


j = []

j += [requests.get('http://127.0.0.1:5000/api/get_jobs').json()]
j += [requests.get('http://127.0.0.1:5000/api/get_job/1').json()]
j += [requests.get('http://127.0.0.1:5000/api/get_job/3').json()]
j += [requests.get('http://127.0.0.1:5000/api/get_job/q').json()]

pprint(j)
