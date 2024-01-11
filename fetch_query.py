from time import sleep
import requests
import json
from cfg_parse import parse_auth
from datetime import timedelta, datetime

BACKEND_URL = "https://api-dashboard-staging.aucode.io"


def get_access_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    auth = parse_auth("BACKEND")
    data = {
        "username": auth["USERNAME"],
        "password": auth["PASSWORD"]
    }

    resp = requests.post(f'{BACKEND_URL}/login', headers=headers, data=data)
    return resp.json()["access_token"]


def get_backend_headers(access_tkn):
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_tkn}'
    }


def parse_response(resp):
    return json.loads(resp.json())


def create_job(query, start_dt, end_dt, access_tkn):
    params = {
        "search_query": query,
        "start": start_dt,
        "end": end_dt,
        "nickname": f"{query}_test"
    }

    resp = requests.post(f'{BACKEND_URL}/twitter/create-job', headers=get_backend_headers(access_tkn), params=params)
    return parse_response(resp)["job_id"]


def check_job_status(job_id, access_tkn):
    resp = requests.get(f'{BACKEND_URL}/twitter/job/{job_id}', headers=get_backend_headers(access_tkn))
    return parse_response(resp)["status"] == "success"


def get_graph_data(job_id, access_tkn):
    params = {
        "limit": 50,
        "service": "twitter"
    }

    resp = requests.get(f'{BACKEND_URL}/posts/gpt3_date_metric/{job_id}',
                        headers=get_backend_headers(access_tkn), params=params)
    return resp.json()


def format_date(dt):
    return dt.strftime('%Y-%m-%d')


def fetch_query_data(query, timeframe):
    dt_end = datetime.now()
    dt_start = dt_end - timedelta(weeks=timeframe)

    access_token = get_access_token()
    job_id = create_job(query, format_date(dt_start), format_date(dt_end), access_token)
    print(f"Created job {job_id}")

    while not check_job_status(job_id, access_token):
        print("Waiting for twitter job to finish.")
        sleep(5)
    print("Job succeeded")
    
    print("Fetching graph data")
    while not (graph_data := get_graph_data(job_id, access_token)):
        print("Waiting for gpt3 job to finish.")
        sleep(30)

    return graph_data


if __name__ == "__main__":
    print(fetch_query_data("(@Eskom_SA)", 1))
