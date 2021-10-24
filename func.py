import requests
from numpy import mean, median, min, max
from scipy import stats

# укажите путь до файла с токеном
with open("token", "r") as f:
    access_token = f.read()

# access_token = <Вставьте токен VK-API>
domain = "https://api.vk.com/method"
v = '5.124'
fields = 'sex, bdate, city, country, home_town, has_photo, photo_max_orig, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group'


def get_id(link):
    try:
        link = link.split('/')[-1]
        query = f"{domain}/utils.resolveScreenName?access_token={access_token}&screen_name={link}&v={v}"
        return requests.get(query).json()['response']['object_id']
    except:
        return "Error"


def get_friends(user_id, fields):
    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
    return requests.get(query).json()


def users_get(user_ids, fields=fields, name_case='nom'):
    query = f"{domain}/users.get?access_token={access_token}&user_ids={user_ids}&fields={fields}&name_case={name_case}&v={v}"
    return requests.get(query).json()


def get_wall(owner_id, count=10, extended=1):
    query = f"{domain}/wall.get?access_token={access_token}&owner_id={owner_id}&count={count}&extended={extended}&v={v}"
    return requests.get(query).json()


def photos_get(owner_id, rev=0, extended=1, album_id='profile', feed_type='photo', count=500):
    query = f"{domain}/wall.get?access_token={access_token}&owner_id={owner_id}&album_id={album_id}&rev={rev}&extended={extended}&feed_type={feed_type}&count={count}&v={v}"
    return requests.get(query).json()


def friends_of_friend(link):
    user = get_id(link)
    data = get_friends(user, 'bdate')
    count = data['response']['count']
    items = data['response']['items']
    ids = []
    for i in items:
        try:
            ids.append(i['id'])
        except:
            continue

    return ids


def pred_age(link):
    user = get_id(link)['response']['object_id']
    data = get_friends(user, 'bdate')
    count = data['response']['count']
    items = data['response']['items']
    ages = []
    for i in items:
        try:
            bd = i['bdate'].split('.')
            if len(bd) > 2:
                age = 2020 - int(bd[-1])
                if age < 65 and age > 7:
                    ages.append(age)
        except:
            continue
    median_res = int(median(ages))
    mean_res = int(mean(ages))
    moda = stats.mode(ages)[0][0]
    # print(f'Медиана: {median_res}\nСреднее арифметическое: {mean_res}\nМода: {stats.mode(ages)[0][0]}')
    # print(f'Min: {min(ages)}\nMax: {max(ages)}')
    return int((mean_res + median_res + moda) / 3)
