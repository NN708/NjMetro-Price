import requests
import urllib
import csv

def encode(text):
    return urllib.parse.quote(text).replace('%', '%25')

# 获取各线站点数据
lines = ['1', '2', '3', '4', '10', 'S1', 'S3', 'S7', 'S8', 'S9']
stations = {}
for line in lines:
    print('获取' + line + '号线站点数据……')
    url = 'http://www.njmetro.com.cn/njdtweb/portal/get-stationList.do?reLineId=L' + line
    r = requests.get(url)
    if r.status_code != 200:
        print('连接失败')
        exit()
    stationList = r.json()['stationList']

    stationsOfLine = []
    for station in stationList:
        stationsOfLine.append(station['stationName'])
    stations[line] = stationsOfLine

stationsFlat = []
for line in stations:
    stationsFlat += stations[line]
# 去重
stationsFlatDuplicate = stationsFlat
stationsFlat = []
for station in stationsFlatDuplicate:
    if not station in stationsFlat:
        stationsFlat.append(station)

# 获取各站之间价格
with open('njmetro_price.csv', 'w', newline='') as csvfile:
    header = ['departure'] + stationsFlat
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    for departure in stationsFlat:
        print('获取从' + departure + '出发的价格……')
        row = {}
        row['departure'] = departure
        for destination in stationsFlat:
            url = 'http://www.njmetro.com.cn/njdtweb/mobileTicketAction/getPrice.do?starts=' + encode(departure) + '&ends=' + encode(destination)
            r = requests.get(url)
            if r.status_code != 200:
                print('连接失败')
                exit()
            row[destination] = r.json()['price']
        writer.writerow(row)