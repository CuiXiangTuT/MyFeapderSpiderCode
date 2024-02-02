import re


html = """
try {
                const initialData = [];
                initialData.push({
                    path: '\/guide',
                    params: JSON.parse('\x7b\x7d'),
                    data: '1-\x7b\x22responseContext\x22:\x7b\x22\x22\x3d\x22\x7d\x7d\x5d\x7d\x7d\x7d\x7d\x5d,\x22trackingParams\x22:\x22CAAQumkiEwij3cStoYmDAxU_BwYAHRXvClA\x3d\x22\x7d'
                });
                initialData.push({
                    path: '\/browse',
                    params: JSON.parse('\x7b\x22browseId\x22:\x22UCPC0L1d253x-KuMNwa05TpA\x22,\x22browseEndpointContextSupportedConfigs\x22:\x22\x7b\\\x22browseEndpointContextMusicConfig\\\x22:\x7b\\\x22pageType\\\x22:\\\x22MUSIC_PAGE_TYPE_ARTIST\\\x22\x7d\x7d\x22\x7d'),
                    data: '2-\x7b\\x5b\x7b\x22url\x22:\x22https:\/\/lh3.w1401-h583-p-l90-rCAAQhGciEwjD4MStoYmDAxWZFgYAHWonDdc\x3d\x22\x7d'
                });
                ytcfg.set({
                    'YTMUSIC_INITIAL_DATA': initialData
                });
"""

# 使用正则表达式提取 data 值
pattern = r"initialData\.push\({([\s\S]*?)}\);"
matches = re.findall(pattern, html)
if len(matches) >= 2:
    second_data = matches[1]
    match = re.search(r"data: '(.*)'", second_data)
    print(match)
    if match:
        data_value = match.group(1)
        print(data_value)
else:
    print("无法找到第二个initialData.push的值")
