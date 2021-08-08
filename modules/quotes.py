import random
import constants.quotes as quotes
def generate_quote():
    return random.sample(quotes.UMBASAM_QUOTES, 1)
