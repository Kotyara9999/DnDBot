import requests
import re


class Monser_Card():
    def __init__(self, name):
        self.params = {"name": name}

    def get_monster(self):
        server = "https://dnd.su/bestiary/"
        name = self.params["name"]
        responce = requests.get(server)
        html = responce.text

        list_left = html.find('<div class="grid-4_lg-3_md-2_xs-1 list">')
        list_right = list_left + html[list_left:].find("<script>")
        list = html[list_left:list_right]
        card = list.find(name)
        left = list[:card].rfind("<div")
        right = list[card:].find("<div") + left
        card = list[left:right]
        # print(card)

        card_id = card[card.find("id=") + 4:]
        card_id = card_id[:card_id.find('data') - 2]
        # print(card.find(","), card.find("data"))
        name = card[card.find(",") + 1:card.find("data-id") - 3].lower()
        # print(card_id, name)

        responce = requests.get(server + card_id + "-" + name)
        html = responce.text
        # print(html)
        card_left = html.find('<div class="card__header">')
        card_right = html[card_left:].find("</section>") + card_left
        card = html[card_left:card_right]
        card = card.replace('<li class="subsection desc">', '<li class="subsection desc"> \n')
        card = card.replace("</h3>", "</h3>\n")
        card = card.replace("<h3", "\n<h3")
        data = re.sub('<[^<]+?>', '', card)
        data = data.replace("Распечатать", "")
        data = data.replace("?", "")
        return data


if __name__ == "__main__":
    card = Monser_Card("Aurnozci")
    print(card.get_monster())
