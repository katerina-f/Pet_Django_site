from main.models import Realty, Saller, Tag

# продавцы
saller_1 = Saller(first_name="Иван", last_name="Иванов")
saller_1.save()

saller_2 = Saller(first_name="Петр", last_name="Петров")
saller_2.save()

# категории
flat = Category.objects.get(name="Квартира")
garage = Category.objects.get(name="Гараж")
storage = Category.objects.get(name="Склад")

# недвижимость
realty_1 = Realty.objects.create(name="Двухкомнатная квартира с видом на парк",
                               price=12000000, space=75,
                               description="Просторная квартира с окнами выходящими в парк, \
                                   в пешей доступности метро, торговые центры",
                               category=flat, saller=saller_1)

realty_2 = Realty.objects.create(name="Большая однушка у метро",
                               price=9000000, space=56,
                               description="Просторная однокомнатная квартира \
                                   с раздельным санузлом, напротив метро",
                               category=flat, saller=saller_1)

realty_3 = Realty(name="Большой гараж у ЖК", price=1000000, space=50,
                  description="Большой гараж во дворе жилого комплекса \
                  с утепленным вторым этажом",
                  category=garage, saller=saller_1)
realty_3.save()

realty_4 = Realty(name="", price=0, space=0,
                  description="",
                  category=garage, saller=saller_2)

realty_4.name = "гараж в охраняемом кооперативе"
realty_4.description = "Гараж типичной планировки в гаражном кооперативе"
realty_4.price = 600000
realty_4.space = 20
realty_4.save()

# получение данных
all_realty_objects = Realty.objects.all()
garages = Realty.objects.filter(category__name="Гараж")
saller_1_realty = saller_1.realty_set.filter(category__name="Квартира")
big_flat = Realty.objects.get(category__name="Квартира", space=75)
