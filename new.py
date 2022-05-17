import os
from mailchimp_marketing import Client, ApiClient
from mailchimp_marketing.api_client import ApiClient
import pandas as pd
from datetime import datetime
import json


def new_report():
    '''
    Creates a new report from included fields below.

    :return: A dataframe written to a csv file in a 'new-reports' folder. If you've forked this copy, either create a 'new-reports' directory or remove it from the .to_csv method at the end of the function
    '''
    # Uses json file as credentials, either replace this block with your own api key and server, or use a
    # 'creds.json' file
    with open("creds.json") as f:
        data = json.load(f)
        api_key = data["credentials"]["new"]["api_key"]
        server = data["credentials"]["new"]["server"]
    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })
    fields = ['reports.id','reports.campaign_title', 'reports.list_name', 'reports.subject_line', 'reports.preview_text',
              'reports.emails_sent', 'reports.unsubscribed', 'reports.send_time', 'reports.bounces.hard_bounces',
              'reports.bounces.soft_bounces', 'reports.forwards.forwards_count', 'reports.forwards.forwards_opens',
              'reports.opens.opens_total', 'reports.opens.unique_opens', 'reports.clicks.clicks_total',
              'reports.clicks.unique_clicks']
    response = mailchimp.reports.get_all_campaign_reports(count=1000,
                                                          fields=fields)
    response_list = []
    for n in range(len(response.get('reports'))):
        get_report = response.get('reports')[n]
        # print(get_report)
        # converting date and time for processing
        try:
            date_sent = datetime(year=int(get_report.get('send_time').split('T')[0].split('-')[0]),
                                      month=int(get_report.get('send_time').split('T')[0].split('-')[1]),
                                      day=int(get_report.get('send_time').split('T')[0].split('-')[2]))
            time_sent = datetime(year=int(get_report.get('send_time').split('T')[0].split('-')[0]),
                                      month=int(get_report.get('send_time').split('T')[0].split('-')[1]),
                                      day=int(get_report.get('send_time').split('T')[0].split('-')[2]),
                                      hour=int(get_report.get('send_time').split('T')[1].split(':')[0]) - 4)
        except ValueError:
            time_sent = None
        try:
            if time_sent is None:
                # contains the data from the request above if the time_sent isn't included
                response_dict = {
                    'id': get_report.get('id'),
                    'campaign_title': get_report.get('campaign_title'),
                    'audience': get_report.get('list_name'),
                    'subject_line': get_report.get('subject_line'),
                    'preview_text': get_report.get('preview_text'),
                    'emails_sent': get_report.get('emails_sent'),
                    'unsubscribed': get_report.get('unsubscribed'),
                    'send_date': date_sent,
                    'send_hour': None,
                    'hard_bounces': get_report.get('bounces').get('hard_bounces'),
                    'soft_bounces': get_report.get('bounces').get('soft_bounces'),
                    'number_of_forwards': get_report.get('forwards').get('forwards_count'),
                    'number_of_forwards_opened': get_report.get('forwards').get('forwards_opens'),
                    'total_opens': get_report.get('opens').get('opens_total'),
                    'unique_opens': get_report.get('opens').get('unique_opens'),
                    'unique_open_rate': get_report.get('opens').get('unique_opens') / get_report.get('emails_sent'),
                    'total_clicks': get_report.get('clicks').get('clicks_total'),
                    'unique_clicks': get_report.get('clicks').get('unique_clicks'),
                    'true_ctr': get_report.get('clicks').get('clicks_total') / get_report.get('opens').get('opens_total'),
                }
            else:
                # contains the data from the request above if the time sent is included
                response_dict = {
                    'id': get_report.get('id'),
                    'campaign_title': get_report.get('campaign_title'),
                    'audience': get_report.get('list_name'),
                    'subject_line': get_report.get('subject_line'),
                    'preview_text': get_report.get('preview_text'),
                    'emails_sent': get_report.get('emails_sent'),
                    'unsubscribed': get_report.get('unsubscribed'),
                    'send_date': date_sent,
                    'send_hour': time_sent.strftime('%I %p'),
                    'hard_bounces': get_report.get('bounces').get('hard_bounces'),
                    'soft_bounces': get_report.get('bounces').get('soft_bounces'),
                    'number_of_forwards': get_report.get('forwards').get('forwards_count'),
                    'number_of_forwards_opened': get_report.get('forwards').get('forwards_opens'),
                    'total_opens': get_report.get('opens').get('opens_total'),
                    'unique_opens': get_report.get('opens').get('unique_opens'),
                    'unique_open_rate': get_report.get('opens').get('unique_opens') / get_report.get('emails_sent'),
                    'total_clicks': get_report.get('clicks').get('clicks_total'),
                    'unique_clicks': get_report.get('clicks').get('unique_clicks'),
                    'true_ctr': get_report.get('clicks').get('clicks_total') / get_report.get('opens').get('opens_total'),
                }
            # adds to the response_list above to be used as a DataFrame
            response_list.append(response_dict)
        except ZeroDivisionError:
            # to account for math errors
            response_dict = {
                'id': get_report.get('id'),
                'campaign_title': get_report.get('campaign_title'),
                'audience': get_report.get('list_name'),
                'subject_line': get_report.get('subject_line'),
                'preview_text': get_report.get('preview_text'),
                'emails_sent': get_report.get('emails_sent'),
                'unsubscribed': get_report.get('unsubscribed'),
                'send_date': date_sent,
                'send_hour': time_sent.strftime('%I %p'),
                'hard_bounces': get_report.get('bounces').get('hard_bounces'),
                'soft_bounces': get_report.get('bounces').get('soft_bounces'),
                'number_of_forwards': get_report.get('forwards').get('forwards_count'),
                'number_of_forwards_opened': get_report.get('forwards').get('forwards_opens'),
                'total_opens': get_report.get('opens').get('opens_total'),
                'unique_opens': get_report.get('opens').get('unique_opens'),
                'unique_open_rate': get_report.get('opens').get('unique_opens') / get_report.get('emails_sent'),
                'total_clicks': get_report.get('clicks').get('clicks_total'),
                'unique_clicks': get_report.get('clicks').get('unique_clicks'),
                'true_ctr': 0,
            }
            response_list.append(response_dict)

    new_data = pd.DataFrame(response_list)
    today = datetime.today().strftime('%Y-%m-%d')
    new_data.to_csv(f'new-reports/{today}-new_hhhunt.csv',index=False)





