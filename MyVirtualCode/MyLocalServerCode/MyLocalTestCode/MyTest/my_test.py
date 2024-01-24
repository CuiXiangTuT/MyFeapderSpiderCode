def get_text_between_dots(data):
    texts = []
    dot_count = 0

    for item in data:
        if isinstance(item, dict) and "text" in item:
            text = item["text"]
            if text == ".":
                dot_count += 1
            elif dot_count == 1:
                texts.append(text)

    return texts

d = [
    {"text": "Playlist"},
    {"text": "."},
    {"text": "Jay Chou", "artist_id": 1000},
    {"text": "."},
    {"text": "2024"}
]

result = get_text_between_dots(d)
print(result)