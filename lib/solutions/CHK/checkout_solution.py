import re
'''
Our price table and offers: 
+------+-------+----------------+
| Item | Price | Special offers |
+------+-------+----------------+
| A    | 50    | 3A for 130     |
| B    | 30    | 2B for 45      |
| C    | 20    |                |
| D    | 15    |                |
+------+-------+----------------+

'''
# Define price and special offers
price_tble = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15
}
offers = {
    'A': '3A for 130',
    'B': '2B for 45'
}

# basket - dictionary of products and quantity
# Returns integer value - total price of products
def calculate_total(basket):
    total = 0
    for product, quantity in basket.items():
        # Check if product qualifies for special offer
        reg_exp = re.compile(r'[0-9]+[A-Z] for [0-9]+')
        if product in offers:
            offer_str = offers[product]



    return
# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    # Validate legal input
    if not isinstance(skus, str) or not skus.isalpha():
        return -1
    
    basket = {}
    for product in skus:
        # Return -1 if product is non existant
        if product not in price_tble:
            return -1
        
        if product in basket:
            basket[product] += 1
        else:
            basket[product] = 1

    raise NotImplementedError()

