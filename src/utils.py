import os
import re
import sys
import glob
import json
import datetime
from collections import Counter
from collections import Counter

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords


def break_combined_weeks(combined_weeks):
    """
    Breaks combined weeks into separate weeks.
    
    Args:
        combined_weeks: list of tuples of weeks to combine
        
    Returns:
        tuple of lists of weeks to be treated as plus one and minus one
    """
    plus_one_week = []
    minus_one_week = []

    for week in combined_weeks:
        if week[0] < week[1]:
            plus_one_week.append(week[0])
            minus_one_week.append(week[1])
        else:
            minus_one_week.append(week[0])
            plus_one_week.append(week[1])

    return plus_one_week, minus_one_week

def get_msgs_df_info(df):
    """
    Retrieves information about messages from a DataFrame.

    Args:
        df (DataFrame): The input DataFrame containing message data.

    Returns:
        tuple: A tuple containing dictionaries with the following information:
            - msgs_count_dict: A dictionary with user counts for messages sent.
            - replies_count_dict: A dictionary with user counts for replies made.
            - mentions_count_dict: A dictionary with user counts for mentions received.
            - links_count_dict: A dictionary with user counts for link occurrences.
    """
    msgs_count_dict = df.user.value_counts().to_dict()
    replies_count_dict = dict(Counter([u for r in df.replies if r != None for u in r]))
    mentions_count_dict = dict(Counter([u for m in df.mentions if m != None for u in m]))
    links_count_dict = df.groupby("user").link_count.sum().to_dict()
    return msgs_count_dict, replies_count_dict, mentions_count_dict, links_count_dict



def get_messages_dict(msgs):
    """
    Extracts relevant information from a list of messages and returns a dictionary.

    Args:
        msgs (list): A list of messages.

    Returns:
        dict: A dictionary containing the extracted information from the messages.
            The dictionary has the following keys:
            - 'msg_id': A list of message IDs.
            - 'text': A list of message texts.
            - 'attachments': A list of message attachments.
            - 'user': A list of user IDs who sent the messages.
            - 'mentions': A list of user IDs mentioned in the messages.
            - 'emojis': A list of emojis used in the messages.
            - 'reactions': A list of reactions received on the messages.
            - 'replies': A list of replies made to the messages.
            - 'replies_to': A list of timestamps indicating the messages being replied to.
            - 'ts': A list of timestamps for the messages.
            - 'links': A list of links found in the messages.
            - 'link_count': A count of the number of links found in the messages.
    """

    msg_list = {
            "msg_id":[],
            "text":[],
            "attachments":[],
            "user":[],
            "mentions":[],
            "emojis":[],
            "reactions":[],
            "replies":[],
            "replies_to":[],
            "ts":[],
            "links":[],
            "link_count":[]
            }


    for msg in msgs:
        if "subtype" not in msg:
            try:
                msg_list["msg_id"].append(msg["client_msg_id"])
            except:
                msg_list["msg_id"].append(None)
            
            msg_list["text"].append(msg["text"])
            msg_list["user"].append(msg["user"])
            msg_list["ts"].append(msg["ts"])
            
            if "reactions" in msg:
                msg_list["reactions"].append(msg["reactions"])
            else:
                msg_list["reactions"].append(None)

            if "parent_user_id" in msg:
                msg_list["replies_to"].append(msg["ts"])
            else:
                msg_list["replies_to"].append(None)

            if "thread_ts" in msg and "reply_users" in msg:
                msg_list["replies"].append(msg["replies"])
            else:
                msg_list["replies"].append(None)
            
            if "blocks" in msg:
                emoji_list = []
                mention_list = []
                link_count = 0
                links = []
                
                for blk in msg["blocks"]:
                    if "elements" in blk:
                        for elm in blk["elements"]:
                            if "elements" in elm:
                                for elm_ in elm["elements"]:
                                    
                                    if "type" in elm_:
                                        if elm_["type"] == "emoji":
                                            emoji_list.append(elm_["name"])

                                        if elm_["type"] == "user":
                                            mention_list.append(elm_["user_id"])
                                        
                                        if elm_["type"] == "link":
                                            link_count += 1
                                            links.append(elm_["url"])


                msg_list["emojis"].append(emoji_list)
                msg_list["mentions"].append(mention_list)
                msg_list["links"].append(links)
                msg_list["link_count"].append(link_count)
            else:
                msg_list["emojis"].append(None)
                msg_list["mentions"].append(None)
                msg_list["links"].append(None)
                msg_list["link_count"].append(0)
    
    return msg_list

