from google_trans_new import google_translator


def translate_categories(location):
    categories = location["categories"]
    translator = google_translator()
    location["categories"] = [
        {"label": str(translator.translate(category, lang_src='en', lang_tgt='ru')).strip().capitalize(),
         "alias": category}
        for category in categories
    ]
    return location


def translate_tags(location):
    tags = location["tags"]
    translator = google_translator()
    location["tags"] = [
        {"label": str(translator.translate(tag.replace("_", " "), lang_src='en', lang_tgt='ru')).strip().capitalize(),
         "alias": tag} for tag in tags
    ]
    return location
