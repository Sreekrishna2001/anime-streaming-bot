import requests
from containers import searchResults,AnimeInfo
baseUrl = 'https://api.consumet.org/'

def callApi(URI):
    return requests.get(baseUrl+URI).json()

def search(query):
    res = callApi('meta/anilist/'+query)["results"]
    s = []
    for r in res:
        s.append(searchResults(r))
    return s
# search("demon")


def animeInfo(anime):
    res = search(anime)[0]
    print(res)
    info = requests.get(baseUrl+'meta/anilist/info/'+res.id).json()
    print(info)
    return AnimeInfo(info)

def getEps(animeId):
    eplinks = requests.get(baseUrl+'meta/anilist/watch/'+animeId).json()['sources'][-2]['url']
    print(eplinks)
    return eplinks


def getSch():
    pass

def getTrending():
    tanime = requests.get(baseUrl+'meta/anilist/trending').json()['results']
    markup = []
    for i,r in enumerate(tanime):
        markup.append(f"{i+1}.`{r['title']['romaji']}`\n")
    return markup