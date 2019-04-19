import boto3
import datetime
import json

HIT_TYPE_ID = '3KTTL66PWHEWV8ZFDTHWRAEV3ELVHE'
LAYOUT_ID = '3WMOO8M43NBXEU3DVKBV8LDXYHD4LO'
SNS_TOPIC = 'arn:aws:sns:us-east-1:277402979440:crowd-art-pointillism-hit'
SANDBOX = True

endpoint_url = 'https://mturk-requester{}.us-east-1.amazonaws.com'.format(
    '-sandbox' if SANDBOX else '')

def lambda_handler(event, context):
    msg = event['Records'][0]['Sns']['Message']
    try:
        msg = msg['Events']
    except TypeError:
        print('Recovering from TypeError')
        msg = json.loads(msg)
        msg = msg['Events']
    msg = msg[0]
    msg = msg['Answer']
    msg_start = msg.find('<FreeText>') + len('<FreeText>')
    msg_end = msg.find('</FreeText>')
    msg = msg[msg_start:msg_end]
    print('MESSAGE:', msg)

    client = boto3.client(
        'mturk',
        endpoint_url=endpoint_url,
    )

    resp = client.create_hit_with_hit_type(
        HITTypeId = HIT_TYPE_ID,
        MaxAssignments = 1000,
        LifetimeInSeconds = int(datetime.timedelta(days=7).total_seconds()),
        HITLayoutId = LAYOUT_ID,
        HITLayoutParameters = [{'Name': 'data', 'Value': msg}],
    )

    notification = {
        'Destination': SNS_TOPIC,
        'Transport': 'SNS',
        'Version': '2014-08-15',
        'EventTypes': ['AssignmentSubmitted']
    }

    client.update_notification_settings(
        HITTypeId = HIT_TYPE_ID,
        Notification = notification,
    )

    output = {
        'HIT_ID': resp['HIT']['HITId'],
        'HIT_GROUP_ID': resp['HIT']['HITGroupId'],
        'INPUT': msg,
    }
    print('OUTPUT:', output)
    return output
