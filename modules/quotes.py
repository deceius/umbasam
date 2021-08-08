import random
import constants.quotes as quotes
def generate_quote():
    return random.sample(quotes.UMBASAM_QUOTES, 1)

def generate_cta():
    return random.sample(quotes.UMBASAM_CTA, 1)


def generate_oath(oath):
    if (oath == "meat"):
        return random.sample(quotes.UMBAMEAT_QUOTES, 1)
    elif (oath == "chokyy"):
        return random.sample(quotes.UMBACHOKYY_QUOTES, 1)
    elif (oath == "ryota"):
        return random.sample(quotes.UMBARYOTA_QUOTES, 1)
    elif (oath == "tanod" or oath == "morethin"):
        return random.sample(quotes.UMBATANOD_QUOTES, 1)
    elif (oath == "frost"):
        return random.sample(quotes.UMBAFROST_QUOTES, 1)
