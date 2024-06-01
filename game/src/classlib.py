import os, json5, wcwidth
from typing import Any


class Player:
    def __init__(self, name: str = "player"):
        self.name = name
        self.location = "home"
        self.stage_lv = 0  # 關卡等級
        self.lv = 0  # 人物等級
        self.language = "zh-tw"
        self.money = 100
        self.bag = Bag(dict(), default=0)
        self.account = BankAccount(self.name)

    def update(self, data: dict):
        for k, v in data.items():
            if k == "bag":
                self.bag = Bag({}, default=0)
                self.bag.loadItem(v)
            elif k == "account":
                self.account = BankAccount(self.name)
                self.account.money = v[0]
                self.account.bag = Bag({}, default=0)
                self.account.bag.loadItem(v[1])
            else:
                self.__dict__[k] = v

    def serialize(self) -> dict:
        temp = {}
        for k, v in self.__dict__.items():
            if k == "bag":
                t = {}
                for k, v in self.bag.items():
                    t[k.id] = v
                temp[k] = v
            elif k == "account":
                t = {}
                for k, v in self.account.bag.items():
                    t[k.id] = v
                temp[k] = v
                temp[k] = [self.account.money, t]
            else:
                temp[k] = v
        return temp


class my_dict(dict):
    def __init__(self, *dicts: dict, default=None):
        di = dicts[0]
        for d in dicts:
            for k, v in d.items():
                if k not in di:
                    di[k] = v
        super().__init__(di)
        self.default = default

    def __getitem__(self, key: str) -> str | Any:
        if key in self:
            return super().__getitem__(key)
        if self.default is None:
            return f"text ['{key}'] not found"
        return self.default


class PlayerManager:
    def __init__(self):
        self.switch_language(default_language)

    def switch_language(self, language: str):
        global TEXT
        with open(data_dir + "\\" + language + "\\text.json5", "r") as f:
            data = json5.load(f)
        if language != default_language:
            with open(data_dir + "\\" + default_language + "\\text.json5", "r") as f:
                TEXT = my_dict(data, json5.load(f))
        else:
            TEXT = my_dict(data)

    def create_role(self):
        def load_archive() -> Player | None:
            while True:
                inp = input(TEXT["create_role_0"])
                if inp == "-1":
                    break
                path = save_dir + "\\" + inp + ".json5"
                if os.path.isfile(path):
                    player = Player()
                    with open(path, "r") as f:
                        player.update(json5.load(f))
                    self.switch_language(player.language)
                    return player
                else:
                    print(TEXT["create_role_1"])

        while True:
            option = input(f"[1.{TEXT['create_role_2']}][2.{TEXT['create_role_3']}][3.{TEXT['create_role_4']}]:")
            if option == "1":
                player = load_archive()
                if player is None:
                    continue
                return player
            elif option == "2":
                return Player(input(TEXT["create_role_5"]))
            elif option == "3":
                return
            else:
                print(TEXT["input_error"])

    def save_archive(self, player: Player, path: str = None):
        if path is None:
            path = save_dir + f"\\{player.name}.json5"
        while True:
            if os.path.isfile(path):
                inp = input(f"{TEXT['save_archive_0']}\t[1.{TEXT['save_archive_1']}][2.{TEXT['save_archive_2']}][3.{TEXT['save_archive_3']}]:")
                match inp:
                    case "1":
                        path = save_dir + "\\" + input(TEXT["save_archive_4"]) + ".json5"
                        continue
                    case "2":
                        pass
                    case "3":
                        break
                    case _:
                        print(TEXT["input_error"])
                        continue
            with open(path, "w+") as f:
                f.write(json5.dumps(player.serialize()))
                break


class BankAccount:
    def __init__(self, account: str):
        self.money = 0
        self.name = account
        self.bag = Bag(dict(), default=0)
        self.credit = 100

    def deposit(self, amount: int) -> int:
        self.money += amount
        return self.money

    def withdraw(self, amount: int) -> int:
        if self.money <= amount:
            self.money -= amount
            return self.money
        else:
            return -1


