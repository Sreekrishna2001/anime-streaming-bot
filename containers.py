class searchResults:
    def __init__(self,result) -> None:
        self.id = result['id']
        self.name = result['title']['romaji']
        self.desc = result['description']
        self.img = result['image']
        self.status = result['status']
        self.genres = result['genres']
        # self.totaleps = result
        # self.rating = rating

    # def __str__(self) -> str:
    #     return self.name


class AnimeInfo:
    def __init__(self,result) -> None:
        self.name = result['title']['romaji']
        self.desc = result['description']
        self.img = result['image']
        self.status = result['status']
        self.genres = ','.join(result['genres'])
        self.totaleps = result['totalEpisodes']
        self.rating = result['rating']
        self.type = result['type']
        self.episodes = result['episodes']
        self.markup = self.getMarkUp()

    def __str__(self) -> str:
                return '''
                \n Name :  {}
                \t Type : {}
                \t Description : {}
                \t Genre : {}
                \t Status : {}
                \t Rating : {} 
                \t Total Episodes : {}
                \n use /watch `{}` to watch 1st episode change episode-\n{episode number\n} to continue watching 
                '''.format(self.name,self.type,self.desc,self.genres,self.status,self.rating,self.totaleps,self.episodes[0]['id'])

    def getMarkUp(self):
        return '''
\n Name :  {} 
Type : {}
Genre : {}
Status : {}
Rating : {} 
Total Episodes : {}
\n *Use /watch `{}` to watch 1st episode change episode-(episode number) to continue watching* 
                '''.format(self.name,self.type,self.genres,self.status,self.rating,self.totaleps,self.episodes[0]['id'])

    def getEpsMarkup(self):
        markup = [f'{i}.<i>{epid}</i>\t' for i,epid in enumerate(self.episodes)]
        return markup