import kopf
import requests
import time

from kr8s.objects import Deployment

@kopf.timer('qtedgeautoscalers', interval=15.0)
def timer_handler(**kwargs):
    arrival_rate, service_rate = poll_metrics()
    scale(arrival_rate, service_rate)

def scale(arrival_rate, service_rate):
    threshold = 0.05
    target = 300
    upperScale = 300 * (1+threshold)
    lowerScale = 300 * (1-threshold)
    vote = Deployment.get("vote", namespace="default")
    result = Deployment.get("result", namespace="default")
    traffic_intensity = arrival_rate / service_rate
    latency = 1 / (service_rate - arrival_rate)
    if latency > upperScale:
        vote_new_replicas = vote.replicas+1
        result_new_replicas = result.replicas+1
        vote.scale(vote_new_replicas)
        result.scale(result_new_replicas)
    if latency < lowerScale:
        if vote.replicas != 1:
            vote_new_replicas = vote.replicas-1
            vote.scale(vote_new_replicas)
        if result.replicas != 1:
            result_new_replicas = result.replicas-1
            result.scale(result_new_replicas)

def poll_metrics():
    res = requests.get('http://139.59.175.39:30909/api/v1/query', params={'query': 'traefik_entrypoint_requests_total', 'time': time.time()-60}).json() 
    total_requests_past = int(res['data']['result'][0]['value'][1])
    res = requests.get('http://139.59.175.39:30909/api/v1/query', params={'query': 'traefik_entrypoint_requests_total'}).json() 
    total_requests = int(res['data']['result'][0]['value'][1])
    new_requests = total_requests - total_requests_past
    arrival_rate = (new_requests) / 60
    res = requests.get('http://139.59.175.39:30909/api/v1/query', params={'query': 'traefik_entrypoint_requests_total', 'time': time.time()-60}).json() 
    total_service_time_past = int(res['data']['result'][0]['value'][1])
    res = requests.get('http://139.59.175.39:30909/api/v1/query', params={'query': 'traefik_entrypoint_requests_total'}).json()
    total_service_time = int(res['data']['result'][0]['value'][1])
    new_service_time = total_service_time - total_service_time_past
    service_rate = new_service_time / new_requests
    return (arrival_rate, service_rate)
