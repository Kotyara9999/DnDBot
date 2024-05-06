import requests
server = "https://dnd.su/bestiary/"
name = input()
responce = requests.get(server)
html = responce.text

list_left = html.find('<div class="grid-4_lg-3_md-2_xs-1 list">')
list_right = list_left + html[list_left:].find("<script>")
list = html[list_left:list_right]
card = list.find(name)
left = list[:card].rfind("<div")
right = list[card:].find("<div") + left
card = list[left:right]
print(card)

card_id = card[card.find("id=") + 4:]
card_id = card_id[:card_id.find('data') - 2]
#print(card.find(","), card.find("data"))
name = card[card.find(",") + 1:card.find("data-id") - 3].lower()
print(card_id, name)

responce = requests.get(server + card_id + "-" + name)
html = responce.text
#print(html)
card_left = html.find('<div class="card__header">')
card_right = html[card_left:].find("</section>") + card_left
card = html[card_left:card_right]
#print(card, card_left, card_right)
hp = card[card.find("Хиты") + len("Хиты</strong> <span data-type='middle'>"):
          card[card.find("Хиты") + len("Хиты</strong> <span data-type='middle'>"):].find("</span>") +
     card.find("Хиты") + len("Хиты</strong> <span data-type='middle'>")]

kd = card[card.find("Класс Доспеха") + len("Класс Доспеха</strong> "):
          card[card.find("Класс Доспеха") + len("Класс Доспеха</strong> "):].find("</li>") +
     card.find("Класс Доспеха") + len("Класс Доспеха</strong> ")]
print(hp, kd)
