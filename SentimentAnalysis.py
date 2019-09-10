import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='RbjmP9V5ptcxdA',
                     client_secret='N5LFwc_DadQWrpSzQDvMoC8BW4M',
                     user_agent='my user agent'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def get_text_negative_proba(text):
   return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
   return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
   return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments


def process_comments(comment_list, neg_list, pos_list, neu_list):
    for comment in comment_list:
        # runs comments/replies through probability methods
        neg = get_text_negative_proba(comment.body)
        pos = get_text_positive_proba(comment.body)
        neu = get_text_neutral_proba(comment.body)
        # compare results and determine
        if neg > pos and neg > neu:
            neg_list.append(comment.body)
        if pos > neu and pos > neg:
            pos_list.append(comment.body)
        if neu > neg and neu > pos:
            neu_list.append(comment.body)
        process_comments(comment.replies, neg_list, pos_list, neu_list)


def main():
    comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')

    negative_comments_list = list()
    positive_comments_list = list()
    neutral_comments_list = list()

    process_comments(comments, negative_comments_list, positive_comments_list, neutral_comments_list)

    print('*** NEGATIVE LIST ***')
    for x in negative_comments_list:
        print('-', x)

    print('\n*** POSITIVE LIST ***')
    for x in positive_comments_list:
        print('-', x)

    print('\n*** NEUTRAL LIST ***')
    for x in neutral_comments_list:
        print('-', x)


main()