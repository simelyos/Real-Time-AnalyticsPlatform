import random
import faker
import sys


'''for _ in range(10):
    print(round(random.uniform(-0.1,0.1),2))


fake = faker.Faker()

print(fake.date_time_between(start_date="-2y",end_date="now"))
'''

'''print(random.random())'''

ORDER_STATUSES = [
    ("completed", 0.88),
    ("pending", 0.05),
    ("cancelled", 0.04),
    ("returned", 0.03),
]

'''status = random.choices(
                [s for s, _ in ORDER_STATUSES], weights=[w for _, w in ORDER_STATUSES],k=1)

print(status)'''

'''columns = "Column"
placeholders = ", ".join(["%s"] * len(columns))

print(placeholders)'''

print(sys.path)