from pprint import  pprint

d0 = [{"text":"Playlist"},{"text":"."},{"text":"Jay Chou","artist_id":1000},{"text":"."},{"text":2024}]
d1 = [{"text":"Playlist"},{"text":"."},{"text":"Jay Chou"},{"text":"."},{"text":2024}]
d2 = [{"text":"Playlist"},{"text":"."},{"text":2024}]
d3 = [{"text":"Playlist"},{"text":"."},{"text":"Jay Chou","artist_id":1000}]
d4 = [{"text":"Playlist"},{"text":"."},{"text":"Jay Chou","artist_id":1000},{"text":"."},{"text":2024}]

# playlist_type = "Playlist"
# artist_name


d = dict()
# artist_name
inner_data = d3
count = sum(1 for item in inner_data if isinstance(item, dict) and item.get("text") == ".")
print(count)
if count==1:
    # publish_date
    last_text = None
    for per_inner_data in inner_data:
        if isinstance(per_inner_data, dict) and "text" in per_inner_data:
            last_text = per_inner_data["text"]
            break
    if last_text is not None and last_text.isdigit() and len(last_text) == 4:
        d["publish_date"] = last_text
        d["artist_name"] = None
        d["artist_channel_id"] = None
    else:
        d["publish_date"] = None
        info = list()
        found_first_marker = False
        for per_inner_data in inner_data:
            if isinstance(per_inner_data, dict) and "text" in per_inner_data:
                text = per_inner_data["text"]
                if text == " • ":
                    if found_first_marker:
                        break
                    found_first_marker = True
                elif found_first_marker and text != "&":
                    info.append(per_inner_data)

        if len(info) == 1:
            # artist_name
            d["artist_name"] = info[0]["text"]
            # artist_channel_id
            if info[0].get("artist_id"):
                d["artist_channel_id"] = info[0]["artist_id"]
            else:
                d["artist_channel_id"] = None
        elif len(info) > 1:
            d["artist_name"] = ";".join([k["text"] for k in info])
            artist_channel_id = ";".join(
                [k["artist_id"] for k in info if
                 k.get("artist_id")])
            if artist_channel_id.startswith(";"):
                d["artist_channel_id"] = artist_channel_id[1:]
            if artist_channel_id.endswith(";"):
                d["artist_channel_id"] = artist_channel_id[:-1]

elif count==2:
    info = list()
    found_first_marker = False
    for per_inner_data in inner_data:
        if isinstance(per_inner_data, dict) and "text" in per_inner_data:
            text = per_inner_data["text"]
            if text == ".":
                if found_first_marker:
                    break
                found_first_marker = True
            elif found_first_marker and text != "&":
                info.append(per_inner_data)
    if len(info) == 1:
        # artist_name
        d["artist_name"] = info[0]["text"]
        # artist_channel_id
        if info[0].get("artist_id"):
            d["artist_channel_id"] = info[0]["artist_id"]
        else:
            d["artist_channel_id"] = None
    elif len(info) > 1:
        d["artist_name"] = ";".join([k["text"] for k in info])
        artist_channel_id = ";".join(
            [k["artist_id"] for k in info if
             k.get("artist_id")])
        if artist_channel_id.startswith(";"):
            d["artist_channel_id"] = artist_channel_id[1:]
        if artist_channel_id.endswith(";"):
            d["artist_channel_id"] = artist_channel_id[:-1]

    # publish_date
    last_text = None
    year_texts = list()
    for per_inner_data in inner_data:
        if isinstance(per_inner_data, dict) and "text" in per_inner_data:
            last_text = str(per_inner_data["text"]) if per_inner_data["text"] else None
            print(last_text)
            if isinstance(last_text, str) and last_text.isdigit() and len(last_text) == 4:
                year_texts.append(last_text)
    print("=====>",year_texts)
    if len(year_texts):
        d["publish_date"] = year_texts[0]
    else:
        d["publish_date"] = None

else:
    d["playlist_type"] = None
    d["artist_name"] = None
    d["artist_channel_id"] = None
    d["publish_date"] = None
pprint(d)


s = "2023"
print(s.isdigit())