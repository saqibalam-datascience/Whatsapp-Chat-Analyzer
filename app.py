import streamlit as stream
import preprocessor,helper
import matplotlib.pyplot as matplot
import seaborn as sns

stream.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = stream.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    data = preprocessor.preprocess(data)

    # fetch unique users
    user_list = data['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = stream.sidebar.selectbox("Show analysis wrt",user_list)

    if stream.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,data)
        stream.title("Top Statistics")
        col1, col2, col3, col4 = stream.columns(4)

        with col1:
            stream.header("Total Messages")
            stream.title(num_messages)
        with col2:
            stream.header("Total Words")
            stream.title(words)
        with col3:
            stream.header("Media Shared")
            stream.title(num_media_messages)
        with col4:
            stream.header("Links Shared")
            stream.title(num_links)

        # monthly timeline
        stream.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,data)
        fig,ax = matplot.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        matplot.xticks(rotation='vertical')
        stream.pyplot(fig)

        # daily timeline
        stream.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, data)
        fig, ax = matplot.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        matplot.xticks(rotation='vertical')
        stream.pyplot(fig)

        # activity map
        stream.title('Activity Map')
        col1,col2 = stream.columns(2)

        with col1:
            stream.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,data)
            fig,ax = matplot.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            matplot.xticks(rotation='vertical')
            stream.pyplot(fig)

        with col2:
            stream.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, data)
            fig, ax = matplot.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            matplot.xticks(rotation='vertical')
            stream.pyplot(fig)

        stream.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,data)
        fig,ax = matplot.subplots()
        ax = sns.heatmap(user_heatmap)
        stream.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            stream.title('Most Busy Users')
            x,new_data = helper.most_busy_users(data)
            fig, ax = matplot.subplots()

            col1, col2 = stream.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                matplot.xticks(rotation='vertical')
                stream.pyplot(fig)
            with col2:
                stream.dataframe(new_data)

        # WordCloud
        stream.title("Wordcloud")
        data_wc = helper.create_wordcloud(selected_user,data)
        fig,ax = matplot.subplots()
        ax.imshow(data_wc)
        stream.pyplot(fig)

        # most common words
        most_common_data = helper.most_common_words(selected_user,data)

        fig,ax = matplot.subplots()

        ax.barh(most_common_data[0],most_common_data[1])
        matplot.xticks(rotation='vertical')

        stream.title('Most commmon words')
        stream.pyplot(fig)

        # emoji analysis
        emoji_data = helper.emoji_helper(selected_user,data)
        stream.title("Emoji Analysis")

        col1,col2 = stream.columns(2)

        with col1:
            stream.dataframe(emoji_data)
        with col2:
            fig,ax = matplot.subplots()
            ax.pie(emoji_data[1].head(),labels=emoji_data[0].head(),autopct="%0.2f")
            stream.pyplot(fig)











