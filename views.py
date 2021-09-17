from django.shortcuts import render, redirect
from .models import data3
from .models import data6
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import PyPDF2
import os.path
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import os
import string
from unidecode import unidecode
import csv
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import tweepy
import pandas as pd
import re




def homepage(request):
    return render(request,'APP1/home.html')

def candhome(request):
    return render(request, 'APP1/candhome.html')

def candregistration(request):
    datas = data3.objects.all()
    context = {'members': datas}
    return render(request, 'APP1/candregistration.html',context)
def create(request):
    Datas = data3(Name=request.POST['name'],filepath=request.POST and request.FILES['filename'], Age=request.POST['Age'],
                   experience=request.POST['experience'],twitter_id=request.POST['twitter'],Gender=request.POST['gender'],Qualification=request.POST['Qualification'],
                   mobile=request.POST['mobile'], post=request.POST['post'], email=request.POST['email'], password=request.POST['password'])
    Datas.save()
    #messages.info(request, 'Your account has been created successfully! please login')
    messages.success(request, 'Account created successfully , please login !')
    return redirect('candhome')




def emphome(request):
    return render(request,'APP1/emphome.html')

def empreg(request):
    datas = data6.objects.all()
    context = {'members': datas}
    return render(request,'APP1/empreg.html',context)

def empcreate(request):
    Datas1 = data6(CName=request.POST['company'],place=request.POST['place'], regno=request.POST['regno'],
                   type=request.POST['type'],about=request.POST['about'],mobile=request.POST['mobile'],
                   email=request.POST['email'], password=request.POST['password1'])
    Datas1.save()
    messages.success(request, 'Account created successfully , please login !')
    return redirect('emphome')




def candprof(request):
    if request.method == 'POST':
        if data3.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            data = data3.objects.get(email=request.POST['email'], password=request.POST['password'])
            return render(request, 'APP1/candprof.html', {'member': data})

        else:
            messages.success(request, 'Invalid details , please try again !')
            #return render(request,'APP1/candhome.html')
            return redirect('candhome')




#def update(request,id):
    #members1=data3.objects.get(id=id)
    #members1.Name=request.POST['name']
    #members1.save()
    #return redirect('/')





def emprof(request):
    if request.method == 'POST':

        if data6.objects.filter(email=request.POST['email'], password=request.POST['password1']).exists():
            data = data6.objects.get(email=request.POST['email'], password=request.POST['password1'])

            return render(request, 'APP1/emprof.html', {'member': data})
        else:
            messages.success(request, 'Invalid details , please try again !')
            #return render(request,'APP1/emphome.html')
            return redirect('emphome')


#ML



def ml(request,id):


    if request.method == 'POST':
        myfiles = request.FILES['filename']
        fs = FileSystemStorage(location='media/Des/')
        filenames = fs.save(myfiles.name,myfiles)
        uploaded_file_path = fs.path(filenames)



        DIR = 'C:/Users/Administrator/PycharmProjects/djangoProject/ML/media'

        len_dir = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

        def clean_text(text):

            text = re.sub('<.*?>', ' ', text)

            text = text.translate(str.maketrans(' ', ' ', string.punctuation))

            text = re.sub('[^a-zA-Z]', ' ', text)

            text = re.sub("\n", " ", text)

            text = text.lower()

            text = ' '.join(text.split())
            return text

            # In[11]:

        res_output = []
        des_output = []
        ls = []
        resu= []

        for i in range(0, len_dir):
            mypath = r'C:/Users/Administrator/PycharmProjects/djangoProject/ML/media'

            onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

            resume = open(onlyfiles[i], 'rb')

            pdfReader = PyPDF2.PdfFileReader(resume)

            pageObject = pdfReader.getPage(0)

            resume = pageObject.extractText()
            resume = clean_text(resume)

            stop_words = set(stopwords.words('english'))

            word_tokens = word_tokenize(resume)

            for w in word_tokens:

                if w not in stop_words:
                    res_output.append(w)

            resume = ' '.join([str(elem) for elem in res_output])

            res_output.clear()

            # job_description = open('C:/Users/Administrator/Downloads/AbResumeL_VqSJtVE.pdf', 'rb')
            job_description = open(uploaded_file_path, 'rb')

            #paths, file_names = os.path.split(uploaded_file_path)

            pdfReader = PyPDF2.PdfFileReader(job_description)

            pageObject = pdfReader.getPage(0)

            job_description = pageObject.extractText()

            job_description = clean_text(job_description)

            stop_words = set(stopwords.words('english'))

            word_tokens = word_tokenize(job_description)

            for y in word_tokens:

                if y not in stop_words:
                    des_output.append(y)

            job_description = ' '.join([str(eleme) for eleme in des_output])

            des_output.clear()

            resume = word_tokenize(resume)
            for wrd in resume:
                if wrd in job_description:
                    resu.append(wrd)

            resume =' '.join([str(eleme) for eleme in resu])

            resu.clear()

            text = [resume, job_description]

            cv = CountVectorizer(lowercase=True, stop_words='english')

            count_matrix = cv.fit_transform(text)

            matchPercentage = cosine_similarity(count_matrix)[0][1] * 100

            matchPercentage = round(matchPercentage)

            path, file_name = os.path.split(onlyfiles[i])

            if matchPercentage> 0:
                ls.append((matchPercentage, file_name))
            else:
                pass
            # ls.append((matchPercentage, onlyfiles[i]))
            ls = sorted(ls, reverse=True)

        newd = data6.objects.get(id=id)

        context2 = {
            'ls': ls,
            'newd':newd
        }

        return render(request, 'APP1/emprof2.html', context2)






