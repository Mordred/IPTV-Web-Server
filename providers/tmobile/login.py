#-*-coding:utf8;-*-


# přihlašovací údaje
user = ""
password = ""


import requests, os, json, uuid, sys


UA = "okhttp/3.12.12"
dev_name = "ANDROID-PHONE"
dev_id = str(uuid.uuid4())


def set_data(data):
    json_object = json.dumps(data, indent=4)
    with open("tmobile_token.json", "w") as outfile:
        outfile.write(json_object)


def login(dev_type):
    params={"dsid": dev_id, "deviceName": dev_name, "deviceType": dev_type, "osVersion": "0.0.0", "appVersion": "0.0.0", "language": "CZ"}
    headers={'Origin': 'https://www.magiogo.cz', 'Pragma': 'no-cache', 'Referer': 'https://www.magiogo.cz/', 'User-Agent': UA, 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site'}
    req = requests.post("https://czgo.magio.tv/v2/auth/init", params=params, headers=headers).json()
    accessToken = req["token"]["accessToken"]
    params = {"loginOrNickname": user, "password": password}
    headers = {"authorization": "Bearer " + accessToken, 'Origin': 'https://www.magiogo.cz', 'Pragma': 'no-cache', 'Referer': 'https://www.magiogo.cz/', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site', 'User-Agent': UA}
    req = requests.post("https://czgo.magio.tv/v2/auth/login", json = params, headers = headers).json()
    if req["success"] == True:
        return req["token"]["accessToken"], req["token"]["refreshToken"]
    else:
        print(req["errorMessage"])
        return "", ""


def reg_device():
    accesstoken, refreshtoken = login("OTT_ANDROID")
    if accesstoken == "":
        input("\nPro ukončení stiskněte klávesu Enter")
        sys.exit(0)
    params={"list": "LIVE", "queryScope": "LIVE"}
    headers = {"authorization": "Bearer " + accesstoken, 'Origin': 'https://www.magiogo.cz', 'Pragma': 'no-cache', 'Referer': 'https://www.magiogo.cz/', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site', 'User-Agent': UA}
    id = requests.get("https://czgo.magio.tv/v2/television/channels", params = params, headers = headers).json()["items"][0]["channel"]["channelId"]
    params={"service": "LIVE", "name": dev_name, "devtype": "OTT_ANDROID", "id": id, "prof": "p5", "ecid": "", "drm": "verimatrix"}
    headers = {"authorization": "Bearer " + accesstoken, 'Origin': 'https://www.magiogo.cz', 'Pragma': 'no-cache', 'Referer': 'https://www.magiogo.cz/', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site', 'User-Agent': UA}
    req = requests.get("https://czgo.magio.tv/v2/television/stream-url", params = params, headers = headers).json()
    if req["success"] == True:
        accesstoken, refreshtoken = login("OTT_LINUX_4302")
        set_data({"accesstoken": accesstoken, "refreshtoken": refreshtoken})
        print("Přihlášení úspěšné")
    else:
        print(req["errorMessage"].replace("exceeded-max-device-count", "Překročen maximální počet zařízení"))
    input("\nPro ukončení stiskněte klávesu Enter")
    sys.exit(0)


if __name__ == "__main__":
    reg_device()