def from_msg_get_replies(msg):
    """
    Extracts replies from a message and returns a list of reply messages.

    Args:
        msg (dict): A dictionary representing a message.

    Returns:
        list: A list of reply messages extracted from the input message.
            Each reply message is represented as a dictionary and contains the following keys:
            - 'thread_ts': The thread timestamp of the original message.
            - 'message_id': The client message ID of the original message.
            Additional keys and values are extracted from the replies themselves.
            If no replies are found or if the input message does not contain the necessary keys,
            an empty list is returned.
    """
    replies = []
    if "thread_ts" in msg and "replies" in msg:
        try:
            for reply in msg["replies"]:
                reply["thread_ts"] = msg["thread_ts"]
                reply["message_id"] = msg["client_msg_id"]
                replies.append(reply)
        except:
            pass
    return replies

def msgs_to_df(msgs):
    """
    Converts a list of messages into a pandas DataFrame.

    Args:
        msgs (list): A list of messages.

    Returns:
        DataFrame: A pandas DataFrame containing the extracted information from the messages.
            The DataFrame has columns corresponding to different message attributes, such as
            'msg_id', 'text', 'attachments', 'user', 'mentions', 'emojis', 'reactions', 'replies',
            'replies_to', 'ts', 'links', and 'link_count'.
    """
    msg_list = get_messages_dict(msgs)
    df = pd.DataFrame(msg_list)
    return df

def process_msgs(msg):
    """
    Selects important columns from a message and extracts its replies.

    Args:
        msg (dict): A dictionary representing a message.

    Returns:
        tuple: A tuple containing two elements:
            - The first element is a dictionary containing selected columns from the message.
              The dictionary has keys such as 'client_msg_id', 'type', 'text', 'user', 'ts',
              'team', 'thread_ts', 'reply_count', and 'reply_users_count'.
            - The second element is a list of reply messages extracted from the input message.
              Each reply message is represented as a dictionary and contains various keys and values.
    """
    keys = ["client_msg_id", "type", "text", "user", "ts", "team", "thread_ts", "reply_count", "reply_users_count"]
    msg_list = {k: msg[k] for k in keys}
    rply_list = from_msg_get_replies(msg)

    return msg_list, rply_list

def get_messages_from_channel(channel_path):
    """
    Retrieves all the messages from a channel.

    Args:
        channel_path (str): The path to the channel directory.

    Returns:
        DataFrame: A pandas DataFrame containing the extracted information from the messages in the channel.
            The DataFrame has columns corresponding to different message attributes, such as
            'msg_id', 'text', 'attachments', 'user', 'mentions', 'emojis', 'reactions', 'replies',
            'replies_to', 'ts', 'links', and 'link_count'.
    """
    channel_json_files = os.listdir(channel_path)
    channel_msgs = [json.load(open(channel_path + "/" + f)) for f in channel_json_files]

    df = pd.concat([pd.DataFrame(get_messages_dict(msgs)) for msgs in channel_msgs])
    print(f"Number of messages in channel: {len(df)}")

    return df
def convert_2_timestamp(column, data):
    """convert from unix time to readable timestamp
        args: column: columns that needs to be converted to timestamp
                data: data that has the specified column
    """
    if column in data.columns.values:
        timestamp_ = []
        for time_unix in data[column]:
            if time_unix == 0:
                timestamp_.append(0)
            else:
                a = datetime.datetime.fromtimestamp(float(time_unix))
                timestamp_.append(a.strftime('%Y-%m-%d %H:%M:%S'))
        return timestamp_
    else: 
        print(f"{column} not in data")

def get_tagged_users(df):
    """get all @ in the messages"""

    return df['msg_content'].map(lambda x: re.findall(r'@U\w+', x))


    
def map_userid_2_realname(user_profile: dict, comm_dict: dict, plot=False):
    """
    map slack_id to realnames
    user_profile: a dictionary that contains users info such as real_names
    comm_dict: a dictionary that contains slack_id and total_message sent by that slack_id
    """
    user_dict = {} # to store the id
    real_name = [] # to store the real name
    ac_comm_dict = {} # to store the mapping
    count = 0
    # collect all the real names
    for i in range(len(user_profile['profile'])):
        real_name.append(dict(user_profile['profile'])[i]['real_name'])

    # loop the slack ids
    for i in user_profile['id']:
        user_dict[i] = real_name[count]
        count += 1

    # to store mapping
    for i in comm_dict:
        if i in user_dict:
            ac_comm_dict[user_dict[i]] = comm_dict[i]

    ac_comm_dict = pd.DataFrame(data= zip(ac_comm_dict.keys(), ac_comm_dict.values()),
    columns=['LearnerName', '# of Msg sent in Threads']).sort_values(by='# of Msg sent in Threads', ascending=False)
    
    if plot:
        ac_comm_dict.plot.bar(figsize=(15, 7.5), x='LearnerName', y='# of Msg sent in Threads')
        plt.title('Student based on Message sent in thread', size=20)
        
    return ac_comm_dict
