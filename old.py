import json
import os
from mailchimp_marketing import Client, ApiClient
from mailchimp_marketing.api_client import ApiClient
import pandas as pd
from datetime import datetime

def old_report():
    with open("creds.json") as f:
        data = json.load(f)
        api_key = data["credentials"]["old"]["api_key"]
        server = data["credentials"]["old"]["server"]
    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })
    fields = ['reports.id','reports.campaign_title', 'reports.list_name', 'reports.subject_line', 'reports.preview_text',
              'reports.emails_sent', 'reports.unsubscribed', 'reports.send_time', 'reports.bounces.hard_bounces',
              'reports.bounces.soft_bounces', 'reports.forwards.forwards_count', 'reports.forwards.forwards_opens',
              'reports.opens.opens_total', 'reports.opens.unique_opens', 'reports.clicks.clicks_total',
              'reports.clicks.unique_clicks', 'reports.ab_split.a.bounces', 'reports.ab_split.a.unsubs',
              'reports.ab_split.a.recipient_clicks', 'reports.ab_split.a.forwards', 'reports.ab_split.a.forwards_opens',
              'reports.ab_split.a.opens', 'reports.ab_split.a.unique_opens', 'reports.ab_split.b.bounces',
              'reports.ab_split.b.unsubs', 'reports.ab_split.b.recipient_clicks', 'reports.ab_split.b.forwards',
              'reports.ab_split.b.forwards_opens', 'reports.ab_split.b.opens', 'reports.ab_split.b.unique_opens']
    response = mailchimp.reports.get_all_campaign_reports(count=1000,
                                                          fields=fields)
    response_list = []
    for n in range(len(response.get('reports'))):
        get_report = response.get('reports')[n]
        # print(get_report)
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
            response_list.append(response_dict)
        except ZeroDivisionError:
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
    today = datetime.today().strftime('%Y-%m-%d')
    pd.DataFrame(response_list).to_csv(f'{today}-old_hhhunt.csv', index=False)
    # old_data = pd.DataFrame(response_list)



