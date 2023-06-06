import requests
import time
import csv

source_url = "https://SOURCE_CANVAS_URL/api/v1/"
dest_url = "https://DESTINATION_CANVAS_URL/api/v1/"

source_course_list = source_url + "accounts/:account_id/courses"
source_export_content = source_url + "courses/:course_id/content_exports"
source_show_content = source_url + "courses/:course_id/content_exports/:id"
sourse_access_token = "ACCESS_TOKEN_FRO_SOURCE_CANVAS"

dest_list_active_course = dest_url + "accounts/:account_id/courses"
dest_create_content_migration = dest_url + "courses/:course_id/content_migrations"  # sis_course_id
dest_access_token = "ACCESS_TOKEN_FRO_DESTINATION_CANVAS"

filename = 'akedema_id.csv'
encoding = 'utf-8'


def get_course_ids():
    course_ids = {}
    with open(filename, 'r', encoding=encoding) as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            print(row)
            course_ids[row['source']] = row['destination']
    print("----------------------    ders id'leri okuntu")

    return course_ids


def post_export_content(course_id):
    print("export content")
    url = source_export_content.replace(":course_id", course_id)
    headers = {
        'Authorization': 'Bearer ' + sourse_access_token,
    }
    payload = {
        "export_type": "common_cartridge",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    resp_json = response.json()
    # print(resp_json)
    return resp_json


def get_show_content(course_id, content_id):
    # source_show_content = source_url + "courses/:course_id/content_exports/:id"
    url = source_show_content.replace(":course_id", course_id).replace(":id", str(content_id))
    # print(url)
    # print("")
    headers = {
        'Authorization': 'Bearer ' + sourse_access_token,
    }
    response = requests.request("Get", url, headers=headers, )
    resp_json = response.json()
    return resp_json


def dest_create_content(course_id, file_url):
    url = dest_create_content_migration.replace(":course_id", course_id)
    headers = {
        'Authorization': 'Bearer ' + dest_access_token,
    }
    payload = {
        "migration_type": "canvas_cartridge_importer",
        "settings[file_url]": file_url
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        print("ders içerikleri ", course_id, " id'li derse kopyalandı")
    else:
        print("hata --- ", course_id, " id'li derse kopyalanmadı")


course_ids = get_course_ids()

for source in course_ids.keys():
    print("*" * 20, source)
    # print(course["id"])
    post_content = post_export_content(source)
    wait_process = True
    show_content = {}
    while wait_process:
        time.sleep(1)
        print(source, " id'li dersin içeriklerinin oluşturulması bekleniyor...")
        show_content = get_show_content(source, post_content['id'])
        if 'attachment' in show_content.keys():
            wait_process = False

    attachment = show_content['attachment']

    dest_create_content(course_ids[source], attachment['url'])
    print("--------------" * 20)
