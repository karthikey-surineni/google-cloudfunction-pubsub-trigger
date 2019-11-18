
def run_build_trigger(payload):
    import requests
    import google-api-python-client
    trigger_id = "0ca14cd0-be48-4ae3-9087-27ee495a55f4"
    project_id = "cb-dataflow-python"
    url = "https://cloudbuild.googleapis.com/v1/projects/{projectId}/triggers/{triggerId}:run".format(projectId=project_id,triggerId=trigger_id)
    data = '''
    {{
    "projectId": cb-dataflow-python,
    "repoName": dataflow-python,
    "dir": ./dataflow/,
    "substitutions":{{
        "_SOURCE_DATASET":{source_dataset},
        "_SOURCE_TABLE": {source_table}
    }}
    }}'''.format(source_dataset=payload["SOURCE_DATASET"],source_table=payload["SOURCE_TABLE"])
    response = requests.post(url=url,data=data)
    return response

def cf_pubsub_trigger(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """
    import base64
    import json

    print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))

    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')
        payload = json.loads(name)
        response = run_build_trigger(payload)
    else:
        response = {}
    print('Response {response}'.format(response=response))