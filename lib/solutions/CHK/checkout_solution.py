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
| F    | 10    | 2F get one F free      |
+------+-------+------------------------+
'''


# Define price and special offers
price_tble = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    'E': 40,
    'F': 10
}
offers = {
    'A': '3A for 130, 5A for 200',
    'B': '2B for 45',
    'E': '2E get one B free',
    'F': '2F get one F free'
}

# Extract special offers from strings
def extract_offers(offer_str):
    reg_exp1 = re.compile(r'([0-9]+)([A-Z]) get one ([A-Z]) free')
    reg_exp2 = re.compile(r'([0-9]+)([A-Z]) for ([0-9]+)')
    gof_offers = reg_exp1.findall(offer_str)
    mv_offers = reg_exp2.findall(offer_str)

    offers = []
    for offer in mv_offers:
        offers.append([offer[0], offer[1], offer[2]])

    for offer in gof_offers:
        if offer[1] == offer[2]:
            price = str(2 * price_tble[offer[1]])
            offers.append(['3', offer[1], price])
        else:
            offers.append([offer[0], offer[1], offer[2]])
    return offers

def getEligibleOffers(offers, basket):
    result = []
    for offer in offers:
        if offer[1] in basket and offer[0] <= basket[offer[1]]:
            if offer[2].isalpha():
                if offer[2] in basket and basket[offer[2]] > 0:
                    result.append(offer)
            else:
                result.append(offer)
    return result
    #mv_offers = list(filter(lambda x: (x[1] in basket and int(x[0]) <= basket[x[1]]), mv_offers))
    #gof_offers = list(filter(lambda x: (x[1] in basket and int(x[0]) <= basket[x[1]] and x[2] in basket and basket[x[2]] > 0), gof_offers))


# Calculate best offer value to apply
def calculate_best_offer(offers, basket):
    best_offer = None
    max_offer_value = 0
    for [q, p, val] in offers:
        if val.isalpha():
            offer_value = price_tble[val]
        else:
            offer_value = (int(q) * price_tble[p]) - int(val)

        # Get max offer value
        if offer_value > max_offer_value:
            max_offer_value = offer_value
            best_offer = [q, p, val]

    return best_offer


# basket - dictionary of products and quantity
# Returns integer value - total price of products
def calculate_total(basket):
    total = 0
    offer_str = ','.join(list(offers.values()))
    extractedOffers = extract_offers(offer_str)
    # Get best special offer
    best_offer = calculate_best_offer(extractedOffers, basket)
        
    # Apply special offer values to total/basket
    while best_offer is not None:
        product = best_offer[1]
        if best_offer[2].isalpha():
            total += int(best_offer[0]) * price_tble[best_offer[1]]
            basket[best_offer[2]] -= 1
            if basket[best_offer[2]] == 0:
                del basket[best_offer[2]]
        else:
            total += int(best_offer[2])

        basket[product] -= int(best_offer[0])

        # Remove from basket
        if basket[product] == 0:
            del basket[product]

        best_offer = calculate_best_offer(extractedOffers, basket)

    # Add normal priced items to total
    for product, quantity in basket.items():
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




