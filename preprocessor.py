import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    msgs = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    dataframe = pd.DataFrame({'user_msg': msgs, 'message_date': dates})
    # convert message_date type
    
    dataframe['message_date'] = pd.to_datetime(dataframe['message_date'], format='%d/%m/%y, %H:%M - ')

    dataframe.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    msgs = []
    for msg in dataframe['user_msg']:
        entry = re.split('([\w\W]+?):\s', msg)
        if entry[1:]:  # user name
            users.append(entry[1])
            msgs.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            msgs.append(entry[0])

    dataframe['user'] = users
    dataframe['msg'] = msgs
    dataframe.drop(columns=['user_msg'], inplace=True)

    dataframe['only_date'] = dataframe['date'].dt.date
    dataframe['year'] = dataframe['date'].dt.year
    dataframe['month_num'] = dataframe['date'].dt.month
    dataframe['month'] = dataframe['date'].dt.month_name()
    dataframe['day'] = dataframe['date'].dt.day
    dataframe['day_name'] = dataframe['date'].dt.day_name()
    dataframe['hour'] = dataframe['date'].dt.hour
    dataframe['minute'] = dataframe['date'].dt.minute

    period = []
    for hour in dataframe[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    dataframe['period'] = period

    return dataframe