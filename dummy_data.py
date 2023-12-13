import os , django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from faker import Faker
import random
from products.models import Product,Brand,Review


def seed_brand(n):
    fake = Faker()
    image = ['01.jpg','02.jpg','03.jpg','04.jpg','05.jpg','06.jpg','07.jpg','08.jpg','09.jpg','10.jpg']
    
    for _ in range(n):
        Brand.objects.create(
            name = fake.name(),
            images = f"brand/{image[random.randint(0,9)]}"
        )
    print(f"{n} Brands was added successfully")


def seed_products(n):
    fake = Faker()
    flag_types = ['New', 'Sale', 'Feature']
    brands = Brand.objects.all()
    images = ['01.jpg','02.jpg','03.jpg','04.jpg','05.jpg','06.jpg','07.jpg','08.jpg','09.jpg','10.jpg']
    
    for _ in range(n):
        Product.objects.create(
           name = fake.name(), 
           flag = flag_types[random.randint(0,2)],
           price = round(random.uniform(20.99,99.99),2),
           images = f"product/{images[random.randint(0,9)]}" ,
           sku = random.randint(100,1000000),
           subtitle = fake.text(max_nb_chars = 450),
           discription = fake.text(max_nb_chars = 4000),
           brand = brands[random.randint(0,len(brands)-1)],
        )
    print(f"{n} Products was added successfully")
        

def seed_reviews(n):
    pass


# seed_brand(200)
seed_products(1500)