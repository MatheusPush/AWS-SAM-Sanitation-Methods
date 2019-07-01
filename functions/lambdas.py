from utils import cnj_sanitization, date_sanitization, num_sanitization, filter_date, filter_num
import json


def format_cnj(event, context):
    cnjs = event['queryStringParameters'].get("data")

    if cnjs is None:
        return {"statusCode": 400,
                "body": "Invalid params"}

    cnjs = json.loads(cnjs)
    if type(cnjs) == list:
        for i in range(len(cnjs)):
            cnjs[i] = cnj_sanitization(cnjs[i])
    elif type(cnjs) == str:
        cnjs = cnj_sanitization(cnjs)

    return {"statusCode": 200,
            "body": json.dumps({"Formated CNJs": cnjs})}


def format_date(event, context):
    dates = event['queryStringParameters'].get("data")

    if dates is None:
        return {"statusCode": 400,
                "body": "Invalid params"}

    dates = json.loads(dates)
    if type(dates) == list:
        for i in range(len(dates)):
            dates[i] = date_sanitization(dates[i])
    elif type(dates) == str:
        dates = date_sanitization(dates)

    return {"statusCode": 200,
            "body": json.dumps({"Formated Dates": dates})}


def format_number(event, context):
    number = event['queryStringParameters'].get("data")

    if number is None:
        return {"statusCode": 400,
                "body": "Invalid params"}

    number = json.loads(number)
    if type(number) == list:
        for i in range(len(number)):
            number[i] = num_sanitization(number[i])
    elif type(number) == str:
        number = num_sanitization(number)

    return {"statusCode": 200,
            "body": json.dumps({"Formated Dates": number})}

def full_sanitization(event, context):
    data = event['queryStringParameters'].get("data")
    rules = event['queryStringParameters'].get("rules")

    if None in [data, rules]:
        return {"statusCode": 400,
                "body": "Invalid params"}

    data = json.loads(data)
    rules = json.loads(rules)

    # Formats
    if rules.get('format_cnj') is not None:
        for col in rules['format_cnj']:
            for i, v in data[col].items():
                data[col][i] = cnj_sanitization(data[col][i])

    if rules.get('format_date') is not None:
        for col in rules['format_date']:
            for i, v in data[col].items():
                data[col][i] = date_sanitization(data[col][i])

    if rules.get('format_number') is not None:
        for col in rules['format_number']:
            for i, v in data[col].items():
                data[col][i] = num_sanitization(data[col][i])

    # Filters
    if rules.get('filter_date') is not None:
        for col, interval in rules['filter_date'].items():
            for i, v in data[col].items():
                data[col][i] = filter_date(data[col][i], interval[0], interval[1])

    if rules.get('filter_number') is not None:
        for col, interval in rules['filter_number'].items():
            for i, v in data[col].items():
                data[col][i] = filter_num(data[col][i], interval[0], interval[1])

    return {"statusCode": 200,
            "body": json.dumps({"Formated Data": data})}

