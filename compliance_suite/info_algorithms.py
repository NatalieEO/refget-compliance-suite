import requests
import json

INFO_ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.seq.v1.0.0+json'
}
INFO_API = 'sequence/service-info'


def base_algorithm(test, runner):
    if True is True:
        test.result = 1


def info_implement(test, runner):
    base_url = str(runner.base_url)
    response = requests.get(base_url + INFO_API, headers=INFO_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def info_implement_default(test, runner):
    base_url = str(runner.base_url)
    response = requests.get(base_url + INFO_API)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def info_circular(test, runner):
    base_url = str(runner.base_url)
    session_params = runner.session_params
    response = requests.get(base_url + INFO_API, headers=INFO_ACCEPT_HEADER)
    try:
        service_info_object = json.loads(response.text)["service"]
        test.result = 1
        if service_info_object['circular_supported'] == 'true':
            session_params['circular_supported'] = True
        else:
            session_params['circular_supported'] = False
    except:
        test.result = -1
        test.fail_text = test.fail_text + str(service_info_object)


def info_algorithms(test, runner):
    base_url = str(runner.base_url)
    session_params = runner.session_params
    response = requests.get(base_url + INFO_API, headers=INFO_ACCEPT_HEADER)
    try:
        service_info_object = json.loads(response.text)["service"]
        test.result = 1
        if 'trunc512' in service_info_object['algorithms']:
            session_params['trunc512'] = True
        else:
            session_params['trunc512'] = False
    except:
        test.result = -1
        test.fail_text = test.fail_text + str(service_info_object)


def info_subsequence(test, runner):
    base_url = str(runner.base_url)
    session_params = runner.session_params
    response = requests.get(base_url + INFO_API, headers=INFO_ACCEPT_HEADER)
    try:
        service_info_object = json.loads(response.text)["service"]
        session_params['subsequence_limit'] = int(service_info_object['subsequence_limit'])
        test.result = 1
    except:
        test.result = -1
        test.fail_text = test.fail_text + str(service_info_object)


def info_api_version(test, runner):
    base_url = str(runner.base_url)
    response = requests.get(base_url + INFO_API, headers=INFO_ACCEPT_HEADER)
    try:
        service_info_object = json.loads(response.text)["service"]
        if "supported_api_versions" in service_info_object:
            test.result = 1
    except:
        test.result = -1
        test.fail_text = test.fail_text + str(service_info_object)