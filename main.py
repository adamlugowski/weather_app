from requests import get

url = 'https://danepubliczne.imgw.pl/api/data/synop/'
response = get(url)

user = input('Napisz w którym Polskim mieście chcesz sprawdzić pogodę: ')
data = response.json()
for foo in data:
    if foo['stacja'] == user:
        print('Temperatura w', user, 'to', foo['temperatura'])