import re

s = """aaaaaaaaaaaaaaaaaaaa
 "continuationCommand": {
                                                                                                                "token": "4qmFsgJmEhhVQzhDVTVuVmhDUUlkQUdyRkZwNGxvT1EaSjhnWXlHakN5QVMwS0JRb0RDSW9MR2lRMk5XWmlOVFk0WlMwd01EQXdMVEl6TmpndFlXVmpPUzB3T0RsbE1EZ3lZamt5WTJNJTNE",
                                                                                                                "request": "CONTINUATION_REQUEST_TYPE_BROWSE"
                                                                                                            }   
                                                                                                                                                                                                                "continuationCommand": {
                                                                                                        "token": "4qmFsgJmEhhVQzhDVTVuVmhDUUlkQUdyRkZwNGxvT1EaSjhnWXlHakN5QVMwS0JRb0RDSW9MR2lRMk5XWmlOVFk1TUMwd01EQXdMVEl6TmpndFlXVmpPUzB3T0RsbE1EZ3lZamt5WTJNJTNE",
                                                                                                        "request": "CONTINUATION_REQUEST_TYPE_BROWSE"
                                                                                                    }}
"""

# 使用正则表达式匹配第一个token内容
pattern = r'"token": "(.*?)",\s+"request": "CONTINUATION_REQUEST_TYPE_BROWSE"'
match = re.search(pattern, s)

if match:
    token = match.group(1)
    print("第一个匹配到的token内容:", token)
else:
    print("未找到匹配的token内容")