def message(request):
    lll=[]

    for data3.Name in data3.objects.all() :
        lll.append(data3.Name)
    a=len(lll)+1

    files = []
    for i in range(1,a):
         newdata = data3.objects.get(id=i)
         files.append(newdata.filepath)
    #k="<FieldFile: AbResumeL_RuDqXax_mSQ3QIU.pdf>"
    #op=[]
    idno = files.index(request.POST['res'])+1
    #idno1=str(idno)
    newdata1 = data3.objects.get(id=idno)
    if newdata1.filepath == request.POST['res']:
       newdata1.invitation = newdata1.invitation + request.POST['name']
       newdata1.save()
       candi={
           "can": newdata1
       }
       #x=data6.objects.get(id=id)
       #y=str(x.id)
       #path= 'emprof/ml/' + y
       return render(request, 'APP1/checknot.html',candi)

       #return render(request, path)


   # cont = {
    #    "memm": files[15],
     #    "len1": idno1,
    #}

    #return render(request, 'APP1/checknot.html',cont)

    # if fileb in files:

        # idno = files.count(fileb)
       # n=22
       # newdata1 = data3.objects.get(id=n)

        #if newdata1.filepath == request.POST['res']:
         #   newdata1.invitation = newdata1.invitation + request.POST['name']
          #  newdata1.save()
           # return redirect('/')


#fileb = request.POST['res']

#for g in range(0,len_dir1) :
        #if request.POST['res'] in files[g]:
         #   newdata1=data3.objects.get(id=g)
         #  newdata1.invitation = newdata1.invitation + request.POST['name']
           # newdata1.save()
            #return redirect('/')







        #if newdata.filepath == request.POST['res']:
         #   newdata.invitation = newdata.invitation + request.POST['name']
          #  newdata.save()
          #  return redirect('/')
       # else:
      #      pass
def edit(request,id):
    members1=data3.objects.get(id=id)
    context1={
        'ab':members1
    }
    return render(request,'APP1/invitation.html',context1)




def twitter(request):
    if request.method == 'POST':
        data = data3.objects.all()

        members = {

            "member": data,
        }
        return render(request, 'APP1/twitter.html', members)


#def twitter4(request):
   # return render(request,'APP1/home.html')



