import random
import constants.quotes as quotes
def generate_quote():
    return random.sample(quotes.UMBASAM_QUOTES, 1)

def generate_cta():
    return random.sample(quotes.UMBASAM_CTA, 1)


def generate_oath(oath):
    if (oath == "meat"):
        return "meatwadcoke says: '{0}'".format(random.sample(quotes.UMBAMEAT_QUOTES, 1)[0])
    elif (oath == "chokyy"):
        return "Chokyy says: '{0}'".format(random.sample(quotes.UMBACHOKYY_QUOTES, 1)[0])
    elif (oath == "ryota"):
        return  "Ryota says: '{0}'".format(random.sample(quotes.UMBARYOTA_QUOTES, 1)[0])
    elif (oath == "tanod" or oath == "morethin"):
        return "MoreThin says: '{0}'".format(random.sample(quotes.UMBATANOD_QUOTES, 1)[0])
    elif (oath == "frost"):
        return "Frost17 says: '{0}'".format(random.sample(quotes.UMBAFROST_QUOTES, 1)[0])
    elif (oath == "web"):
        return "https://deceius.github.io/oathbreakers/"
