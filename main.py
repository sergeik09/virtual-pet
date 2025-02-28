import pygame as pg
import random
import json

# Инициализация pg
pg.init()

click_sound = pg.mixer.Sound('click_sound.mp3')
# Размеры окна
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550


DOG_SIZE = (310, 500)

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

FOOD_SIZE = 200

TOY_SIZE = 100

MENU_NAV_XPAD = 90
MENU_NAV_YPAD = 130
ICON_SIZE = 85

PADDING = 5


FPS = 60

DOG_COORDS = (SCREEN_WIDTH//2 - DOG_SIZE[0]//2, SCREEN_HEIGHT-PADDING - DOG_SIZE[1])

main_font = pg.font.Font(None, 42)
mini_font = pg.font.Font(None, 15)
max_font = pg.font.Font(None, 72)
def text_render(text, font=main_font):
    return font.render(str(text), True, pg.Color('black'))


def load_image(file, width, height):
    image = pg.image.load(file)
    return pg.transform.scale(image, (width, height))

class Button:
    def __init__(self, text, x, y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=main_font, func=None):
        self.func = func
        self.idle_image = load_image('images/button.png', width, height)
        self.pressed_image = load_image('images/button_clicked.png', width, height)

        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.is_pressed = False
        self.text = text_render(text, font)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and self.is_pressed:
            self.image = self.pressed_image
        else:
            self.image = self.idle_image

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                click_sound.play()
                self.func()
        elif event.type == pg.MOUSEBUTTONUP and event.button ==1:
            self.is_pressed = False



class Item:
    def __init__(self, name, price, file, is_bought=False, is_using=False):
        self.file = file
        self.image = load_image(file, DOG_SIZE[0]//1.7, DOG_SIZE[1]//1.7)
        self.name = name
        self.price = price
        self.is_bought=is_bought
        self.is_using = is_using
        self.full_image = load_image(file, *DOG_SIZE)
class Food:
    def __init__(self, name, price, file, satiety, medicine_power=0):
        self.name = name
        self.price = price
        self.image = load_image(file, FOOD_SIZE, FOOD_SIZE)
        self.satiety = satiety
        self.medicine_power = medicine_power


class ClothesMenu:
    def __init__(self, game, data):
        self.game = game

        self.menu_page = load_image('images/menu/menu_page.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_off = load_image('images/menu/bottom_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image('images/menu/bottom_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image('images/menu/top_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image('images/menu/top_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [Item(**item) for item in data["clothes"]]



        self.current_item  = 0
        self.item_rect = self.items[self.current_item].image.get_rect()
        self.item_rect.center = SCREEN_WIDTH //2, SCREEN_HEIGHT //2

        self.next_button = Button('Вперёд', SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD, width=BUTTON_WIDTH //1.2, height=BUTTON_HEIGHT // 1.2,
                                  func=self.to_next)
        self.previous_button = Button('Назад', MENU_NAV_XPAD + 30, SCREEN_HEIGHT - MENU_NAV_YPAD,
                                      width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT //1.2),
                                      func=self.to_previous)

        self.use_button = Button('Надеть', MENU_NAV_XPAD + 30, SCREEN_HEIGHT - MENU_NAV_YPAD - 50 - PADDING,
                                  width=BUTTON_WIDTH // 1.2, height=BUTTON_HEIGHT // 1.2,
                                  func=self.use_item)
        self.buy_button = Button('Купить', SCREEN_WIDTH//2 - int(BUTTON_WIDTH//1.5)//2, SCREEN_HEIGHT//2+95,
                                 width=int(BUTTON_WIDTH//1.5), height=int(BUTTON_HEIGHT//1.5),
                                 func=self.buy)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH //2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH //2, 120)

        self.use_text = text_render('Надето')
        self.use_text_rect = self.use_text.get_rect()
        self.use_text_rect.midright = (SCREEN_WIDTH - 150, 130)


        self.buy_text = text_render('Куплено')
        self.buy_text_rect = self.buy_text.get_rect()
        self.buy_text_rect.midright = (SCREEN_WIDTH - 140, 200)



    def draw(self, screen:pg.Surface):
        screen.blit(self.menu_page, (0,0))
        screen.blit(self.items[self.current_item].image, self.item_rect)

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0,0))
        else:
            screen.blit(self.bottom_label_off, (0,0))


        if self.items[self.current_item].is_using:
            screen.blit(self.top_label_on, (0,0))
        else:
            screen.blit(self.top_label_off, (0,0))

        self.next_button.draw(screen)
        self.use_button.draw(screen)
        self.buy_button.draw(screen)
        self.previous_button.draw(screen)

        screen.blit(self.buy_text, self.buy_text_rect)

        screen.blit(self.use_text, self.use_text_rect)

        screen.blit(self.name_text, self.name_text_rect)

        screen.blit(self.price_text, self.price_text_rect)
    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.use_button.is_clicked(event)
        self.buy_button.is_clicked(event)
        self.previous_button.is_clicked(event)

    def update(self):
        self.next_button.update()


    def to_next(self):
        if self.current_item != len(self.items) -1:
            self.current_item += 1
        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def to_previous(self):
        if self.current_item != 0:
            self.current_item -= 1
        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)



    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True

    def use_item(self):
        self.items[self.current_item].is_using = not self.items[self.current_item].is_using

class FoodMenu:
    def __init__(self, game):
        self.game = game

        self.menu_page = load_image('images/menu/menu_page.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_off = load_image('images/menu/bottom_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image('images/menu/bottom_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image('images/menu/top_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image('images/menu/top_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [
            Food('Яблоко', 20, 'images/food/apple.png', 10),
            Food('Лекарства', 30, 'images/food/medicine.png', 0,20),
            Food('Мясо', 20, 'images/food/meat.png', 40),
            Food('Собачий корм', 20, 'images/food/dog food.png', 30)

        ]

        self.current_item  = 0
        self.item_rect = self.items[self.current_item].image.get_rect()
        self.item_rect.center = SCREEN_WIDTH //2, SCREEN_HEIGHT //2

        self.next_button = Button('Вперёд', SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD, width=BUTTON_WIDTH //1.2, height=BUTTON_HEIGHT // 1.2,
                                  func=self.to_next)
        self.previous_button = Button('Назад', MENU_NAV_XPAD + 30, SCREEN_HEIGHT - MENU_NAV_YPAD,
                                      width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT //1.2),
                                      func=self.to_previous)

        self.buy_button = Button('Cъесть', SCREEN_WIDTH//2 - int(BUTTON_WIDTH//1.5)//2, SCREEN_HEIGHT//2+95,
                                 width=int(BUTTON_WIDTH//1.5), height=int(BUTTON_HEIGHT//1.5),
                                 func=self.buy)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH //2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH //2, 120)






    def draw(self, screen:pg.Surface):
        screen.blit(self.menu_page, (0,0))
        screen.blit(self.items[self.current_item].image, self.item_rect)

        # if self.items[self.current_item].is_bought:
        #     screen.blit(self.bottom_label_on, (0,0))
        # else:
        #     screen.blit(self.bottom_label_off, (0,0))
        #
        #
        # if self.items[self.current_item].is_using:
        #     screen.blit(self.top_label_on, (0,0))
        # else:
        #     screen.blit(self.top_label_off, (0,0))

        self.next_button.draw(screen)
        self.buy_button.draw(screen)
        self.previous_button.draw(screen)


        screen.blit(self.name_text, self.name_text_rect)

        screen.blit(self.price_text, self.price_text_rect)
    def is_clicked(self, event):
        self.next_button.is_clicked(event)

        self.buy_button.is_clicked(event)
        self.previous_button.is_clicked(event)

    def update(self):
        self.next_button.update()


    def to_next(self):
        if self.current_item != len(self.items) -1:
            self.current_item += 1
        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def to_previous(self):
        if self.current_item != 0:
            self.current_item -= 1
        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)



    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price

            self.game.satiety += self.items[self.current_item].satiety
            if self.game.satiety >100:
                self.game.satiety = 100
            self.game.health += self.items[self.current_item].medicine_power
            if self.game.health > 100:
                self.game.health = 100


class Dog(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = load_image('images/dog.png', DOG_SIZE[0]//2, DOG_SIZE[1]//2)
        self.rect = self.image.get_rect()
        self.rect.center = SCREEN_WIDTH//2, SCREEN_HEIGHT - MENU_NAV_YPAD - 20

    def update(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.rect.x -= 5

        if keys[pg.K_d]:
            self.rect.x += 5







class MiniGame:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image('images/game_background.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dog = Dog()

        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 5000000

        self.item_interval = pg.time.get_ticks()

    def new_game(self):

        self.dog = Dog()

        self.toys = pg.sprite.Group(Toy())

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 5000
        self.item_interval = pg.time.get_ticks()
    def update(self):
        self.dog.update()
        self.toys.update()
        if pg.time.get_ticks() - 500 > self.item_interval:
            self.toys.add(Toy())
            self.item_interval = pg.time.get_ticks()
        hits = pg.sprite.spritecollide(self.dog, self.toys, True, pg.sprite.collide_rect_ratio(0.6))
        self.score += len(hits)
        if pg.time.get_ticks() - self.start_time > self.interval:
            self.game.happiness += int(self.score //2)
            self.game.mode = "Main"

    def draw(self, screen: pg.Surface):
        screen.blit(self.menu_page, (0,0))
        screen.blit(text_render(self.score), (MENU_NAV_XPAD + 20, 80))
        self.toys.draw(screen)
        screen.blit(self.dog.image, self.dog.rect)

class Toy(pg.sprite.Sprite):
    toys = [load_image('images/toys/ball.png', TOY_SIZE, TOY_SIZE),
            load_image('images/toys/blue bone.png', TOY_SIZE, TOY_SIZE),
            load_image('images/toys/red bone.png', TOY_SIZE, TOY_SIZE)]
    def __init__(self):
        super().__init__()
        self.image = random.choice(self.toys)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(MENU_NAV_XPAD, SCREEN_WIDTH - MENU_NAV_XPAD - TOY_SIZE)
        self.rect.y = 30


    def update(self):

        self.rect.y += 5

class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.satiety_image = load_image('images/satiety.png', ICON_SIZE, ICON_SIZE)
        self.health_image = load_image('images/health.png', ICON_SIZE, ICON_SIZE)

        self.happiness_image = load_image('images/happiness.png', ICON_SIZE, ICON_SIZE)
        self.dog_image = load_image('images/dog.png', *DOG_SIZE)
        self.money_image = load_image('images/money.png', ICON_SIZE, ICON_SIZE)

        button_x = SCREEN_WIDTH - BUTTON_WIDTH - PADDING

        self.eat_button = Button('Еда',button_x, PADDING + ICON_SIZE, func=self.food_menu_on)

        self.clothes_button = Button('Одежда', button_x, PADDING*2 + ICON_SIZE + BUTTON_HEIGHT, func=self.clothes_menu_on)

        self.games_button = Button('Игры', button_x, PADDING*3 + ICON_SIZE + BUTTON_HEIGHT*2, func=self.game_menu_on)

        self.upgrade_button = Button('Улучшить', SCREEN_WIDTH - ICON_SIZE, 0,
                                     width=BUTTON_WIDTH //3, height=BUTTON_HEIGHT//3,
                                     font=mini_font, func=self.increase_money)




        self.buttons = [self.eat_button, self.clothes_button, self.upgrade_button, self.games_button]
        with open('save.json', 'r', encoding="utf-8") as save:
            data = json.load(save)
        self.happiness = data["happiness"]
        self.satiety = data["satiety"]
        self.health = data["health"]
        self.money = data["money"]
        self.coins_per_second = data["coins_per_second"]

        self.mode = 'Main'

        self.costs_of_upgrade = {}
        for key, value in data["costs_of_upgrade"].items():
            self.costs_of_upgrade[int(key)] = value


        self.INCREASE_COINS = pg.USEREVENT + 1
        self.DECREASE = pg.USEREVENT + 2
        self.clothes_menu = ClothesMenu(self, data)

        self.game_menu = MiniGame(self)
        self.food_menu = FoodMenu(self)



        pg.time.set_timer(self.INCREASE_COINS, 1000)
        pg.time.set_timer(self.DECREASE, 1000)

        pg.display.set_caption("Виртуальный питомец")
        self.clock = pg.time.Clock()
        self.clock.tick(FPS)
        self.run()




    def increase_money(self):
        for i in self.costs_of_upgrade:
            if self.money >= i and not self.costs_of_upgrade[i]:
                self.costs_of_upgrade[i] = True
                self.money -= i
                self.coins_per_second += 5
                break
    def clothes_menu_on(self):
        self.mode = 'Clothes menu'
    def food_menu_on(self):
        self.mode = 'Food menu'
    def game_menu_on(self):
        self.mode = 'Game menu'

    def run(self):
        while True:

            self.event()
            self.update()
            self.draw()

    def event(self):
        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN and event.button==1:
                self.money += 1
            if event.type == self.INCREASE_COINS:
                self.money += self.coins_per_second

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.mode="Main"

            if event.type == self.DECREASE:
                chance = random.randint(1, 10)
                if chance <= 5:
                    self.satiety -= 1
                elif 5 < chance <= 9:
                    self.happiness -= 1
                else:
                    self.health -= 1

            if event.type == pg.QUIT:
                if self.mode == "Game over":
                    data = {
                        "happiness": 100,
                        "satiety": 100,
                        "health": 100,
                        "money": 12930,
                        "coins_per_second": 1,
                        "costs_of_upgrade": {
                            "100": False,
                            "1000": False,
                            "5000": False,
                            "10000": False
                        },
                        "clothes": [
                            {"name": "Синяя футболка",
                             "price": 10,
                             "file": "images/items/blue t-shirt.png",
                             "is_bought": False,
                             "is_using": False
                             },
                            {"name": "Золотая цепь",
                             "price": 20,
                             "file": "images/items/gold chain.png",
                             "is_bought": False,
                             "is_using": False
                             },
                            {"name": "Ботинки",
                             "price": 5,
                             "file": "images/items/boots.png",
                             "is_bought": False,
                             "is_using": False
                             }
                        ]
                    }
                else:
                    data = {
                        "happiness": self.happiness,
                        "satiety": self.satiety,
                        "health": self.health,
                        "money": self.money,
                        "coins_per_second": self.coins_per_second,
                        "costs_of_upgrade": {
                            "100": self.costs_of_upgrade[100],
                            "1000": self.costs_of_upgrade[1000],
                            "5000": self.costs_of_upgrade[5000],
                            "10000": self.costs_of_upgrade[10000]
                        },
                        "clothes": []
                    }
                    for item in self.clothes_menu.items:
                        item_data = item.__dict__
                        del item_data["image"]
                        del item_data["full_image"]
                        data["clothes"].append(item_data)
                with open("save.json", "w", encoding="utf-8") as save:
                    json.dump(data, save, ensure_ascii = False, indent = 2)

                pg.quit()
                exit()
            if self.mode == 'Clothes menu':
                self.clothes_menu.is_clicked(event)
            if self.mode == 'Food menu':
                self.food_menu.is_clicked(event)
            self.eat_button.is_clicked(event)
            self.clothes_button.is_clicked(event)
            self.games_button.is_clicked(event)
            self.upgrade_button.is_clicked(event)

    def update(self):
        if self.mode == "Game over":
            return
        for button in self.buttons:
            button.update()

        if self.mode == 'Clothes menu':
            self.clothes_menu.update()
        if self.mode == 'Food menu':
            self.food_menu.update()

        if self.mode == 'Game menu':
            self.game_menu.update()
        if self.satiety <= 0:
            self.health -= 5
        if self.health <= 0 or self.happiness <=0:
            self.mode = "Game over"
    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.happiness_image, (PADDING, PADDING))
        self.screen.blit(self.satiety_image, (PADDING, PADDING + ICON_SIZE))
        self.screen.blit(self.health_image, (PADDING, PADDING + ICON_SIZE*2))
        self.screen.blit(self.dog_image, DOG_COORDS)
        self.screen.blit(self.money_image, (SCREEN_WIDTH - PADDING - ICON_SIZE, PADDING))
        self.screen.blit(text_render(self.happiness), (PADDING + ICON_SIZE, ICON_SIZE//2))
        self.screen.blit(text_render(self.satiety), (PADDING + ICON_SIZE, ICON_SIZE + ICON_SIZE//2))
        self.screen.blit(text_render(self.happiness), (PADDING + ICON_SIZE, ICON_SIZE*2 + ICON_SIZE//2))
        self.screen.blit(text_render(self.money), (SCREEN_WIDTH - ICON_SIZE*2 + PADDING*4, ICON_SIZE//2 - PADDING))


        for button in self.buttons:
            button.draw(self.screen)

        for item in self.clothes_menu.items:
            if item.is_using:
                self.screen.blit(item.full_image, (SCREEN_WIDTH//2-DOG_SIZE[0]//2, DOG_COORDS[1]))
        if self.mode == 'Clothes menu':
            self.clothes_menu.draw(self.screen)

        if self.mode == 'Food menu':
            self.food_menu.draw(self.screen)

        if self.mode == 'Game menu':
            self.game_menu.draw(self.screen)
        if self.mode == "Game over":
            text = max_font.render("ПРОИГРЫШ", "Red")
            text_rect = text.get_Rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, text_rect)
        pg.display.flip()
  

if __name__ == "__main__":
    Game()