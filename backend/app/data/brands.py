# ============================================================
# Known brands and their legitimate domains
# ============================================================

KNOWN_BRANDS: dict[str, list[str]] = {
    "amazon": [
        "amazon.com",
        "amazon.in",
    ],
    "google": [
        "google.com",
        "google.co.in",
    ],
    "microsoft": [
        "microsoft.com",
    ],
    "apple": [
        "apple.com",
    ],
    "paypal": [
        "paypal.com",
    ],
    "instagram": [
        "instagram.com",
    ],
    "facebook": [
        "facebook.com",
        "fb.com",
    ],
    "flipkart": [
        "flipkart.com",
    ],
    "youtube": [
        "youtube.com",
        "youtu.be",
    ],
    "whatsapp": [
        "whatsapp.com",
    ],
    "meta": [
        "meta.com",
    ],
    "linkedin": [
        "linkedin.com",
    ],
    "x": [
        "x.com",
        "twitter.com",
    ],
    "snapchat": [
        "snapchat.com",
    ],
    "tiktok": [
        "tiktok.com",
    ],
    "reddit": [
        "reddit.com",
    ],
    "pinterest": [
        "pinterest.com",
    ],
    "telegram": [
        "telegram.org",
    ],
    "discord": [
        "discord.com",
    ],
    "twitch": [
        "twitch.tv",
    ],
    "spotify": [
        "spotify.com",
    ],
    "netflix": [
        "netflix.com",
    ],
    "prime video": [
        "primevideo.com",
    ],
    "disney+": [
        "disneyplus.com",
    ],
    "hotstar": [
        "hotstar.com",
    ],
    "jiohotstar": [
        "jiohotstar.com",
    ],
    "hulu": [
        "hulu.com",
    ],
    "hbo max": [
        "max.com",
    ],
    "peacock": [
        "peacocktv.com",
    ],
    "paramount+": [
        "paramountplus.com",
    ],
    "soundcloud": [
        "soundcloud.com",
    ],
    "apple music": [
        "music.apple.com",
    ],
    "youtube music": [
        "music.youtube.com",
    ],
    "adobe": [
        "adobe.com",
    ],
    "canva": [
        "canva.com",
    ],
    "figma": [
        "figma.com",
    ],
    "notion": [
        "notion.so",
    ],
    "slack": [
        "slack.com",
    ],
    "zoom": [
        "zoom.us",
    ],
    "dropbox": [
        "dropbox.com",
    ],
    "box": [
        "box.com",
    ],
    "salesforce": [
        "salesforce.com",
    ],
    "oracle": [
        "oracle.com",
    ],
    "ibm": [
        "ibm.com",
    ],
    "intel": [
        "intel.com",
    ],
    "amd": [
        "amd.com",
    ],
    "nvidia": [
        "nvidia.com",
    ],
    "dell": [
        "dell.com",
    ],
    "hp": [
        "hp.com",
    ],
    "lenovo": [
        "lenovo.com",
    ],
    "asus": [
        "asus.com",
    ],
    "acer": [
        "acer.com",
    ],
    "samsung": [
        "samsung.com",
    ],
    "sony": [
        "sony.com",
    ],
    "lg": [
        "lg.com",
    ],
    "xiaomi": [
        "mi.com",
        "xiaomi.com",
    ],
    "oneplus": [
        "oneplus.com",
    ],
    "oppo": [
        "oppo.com",
    ],
    "vivo": [
        "vivo.com",
    ],
    "realme": [
        "realme.com",
    ],
    "motorola": [
        "motorola.com",
    ],
    "nothing": [
        "nothing.tech",
    ],
    "huawei": [
        "huawei.com",
    ],
    "honor": [
        "honor.com",
    ],
    "dji": [
        "dji.com",
    ],
    "boat": [
        "boat-lifestyle.com",
    ],
    "noise": [
        "gonoise.com",
    ],
    "jbl": [
        "jbl.com",
    ],
    "bose": [
        "bose.com",
    ],
    "beats": [
        "beatsbydre.com",
    ],
    "nike": [
        "nike.com",
    ],
    "adidas": [
        "adidas.com",
    ],
    "puma": [
        "puma.com",
    ],
    "reebok": [
        "reebok.com",
    ],
    "under armour": [
        "underarmour.com",
    ],
    "new balance": [
        "newbalance.com",
    ],
    "skechers": [
        "skechers.com",
    ],
    "asics": [
        "asics.com",
    ],
    "converse": [
        "converse.com",
    ],
    "vans": [
        "vans.com",
    ],
    "zara": [
        "zara.com",
    ],
    "h&m": [
        "hm.com",
    ],
    "uniqlo": [
        "uniqlo.com",
    ],
    "levis": [
        "levi.com",
    ],
    "gucci": [
        "gucci.com",
    ],
    "prada": [
        "prada.com",
    ],
    "louis vuitton": [
        "louisvuitton.com",
    ],
    "chanel": [
        "chanel.com",
    ],
    "dior": [
        "dior.com",
    ],
    "hermes": [
        "hermes.com",
    ],
    "burberry": [
        "burberry.com",
    ],
    "versace": [
        "versace.com",
    ],
    "armani": [
        "armani.com",
    ],
    "calvin klein": [
        "calvinklein.com",
    ],
    "tommy hilfiger": [
        "tommy.com",
    ],
    "myntra": [
        "myntra.com",
    ],
    "meesho": [
        "meesho.com",
    ],
    "ajio": [
        "ajio.com",
    ],
    "nykaa": [
        "nykaa.com",
    ],
    "tata cliq": [
        "tatacliq.com",
    ],
    "reliance digital": [
        "reliancedigital.in",
    ],
    "croma": [
        "croma.com",
    ],
    "jiomart": [
        "jiomart.com",
    ],
    "bigbasket": [
        "bigbasket.com",
    ],
    "blinkit": [
        "blinkit.com",
    ],
    "zepto": [
        "zepto.com",
    ],
    "swiggy": [
        "swiggy.com",
    ],
    "zomato": [
        "zomato.com",
    ],
    "ubereats": [
        "ubereats.com",
    ],
    "doordash": [
        "doordash.com",
    ],
    "ubereats india": [
        "ubereats.com",
    ],
    "uber": [
        "uber.com",
    ],
    "ola": [
        "olacabs.com",
    ],
    "rapido": [
        "rapido.bike",
    ],
    "lyft": [
        "lyft.com",
    ],
    "airbnb": [
        "airbnb.com",
    ],
    "booking.com": [
        "booking.com",
    ],
    "expedia": [
        "expedia.com",
    ],
    "makemytrip": [
        "makemytrip.com",
    ],
    "goibibo": [
        "goibibo.com",
    ],
    "cleartrip": [
        "cleartrip.com",
    ],
    "irctc": [
        "irctc.co.in",
    ],
    "indigo": [
        "goindigo.in",
    ],
    "air india": [
        "airindia.com",
    ],
    "emirates": [
        "emirates.com",
    ],
    "qatar airways": [
        "qatarairways.com",
    ],
    "singapore airlines": [
        "singaporeair.com",
    ],
    "united airlines": [
        "united.com",
    ],
    "delta air lines": [
        "delta.com",
    ],
    "american airlines": [
        "aa.com",
    ],
    "visa": [
        "visa.com",
    ],
    "mastercard": [
        "mastercard.com",
    ],
    "american express": [
        "americanexpress.com",
    ],
    "stripe": [
        "stripe.com",
    ],
    "wise": [
        "wise.com",
    ],
    "revolut": [
        "revolut.com",
    ],
    "phonepe": [
        "phonepe.com",
    ],
    "google pay": [
        "pay.google.com",
    ],
    "paytm": [
        "paytm.com",
    ],
    "bharatpe": [
        "bharatpe.com",
    ],
    "razorpay": [
        "razorpay.com",
    ],
    "cash app": [
        "cash.app",
    ],
    "venmo": [
        "venmo.com",
    ],
    "square": [
        "squareup.com",
    ],
    "hdfc bank": [
        "hdfcbank.com",
    ],
    "icici bank": [
        "icicibank.com",
    ],
    "state bank of india": [
        "sbi.co.in",
    ],
    "axis bank": [
        "axisbank.com",
    ],
    "kotak mahindra bank": [
        "kotak.com",
    ],
    "yes bank": [
        "yesbank.in",
    ],
    "indusind bank": [
        "indusind.com",
    ],
    "bank of baroda": [
        "bankofbaroda.in",
    ],
    "punjab national bank": [
        "pnbindia.in",
    ],
    "canara bank": [
        "canarabank.com",
    ],
    "union bank of india": [
        "unionbankofindia.co.in",
    ],
    "federal bank": [
        "federalbank.co.in",
    ],
    "idfc first bank": [
        "idfcfirstbank.com",
    ],
    "standard chartered": [
        "sc.com",
    ],
    "hsbc": [
        "hsbc.com",
    ],
    "barclays": [
        "barclays.com",
    ],
    "chase": [
        "chase.com",
    ],
    "bank of america": [
        "bankofamerica.com",
    ],
    "wells fargo": [
        "wellsfargo.com",
    ],
    "citibank": [
        "citi.com",
    ],
    "tesla": [
        "tesla.com",
    ],
    "toyota": [
        "toyota.com",
    ],
    "honda": [
        "honda.com",
    ],
    "hyundai": [
        "hyundai.com",
    ],
    "kia": [
        "kia.com",
    ],
    "maruti suzuki": [
        "marutisuzuki.com",
    ],
    "tata motors": [
        "tatamotors.com",
    ],
    "mahindra": [
        "mahindra.com",
    ],
    "bmw": [
        "bmw.com",
    ],
    "mercedes-benz": [
        "mercedes-benz.com",
    ],
    "audi": [
        "audi.com",
    ],
    "volkswagen": [
        "volkswagen.com",
    ],
    "ford": [
        "ford.com",
    ],
    "chevrolet": [
        "chevrolet.com",
    ],
    "volvo": [
        "volvocars.com",
    ],
    "nissan": [
        "nissan-global.com",
    ],
    "renault": [
        "renault.com",
    ],
    "skoda": [
        "skoda-auto.com",
    ],
    "jeep": [
        "jeep.com",
    ],
    "porsche": [
        "porsche.com",
    ],
    "ferrari": [
        "ferrari.com",
    ],
    "lamborghini": [
        "lamborghini.com",
    ],
    "land rover": [
        "landrover.com",
    ],
    "jaguar": [
        "jaguar.com",
    ],
    "royal enfield": [
        "royalenfield.com",
    ],
    "bajaj": [
        "bajajauto.com",
    ],
    "tvs": [
        "tvsmotor.com",
    ],
    "hero motocorp": [
        "heromotocorp.com",
    ],
    "ather energy": [
        "atherenergy.com",
    ],
    "ola electric": [
        "olaelectric.com",
    ],
    "ducati": [
        "ducati.com",
    ],
    "ktm": [
        "ktm.com",
    ],
    "foodpanda": [
        "foodpanda.com",
    ],
    "mcdonalds": [
        "mcdonalds.com",
    ],
    "burger king": [
        "bk.com",
    ],
    "kfc": [
        "kfc.com",
    ],
    "pizza hut": [
        "pizzahut.com",
    ],
    "dominos": [
        "dominos.com",
    ],
    "subway": [
        "subway.com",
    ],
    "starbucks": [
        "starbucks.com",
    ],
    "dunkin": [
        "dunkindonuts.com",
    ],
    "taco bell": [
        "tacobell.com",
    ],
    "wendys": [
        "wendys.com",
    ],
    "chipotle": [
        "chipotle.com",
    ],
    "coca-cola": [
        "coca-cola.com",
    ],
    "pepsi": [
        "pepsi.com",
    ],
    "red bull": [
        "redbull.com",
    ],
    "monster energy": [
        "monsterenergy.com",
    ],
    "nestle": [
        "nestle.com",
    ],
    "britannia": [
        "britannia.co.in",
    ],
    "amul": [
        "amul.com",
    ],
    "mother dairy": [
        "motherdairy.com",
    ],
    "parle": [
        "parleproducts.com",
    ],
    "cadbury": [
        "cadbury.co.uk",
    ],
    "oreo": [
        "oreo.com",
    ],
    "lays": [
        "lays.com",
    ],
    "doritos": [
        "doritos.com",
    ],
    "patanjali": [
        "patanjaliayurved.net",
    ],
    "hindustan unilever": [
        "hul.co.in",
    ],
    "unilever": [
        "unilever.com",
    ],
    "procter & gamble": [
        "pg.com",
    ],
    "colgate": [
        "colgate.com",
    ],
    "dove": [
        "dove.com",
    ],
    "nivea": [
        "nivea.com",
    ],
    "loreal": [
        "loreal.com",
    ],
    "maybelline": [
        "maybelline.com",
    ],
    "lakme": [
        "lakmeindia.com",
    ],
    "mamaearth": [
        "mamaearth.in",
    ],
    "minimalist": [
        "beminimalist.co",
    ],
    "the ordinary": [
        "theordinary.com",
    ],
    "cerave": [
        "cerave.com",
    ],
    "cetaphil": [
        "cetaphil.com",
    ],
    "dettol": [
        "dettol.com",
    ],
    "lifebuoy": [
        "lifebuoy.com",
    ],
    "tide": [
        "tide.com",
    ],
    "surf excel": [
        "surfexcel.in",
    ],
    "vim": [
        "vim.com",
    ],
    "ikea": [
        "ikea.com",
    ],
    "home depot": [
        "homedepot.com",
    ],
    "lowes": [
        "lowes.com",
    ],
    "walmart": [
        "walmart.com",
    ],
    "target": [
        "target.com",
    ],
    "costco": [
        "costco.com",
    ],
    "ebay": [
        "ebay.com",
    ],
    "etsy": [
        "etsy.com",
    ],
    "aliexpress": [
        "aliexpress.com",
    ],
    "alibaba": [
        "alibaba.com",
    ],
    "temu": [
        "temu.com",
    ],
    "shein": [
        "shein.com",
    ],
    "shopee": [
        "shopee.com",
    ],
    "rakuten": [
        "rakuten.com",
    ],
    "mercari": [
        "mercari.com",
    ],
    "coursera": [
        "coursera.org",
    ],
    "udemy": [
        "udemy.com",
    ],
    "edx": [
        "edx.org",
    ],
    "khan academy": [
        "khanacademy.org",
    ],
    "duolingo": [
        "duolingo.com",
    ],
    "byju's": [
        "byjus.com",
    ],
    "unacademy": [
        "unacademy.com",
    ],
    "physics wallah": [
        "pw.live",
    ],
    "simplilearn": [
        "simplilearn.com",
    ],
    "wikipedia": [
        "wikipedia.org",
    ],
    "quora": [
        "quora.com",
    ],
    "medium": [
        "medium.com",
    ],
    "wordpress": [
        "wordpress.com",
    ],
    "wix": [
        "wix.com",
    ],
    "squarespace": [
        "squarespace.com",
    ],
    "shopify": [
        "shopify.com",
    ],
    "github": [
        "github.com",
    ],
    "gitlab": [
        "gitlab.com",
    ],
    "bitbucket": [
        "bitbucket.org",
    ],
    "stackoverflow": [
        "stackoverflow.com",
    ],
    "openai": [
        "openai.com",
    ],
    "anthropic": [
        "anthropic.com",
    ],
    "hugging face": [
        "huggingface.co",
    ],
    "perplexity": [
        "perplexity.ai",
    ],
    "deepseek": [
        "deepseek.com",
    ],
    "cloudflare": [
        "cloudflare.com",
    ],
    "aws": [
        "aws.amazon.com",
    ],
    "azure": [
        "azure.microsoft.com",
    ],
    "google cloud": [
        "cloud.google.com",
    ],
    "digitalocean": [
        "digitalocean.com",
    ],
    "vercel": [
        "vercel.com",
    ],
    "netlify": [
        "netlify.com",
    ]
}