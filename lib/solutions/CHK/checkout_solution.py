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

'''
    - {"method":"checkout","params":["AAAAAAAA"],"id":"CHK_R2_020"}, expected: 330, got: 350
    - {"method":"checkout","params":["AAAAAAAAA"],"id":"CHK_R2_021"}, expected: 380, got: 400
    - {"method":"checkout","params":["AAAAAAAAAA"],"id":"CHK_R2_022"}, expected: 400, got: 450
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
def extract_gof_offers(offer_str):
    reg_exp = re.compile(r'([0-9]+)([A-Z]) get one ([A-Z]) free')
    offers = reg_exp.findall(offer_str)
    return offers

# Return eligible multi value offers - based on product quantity
def extract_mv_offers(offer_str):
    reg_exp = re.compile(r'([0-9]+)([A-Z]) for ([0-9]+)')
    offers = reg_exp.findall(offer_str)
    return offers

# Calculate best offer value to apply
def calculate_best_offer(mv_offers, gof_offers, quantity, basket):
    # Get eligible offers
    mv_offers = list(filter(lambda x: (int(x[0]) <= quantity), mv_offers))
    gof_offers = list(filter(lambda x: (int(x[0]) <= quantity and x[2] in basket and basket[x[2]] > 0), gof_offers))

    offers = mv_offers + gof_offers
    best_offer = None
    max_offer_value = 0
    for offer in offers:
        if offer[2].isalpha():
            offer_value = price_tble[offer[2]]
        else:
            offer_value = (int(offer[0]) * price_tble[offer[1]]) - int(offer[2])

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
        # Check if product is eligible for special offers
        if product in offers:
            offer_str = offers[product]
            mv_offers = extract_mv_offers(offer_str)
            gof_offers = extract_gof_offers(offer_str)

            best_offer = calculate_best_offer(mv_offers, gof_offers, quantity, basket)
            
            # Apply best special offer value to total/basket
            while best_offer is not None:
                if best_offer[2].isalpha():
                    basket[best_offer[2]] -= 1
                else:
                    total += int(best_offer[2])
                    quantity -= int(best_offer[0])

                best_offer = calculate_best_offer(mv_offers, gof_offers, quantity, basket)
            
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