def twitter3(request):
    if request.method == 'POST':

        data = data3.objects.all()

        ckey = 'ZSTjRgpSwrcpgLDqTug1tnHVS'
        csecret = '2mfFBHGIV0OT7b5LbgWrAbBhoyr3tB7GiGTtCGiz0pN8S9EFKv'
        atoken = '1014097837381111808-1ZmyTn9NwXhnlnH3rLJdjLg7WmwFTG'
        asecret = 'siiC7b529NpcGT8uwopjOaauSRZoUQdlN38mLL0gX2TLK'
        auth = tweepy.OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        api = tweepy.API(auth)

        emoticons_str = r"""
            (?:
                [:=;] # Eyes
                [oO\-]? # Nose (optional)
                [D\)\]\(\]/\\OpP] # Mouth
            )"""

        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)

        regex_str = [
            emoticons_str,
            r'<[^>]+>',  # HTML tags
            r'(?:@[\w_]+)',  # @-mentions
            r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
            r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

            r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
            r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
            r'(?:[\w_]+)',  # other words
            r'(?:\S)'  # anything else
        ]

        tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
        emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

        def tokenize(s):
            return tokens_re.findall(s)

        def preprocess(s, lowercase=False):
            tokens = tokenize(s)
            if lowercase:
                tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
            return tokens

        def preproc(s):
            # s=emoji_pattern.sub(r'', s) # no emoji
            s = unidecode(s)
            POSTagger = preprocess(s)
            # print(POSTagger)

            tweet = ' '.join(POSTagger)
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(tweet)
            # filtered_sentence = [w for w in word_tokens if not w in stop_words]
            filtered_sentence = []
            for w in POSTagger:
                if w not in stop_words:
                    filtered_sentence.append(w)
            # print(word_tokens)
            # print(filtered_sentence)
            stemmed_sentence = []
            stemmer2 = SnowballStemmer("english", ignore_stopwords=True)
            for w in filtered_sentence:
                stemmed_sentence.append(stemmer2.stem(w))
            # print(stemmed_sentence)

            temp = ' '.join(c for c in stemmed_sentence if c not in string.punctuation)
            preProcessed = temp.split(" ")
            final = []
            for i in preProcessed:
                if i not in final:
                    if i.isdigit():
                        pass
                    else:
                        if 'http' not in i:
                            final.append(i)
            temp1 = ' '.join(c for c in final)
            # print(preProcessed)
            return temp1

        def getTweets(user):
            csvFile = open('user.csv', 'a', newline='')
            csvWriter = csv.writer(csvFile)
            try:
                for i in range(0, 4):
                    tweets = api.user_timeline(screen_name=user, count=1000, include_rts=True, page=i)
                    for status in tweets:
                        tw = preproc(status.text)
                        if tw.find(" ") == -1:
                            tw = "blank"
                        csvWriter.writerow([tw])
            except tweepy.TweepError:
                print("Failed to run the command on that user, Skipping...")
            csvFile.close()

        username = request.POST['name']
        getTweets(username)
        with open('user.csv', 'rt') as f:
            csvReader = csv.reader(f)
            tweetList = [rows[0] for rows in csvReader]
        os.remove('user.csv')
        with open('C:/Users/Administrator/Desktop/personality traits/CSV_Data/newfrequency300.csv', 'rt') as f:
            csvReader = csv.reader(f)
            mydict = {rows[1]: int(rows[0]) for rows in csvReader}

        vectorizer = TfidfVectorizer(vocabulary=mydict, min_df=1)
        x = vectorizer.fit_transform(tweetList).toarray()
        df = pd.DataFrame(x)

        model_IE = pickle.load(
            open("C:/Users/Administrator/Desktop/personality traits/Pickle_Data/BNIEFinal.sav", 'rb'))
        model_SN = pickle.load(
            open("C:/Users/Administrator/Desktop/personality traits/Pickle_Data/BNSNFinal.sav", 'rb'))
        model_TF = pickle.load(
            open('C:/Users/Administrator/Desktop/personality traits/Pickle_Data/BNTFFinal.sav', 'rb'))
        model_PJ = pickle.load(
            open('C:/Users/Administrator/Desktop/personality traits/Pickle_Data/BNPJFinal.sav', 'rb'))

        answer = []
        IE = model_IE.predict(df)
        SN = model_SN.predict(df)
        TF = model_TF.predict(df)
        PJ = model_PJ.predict(df)

        b = Counter(IE)
        value = b.most_common(1)
        # print(value)


        if value[0][0] == 1.0:
            answer.append("I")
        else:
            answer.append("E")

        b = Counter(SN)
        value = b.most_common(1)
        # print(value)
        if value[0][0] == 1.0:
            answer.append("S")
        else:
            answer.append("N")

        b = Counter(TF)
        value = b.most_common(1)
        # print(value)
        if value[0][0] == 1:
            answer.append("T")
        else:
            answer.append("F")

        b = Counter(PJ)
        value = b.most_common(1)
        # print(value)
        if value[0][0] == 1:
            answer.append("P")
        else:
            answer.append("J")
        mbti = "".join(answer)

        if mbti == 'ENFJ':
            str1 = '"The Giver \n They are extroverted, idealistic, charismatic, outspoken, \n highly principled and ethical, and usually know how to connect \n with others no matter their background."'
            #return mbti, str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }


        elif mbti == 'ISTJ':
            str1 = '" The Inspector \n They appear serious, formal, and proper. They also love \n traditions and old-school values that uphold patience, hard work,\n honor, and social and cultural responsibility. They are reserved, calm, quiet, and upright."'
            #return mbti, str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }

        elif mbti == 'INFJ':
            str1 = '" The Counselor \n They have a different, and usually more profound, way of\n looking at the world. They have a substance and depth in the way \n they think, never taking anything at surface level or accepting things the way they are"'
            #return mbti, str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }


        elif mbti == 'INTJ':
            str1 = '" The Mastermind \n They are usually self-sufficient and would rather work \n alone than in a group. Socializing drains an introvert’s energy, \n causing them to need to recharge." "'
            #return mbti, str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }


        elif mbti == 'ISTP':
            str1 = '" The Craftsman \n  They are mysterious people who are usually very rational\n and logical, but also quite spontaneous and enthusiastic. Their \n personality traits are less easily recognizable than those of other \n types, and even people who know them well can’t always anticipate \n their reactions. Deep down, ISTPs are spontaneous, unpredictable individuals,\n but they hide those traits from the outside world, often very successfully."'
            #return mbti, str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }


        elif mbti == 'ESFJ':
            str1 = '"The Provider \n They are social butterflies, and their need to interact\n with others and make people happy usually ends up making them popular.\n The ESFJ usually tends to be the cheerleader or sports hero in high school\n and college. Later on in life, they continue to revel in the \n spotlight, and are primarily focused on organizing social events for their families,\n friends and communities. "'
            #return mbti, str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }


        elif mbti == 'INFP':
            str1 = '" The Idealist \n  They prefer not to talk about themselves, especially in \n the first encounter with a new person. They like spending time alone in \n quiet places where they can make sense of what is happening around them. \n They love analyzing signs and symbols, and consider them to be \n metaphors that have deeper meanings related to life. "'
            #return mbti, str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }



        elif mbti == 'ESFP':
            str1 = '" The Performer \n They have an Extraverted, Observant, Feeling and Perceiving \n personality, and are commonly seen as Entertainers. Born to be in \n front of others and to capture the stage, ESFPs love the spotlight. ESFPs \n are thoughtful explorers who love learning and sharing what they \n learn with others. ESFPs are “people people” with strong interpersonal skills."'
            #return mbti, str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }


        elif mbti == 'ENFP':
            str1 = '" The Champion \n They have an Extraverted, Intuitive, Feeling and Perceiving \n personality. This personality type is highly individualistic and \n Champions strive toward creating their own methods, looks, actions, habits, \n and ideas — they do not like cookie cutter people and hate when they \n are forced to live inside a box.  "'
            #return mbti, str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }


        elif mbti == 'ESTP':
            str1 = '" The Doer \n  They have an Extraverted, Sensing, Thinking, and Perceptive\n personality. ESTPs are governed by the need for social interaction,\n feelings and emotions, logical processes and reasoning, along with a need \n for freedom. "'
            #return mbti, str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }


        elif mbti == 'ESTJ':
            str1 = '" The Supervisor \n They are organized, honest, dedicated, dignified, traditional,\n and are great believers of doing what they believe is right and \n socially acceptable. Though the paths towards “good” and “right” are difficult,\n they are glad to take their place as the leaders of the pack. \n They are the epitome of good citizenry.  "'
            #return mbti, str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }


        elif mbti == 'ENTJ':
            str1 = '" The Commander \n  Their secondary mode of operation is internal, where intuition \n and reasoning take effect. ENTJs are natural born leaders among \n the 16 personality types and like being in charge. They live in a world of \n possibilities and they often see challenges and obstacles as great \n opportunities to push themselves. "'
            #return mbti, str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }


        elif mbti == 'INTP':
            str1 = '" The Thinker \n  They are well known for their brilliant theories and unrelenting\n logic, which makes sense since they are arguably the most logical \n minded of all the personality types. They love patterns, have a keen eye \n for picking up on discrepancies, and a good ability to read people, \n making it a bad idea to lie to an INTP."'
            #return mbti,str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }


        elif mbti == 'ISFJ':
            str1 = '" The Nurturer \n They are philanthropists and they are always ready to give back \n and return generosity with even more generosity. The people \n and things they believe in will be upheld and supported with enthusiasm\n  and unselfishness."'
            #return mbti,str1
            members = {
                "mem": mbti,
                "m": str1,
                "member": data,
            }




        elif mbti == 'ENTP':
            str1 = '" The Visionary \n Those with the ENTP personality are some of the rarest in the world,\n  which is completely understandable. Although they are \n extroverts, they don’t enjoy small talk and may not thrive in many social \n situations, especially those that involve people who are too different\n from the ENTP. ENTPs are intelligent and knowledgeable need to \n be constantly mentally stimulated."'
            #return mbti,str1
            members = {
            "mem": mbti,
            "m": str1,
            "member": data,
            }


        else:
            str1 = '" The Composer \n They are introverts that do not seem like introverts. It is \n because even if they have difficulties connecting to other people\n at first, they become warm, approachable, and friendly eventually. They \n are fun to be with and very spontaneous, which makes them the perfect \n friend to tag along in whatever activity, regardless if planned \n or unplanned. ISFPs want to live their life to the fullest and embrace the\n present, so they make sure they are always out to explore new things and \n discover new experiences."'
            #return mbti,str1
            members = {
                "mem": mbti,
                "m": str1,
                "member":data,
            }

       # members = {
        #    "mem": mbti,
         #   "member": str1,
         #}
        return render(request, 'APP1/twitter4.html',members)






       # consumerKey = 'ZSTjRgpSwrcpgLDqTug1tnHVS'
       # consumerSecret = '2mfFBHGIV0OT7b5LbgWrAbBhoyr3tB7GiGTtCGiz0pN8S9EFKv'
       # accessToken = '1014097837381111808-1ZmyTn9NwXhnlnH3rLJdjLg7WmwFTG'
       # accessTokenSecret = 'siiC7b529NpcGT8uwopjOaauSRZoUQdlN38mLL0gX2TLK'

       # authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

        #authenticate.set_access_token(accessToken, accessTokenSecret)

        #api = tweepy.API(authenticate, wait_on_rate_limit=True)
#
#        posts = api.user_timeline(screen_name=request.POST['name'],count=100, lang="en", tweet_mode="extended")
        #narendramodi_in
 #       i = 1
 #       for tweet in posts[0:5]:
  #          str(i) + ')' + tweet.full_text + '\n'
   #         i = i + 1

        #   df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

        # def cleanTxt(text):
        #    text = re.sub('@[A-Za-z0-9]+', '', text)
        #    text = re.sub('#', '', text)
        #    text = re.sub('\n', '', text)
        #    text = re.sub('RT[\s]+', '', text)
        #    text = re.sub('https?:\/\/\S+', '', text)

        #    return text
        #
        # df['Tweets'] = df['Tweets'].apply(cleanTxt)

        #  def getSubjectivity(text):
        #    return TextBlob(text).sentiment.subjectivity

    #
        # def getPolarity(text):
        #  return TextBlob(text).sentiment.polarity

        #df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
        # df['polarity'] = df['Tweets'].apply(getPolarity)
        #

        #members = {
           # "mem": mbti,
           # "member": str1,
        #}




# polarity = df['polarity'].mean()

















#byareebmahfooz


