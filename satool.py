from nltk.stem.wordnet import WordNetLemmatizer  #Use NLTK to import lemmatizer tool for utilisation below 
from nltk.corpus import twitter_samples, stopwords #Use NLTK to import twitter_samples allowing for the determination of positive and negative tweets and stopwords 
from nltk.tag import pos_tag  #Uses NLTK to call pos_tag which is a list of strings 
from nltk.tokenize import word_tokenize #Uses NLTK to import tokenizer which splits statement into tokens 
from nltk import FreqDist, classify, NaiveBayesClassifier  #Use NLTK to import NaivesBayesClassifier which allows for classification of text

import re, random, string

def remove_allnoise(tweet_tokenized, stop_words = ()):
    cleaned_tokens = []  #A new arraylist is created under the variable cleaned_tokens

    for token, tag in pos_tag(tweet_tokenized):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token) 

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith("VB"):
            pos = 'v'
        else: 
            pos = 'a'
        
        lemmatizer = WordNetLemmatizer()  #Applies WordNetLemmatizer() to lemmatizer and declares it as such
        token = lemmatizer.lemmatize(token, pos) #Declares token  

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:  #If the length of the token is greater than 0 and the token when declared is not found in the list of stopwords:
            cleaned_tokens.append(token.lower())  #Append() adds the cleaned token to the list 
    return cleaned_tokens  #ends the function and returns the value 


def fetch_tweets_for_tool(cleaned_tokens_list):  #Declares variable which can be called later 
    for tweet_tokenized in cleaned_tokens_list:  #For loop declaring number of tokenized tweet in the cleaned token list
        yield dict([token, True] for token in tweet_tokenized)  #runs iteration through yield 

def fetch_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token  #Yield is used as opposed to return when iterations occur with no requirement to store it in memory 


if __name__ == "__main__":

    positive_tweets = twitter_samples.strings('positive_tweets.json')  #Calls twitter_samples and declares them as strings and looks at the dataset 'positive_tweets.json' and declares it as the variable positive_tweets
    negative_tweets = twitter_samples.strings('negative_tweets.json')  #Calls twitter_samples and declares them as strings and looks at the dataset 'negative_tweets.json' and declares it as the variable negative_tweets
    text = twitter_samples.strings('tweets.20150430-223406.json')  #Calls twitter_samples and declares them as strings and looks at the dataset 'tweets.20150430-223406.json' and declares it as the variable text which is more of a generalised data set void of sentiment classification
    tweet_tokenized = twitter_samples.tokenized('positive_tweets.json')[0]  #declares tweet_tokenized variable and tokenizes the dataset 'positive_tweets.json'

    stop_words = stopwords.words('english')  #Makes use of the stopwords import and declares the variable stop_words as such, making use of english stop words only

    positive_tweets_tokenized = twitter_samples.tokenized('positive_tweets.json')  #declares positive_tweet_tokenized variable and tokenizes the dataset 'positive_tweets.json'
    negative_tweets_tokenized = twitter_samples.tokenized('negative_tweets.json')  #declares negative_tweet_tokenized variable and tokenizes the dataset 'negative_tweets.json'

    positive_cleaned_tokens_list = []  #A new arraylist is created as assigned to the variable positive_cleaned_tokens_list
    negative_cleaned_tokens_list = []  #A new arraylist is created as assigned to the variable negative_cleaned_tokens_list

    for tokens in positive_tweets_tokenized:
        positive_cleaned_tokens_list.append(remove_allnoise(tokens, stop_words))  #Looks at tokens in tokenized positive tweets and adds all tokens to the positive cleaned tokens list once lemmatized and once the remove_allnosie function is called 

    for tokens in negative_tweets_tokenized:
        negative_cleaned_tokens_list.append(remove_allnoise(tokens, stop_words))  #Looks at tokens in tokenized negative tweets and adds all tokens to the negative cleaned tokens list once lemmatized and once the remove_allnosie function is called 

    all_positive_words = fetch_words(positive_cleaned_tokens_list)  #Runs an iteration which calls the fetch_words function and yields records and adds to all_positive_words as a variable 

    frequency_dist_positive = FreqDist(all_positive_words)  #Runs iteration which records number of times positive words occur and stores in variable called frequency_dist_positive
    positive_tokens_for_tool = fetch_tweets_for_tool(positive_cleaned_tokens_list)  #
    negative_tokens_for_tool = fetch_tweets_for_tool(negative_cleaned_tokens_list)

    positive_data = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_tool] 

    negative_data = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_tool] 

    dataset = positive_data + negative_data  #Produces variable called dataset which combines positive data and negative data 

    random.shuffle(dataset)  #randomly shuffles dataset to avoid skew of data 

    training_data = dataset[:11200]  #Abides by 80:20 split of dataset data allowance 
    testing_data = dataset[2000:]  #Abides by 80:20 split of dataset data allowance 

    classifier = NaiveBayesClassifier.train(training_data)  #Utilises machine learning to declare classifier as a variable and trains the algorithm using training_data dataset 

    print("The Accuracy of the Classifier is: ", classify.accuracy(classifier, testing_data))  #Prints out accuracy of classifier by using the machine learning algorithm against the testing data, producing a near perfect score for accuracy out of 1 

    usertweet = "That food was good, i loved it!!!!"  #User inputted tweet declared in code and changed to challenge and analyse sentiment 

    custom_tokens = remove_allnoise(word_tokenize(usertweet))  #Runs lemmatization and tokenization and stopword removal hence cleaning user inputted text to effectively analyse sentiment 

    print(usertweet, classifier.classify(dict([token, True] for token in usertweet)))  #Prints statement determining sentiment i.e. positive or negative 