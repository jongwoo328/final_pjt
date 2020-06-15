from pprint import pprint
import requests, time, random, json

API_KEY = '0de948fbb0f0958879bbe2a00011845d'
BASE_URL = 'https://api.themoviedb.org/3/movie/'

url = BASE_URL + 'popular?api_key=' + API_KEY + '&language=ko-KR&page='

page_num = 1
data = []
count = 1
MAX_COUNT = 100
for page_num in range(1, MAX_COUNT+1):
    response = requests.get(url+ str(page_num))
    print(response.status_code)
    print(f'response {page_num}/{MAX_COUNT}')
    res_dict = json.loads(response.text)
    movie_list = res_dict['results']
    for movie in movie_list:
        if not movie.get('backdrop_path', False):
            movie['backdrop_path'] = ''
        if not movie.get('poster_path', False):
            movie['poster_path'] = ''
        movie['genres'] = movie.get('genre_ids')
        movie['api_id'] = movie.get('id')
        del movie['genre_ids']
        del movie['video']
        del movie['id']
        trailer_response = requests.get(BASE_URL + str(movie['api_id']) + '/videos?api_key=' + API_KEY + '&language=en-US')
        res_dict2 = json.loads(trailer_response.text)
        try:
            if res_dict2.get('results')[0].get('site') == 'YouTube':
                movie['trailer'] = res_dict2.get('results')[0].get('key')
            else:
                raise KeyError
        except:
            movie['trailer'] = ''
        data += [{
            'model': 'movies.movie',
            'pk': count,
            'fields': movie
        }]
        count += 1
    time.sleep(random.uniform(1, 2))


with open('movies/fixtures/movie_data2.json', 'w', encoding='utf-8') as make_db:
    json.dump(data, make_db, indent='\t', ensure_ascii=False)