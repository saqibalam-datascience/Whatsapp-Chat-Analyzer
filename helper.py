from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user,data):

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    # fetch the number of msgs
    num_messages = data.shape[0]

    # fetch the total number of words
    words = []
    for msg in data['msg']:
        words.extend(msg.split())

    # fetch number of media msgs
    num_media_messages = data[data['msg'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for msg in data['msg']:
        links.extend(extract.find_urls(msg))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(data):
    x = data['user'].value_counts().head()
    data = round((data['user'].value_counts() / data.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,data

def create_wordcloud(selected_user,data):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    temp_var = data[data['user'] != 'group_notification']
    temp_var = temp_var[temp_var['msg'] != '<Media omitted>\n']

    def remove_stop_words(msg):
        y = []
        for word in msg.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp_var['msg'] = temp_var['msg'].apply(remove_stop_words)
    df_whatsapp_chat = wc.generate(temp_var['msg'].str.cat(sep=" "))
    return df_whatsapp_chat

def most_common_words(selected_user,data):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    temp_var = data[data['user'] != 'group_notification']
    temp_var = temp_var[temp_var['msg'] != '<Media omitted>\n']

    words = []

    for msg in temp_var['msg']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    emojis = []
    for msg in data['msg']:
        emojis.extend([c for c in msg if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,data):

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    timeline = data.groupby(['year', 'month_num', 'month']).count()['msg'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,data):

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    daily_timeline = data.groupby('only_date').count()['msg'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,data):

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    return data['day_name'].value_counts()

def month_activity_map(selected_user,data):

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    return data['month'].value_counts()

def activity_heatmap(selected_user,data):

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    user_heatmap = data.pivot_table(index='day_name', columns='period', values='msg', aggfunc='count').fillna(0)

    return user_heatmap















