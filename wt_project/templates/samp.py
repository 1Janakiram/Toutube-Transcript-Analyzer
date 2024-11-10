import requests

import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger_eng')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer



def main():

    query = input("Search Here ")

    keywords = extract_keywords(query)

    #print("Keywords:", keywords)


    vid_id = get_videos(query)

    for i in range(0, len(vid_id)):

        id = vid_id[i]
        responses = get_transcript(id)



        if(responses["is_available"] == True and responses["lang"] == "en"):
            print()
            title = get_video_title(id)
            print(title)
            print("\n\n")

            subtitles = responses["subtitles"]
            for part in subtitles:
                if any(words in part['text'] for words in keywords) or any(words in part['text'].lower() for words in keywords) :
                    print(f"{part['text']} at {part['start']}s",end="  ")
                    print(f"https://www.youtube.com/watch?v={id}&t={part['start']}s")
                    print()
        else:
            continue

        choice = input("Do You want to get the results for the next video(Y/N): ")
        if(choice.lower() == 'n'):
            break





def extract_keywords(text):
        """Extracts keywords from a given text."""

        # Tokenize the text into words
        words = word_tokenize(text)

        # Remove stop words (common words that don't carry much meaning)
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]


        # Stem words to their root form
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(word) for word in filtered_words]

        # Identify keywords based on frequency and part-of-speech tags
        tagged_words = nltk.pos_tag(stemmed_words)
        keywords = []
        for word, tag in tagged_words:
            if tag.startswith('NN') or tag.startswith('VB'):  # Nouns and verbs are often keywords
                keywords.append(word)

        return keywords

def get_videos(text):
    url = "https://youtube-v2.p.rapidapi.com/search/"

    querystring = {"query":text,"lang":"en","order_by":"this_month","country":"us"}

    headers = {
        "x-rapidapi-key": " ",
        "x-rapidapi-host": "youtube-v2.p.rapidapi.com"
    }
    vid_id=[]
    response = requests.get(url, headers=headers, params=querystring)

    response =response.json()

    response = response['videos']
    for i in range(0,len(response)):
        vid_id.append(response[i]['video_id'])

    return vid_id

def get_transcript(id):
    url = "https://youtube-v2.p.rapidapi.com/video/subtitles"

    headers = {
        "x-rapidapi-key": " ",
        "x-rapidapi-host": "youtube-v2.p.rapidapi.com"
    }

    query_string = {"video_id":id}
    responses = requests.get(url, headers=headers, params=query_string)

    responses = responses.json()

    return responses
def get_video_title(id):
    url = "https://youtube-v2.p.rapidapi.com/video/details"

    headers = {
        "x-rapidapi-key": " ",
        "x-rapidapi-host": "youtube-v2.p.rapidapi.com"
    }
    querystring = {"video_id":id}

    headers = {
        "x-rapidapi-key": " ",
        "x-rapidapi-host": "youtube-v2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    response = response.json()


    return f"{response['title']} by {response['author']}"


if __name__ == "__main__":
    main()

