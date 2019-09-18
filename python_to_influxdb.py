from influxdb import InfluxDBClient
from datetime import datetime


client = InfluxDBClient(host='influxdb.default.svc.cluster.local', port=80, username='root', password='root', database='student')

client.create_database('student')
client.get_list_database()
client.switch_database('student')

current_time = datetime.now().isoformat(timespec='seconds')

json_body = [
    {
        "measurement": "tasks_status",
        "tags": {
            "user": "Ivan Ivanov",
        },
        "time": "%s" % (str(current_time)),
        "fields": {
            "task1": "READY",
            "task2": "NOT READY",
            "task3": "READY",
            "task4": "NOT READY",
            "task5": "NOT READY",
            "task6": "READY"
        }
    }
]

client.write_points(json_body)
client.query('SELECT * FROM "student"."autogen"."tasks_status" WHERE time > now() - 300d GROUP BY "user"')