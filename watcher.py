import kubernetes.client
from kubernetes import config
from kubernetes.client.rest import ApiException
import json
import yaml
from copy import deepcopy
import datetime
import time
from dateutil.tz import *
import requests
import socket



while True:
	config.load_incluster_config()
	cluster = kubernetes.client.CoreV1Api()
	cluster_ext = kubernetes.client.ExtensionsV1beta1Api()

	# init cluster state
	nodes = namespaces = pods = deployments = []
	services = configmaps = secrets = ingresses = []
	persistentVolumes = persistentVolumeClaims = []

	# tasks and results
	tasks = []
	tasksResults = [] # True / False


	def parseClusterState():
		global nodes, namespaces, pods, deployments, services
		global configmaps, secrets, persistentVolumes, persistentVolumeClaims

		try:
			nd = cluster.list_node(watch=False)
			for node in nd.items:
				node_json = json.dumps(eval(str(node)), indent=4, sort_keys=True, default=str)
				node_dict = json.loads(node_json)
				nodes.append(node_dict)
		except ApiException:
			nodes = []
		
		try:
			ns = cluster.list_namespace(watch=False)
			for namespace in ns.items:
				namespace_json = json.dumps(eval(str(namespace)), indent=4, sort_keys=True, default=str)
				namespace_dict = json.loads(namespace_json)
				nodes.append(namespace_dict)
		except ApiException:
			namespaces = []
		
		try:
			pd = cluster.list_pod_for_all_namespaces(watch=False)
			for pod in pd.items:
				pod_json = json.dumps(eval(str(pod)), indent=4, sort_keys=True, default=str)
				pod_dict = json.loads(pod_json)
				pods.append(pod_dict)
		except ApiException:
			pods = []
		
		try:	
			sv = cluster.list_service_for_all_namespaces(pretty=True, watch=False)
			for service in sv.items:
				service_json = json.dumps(eval(str(service)), indent=4, sort_keys=True, default=str)
				service_dict = json.loads(service_json)
				services.append(service_dict)
		except ApiException:
			services = []
		
		try:
			cm = cluster.list_config_map_for_all_namespaces(watch=False)
			for configmap in cm.items:
				configmap_json = json.dumps(eval(str(configmap)), indent=4, sort_keys=True, default=str)
				configmap_dict = json.loads(configmap_json)
				configmaps.append(configmap_dict)
		except ApiException:
			configmaps = []

		try:
			scr = cluster.list_secret_for_all_namespaces(watch=False)
			for secret in scr.items:
				secret_json = json.dumps(eval(str(secret)), indent=4, sort_keys=True, default=str)
				secret_dict = json.loads(secret_json)
				secrets.append(secret_dict)
		except ApiException:
			secrets = []

		try:
			pv = cluster.list_persistent_volume(watch=False)
			for persvol in pv.items:
				persvol_json = json.dumps(eval(str(persvol)), indent=4, sort_keys=True, default=str)
				persvol_dict = json.loads(persvol_json)
				persistentVolumes.append(persvol_dict)
		except ApiException:
			persistentVolumes = []

		try:
			pvc = cluster.list_persistent_volume_claim_for_all_namespaces(watch=False)
			for persvolclaim in pvc.items:
				persvolclaim_json = json.dumps(eval(str(persvolclaim)), indent=4, sort_keys=True, default=str)
				persvolclaim_dict = json.loads(persvolclaim_json)
				persistentVolumeClaims.append(persvolclaim_dict)
		except ApiException:
			persistentVolumeClaims = []

		# doesn't work
		try:
			dep = cluster_ext.list_deployment_for_all_namespaces(watch=False)
			for deploy in dep.items:
				deploy_json = json.dumps(eval(str(deploy)), indent=4, sort_keys=True, default=str)
				deploy_dict = json.loads(deploy_json)
				deployments.append(deploy_dict)
		except ApiException:
			deployments = []

		try:
			ing = cluster_ext.list_ingress_for_all_namespaces(watch=False)
			for ingress in ing.items:
				ingress_json = json.dumps(eval(str(ingress)), indent=4, sort_keys=True, default=str)
				ingress_dict = json.loads(ingress_json)
				ingresses.append(ingress_dict)
		except ApiException:
			ingresses = []


	def parseTasks():
		global tasks, tasksResults
		with open("tasks.yaml", 'r') as stream:
			try:
				tasks = yaml.safe_load(stream)
			except yaml.YAMLError:
				tasks = []


	def checkNamespace(currentNamespaces, taskNamespace):
		for namespace in currentNamespaces:
			namespace_copy = deepcopy(namespace)
			namespace_copy['metadata'].update(taskNamespace['metadata'])
			if namespace == namespace_copy:
				return True
		return False



	def tasksCompletionCheck():
		globals()
		for task in tasks:
			kind = task['kind']
			if kind == 'Namespace':
				del task['kind']
				tasksResults.append(checkNamespace(namespaces, task))
			elif kind == 'Pod':
				pass
			elif kind == 'Service':
				pass

	parseClusterState()
	parseTasks()
	tasksCompletionCheck()

	# print(yaml.dump(secrets))


	hostname = nodes[0]['metadata']['name'] # get hostname where cluster is running
	rating = round(tasksResults.count(True)/len(tasksResults), 2)
	results = " ".join(str(x) for x in tasksResults)
	current_time = datetime.datetime.now().strftime('%H:%M %m/%d/%y')
	answer = "PC-%s; rat.-%s; res: %s; %s" % (str(hostname), str(rating), results, str(current_time))

	# set values
	s = requests.get('http://frontend.default.svc.cluster.local/guestbook.php?cmd=set&key=messages&value=%s' % answer)

	# get values
	g = requests.get('http://frontend.default.svc.cluster.local/guestbook.php?cmd=get&key=messages')
	# print(g.json())

	print(answer)



	time.sleep(60)