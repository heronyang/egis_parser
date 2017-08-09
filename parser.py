# -*- coding: utf-8 -*-
import urllib, json
import unicodecsv as csv
import os

# http://egis.moea.gov.tw/MoeaEGFxData_WebAPI_Inside/WebAPI/PItemStatistics?&type=PowerItemUse&year=104&month=12&counID=66000&townID=-1&industryClass1=-1&powerType=-1&code=-1
URL_TEMPLATE = "http://egis.moea.gov.tw/MoeaEGFxData_WebAPI_Inside/WebAPI/{0}?&type={1}&year={2}&month={3}&counID={4}&townID={5}&industryClass1={6}&powerType={7}&code={8}"
MONTHS_PER_YEAR = 12

COUN_ID = 66000
TOWN_ID = -1    # list all
CODE = -1

api_types = [("PHighStatistics", "PowerHighUse"),
             ("PItemStatistics", "PowerItemUse")]
industry_classes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "Z"]
industry_names = {
    "A": u"農、林、漁、牧業",
    "B": u"礦業及土石採取業",
    "C": u"製造業",
    "D": u"水電燃氣業",
    "E": u"營造及工程業",
    "F": u"批發、零售及餐飲業",
    "G": u"運輸、倉儲及通信業",
    "H": u"金融、保險及不動產業",
    "I": u"專業、科學及技術服務業",
    "J": u"文化、運動、休閒及其他服務業",
    "Z": u"其他未分類業務"
}

years = [102, 103, 104]

def main():
    run_all()

def run_all():
    run_highstatistics()
    run_itemstatistics()

def run_highstatistics():
    api_type = api_types[0]
    filename = api_type[0] + ".csv"
    power_type = 0

    remove_if_exist(filename)

    is_first_row = True
    for year in years:
        for month in range(1, MONTHS_PER_YEAR + 1):
            for industry_class in industry_classes:
                grab_and_save(api_type, year, month, industry_class,
                              power_type, filename, is_first_row)
                is_first_row = False

def run_itemstatistics():
    api_type = api_types[1]
    filename = api_type[1] + ".csv"
    power_type = -1

    remove_if_exist(filename)

    is_first_row = True
    for year in years:
        for month in range(1, MONTHS_PER_YEAR + 1):
            grab_and_save(api_type, year, month, None, power_type, filename,
                          is_first_row)
            is_first_row = False

def remove_if_exist(filename):
    try:
        os.remove(filename)
    except OSError:
        pass

def save_to_file(items, filename, is_first_row):
    keys = items[0].keys()
    with open(filename, "a") as f:
        dict_writer = csv.DictWriter(f, keys)
        if is_first_row:
            dict_writer.writeheader()
        dict_writer.writerows(items)
        f.close()

def grab_and_save(api_type, year, month, industry_class, power_type, filename,
                 is_first_row):
    print api_type, year, month, industry_class
    url = get_url(api_type, year, month, industry_class, power_type)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    if "INFOS" not in data:
        print "skip"
        return None
    items = data["INFOS"]
    for item in items:
        del item["POLYGONS"]
        item["api_type"] = api_type[0]
        item["year"] = year
        item["month"] = month
        item["industry_class"] = industry_class
        if industry_class is not None:
            item["industry_name"] = industry_names[industry_class]

    save_to_file(items, filename, is_first_row)

def get_url(api_type, year, month, industry_class, power_type):
    if industry_class is None:
        industry_class = -1
    return URL_TEMPLATE.format(api_type[0], api_type[1], year, month,
                               COUN_ID, TOWN_ID, industry_class,
                               power_type, CODE)

if __name__ == "__main__":
    main()
