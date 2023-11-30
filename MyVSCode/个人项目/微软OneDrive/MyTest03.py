import requests

url = "https://graph.microsoft.com/v1.0/me/drive/root:/HuTaoFile/HelloWorld.txt/content"
headers = {
    'Authorization': 'EwBgA8l6BAAUkj1NuJYtTVha+Mogk+HEiPbQo04AAQIp6auDEaRZJcscwl5eTJfWWDaB8U3fsc+wmhqkXKSsIE6CrlpI9MndDAGWZSMcPL1lHE4IQz7qs5dYAnMiJzWIlvhmXV1yu/og7NNIjB4ybh4Lg+0apJMF7/9NRTpR7VZiCgaLflaaOzMLhm+vgw1HpZVUQZvKen1x2fJ144frAJPXiGlTrza8KftJW1Enn+/rhOokRpsgMiyehduq/tfJoM8w8LXmsa638JCtMDTg525CCXX7Ri20CwHhIbPuCgq/JVqpgbmynGIf60wRrVjx5mp5DkUqT/TJviz6idohULCysdAQQbpRFC+tZPu8nve38+NK5Ao4tgU/xR9IGR8DZgAACG++XNNwBC1ZMALo51D24iNdHYyvy93Cg6e15dJzi5bCAHLlnagWnJLPxMm6njEFer6FjgH66FuEbgvVcHsHd680UKT2MQM/gY94MZYHTN4/1Gb0Ese8QQ3raplnC48+grM00urXIcRRevldpIG27SJpkjlKJ8hOEn2LO73+tLa1BipAY3Rxafn5FOKrqVrY0kOm5it/w2MlyGvzR4sqZJRSPCz1qw0ByeaA21IQ2W0MBK5A1JZpaqy0LB403oGWeqhDrXTD07Sffmy0xQjp3Q7BraogqLRs3P3sAnoWprrEo3pjBwufDhhtFxKMR2NdnUO3eIbpk5qZdu57KBC9RaczHsMecd6TM7JUnUtGoaf+F5NEtT6ho1wPJsg3j494pu6OfmAZAL+yFgayrjz7ISwGhL+2OP83G3NTY7iW1dcMF2afxVOFpV16TsRTKEo43tuCJ/T4i3Pn329Jaoy26HA/sQJQ7drvldf72rQl2dxGOc9mAuVLiiHUiLLv0Gp3s0IkwrX20F24ia9PmuTewTtyBvtx314ISPRNRgkF5k0DJzEYYuuN1XmQHqqtNpv0h2SNIRXt58S2oWcVQkGfTZp8RYLUDYgMWCMVOPEDplnWc3e2SvH8ksh6IDXniuE8I6ervpaV/GK7bPQkUrnDIFzpzjbCIEfemKf/Ye0HDwnwYfDqkUbkxd3K2cPo+VPupVzIXt1JAjXRpjioyhWoT0mUZd790ptN3uFiYoRSN4EsGaTOSa6H0gRuamgC'
}

# 根URL：https://graph.microsoft.com/v1.0
# 1.获取当前用户OneDrive：/me/drive
# 2.获取其他用户OneDrive：/users/{idOrUserPrincipalName}/drive
# 3.列出当前用户的驱动器根目录中的子项：/me/drive/root/children
# 4.获取当前用户的driveItem资源：/me/drive/items/{item-id}，item-id 是 driveItem 的 ID

response = requests.get('https://graph.microsoft.com/v1.0/me/drive/root/children', headers=headers).json()

print(response)
# Save the file in the disk 
# with open('./MyFile', 'wb') as file:
#     file.write(response.content)
    

