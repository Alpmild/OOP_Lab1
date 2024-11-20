import requests as req
import webbrowser

url = "https://ru.wikipedia.org/w/api.php"
search_params = {
    "action": "query",
    "list": "search",
    "format": "json",
    "srsearch": None
}


class RequestHandler:
    @staticmethod
    def search(url_: str, params_: dict):
        res = req.get(url_, params=params_).json()
        return res["query"]["search"]

    @staticmethod
    def get_url(url_: str, params_: dict):
        pass


class User:
    def __init__(self):
        self.request = None
        self.set_req()

    def set_req(self):
        self.request = input("Введите запрос: ")
        if not self.request:
            self.request = " "

    def prompt(self, url_: str, params_: dict):
        params_["srsearch"] = self.request
        return RequestHandler.search(url_, params_)

    @staticmethod
    def get_id(*args):
        n = len(args)
        ind = -1

        if n == 0:
            print("Нет результатов поиска")
            return -1
        for i in range(n):
            print(f"{str(i + 1).rjust(2, '0')}. {args[i]['title']}")
        print()

        while not 1 <= ind <= n:
            try:
                ind = int(input(f"Введите цифру от 1 до {n}: "))
                assert 1 <= ind <= n
            except (ValueError, AssertionError):
                print("Неверный ввод. ", end='')

        return args[ind - 1]['pageid']


def main():
    user = User()
    result = user.prompt(url, search_params.copy())
    page_id = user.get_id(*result)

    if page_id != -1:
        webbrowser.open(f"https://ru.wikipedia.org/?curid={page_id}")


if __name__ == '__main__':
    main()
