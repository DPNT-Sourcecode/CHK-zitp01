import re

'''
Our price table and offers: 
+------+-------+------------------------+
| Item | Price | Special offers         |
+------+-------+------------------------+
| A    | 50    | 3A for 130, 5A for 200 |
| B    | 30    | 2B for 45              |
| C    | 20    |                        |
| D    | 15    |                        |
| E    | 40    | 2E get one B free      |
+------+-------+------------------------+
'''
# Define price and special offers
price_tble = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    'E': 40
}
offers = {
    'A': '3A for 130, 5A for 200',
    'B': '2B for 45',
    'E': '2E get one B free'
}

def extractOffer(offer_str):
    reg_exp = re.compile(r'([0-9]+)([A-Z]) for ([0-9]+)')
    offer = reg_exp.fullmatch(offer_str)
    return offer.groups() if offer else None

# basket - dictionary of products and quantity
# Returns integer value - total price of products
def calculate_total(basket):
    total = 0
    for product, quantity in basket.items():
        # Check if product qualifies for special offer
        if product in offers:
            offer_str = offers[product]
            offer = extractOffer(offer_str)
            # Check quantity matches offer
            while offer is not None and quantity >= int(offer[0]):
                # Add special offer value to total
                total += int(offer[2])
                quantity -= int(offer[0])

        # Add price value to total
        total += quantity * price_tble[product]
    
    return total

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    # Validate legal input
    if not isinstance(skus, str)and not skus.isalpha() and len(skus) > 0:
        return -1
    if len(skus) == 0:
        return 0
    
    basket = {}
    for product in skus:
        # Return -1 if product is non existant
        if product not in price_tble:
            return -1
        
        if product in basket:
            basket[product] += 1
        else:
            basket[product] = 1

    total = calculate_total(basket)
    return total


