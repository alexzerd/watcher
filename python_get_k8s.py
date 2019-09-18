#import kubernetes.client
#from kubernetes import config
#from kubernetes.client.rest import ApiException
import json
import yaml
import requests
import pprint

#namespace_json = json.dumps(eval(str(namespace)), indent=4, sort_keys=True, default=str)
#namespace_dict = json.loads(namespace_json)    

#with open("tasks.yaml", 'r') as stream:
#       tasks = yaml.safe_load(stream)

token = ''
with open("/var/run/secrets/kubernetes.io/serviceaccount/token", 'r') as stream:
       token = stream.read()

url = 'https://kubernetes.default.svc.cluster.local/api/v1/namespaces/testns1'
headers = { 'Authorization': "Bearer %s" % token }
r = requests.get(url, headers=headers, verify=False)
pprint.pprint(r.json())
