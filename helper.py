from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji # Make sure emoji is imported

extract = URLExtract()

def fetch_stats(selected_user,df):
    # (Keep the rest of this function as it was)
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    # (Keep this function as it was)
    x = df['user'].value_counts().head()
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'}) # Adjusted column names based on potential pandas version
    return x,df_percent


def create_wordcloud(selected_user,df):
    # (Keep this function as it was)
    f = open('stop_hinglish.txt', 'r', encoding='utf-8') # Added encoding
    stop_words = f.read()
    f.close() # Close the file

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Filter out non-string messages just in case
    temp = temp[temp['message'].apply(lambda x: isinstance(x, str))]

    def remove_stop_words(message):
        y = []
        # Ensure message is treated as string
        for word in str(message).lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    # Apply stop word removal safely
    temp['message'] = temp['message'].apply(remove_stop_words)
    # Ensure there's text to generate the word cloud from
    text_corpus = temp['message'].str.cat(sep=" ")
    if text_corpus: # Check if the corpus is not empty
        df_wc = wc.generate(text_corpus)
        return df_wc
    else:
        # Return an empty word cloud or handle as needed
        # For now, generate a blank image or similar placeholder
        return wc.generate(" ") # Generate with a space to avoid error


def most_common_words(selected_user,df):
    # (Keep this function as it was)
    f = open('stop_hinglish.txt','r', encoding='utf-8') # Added encoding
    stop_words = f.read()
    f.close() # Close the file

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Filter out non-string messages
    temp = temp[temp['message'].apply(lambda x: isinstance(x, str))]

    words = []

    for message in temp['message']:
        for word in str(message).lower().split(): # Ensure message is string
            if word not in stop_words:
                words.append(word)

    # Check if words list is empty before creating DataFrame
    if not words:
        return pd.DataFrame(columns=[0, 1]) # Return empty DataFrame

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


# --- Start of Emoji Fix ---
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    # Filter out non-string messages first
    string_messages = df[df['message'].apply(lambda x: isinstance(x, str))]['message']

    for message in string_messages:
        # Use emoji.EMOJI_DATA which is available in newer versions
        # The keys of this dictionary are the emoji characters
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    # Check if emojis list is empty before creating DataFrame
    if not emojis:
        return pd.DataFrame(columns=[0, 1]) # Return empty DataFrame with expected columns

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
# --- End of Emoji Fix ---


def monthly_timeline(selected_user,df):
    # (Keep this function as it was)
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month'])['message'].count().reset_index() # Corrected groupby

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user,df):
    # (Keep this function as it was)
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date')['message'].count().reset_index() # Corrected groupby
    return daily_timeline


def week_activity_map(selected_user,df):
    # (Keep this function as it was)
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    # (Keep this function as it was)
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    # (Keep this function as it was)
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Check if 'period' column exists and df is not empty before pivoting
    if 'period' in df.columns and not df.empty:
        user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
        return user_heatmap
    else:
        # Return an empty DataFrame or handle appropriately if data is missing
        # Creating an empty DataFrame with expected index/columns might be safer for heatmap plotting
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        periods = [f"{h:02d}-{h+1:02d}" for h in range(24)] # Example period labels
        periods[-1] = "23-00" # Adjust last label
        return pd.DataFrame(0, index=days, columns=periods) # Return DataFrame filled with 0from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji # Make sure emoji is imported

extract = URLExtract()

def fetch_stats(selected_user,df):
    # (Keep the rest of this function as it was)
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    # (Keep this function as it was)
    x = df['user'].value_counts().head()
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'}) # Adjusted column names based on potential pandas version
    return x,df_percent


def create_wordcloud(selected_user,df):
    # (Keep this function as it was)
    f = open('stop_hinglish.txt', 'r', encoding='utf-8') # Added encoding
    stop_words = f.read()
    f.close() # Close the file

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Filter out non-string messages just in case
    temp = temp[temp['message'].apply(lambda x: isinstance(x, str))]

    def remove_stop_words(message):
        y = []
        # Ensure message is treated as string
        for word in str(message).lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    # Apply stop word removal safely
    temp['message'] = temp['message'].apply(remove_stop_words)
    # Ensure there's text to generate the word cloud from
    text_corpus = temp['message'].str.cat(sep=" ")
    if text_corpus: # Check if the corpus is not empty
        df_wc = wc.generate(text_corpus)
        return df_wc
    else:
        # Return an empty word cloud or handle as needed
        # For now, generate a blank image or similar placeholder
        return wc.generate(" ") # Generate with a space to avoid error


def most_common_words(selected_user,df):
    # (Keep this function as it was)
    f = open('stop_hinglish.txt','r', encoding='utf-8') # Added encoding
    stop_words = f.read()
    f.close() # Close the file

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Filter out non-string messages
    temp = temp[temp['message'].apply(lambda x: isinstance(x, str))]

    words = []

    for message in temp['message']:
        for word in str(message).lower().split(): # Ensure message is string
            if word not in stop_words:
                words.append(word)

    # Check if words list is empty before creating DataFrame
    if not words:
        return pd.DataFrame(columns=[0, 1]) # Return empty DataFrame

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


# --- Start of Emoji Fix ---
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    # Filter out non-string messages first
    string_messages = df[df['message'].apply(lambda x: isinstance(x, str))]['message']

    for message in string_messages:
        # Use emoji.EMOJI_DATA which is available in newer versions
        # The keys of this dictionary are the emoji characters
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    # Check if emojis list is empty before creating DataFrame
    if not emojis:
        return pd.DataFrame(columns=[0, 1]) # Return empty DataFrame with expected columns

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
# --- End of Emoji Fix ---


def monthly_timeline(selected_user,df):
    # (Keep this function as it was)
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month'])['message'].count().reset_index() # Corrected groupby

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user,df):
    # (Keep this function as it was)
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date')['message'].count().reset_index() # Corrected groupby
    return daily_timeline


def week_activity_map(selected_user,df):
    # (Keep this function as it was)
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    # (Keep this function as it was)
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    # (Keep this function as it was)
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Check if 'period' column exists and df is not empty before pivoting
    if 'period' in df.columns and not df.empty:
        user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
        return user_heatmap
    else:
        # Return an empty DataFrame or handle appropriately if data is missing
        # Creating an empty DataFrame with expected index/columns might be safer for heatmap plotting
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        periods = [f"{h:02d}-{h+1:02d}" for h in range(24)] # Example period labels
        periods[-1] = "23-00" # Adjust last label
        return pd.DataFrame(0, index=days, columns=periods) # Return DataFrame filled with 0