class CreatItem:
    def __init__(self, id: str):
        self.id = id
        data = ITEM[id]
        self.name = data["name"]
        self.price = data["price"]
        self.decoration = data["decoration"]
        self.type = data["type"]
        if "other" in data:
            self.other = data["other"]

    def __str__(self) -> str:
        if self.decoration == 0:
            return self.name
        elif self.decoration == 1 or self.decoration == 2:
            name = self.name
            name = name.replace(TEXT["creat_item_0"], f"\033[32m{TEXT['creat_item_0']}\033[0m")
            name = name.replace(TEXT["creat_item_1"], f"\033[34m{TEXT['creat_item_1']}\033[0m")
            name = name.replace(TEXT["creat_item_2"], f"\033[35m{TEXT['creat_item_2']}\033[0m")
            name = name.replace(TEXT["creat_item_3"], f"\033[47m{TEXT['creat_item_3']}\033[0m")
            name = name.replace(TEXT["creat_item_4"], f"\033[43m{TEXT['creat_item_4']}\033[0m")
            name = name.replace(TEXT["creat_item_5"], f"\033[42m{TEXT['creat_item_5']}\033[0m")
            name = name.replace(TEXT["creat_item_6"], f"\033[46m{TEXT['creat_item_6']}\033[0m")
            name = name.replace(TEXT["creat_item_7"], f"\033[44m{TEXT['creat_item_7']}\033[0m")
            name = name.replace(TEXT["creat_item_8"], f"\033[41m{TEXT['creat_item_8']}\033[0m")
            name = name.replace(TEXT["creat_item_9"], f"\033[40m{TEXT['creat_item_9']}\033[0m")
            name = name.replace(TEXT["creat_item_10"], f"\033[45m{TEXT['creat_item_10']}\033[0m")
            name = name.replace(TEXT["creat_item_11"], f"\033[47m{TEXT['creat_item_11']}\033[0m")
            name = name.replace(TEXT["creat_item_12"], f"\033[42m{TEXT['creat_item_12']}\033[0m")
            name = name.replace(TEXT["creat_item_13"], f"\033[40m{TEXT['creat_item_13']}\033[0m")
            name = name.replace(TEXT["creat_item_14"], f"\033[41m{TEXT['creat_item_14']}\033[0m")
            name = name.replace(TEXT["creat_item_15"], f"\033[43m{TEXT['creat_item_15']}\033[0m")
            name = name.replace(TEXT["creat_item_16"], f"\033[32m{TEXT['creat_item_16']}\033[0m")
            name = name.replace(TEXT["creat_item_17"], f"\033[36m{TEXT['creat_item_17']}\033[0m")
            name = name.replace(TEXT["creat_item_18"], f"\033[31m{TEXT['creat_item_18']}\033[0m")
            return name
        elif self.decoration == 2:
            name = self.name
            name = name.replace(TEXT["creat_item_0"], f"\033[32m{TEXT['creat_item_0']}\033[0m")
            name = name.replace(TEXT["creat_item_1"], f"\033[34m{TEXT['creat_item_1']}\033[0m")
            name = name.replace(TEXT["creat_item_2"], f"\033[35m{TEXT['creat_item_2']}\033[0m")
            name = name.replace(TEXT["creat_item_3"], f"\033[47m{TEXT['creat_item_3']}\033[0m")
            name = name.replace(TEXT["creat_item_4"], f"\033[43m{TEXT['creat_item_4']}\033[0m")
            name = name.replace(TEXT["creat_item_5"], f"\033[42m{TEXT['creat_item_5']}\033[0m")
            name = name.replace(TEXT["creat_item_6"], f"\033[46m{TEXT['creat_item_6']}\033[0m")
            name = name.replace(TEXT["creat_item_7"], f"\033[44m{TEXT['creat_item_7']}\033[0m")
            name = name.replace(TEXT["creat_item_8"], f"\033[41m{TEXT['creat_item_8']}\033[0m")
            name = name.replace(TEXT["creat_item_9"], f"\033[40m{TEXT['creat_item_9']}\033[0m")
            name = name.replace(TEXT["creat_item_10"], f"\033[45m{TEXT['creat_item_10']}\033[0m")
            return name

    def __format__(self, format_space) -> str:
        return self.__str__()


class Bag(my_dict):
    def __init__(self, *dicts: dict, default=None):
        super().__init__(*dicts, default=default)

    def renew(self):
        for k, v in list(self.items()):
            if v <= 0:
                del self[k]

    def getItem(self) -> tuple[CreatItem, int]:
        self.show()
        while True:
            item = input(TEXT["store_item_0"])
            if item == "-1":
                return -1, -1
            try:
                item = int(item)
            except ValueError:
                print(TEXT["store_item_1"])
                continue
            if item < 1 or item > len(self):
                print(TEXT["store_item_2"])
                continue
            item = list(self)[item - 1]
            quantity = input(TEXT["store_item_3"])
            try:
                quantity = int(quantity)
            except TypeError:
                print(TEXT["store_item_1"])
                continue
            if quantity < 1:
                print(TEXT["store_item_4"])
                continue
            if quantity > self[item]:
                print(TEXT["store_item_5"])
                continue
            return item, quantity

    def show(self):
        if len(self) != 0:
            l0 = max(len(str(len(self))), len(TEXT["show_1"]))
            l1 = max(max(len(k.name) for k in self), len(TEXT["show_1"]))
            l2 = max(max(len(str(v)) for v in self.values()), len(TEXT["show_1"]))
            i = 1
            print(f"{TEXT['show_0']:^{l0+2}}{TEXT['show_1']:^{l1+2}}{TEXT['show_2']:^{l2+2}} {TEXT['show_3']}")
            for k, v in self.items():
                print(f"[{str(i)+'.':<{l0+1}}][{k:<{l1}}][{v:<{l2}}][{k.price}]")
                i += 1
        else:
            print(f"{TEXT['show_0']} {TEXT['show_1']} {TEXT['show_2']} {TEXT['show_3']}")
            print(TEXT["show_4"])

    def loadItem(self, itemDict: dict):
        for k, v in itemDict.items():
            self[CreatItem(k)] += v


