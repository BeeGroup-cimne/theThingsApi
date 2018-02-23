import requests
import API.endpoints as endpoints
import pandas as pd
import dateutil.parser


def get_resources(token):
    response = requests.get(endpoints.resources_url.format(THING_TOKEN=token)).json()
    return [resp['key'] for resp in response]


def _create_parameters(**kwargs):
    params = "&".join(["=".join([k, str(v)]) for k, v in kwargs.items() if v is not None])
    params = "?" + params if params else ""
    return params


def get_values(token, device, limit=1000, start_date=None, end_date=None):
    dataframe = pd.DataFrame()
    while start_date <= end_date:
        start_date_str = start_date.strftime(format="%Y%m%d%H%M%S") if start_date else None
        end_date_str = end_date.strftime(format="%Y%m%d%H%M%S") if end_date else None
        response = requests.get(endpoints.read_url.format(THING_TOKEN=token,
                              KEY=device,
                              PARAMS=_create_parameters(limit=limit, startDate=start_date_str, endDate=end_date_str))).json()
        if response:
            dataframe_t = pd.DataFrame.from_records(response)
            dataframe_t = dataframe_t.rename(columns={"datetime":"timestamp", "key":"deviceId"})
            end_date = dateutil.parser.parse(min(dataframe_t.timestamp))
            dataframe = dataframe.append(dataframe_t)
        else:
            break
    return dataframe
