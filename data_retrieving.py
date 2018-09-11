#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import preprocessor as p
import re
import time
import json
import emoji
#Variables that contains the user credentials to access Twitter API
access_token = "780478082469785601-Em9OdZ3tA01bPwV6GfkU3SLRdfemsbE"
access_token_secret = "9888AimNpnW4dM8QFl1zoUm1tHPRAYvUp9ZMlycHNltkH"
consumer_key = "dOGYRS3A3pUYNWfTwfl4vi6Wt"
consumer_secret = "K2pYj192M4uGwSpk6oe6UN9QEbgoGYwPKsXwMMQI5gHlK9h2He"
p.set_options(p.OPT.RESERVED)
emoticons = [' :) ', ' =) ', ' :( ', ' ;P ', ' ;) ', ' :-D ', ' :D ', ' :-) ', ' ;( ', ' :/ ', ' (: ', ' :-/ ', ' :P ', ':|', ' xD ', " :') ", ' =D ',  ' :] ', ' ;-) ', ' :p ', ' DX ', " :'( ", ' :-P ', ' :@ ', ' =] ', ' :-( ', ' >:( ', ' ;D ', ' XP ', ' 8) ', ' :\\ ',' XD ']
s = set()
htgs =[ '#ador', '#fond', '#like', '#attract', '#care', '#tender', '#compass',
                      '#sentiment', '#desir', '#passion', '#infatu', '#long', '#amus', '#bliss',
                      '#gaieti', '#glee', '#jolli', '#jovial', '#joy', '#delight', '#enjoy', '#glad',
                      '#happi', '#jubil', '#elat', '#satisfact', '#ecstasi', '#euphoria', '#enthusiasm',
                      '#zeal', '#excit', '#thrill', '#exhilar', '#pleasur', '#triumph', '#eager',
                      '#hope', '#enthral', '#raptur', '#relief', '#amaz', '#astonish', '#aggrav',
                      '#agit', '#annoy', '#grouchi', '#grumpi', '#crosspatch', '#frustrat', '#anger',
                      '#outrag', '#furi', '#wrath', '#hostil', '#feroc', '#bitter', '#hatr', '#scorn',
                      '#spite', '#veng', '#dislik', '#resent', '#revuls', '#contempt', '#loath',
                      '#jealousi', '#torment', '#agoni', '#anguish', '#hurt', '#depress', '#despair',
                      '#gloom', '#glum', '#unhappi', '#grief', '#sorrow', '#woe', '#miseri',
                      '#melancholi', '#dismay', '#displeasur', '#guilt', '#regret', '#remors',
                      '#alien', '#defeat', '#deject', '#embarrass', '#homesick', '#humili', '#insecur',
                      '#insult', '#isol', '#loneli', '#reject', '#piti', '#mononoawar', '#sympathi',
                      '#alarm', '#shock', '#fear', '#fright', '#horror', '#terror', '#panic', '#hysteria',
                      '#mortif', '#anxieti', '#suspens', '#uneasi', '#apprehens', '#worri', '#distress',
                      '#dread', '#love', '#good', '#lol', '#lmao', '#awesome', '#family', '#hot',
                      '#sexy', '#lust', '#happy', '#smile', '#gleeful', '#grateful', '#blessed',
                      '#comfortable', '#appreciative', '#motivation', '#hopeful', '#spirited', '#wow',
                      '#woah', '#grumpy', '#badmood', '#annoyed', '#anger', '#irate', '#jealous',
                      '#destroyed', '#wrecked', '#fml', '#sad', '#depressed', '#smh', '#damnshame',
                      '#awful', '#scary', '#spooky', '#nerves', '#stress', '#stressed', '#anxious']
re = emoji.get_emoji_regexp()
print emoticons
def contain_emoji(text):
    #all_emoji
    try:
        new_text =  unicode(text, 'unicode-escape')
        return len(re.findall(new_text))>0
    except:
        return False
def contain_emoticons(text):

    for emoticon in emoticons:
        if emoticon in text:
            print emoticon
            return True
    return False

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            t_start, full = 0, False
            if 'full_text' in data:
                full = True
                t_start = data.index("\"full_text\":\"")
            else:
                t_start = data.index("\"text\":\"")


            t_end, text = data[t_start:].index("\",\"") + t_start, ''
            if full:
                text = str(data[t_start+13: t_end])
            else:
                text = str(data[t_start + 8: t_end])
            if text not in s:
                s.add(text)
                text = text.replace("\\n", ' ')
                text = text.replace("\\r", ' ')
                text = text.replace('Reposting', ' ')
                text = text.replace('RT', ' ')
                text = text.replace('\"', ' ')
                text = p.clean(text)
                text = text.lower()

                # text = re.sub(r'\\u[0-9abcdef][0-9abcdef][0-9abcdef][0-9abcdef]', '', text)
                num = 0


                if num > 1 and  (contain_emoticons(text) or contain_emoji(text)) and 'sex' not in text:
                    with open('test_data.txt', 'a') as file:
                        file.write(text + '\n')
                    print unicode(text, 'unicode-escape')
                    print '\n'
            else:
                pass




        except:
            print 'bug'
            pass

        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    while True:
        try:
            #This handles Twitter authetification and the connection to Twitter Streaming API
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l)

            #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
            stream.filter(track= htgs)
        except:
            pass



