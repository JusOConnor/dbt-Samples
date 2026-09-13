'''
Builds the sample foodservice distribution data for the dbt lab.

You run this once (from the setup notebook or the command line) to create four
CSV files in the raw_data folder. The data is intentionally a little messy:
inconsistent capitalization, mixed date formats, a duplicate customer, and some
missing values. That mess is on purpose. It gives your dbt staging models real
cleaning work to do, which is exactly what staging models are for.

The data is generated with a fixed random seed, so you get the same rows every
time you run it. That makes your results reproducible.
'''

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

# A fixed seed means 'random' produces the same sequence on every run.
RANDOM_SEED = 47

# How much data to create.
NUM_CUSTOMERS = 2000
NUM_PRODUCTS = 1500
NUM_ORDERS = 30000

# The two year window that orders fall within.
START_DATE = date(2020, 1, 1)
END_DATE = date(2025, 12, 31)


def build_customers():
    '''Create the customer (operator) records with deliberate mess.'''
    segments = ['Independent', 'Regional Chain', 'National Account']
    cities = [
        ('Chicago', 'IL'), ('Milwaukee', 'WI'), ('Detroit', 'MI'),
        ('Indianapolis', 'IN'), ('Columbus', 'OH'), ('Minneapolis', 'MN'),
        ('St. Louis', 'MO'), ('Kansas City', 'MO'), ('Nashville', 'TN'),
    ]
    first_words = ['Prairie', 'Lakeside', 'Golden', 'Corner', 'Harvest',
                   'Sunrise', 'Maple', 'Copper', 'Cedar', 'River']
    second_words = ['Diner', 'Bistro', 'Grill', 'Kitchen', 'Cafe',
                    'Eatery', 'Table', 'Provisions', 'Foods', 'Catering']

    rows = []
    for customer_id in range(1, NUM_CUSTOMERS + 1):
        name = f'{random.choice(first_words)} {random.choice(second_words)}'

        # Randomly force some names to upper or lower case, and padding a few
        # with stray spaces. Your staging model will standardize all of this.
        style = random.random()
        if style < 0.2:
            name = name.upper()
        elif style < 0.4:
            name = name.lower()
        elif style < 0.5:
            name = f'  {name}  '

        city, state = random.choice(cities)

        # signup_date is stored as text in two different formats with some null values.
        signup = random_date(START_DATE, END_DATE)
        roll = random.random()
        if roll < 0.15:
            signup_text = None
        elif roll < 0.4:
            signup_text = signup.strftime('%m/%d/%Y')
        else:
            signup_text = signup.strftime('%Y-%m-%d')

        rows.append({
            'customer_id': customer_id,
            'customer_name': name,
            'segment': random.choice(segments),
            'city': city,
            'state': state,
            'signup_date': signup_text,
        })

    # Add one exact duplicate row.
    rows.append(dict(rows[0]))
    return pd.DataFrame(rows)


def build_products():
    '''Create the product catalog with category casing mess and some null costs.'''
    catalog = {
        'Eggs': ['Shell Eggs', 'Liquid Eggs', 'Specialty Eggs'],
        'Dairy': ['Milk', 'Butter', 'Cream', 'Yogurt'],
        'Bakery': ['Bread', 'Rolls', 'Pastries', 'Tortillas'],
        'Cheese': ['Block Cheese', 'Shredded Cheese', 'Specialty Cheese'],
    }
    brands = ['Farmstead', 'ValuePro', 'Chef Select', 'Heartland', 'Golden Crate']
    units = ['Case', 'Dozen', 'Each', 'Pound', 'Gallon']

    categories = list(catalog.keys())
    rows = []
    for product_id in range(1, NUM_PRODUCTS + 1):
        category = random.choice(categories)
        subcategory = random.choice(catalog[category])

        # The category is stored with random capitalization, so the same
        # category shows up as 'Dairy', 'dairy', and 'DAIRY'. Your staging model
        # will collapse these into one clean value.
        category_text = random.choice([category, category.upper(), category.lower()])

        # list_price is what the customer pays; unit_cost is what it costs us.
        list_price = round(random.uniform(8, 60), 2)
        unit_cost = round(list_price * random.uniform(0.55, 0.8), 2)

        # A few products are missing a cost that need to handled before we can calculate margin.
        if random.random() < 0.1:
            unit_cost = None

        rows.append({
            'product_id': product_id,
            'product_name': f'{random.choice(brands)} {subcategory}',
            'category': category_text,
            'subcategory': subcategory,
            'brand': random.choice(brands),
            'unit_of_measure': random.choice(units),
            'list_price': list_price,
            'unit_cost': unit_cost,
        })
    return pd.DataFrame(rows)


def build_orders():
    '''Create order headers. Dates are text, and status casing varies.'''
    statuses = ['placed', 'shipped', 'delivered', 'returned']
    channels = ['Phone', 'Online', 'Sales Rep']

    rows = []
    for order_id in range(1, NUM_ORDERS + 1):
        order_day = random_date(START_DATE, END_DATE)
        status = random.choices(statuses, weights=[10, 15, 70, 5])[0]

        # Occasionally the status arrives capitalized differently
        if random.random() < 0.2:
            status = status.capitalize()

        rows.append({
            'order_id': order_id,
            'customer_id': random.randint(1, NUM_CUSTOMERS),
            # Stored as an ISO text.  Need to use casting text to a date.
            'order_date': order_day.strftime('%Y-%m-%d'),
            'status': status,
            'channel': random.choice(channels),
        })
    return pd.DataFrame(rows)


def build_order_items(orders_df):
    '''Create the order line items.'''
    rows = []
    order_item_id = 1
    for order_id in orders_df['order_id']:
        # Each order has up to five different products on it.
        for _ in range(random.randint(1, 5)):
            product_id = random.randint(1, NUM_PRODUCTS)
            quantity = random.randint(1, 40)

            # The price actually charged flucuates around a base price and sometimes carries a discount
            unit_price = round(random.uniform(8, 60), 2)
            discount = round(random.choice([0, 0, 0, 0.05, 0.1, 0.15]), 2)

            rows.append({
                'order_item_id': order_item_id,
                'order_id': order_id,
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'discount': discount,
            })
            order_item_id += 1
    return pd.DataFrame(rows)


def random_date(start, end):
    '''Return a random date between two dates, inclusive.'''
    span = (end - start).days
    return start + timedelta(days=random.randint(0, span))


def generate_all(output_dir='raw_data'):
    '''
    Build every table and write it to CSV.

    Call this once to produce the raw files. Returns a dictionary of the
    DataFrames as well, in case you want to peek at them in the notebook.
    '''
    # Seed the generator so every run produces identical data.
    random.seed(RANDOM_SEED)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    customers = build_customers()
    products = build_products()
    orders = build_orders()
    order_items = build_order_items(orders)

    tables = {
        'raw_customers': customers,
        'raw_products': products,
        'raw_orders': orders,
        'raw_order_items': order_items,
    }

    for name, frame in tables.items():
        destination = output_path / f'{name}.csv'
        frame.to_csv(destination, index=False)
        print(f'Wrote {len(frame):>6} rows to {destination}')

    return tables


if __name__ == '__main__':
    generate_all()
