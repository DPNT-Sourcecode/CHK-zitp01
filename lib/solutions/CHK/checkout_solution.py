import re
'''
+------+-------+---------------------------------+
| Item | Price | Special offers                  |
+------+-------+---------------------------------+
| A    | 50    | 3A for 130, 5A for 200          |
| B    | 30    | 2B for 45                       |
| C    | 20    |                                 |
| D    | 15    |                                 |
| E    | 40    | 2E get one B free               |
| F    | 10    | 2F get one F free               |
| G    | 20    |                                 |
| H    | 10    | 5H for 45, 10H for 80           |
| I    | 35    |                                 |
| J    | 60    |                                 |
| K    | 70    | 2K for 120                      |
| L    | 90    |                                 |
| M    | 15    |                                 |
| N    | 40    | 3N get one M free               |
| O    | 10    |                                 |
| P    | 50    | 5P for 200                      |
| Q    | 30    | 3Q for 80                       |
| R    | 50    | 3R get one Q free               |
| S    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
| T    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
| U    | 40    | 3U get one U free               |
| V    | 50    | 2V for 90, 3V for 130           |
| W    | 20    |                                 |
| X    | 17    | buy any 3 of (S,T,X,Y,Z) for 45 |
| Y    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
| Z    | 21    | buy any 3 of (S,T,X,Y,Z) for 45 |
+------+-------+---------------------------------+
'''

# Define price and special offers
price_tble = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    'E': 40,
    'F': 10,
    'G': 20,
    'H': 10,
    'I': 35,
    'J': 60,
    'K': 70,
    'L': 90,
    'M': 15,
    'N': 40,
    'O': 10,
    'P': 50,
    'Q': 30,
    'R': 50,
    'S': 20,
    'T': 20,
    'U': 40,
    'V': 50,
    'W': 20,
    'X': 17,
    'Y': 20,
    'Z': 21
}
offers = {
    'A': '3A for 130, 5A for 200',
    'B': '2B for 45',
    'E': '2E get one B free',
    'F': '2F get one F free',
    'H': '5H for 45, 10H for 80',
    'K': '2K for 120',
    'N': '3N get one M free',
    'P': '5P for 200',
    'Q': '3Q for 80',
    'R': '3R get one Q free',
    'S': 'buy any 3 of (S,T,X,Y,Z) for 45',
    'T': 'buy any 3 of (S,T,X,Y,Z) for 45',
    'U': '3U get one U free',
    'V': '2V for 90, 3V for 130',
    'X': 'buy any 3 of (S,T,X,Y,Z) for 45',
    'Y': 'buy any 3 of (S,T,X,Y,Z) for 45',
    'Z': 'buy any 3 of (S,T,X,Y,Z) for 45'
}

# Extract special offers from strings
def extract_offers(offer_str):
    reg_exp1 = re.compile(r'([0-9]+)([A-Z]) get one ([A-Z]) free')
    reg_exp2 = re.compile(r'([0-9]+)([A-Z]) for ([0-9]+)')
    reg_exp3 = re.compile(r'buy any ([0-9]+) of ([A-Z,]+) for ([0-9]+)')
    gof_offers = reg_exp1.findall(offer_str)
    mv_offers = reg_exp2.findall(offer_str)
    bundle_offers = reg_exp3.findall(offer_str)

    offers = []
    for offer in mv_offers:
        offers.append({
            'quantity': offer[0],
            'required': offer[1], 
            'offerValue': offer[2]
        })
    
    for offer in bundle_offers:
        print(offer[1])
        offers.append({
            'quantity': offer[0],
            'required': offer[1], 
            'offerValue': offer[2]
        })

    for offer in gof_offers:
        if offer[1] == offer[2]:
            price = str(int(offer[0]) * price_tble[offer[1]])
            offers.append({
                'quantity': str(int(offer[0])+1),
                'required': offer[1],
                'offerValue': price
            })
        else:
            offers.append({
                'quantity': offer[0],
                'required': offer[1],
                'offerValue': offer[2]
            })
    return offers

def getEligibleOffers(offers, basket):
    result = []
    for offer in offers:
        if offer['required'] in basket and int(offer['quantity']) <= basket[offer['required']]:
            if isinstance(offer['offerValue'], str):
                if offer['offerValue'] in basket and basket[offer['offerValue']] > 0:
                    result.append(offer)
            else:
                result.append(offer)
    return result

# Calculate best offer value to apply
def calculate_best_offer(offers, basket):
    offers = getEligibleOffers(offers, basket)
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


