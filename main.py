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
        return url_.format(**params_)

    def open(self, url_: str):
        if self.check_connection():
            webbrowser.open(url_)
        else:
            print("Нет подключения.")

    @staticmethod
    def check_connection():
        return req.get('http://ya.ru').ok


class User:
    def __init__(self, _search_engine):
        self._request = None
        self._search_engine = RequestHandler()
        self.set_req()

    def set_req(self):
        self._request = input("Введите запрос: ")
        if not self._request:
            self._request = " "

    def prompt(self, url_: str, params_: dict):
        params_["srsearch"] = self._request
        if not self._search_engine.check_connection():
            return None
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
    searcher = RequestHandler()

    user = User(searcher)
    result = user.prompt(url, search_params.copy())
    if result is None:
        print("Нет подключения.")
        exit(0)

    page_id = user.get_id(*result)
    if page_id != -1:
        searcher.open(f"https://ru.wikipedia.org/?curid={page_id}")


if __name__ == '__main__':
    main()
