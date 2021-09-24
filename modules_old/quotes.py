import random
import constants.quotes as quotes
def generate_quote():
    return random.sample(quotes.UMBASAM_QUOTES, 1)

def generate_judwig_quote():
    return random.sample(quotes.ASK_JUDWIG, 1)

def generate_cta():
    return random.sample(quotes.UMBASAM_CTA, 1)


def generate_oath(oath):
    if oath == "killboard":
        return "https://kill-board.com/battles?search=The+Oathbreakers"
    elif oath == "web" or  oath == "deceius":
        return "http://deceius.github.io/oathbreakers"
    
    return random.sample(quotes.OATH_QUOTES[oath], 1)[0]
