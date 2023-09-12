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

# Return eligible get one free offers - based on product quantity
def extract_gof_offers(offer_str, quantity):
    reg_exp = re.compile(r'([0-9]+)([A-Z]) get one ([A-Z]) free')
    offers = reg_exp.findall(offer_str)
    return filter(lambda x: (x <= quantity), offers)

# Return eligible multi value offers - based on product quantity
def extract_mv_offers(offer_str, quantity):
    reg_exp = re.compile(r'([0-9]+)([A-Z]) for ([0-9]+)')
    offers = reg_exp.findall(offer_str)
    return filter(lambda x: (x <= quantity), offers)

# Calculate best offer value to apply
def calculate_best_offer(offers):
    best_offer = None
    max_offer_value = 0
    for offer in offers:
        if offer[2].isalpha():
            offer_value = price_tble[offer[2]]
        else:
            offer_value = (offer[0] + (offer[1] * price_tble[offer[0]])) - offer[2]

        # Get max offer value
        if offer_value > max_offer_value:
            max_offer_value = offer_value
            best_offer = offer

    return best_offer


# basket - dictionary of products and quantity
# Returns integer value - total price of products
def calculate_total(basket):
    total = 0
    for product, quantity in basket.items():
        # Skip item
        if quantity == 0:
            continue
        # Check if product qualifies for special offer
        if product in offers:
            # Get eligible offers
            offer_str = offers[product]
            mv_offers = extract_mv_offers(offer_str)
            gof_offers = extract_gof_offers(offer_str)
            best_offer = calculate_best_offer(mv_offers + gof_offers)

            # Apply special offer value to total/basket
            if best_offer[2].isalpha():
                basket[product] -= 1
            else:
                total += int(best_offer[2])
                quantity -= int(best_offer[0])

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