def locationDecorator(fn):
    def f(*args, **kwargs):
        location = player.location
        result = fn(*args, **kwargs)
        player.location = location
        return result

    return f


class Shop:
    def __init__(self, name: str, top_floor):
        self.name = name
        self.top_floor = top_floor

    @locationDecorator
    def run(self):
        f = True
        floor = 1
        while f:
            if 1 <= floor <= self.top_floor:
                print(TEXT[f"{self.name}_shop_{floor-1}"])
                player.location = f"{self.name}_shop_f{floor}"
            else:
                print(TEXT["shop_0"].format(floor))
                if floor > self.top_floor:
                    floor = self.top_floor
                elif floor < 1:
                    floor = 1
                continue
            with open(data_dir + "\\product_list.json5", "r") as f:
                product_list: list[CreatItem] = list(map(CreatItem, json5.load(f)[f"{self.name}_shop_f{floor}"]))
            player.bag.renew()
            while f:
                option = input(f"[1.{TEXT[f'shop_1']}][2.{TEXT[f'shop_2']}][3.{TEXT[f'shop_3']}][4.{TEXT[f'shop_4']}][5.{TEXT[f'shop_5']}]:")
                match option:
                    case "1":
                        print(TEXT["shop_6"])
                        l1 = len(str(len(product_list))) + 1
                        l2 = max(wcwidth.wcswidth(v.name) for v in product_list)
                        l3 = max(len(str(v.price)) for v in product_list)
                        for i in range(len(product_list)):
                            print(f"[{str(i+1)+'.':<{l1}}][{pad(product_list[i], l2, '<')}][{product_list[i].price:>{l3}}$]")
                        while True:
                            choose = input(TEXT["shop_7"])
                            if choose == "-1":
                                break
                            try:
                                choose = int(choose)
                            except ValueError:
                                print(TEXT["shop_8"])
                                continue
                            if choose < 1 or choose > len(product_list):
                                print(TEXT["shop_9"])
                                continue
                            choose = product_list[choose - 1]
                            quantity = input(TEXT["shop_10"])
                            try:
                                quantity = int(quantity)
                            except TypeError:
                                print(TEXT["shop_8"])
                                continue
                            if quantity < 1:
                                print(TEXT["shop_11"])
                                continue
                            if player.money >= choose.price * quantity:
                                player.money -= choose.price * quantity
                                player.bag[choose] += quantity
                                print(TEXT["shop_12"].format(quantity, choose, choose.price * quantity, player.money))
                                break
                            else:
                                print(TEXT["shop_13"].format(player.money))
                    case "2":
                        choose, quantity = player.bag.getItem()
                        if choose == -1 and quantity == -1:
                            continue
                        m = choose.price // 2 * quantity
                        player.money += m
                        player.bag[choose] -= quantity
                        player.bag.renew()
                        print(TEXT["shop_14"].format(quantity, choose, m, player.money))
                    case "3":
                        floor += 1
                        break
                    case "4":
                        floor -= 1
                        break
                    case "5":
                        f = False
                    case _:
                        print(TEXT["input_error"])


def init(data: str, save: str) -> my_dict[str:str]:
    global data_dir, save_dir, default_language, ITEM, TEXT, CONFIG
    data_dir = data
    save_dir = save
    with open(data_dir + "\\config.json5", "r") as f:
        CONFIG = my_dict(json5.load(f))
    default_language = CONFIG["default_language"]
    with open(data_dir + "\\" + default_language + "\\text.json5", "r") as f:
        TEXT = my_dict(json5.load(f))
    with open(data_dir + "\\" + default_language + "\\item_list.json5", "r") as f:
        ITEM = my_dict(json5.load(f))
    return TEXT


def set_player(p: Player):
    global player
    player = p


def pad(s: CreatItem | str, width, align=">") -> str:
    if type(s) == CreatItem:
        padding = width - wcwidth.wcswidth(s.name)
        s = s.__str__()
    else:
        padding = width - wcwidth.wcswidth(s)
    if align == ">":
        return " " * padding + s
    elif align == "<":
        return s + " " * padding
    elif align == "^":
        left_padding = padding // 2
        right_padding = padding - left_padding
        return " " * left_padding + s + " " * right_padding
    else:
        raise ValueError("Invalid alignment")
