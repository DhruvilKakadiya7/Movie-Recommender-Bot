

#Importing ML Modules
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import art
import discord
import random
from keep_alive import keep_alive

TOKEN = 'MTAxNzA5NDA5NjQ2NjIxOTA3MQ.G3bAgn.oAHFX3H4RnNeOkDXuCUhB5lSv9A5MISFzPn6PU'
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#Reading The Dataset
df = pd.read_csv('movie.csv')
# df['title']=df['title'].apply(lambda x: x.lower())
# print(df)
features = ['title','keywords','cast','genres','director']

#Returns features of a particular Movie row
def combFeatures(row):
    return row['title']+" "+row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']

#Returns title from the index of the movie
def getTitle(index):
    return df[df.index == index]["title"].values[0]

#Returns index from the title of the movie and if not found returns -1
def getIndex(title):
    data = pd.read_csv('movie.csv')
    data['title'] = data['title'].apply(lambda x: x.lower())
    ok=-1
    if(str((data[data.title == title])).startswith("Empty")):
        ok=-1
    else:
        ok = data[data.title == title]["index"].values[0]
    if ok==-1:
        i=0;
        for x in data['title']:
            if title in x:
                ok=i
                break
            i=i+1;
    print(ok)
    return ok



#Removing Null/Empty Values from the data set and creating single feature column
for feature in features:
    df[feature] = df[feature].fillna('')
df["combinedFeatures"] = df.apply(combFeatures,axis=1)

# print(df["combinedFeatures"])



#Plotting similarity using count matrix
cv = CountVectorizer()
countMatrix = cv.fit_transform(df["combinedFeatures"])
similarityElement = cosine_similarity(countMatrix)
# print(similarityElement)
print(art.text2art("Movie Recommender"))
print("\n==> This model asks for the movie of you liking and returns any amount of similar movies.\n")

def recommend_movies(usersMovie):
    usersMovie = usersMovie.lower()
    movieIndex = getIndex(usersMovie)
    if movieIndex == -1:
        return [-10000]
    similarMovies = list(enumerate(similarityElement[movieIndex]))
    # print(similarMovies+"\n\n\n");
    sortedSimilar = sorted(similarMovies,key=lambda x:x[1],reverse=True)[1:]
    # print(sortedSimilar);
    i=0
    ret=[]
    tmp = str(getTitle(movieIndex))
    if usersMovie != tmp.lower():
        ret.append(str(getTitle(movieIndex)))
    for element in sortedSimilar:
        i=i+1
        ret.append(str(getTitle(element[0])))
        # print(str(i)+". "+getTitle(element[0]))
        if i == 8:
            break
    random.shuffle(ret)
    return ret

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!recommend'):
        ok = message.content.split(' ')
        print(ok)
        genre = ""
        for i in ok:
            if(i!='!recommend'):
                genre += f'{i} '
        genre = genre.strip()
        # print(genre)
        recommended_movies = recommend_movies(genre)
        response = f'ok'
        # print(recommended_movies)
        if(recommended_movies[0]==-10000):
            response = f'No such movie found in dataset.'
        else:
            # print(recommended_movies)
            response = f'Here are the top 5 recommended {genre} movies:\n'
            i=0
            # random.shuffle(recommend_movies)
            for x in recommended_movies:
                i=i+1
                response += f'{i}. {x}\n'
                if i==5:
                    break
        embed = discord.Embed(title="Hi there!",description=f"{response}",color=discord.Color.green())
        embed.set_author(name="DVS",icon_url="https://i.ibb.co/9yF0trY/logo.png")
        embed.set_footer(text=f'Thank you.')
        await message.channel.send(embed=embed)

    if message.content.startswith('!help'):
        embed = discord.Embed(title="Hi there!", description="Welcome to the Movie Recommender BOT. ", color=discord.Color.blue())
        embed.set_author(name="DVS",icon_url="https://i.ibb.co/9yF0trY/logo.png")
        embed.add_field(name=f'!recommend <movie name>',value=f"To get at most 10 similar movies.\n",inline=False)
        embed.add_field(name=f'!help',value=f"To get help.",inline=False)
        embed.add_field(name=f'!gen <genre>',value=f"To get random 20 movies of given geneation from dataset (year < 2017).",inline=False)
        embed.add_field(name=f'!listbyyear <year>',value=f"To get random 20 movies of given year from dataset. (year < 2017)",inline=False)
        embed.set_footer(text=f'Thank you.')
        await message.channel.send(embed=embed)

    if message.content.startswith('!gen'):
        ok = message.content.split(' ')
        genre = ""
        for i in ok:
            if(i!='!gen'):
                genre += f'{i} '
        genre = genre.strip()
        genre = genre.lower()
        data = df['genres'].tolist()
        # print(data)
        ls=[]
        i=0
        for x in data:
            if genre in x.lower():
                i=i+1
                ls.append(i)
            
            if i == 50:
                break
        # print(ls)
        random.shuffle(ls)
        response = f'Here are the 5 recommended {genre} movies:\n'
        i=0
        for x in ls:
            i=i+1
            response += f'{i}. {str(getTitle(x))}\n'
            if i==5:
                break
        embed = discord.Embed(title="Hi there!",description=f"{response}",color=discord.Color.red())
        embed.set_author(name="DVS",icon_url="https://i.ibb.co/9yF0trY/logo.png")
        embed.set_footer(text=f'Thank you.')
        await message.channel.send(embed=embed)

    if message.content.startswith('!listbyyear'):
        ok = message.content.split(' ')[1]
        ok = ok.strip()
        data = df['release_date'].tolist()
        # print(data)
        ls=[]
        i=0
        for x in data:
            if ok in x:
                i=i+1
                ls.append(i)
            
            if i == 100:
                break
        random.shuffle(ls)
        response = f'Here are the 5 recommended movies from year {ok}:\n'
        i=0
        for x in ls:
            i=i+1
            response += f'{i}. {str(getTitle(x))}\n'
            if i==5:
                break
        if i==0:
            response = f'No such movies found in dataset\nDataset only contains movie which realeased before year 2017.'
        embed = discord.Embed(title="Hi there!",description=f"{response}",color=discord.Color.red())
        embed.set_author(name="DVS",icon_url="https://i.ibb.co/9yF0trY/logo.png")
        embed.set_footer(text=f'Thank you.')
        await message.channel.send(embed=embed)

keep_alive()
client.run(TOKEN)
