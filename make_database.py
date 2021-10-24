from func import *
import urllib.request
import os

#Служебные словари и списки
sex={
    0: "-",
    1:"Женский",
    2:"Мужской",
    3:"-"
}
has_mobile={
    1:"Да",
    0:"-"
}
relation={1:"не женат/не замужем",
          2:"есть друг/есть подруга",
          3:"помолвлен/помолвлена",
          4:"женат/замужем",
          5:"всё сложно",
          6:"в активном поиске",
          7:"влюблён/влюблена",
          8:"в гражданском браке",
          0:"-"}
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
political={
    0: "-",
    1:"коммунистические",
    2:"социалистические",
    3:"умеренные",
    4:"либеральные",
    5:"консервативные",
    6:"монархические",
    7:"ультраконсервативные",
    8:"индифферентные",
    9:"либертарианские"
}
people_main={
    0: "-",
    1: "ум и креативность",
    2: "доброта и честность",
    3: "красота и здоровье",
    4: "власть и богатство",
    5: "смелость и упорство",
    6: "юмор и жизнелюбие"
}
life_main={
    0:"-",
    1: "семья и дети",
    2: "карьера и деньги",
    3: "развлечения и отдых",
    4: "наука и исследования",
    5: "совершенствование мира",
    6: "саморазвитие",
    7: "красота и искусство",
    8: "слава и влияние"
}
smoking_alcohol={
    0:"-",
    1: "резко негативное",
    2: "негативное",
    3: "компромиссное",
    4: "нейтральное",
    5: "положительное",
}




def get_img(URL,filename):
    img = urllib.request.urlopen(URL).read()
    out = open(filename, "wb")
    out.write(img)
    out.close()

def parse_b_day(bday):
    try:
        bday=bday.split('.')
    except:
        return 'Не указана'
    day = bday[0]
    month = months[int(bday[1])-1]
    year =''
    if len(bday)>2:
        year=bday[2]
    return day+' '+month+' '+year

def write_info(info):
    data=info['response'][0]

    personal_data=data['personal'] if 'personal' in data else {}


    fileway=os.getcwd()+f"/static/database/{data['id']}"
    try:
        os.mkdir(fileway)
    except FileExistsError:
        print("Directory exists")
    except FileNotFoundError:
        os.mkdir(os.getcwd()+f"/static/database/")
        print("No such directory")

    get_img(data['photo_max_orig'],fileway+'/photo.jpg')

    with open(fileway+'/info.txt','w') as f:
        f.write(f"""id_vk: {data['id']};
Имя: {data['first_name']};
Фамилия: {data['last_name']};
Закрытый профиль VK: {'Да'  if data['is_closed']==1 else 'Нет'};
Пол: {sex[data['sex']] if 'sex' in data else '-'};
Ник: {data['nickname'] if 'nickname' in data else '-'};
Коротка ссылка vk: {data['domain'] if 'domain' in data else '-'};
Короткое имя страницы vk: {data['screen_name'] if 'screen_name' in data else '-'};
День рождения: {parse_b_day(data['bdate']) if 'bdate' in data else '-'};
Город: {data['city']['title'] if 'city' in data else '-'};
Страна: {data['country']['title'] if 'country' in data else '-'};
Наличие мобильного vk: {has_mobile[data['has_mobile']] if 'has_mobile' in data else '-'};
Мобильный телефон: {data['mobile_phone'] if 'mobile_phone' in data else '-'};
Сайт: {data['site'] if 'site' in data else '-'};
Статус: {data['status'] if 'status' in data else '-'};
Кол-во подписчиков: {data['followers_count'] if 'followers_count' in data else '-'};
Текущий род занятий: {data['occupation']['name'] if 'occupation' in data else '-'};
Карьера: {data['career'] if 'career' in data else '-'};
Родной город: {data['home_town'] if 'home_town' in data else '-'};
Семейное положение: {relation[data['relation']] if 'relation' in data else '-'};
Политические предпочтения: {political[personal_data['political']] if 'political' in personal_data else '-'};
Владение языками:{personal_data['langs'] if 'langs' in personal_data else '-'};
Мировозрение: {personal_data['religion'] if 'religion' in personal_data else '-'};
Источники вдохновения: {personal_data['inspired_by'] if 'inspired_by' in personal_data else '-'};
Главное в людях: {people_main[personal_data['people_main']] if 'people_main' in personal_data else '-'};
Главное в жизни: {life_main[personal_data['life_main']] if 'life_main' in personal_data else '-'};
Отношение к курению: {smoking_alcohol[personal_data['smoking']] if 'smoking' in personal_data else '-'};
Отношение к алкоголю: {smoking_alcohol[personal_data['alcohol']] if 'alcohol' in personal_data else '-'};
Интересы: {data['interests'] if 'interests' in data else '-'};
Любимая музыка: {data['music'] if 'music' in data else '-'};
Деятельность: {data['activities'] if 'activities' in data else '-'};
Любимые фильмы: {data['movies'] if 'movies' in data else '-'};
Любимые телешоу: {data['tv'] if 'tv' in data else '-'};
Любимые книги: {data['books'] if 'books' in data else '-'};
Любимые игры: {data['games'] if 'games' in data else '-'};
Университеты: {[i for i in data['universities']] if 'universities' in data else '-'};
Школы: {[i['name'] for i in data['schools']] if 'schools' in data else '-'};
О себе: {data['about'] if 'about' in data else '-'};
Родственники: {['https://vk.com/id'+str(i['id']) for i in data['relatives']] if 'relatives' in data else '-'};
Любимые цитаты: {data['quotes'] if 'quotes' in data else '-'};
""")
    return fileway
# write_info(users_get(get_id('https://vk.com/obolenskya')))
