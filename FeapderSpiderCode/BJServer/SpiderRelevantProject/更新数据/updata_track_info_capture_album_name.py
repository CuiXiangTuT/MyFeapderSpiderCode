"""
更新数据库中capture_album_name中带有album:字样的数据
"""
"""
SELECT * FROM `boomplay_track_info_batch_data`
WHERE capture_album_name REGEXP '^album:';


UPDATE boomplay_track_info_batch_data
SET capture_album_name=REPLACE(capture_album_name,'album:','')
WHERE capture_album_name REGEXP '^album:';

"""