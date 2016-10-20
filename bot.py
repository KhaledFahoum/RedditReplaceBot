import praw
import time
import re
import sys
import os.path


''' CONSTANTS '''
# Set to: '1' to only print comments, '0' to enable posting.
debug_mode = 0
username = '<YOUR_USERNAME>'
password = '<YOUR_PASSWORD>'
bot_comment_text = '<YOUR_CUSTOM_REPLY>'
# Add more subreddits to crawl them.
subreddits = ['funny', 'pics', 'todayilearned', 'IAmA', 'videos', 'gaming', 'movies', 'gifs']
# Enter your (keyword,replacement) values here, split across the 2 lists in order.
keywords_original = ['before1', 'before2', 'before3']
keywords_substitute = ['after1', 'after2', 'after3']
comment_history_filename = 'bot_comment_history.txt'
submission_count = 10
sleep_interval = 10*60

''' log_reply(): writes to stdout whenever a new comment
    is posted.  '''


def log_reply(reply):
    print '============ New Reply ============'
    print reply


''' build_reply(): Builds a bot reply from a given comment by
    substituting keywords with their replacements. '''


def build_reply(comment):
    i = 0
    for keyword in keywords_original:
        regex = r'\b'+re.escape(keyword)+r'\b'
        comment = re.sub(regex, '**' + keywords_substitute[i] + '**', comment)
        i += 1
    reply_prefix = ">"
    reply_suffix = '\n\n'+bot_comment_text

    # Catching Reddit-style newlines '\n\n' to add quotes.
    regex = r'\n\n'
    comment = re.sub(regex, '\n\n' + reply_prefix, comment)
    return reply_prefix + comment + reply_suffix


''' handle_comment(): Checks if a comment contains any of the keywords,
    and if found, builds a reply and posts it. '''


def handle_comment(comment, submission_id):
    relevant_flag = 0
    if not isinstance(comment, praw.objects.Comment):
        return
    comment_unique_id = str(comment.id)+'_'+str(submission_id)
    if comment_unique_id in comment_history_list:
        return
    comment_text = comment.body
    if comment_text is None or comment_text == '':
        return

    # Checking if the comment contains a keyword.
    for keyword in keywords_original:
        regex = r'\b'+re.escape(keyword)+r'\b'
        if re.search(regex, comment_text):
            relevant_flag = 1
            break
    if relevant_flag == 0:
        return

    # Building and posting a reply to the comment.
    bot_reply = build_reply(comment_text)
    try:
        if debug_mode == 0:
            comment.reply(bot_reply)
        log_reply(bot_reply)
    except Exception, e:
        print str(e)
        sys.exit(1)

    # Track comment ID to avoid commenting again.
    comment_history_list.append(comment_unique_id)
    comment_history_file.write('\n' + str(comment_unique_id))
    comment_history_file.flush()
    if debug_mode == 0:
        time.sleep(sleep_interval)


# ENTRY POINT
r = praw.Reddit(user_agent='Rob')
r.login(username, password, disable_warning=True)

# Setting up own comment history.
comment_history_list = []
if not os.path.isfile(comment_history_filename):
    open(comment_history_filename, 'a').close()
comment_history_file = open(comment_history_filename, 'r')
tagged_comments_history = comment_history_file.read().splitlines()
comment_history_list += tagged_comments_history
comment_history_file = open(comment_history_filename, 'a+')


'''
# To monitor '/r/all'.
while True:
    flat_comments = praw.helpers.flatten_tree(r.get_comments('all'))
    for new_comment in flat_comments:
        handle_comment(new_comment)
'''

# To monitor specific subreddits.
subreddit_index = -1
while True:
    # Iterate on subreddits.
    subreddit_index += 1
    subreddit_index %= len(subreddits)
    subreddit = r.get_subreddit(subreddits[subreddit_index])
    for submission in subreddit.get_hot(limit=submission_count):
        submission.replace_more_comments(limit=None, threshold=0)
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for in_comment in flat_comments:
            handle_comment(in_comment, submission.id)