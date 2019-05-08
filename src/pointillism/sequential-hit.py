import boto3
import datetime
import json

HIT_TYPE_ID = '37D300AOKNWAXMADSQZNL0933KXIDW'
LAYOUT_ID = '3D5J2DF5KQGO2LON470T6AXXPJT9PO'
SNS_TOPIC = 'arn:aws:sns:us-east-1:277402979440:crowd-art-pointillism-hit'
SANDBOX = True
EVENT_TYPES = ['AssignmentSubmitted']

endpoint_url = 'https://mturk-requester{}.us-east-1.amazonaws.com'.format(
    '-sandbox' if SANDBOX else '')

def lambda_handler(event, context):
    print('EVENT:', event)

    records = event['Records']
    first_record = records[0]
    sns = first_record['Sns']
    msg = sns['Message']
    msg = json.loads(msg)
    events = msg['Events']
    first_event = events[0]

    type_id = first_event['HITTypeId']
    if type_id != HIT_TYPE_ID:
        print('WRONG HIT TYPE ID:', type_id)
        return

    event_type = first_event['EventType']
    if event_type not in EVENT_TYPES:
        print('WRONG EVENT TYPE:', event_type)
        return

    parent_hit_id = first_event['HITId']
    print('PARENT HIT ID:', parent_hit_id)

    parent_assignment_id = first_event['AssignmentId']
    print('PARENT ASSIGNMENT ID:', parent_assignment_id)

    parent_timestamp = first_event['EventTimestamp']
    print('PARENT TIMESTAMP:', parent_timestamp)

    answer = first_event['Answer']
    data_start = answer.find('<FreeText>') + len('<FreeText>')
    data_end = answer.find('</FreeText>')
    data = answer[data_start:data_end]
    print('DATA:', data)

    publish_hit(data)


def publish_hit(data):
    client = boto3.client(
        'mturk',
        endpoint_url=endpoint_url,
    )

    resp = client.create_hit_with_hit_type(
        HITTypeId = HIT_TYPE_ID,
        MaxAssignments = 1,
        LifetimeInSeconds = int(datetime.timedelta(days=7).total_seconds()),
        HITLayoutId = LAYOUT_ID,
        HITLayoutParameters = [{'Name': 'data', 'Value': data}],
    )
    print('CREATE HIT RESPONSE:', resp)

    notification = {
        'Destination': SNS_TOPIC,
        'Transport': 'SNS',
        'Version': '2014-08-15',
        'EventTypes': EVENT_TYPES,
    }

    client.update_notification_settings(
        HITTypeId = HIT_TYPE_ID,
        Notification = notification,
    ) 
