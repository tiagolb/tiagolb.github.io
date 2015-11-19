import sys
import re


class TwitterEntry:
    def __init__(self, direction, msg_id, username, user_id, avatar, content, timestamp):
        self.direction = direction
        self.msg_id = msg_id
        self.username = username
        self.user_id = user_id
        self.avatar = avatar
        self.content = content
        self.timestamp = timestamp

    def __eq__(self, other):
        return self.timestamp == other.timestamp and self.content == other.content

    def __hash__(self):
        return hash((self.timestamp, self.content))

    def __str__(self):
        return self.direction + ", " + self.msg_id + ", " + self.username + ", " + self.user_id + ", " + self.avatar + \
               ", " + self.content + ", " + self.timestamp

class NewModuleParser:
    def get_module_set(self, input_file):
        strings_joined = '\n'.join(input_file.readlines())

        processed_input = re.sub(r'\\(.)', r'\1', strings_joined)

        message_type = r'<div.*?DirectMessage--(sent|received).*?data-message-id="(\d+)'
        handler = r'a\s*href="/([^"]+?)".*?data-user-id="(\d+)'
        avatar = r'DMAvatar-image"\s*src="([^"]+?.jpe?g)".'
        content = r'class="TweetTextSize[^>]+?>([^<]+?)<'
        date = r'data-time="(\d+)"'

        talk_regex = re.compile(
            '.*?'.join([message_type, handler, avatar, content, date]),
            re.VERBOSE | re.DOTALL)

        talk = set(map(lambda t: TwitterEntry(t[0], t[1], t[2], t[3], t[4], t[5], t[6]),
                       talk_regex.findall(processed_input)))

        return map(lambda t: (t.direction, t.msg_id, t.username, t.user_id, t.avatar, t.content, t.timestamp), talk)

    def get_module_timeline(self, twitter_set):
        twitter_list = list(twitter_set)
        return sorted(twitter_list, key=lambda t_list: t_list[6])

    def get_timeline(self, input_file):
        twitter_set      = self.get_module_set(input_file)
        twitter_timeline = self.get_module_timeline(twitter_set)
        return twitter_timeline

import datetime
import os

AUDIT_DIR = "audit_result"
AUDIT_HTML = AUDIT_DIR + "/audit.html"
AUDIT_TEXT = AUDIT_DIR + "/audit.text"

def time_convert(time_long):
    return datetime.datetime.fromtimestamp(
        int(time_long)
    ).strftime('%Y-%m-%d %H:%M:%S')

class OutputFactory(object):

    verbose = False

    def __init__(self, verbose):
        self.verbose = verbose

    def module_output(self, input_list): pass

    def append(self, input_list):
            self.module_output(input_list)

class TextOutput(OutputFactory):

    def __format_twitter_message(self, message):
        messenger_id = message[2]+"("+message[3]+")"
        datetime = time_convert(message[6])
        formated_message = datetime +\
            " by " + messenger_id +\
            ":"   + message[5]
        return formated_message


    def module_output(self, input_list):
        if self.verbose:
                print "[*] TWITTER"
        file_handler = open(AUDIT_DIR + "/newTwitter.txt", "w")
        for twitter_tuple in input_list:
            message = self.__format_twitter_message(twitter_tuple)
            file_handler.write(message + "\n")
            if self.verbose:
                print "[+]", message
        file_handler.close()

###################################

def __create_directories():
    if not os.path.exists(AUDIT_DIR):
        os.makedirs(AUDIT_DIR)

def create_output_manager(verbose):
    __create_directories()
    output = TextOutput(verbose)
    return output

