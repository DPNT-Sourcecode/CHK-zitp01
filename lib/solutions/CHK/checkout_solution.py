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
    reg_exp3 = re.compile(r'buy\s+any\s+(\d+)\s+of\s+\(([^)]+)\)\s+for\s+(\d+)')
    #reg_exp3 = re.compile(r'buy any ([0-9]+) of (\([A-Z]+(?:,[A-Z]+\)) for ([0-9]+)')
    gof_offers = reg_exp1.findall(offer_str)
    mv_offers = reg_exp2.findall(offer_str)
    bundle_offers = reg_exp3.findall(offer_str)

    offers = []
    for offer in mv_offers:
        offers.append({
            'quantity': int(offer[0]),
            'required': [offer[1]], 
            'offerValue': int(offer[2])
        })

    for offer in gof_offers:
        if offer[1] == offer[2]:
            offers.append({
                'quantity': int(offer[0])+1,
                'required': [offer[1]],
                'offerValue': int(offer[0]) * price_tble[offer[1]]
            })
        else:
            offers.append({
                'quantity': int(offer[0]),
                'required': [offer[1]],
                'offerValue': offer[2]
            })

    for offer in bundle_offers:
        offers.append({
            'quantity': int(offer[0]),
            'required': sorted(offer[1].split(","), key = lambda x: price_tble[x], reverse=True),
            'offerValue': int(offer[2])
        })

    return offers

def getEligibleOffers(offers, basket):
    result = []
    for offer in offers:
        # Check if required products exist in basket
        requiredProductsExist = False
        requiredProductsCount = 0
        for product in offer['required']:
            if product in basket:
                requiredProductsExist = True
                requiredProductsCount += basket[product]

        if requiredProductsExist and offer['quantity'] <= requiredProductsCount:
            if isinstance(offer['offerValue'], str):
                # Check free product exists
                if offer['offerValue'] in basket and basket[offer['offerValue']] > 0:
                    result.append(offer)
            else:
                result.append(offer)
    return result

# Calculate best offer value to apply
def calculate_best_offer(offers, basket):
    offers = getEligibleOffers(offers, basket)
    print(offers)
    best_offer = None
    max_offer_value = 0
    for offer in offers:
        # GOF Offer
        if isinstance(offer['offerValue'], str):
            offer_value = price_tble[offer['offerValue']]
        # Multi-value Offer
        elif len(offer['required']) == 1:
            offer_value = (offer['quantity'] * price_tble[offer['required'][0]]) - offer['offerValue']
        # Group offer
        else:
            productsRequired = []
            offer_value = 0
            nCount = 0
            # Calculate the max value combination of products for offer
            for product in offer['required']:
                n = 0
                while nCount < offer['quantity'] and n < basket[product]:
                    offer_value += price_tble[product]
                    productsRequired.append(product)
                    nCount += 1
                    n += 1
                
            offer_value -= offer['offerValue']
            print(productsRequired, "\n")

        # Get max offer value
        if offer_value > max_offer_value:
            max_offer_value = offer_value
            best_offer = {
                'quantity': offer['quantity'],
                'required': productsRequired,
                'offerValue': offer['offerValue']
            }

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
        # GOF Offer
        if isinstance(best_offer['offerValue'], str):
            product = best_offer['required'][0]
            total += best_offer['quantity'] * price_tble[product]
            
            # Remove items from basket
            basket[product] -= best_offer['quantity']
            basket[best_offer['offerValue']] -= 1

            if basket[product] == 0:
                del basket[product]

            if basket[best_offer['offerValue']] == 0:
                del basket[best_offer['offerValue']]
        
        else:
            total += best_offer['offerValue']
            # Multi-value Offer
            if len(best_offer['required']) == 1:
                product = best_offer['required'][0]
                basket[product] -= best_offer['quantity']

                # Remove from basket
                if basket[product] == 0:
                    del basket[product]

            # Group Offer
            else:
                for product in best_offer['required']:
                    basket[product] -= 1

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
    if (not isinstance(skus, str) or not skus.isalpha()) and len(skus) > 0:
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





