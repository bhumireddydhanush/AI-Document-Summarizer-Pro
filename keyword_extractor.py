import yake

def extract_keywords(text, num_keywords=5):
    kw_extractor = yake.KeywordExtractor(
        lan="en",
        n=1,
        top=num_keywords
    )

    keywords = kw_extractor.extract_keywords(text)

    return [keyword for keyword, score in keywords]