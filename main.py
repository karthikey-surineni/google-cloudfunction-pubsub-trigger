
def run_build_trigger(data):
    import requests
    trigger_id = "0ca14cd0-be48-4ae3-9087-27ee495a55f4"
    project_id = "cb-dataflow-python"
    url = "https://cloudbuild.googleapis.com/v1/projects/{projectId}/triggers/{triggerId}:run".format(projectId=project_id,triggerid=trigger_id)
    data = '''
    {
    "projectId": cb-dataflow-python,
    "repoName": dataflow-python,
    "dir": ./dataflow/
    }'''
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
        data = json.loads(name)
        response = run_build_trigger(data)
    else:
        name = 'World'
    print('Hello {}!'.format(name))

def hello_error_1(request):
    # [START functions_helloworld_error]
    # This WILL be reported to Stackdriver Error
    # Reporting, and WILL NOT show up in logs or
    # terminate the function.
    from google.cloud import error_reporting
    client = error_reporting.Client()

    try:
        raise RuntimeError('I failed you')
    except RuntimeError:
        client.report_exception()

    # This WILL be reported to Stackdriver Error Reporting,
    # and WILL terminate the function
    raise RuntimeError('I failed you')

    # [END functions_helloworld_error]

def hello_error_2(request):
    # [START functions_helloworld_error]
    # WILL NOT be reported to Stackdriver Error Reporting, but will show up
    # in logs
    import logging
    print(RuntimeError('I failed you (print to stdout)'))
    logging.warn(RuntimeError('I failed you (logging.warn)'))
    logging.error(RuntimeError('I failed you (logging.error)'))
    sys.stderr.write('I failed you (sys.stderr.write)\n')
    # This WILL be reported to Stackdriver Error Reporting
    from flask import abort
    return abort(500)
    # [END functions_helloworld_error]