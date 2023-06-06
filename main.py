import requests
import time

source_url = "https://SOURCE_CANVAS_URL/api/v1/"
dest_url = "https://DESTINATION_CANVAS_URL/api/v1/"

source_course_list = source_url + "accounts/:account_id/courses"
source_export_content = source_url + "courses/:course_id/content_exports"
source_show_content = source_url + "courses/:course_id/content_exports/:id"
sourse_access_token = "ACCESS_TOKEN_FRO_SOURCE_CANVAS"

dest_list_active_course = dest_url + "accounts/:account_id/courses"
dest_create_content_migration = dest_url + "courses/:course_id/content_migrations"  # sis_course_id
dest_access_token = "ACCESS_TOKEN_FRO_DESTINATION_CANVAS"


def get_sources_active_courses():
    # print("get course list")
    # url = source_course_list.replace(":account_id", "4")
    # print(url)
    # headers = {
    #     'Authorization': 'Bearer ' + sourse_access_token,
    # }
    # response = requests.request("GET", url, headers=headers)
    # resp_json = response.json()
    # # print(resp_json)
    # return resp_json
    source_courses = []
    source_courses_file = 'source_ids.txt'
    with open(source_courses_file) as f:
        lines = f.readlines()
        # Her satırı döngüyle okuyun ve ekrana yazdırın
        for row in lines:
            print(row.replace('\n', ''))
            row = row.replace('\n', '')
            row = row.split(";")
            dictionary = {'id': row[1], 'sis_course_id': row[0]}
            source_courses.append(dictionary)
            # source_courses.append(row)

    return source_courses


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


def get_dest_active_courses():
    # print("get dest active courses")
    url = dest_list_active_course.replace(":account_id", "1")

    headers = {
        'Authorization': 'Bearer ' + dest_access_token,
    }

    response = requests.request("GET", url, headers=headers)
    resp_json = response.json()
    return resp_json


def dest_create_content(course_id, file_url):
    # print("create content", course_id, file_url)
    # dest_create_content_migration = dest_url + "courses/:course_id/content_migrations"  # sis_course_id
    url = dest_create_content_migration.replace(":course_id", course_id)
    # print(url)
    headers = {
        'Authorization': 'Bearer ' + dest_access_token,
    }
    payload = {
        "migration_type": "canvas_cartridge_importer",
        "settings[file_url]": file_url
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    resp_json = response.json()
    # print(resp_json)
    # return resp_json


source_courses = get_sources_active_courses()
# dest_course_list = get_dest_active_courses()

# with open(filename, 'r', encoding=encoding) as file:
#     reader = csv.DictReader(file, delimiter=',',)
destination_courses_ids = {}
filename = 'data.txt'

with open(filename) as f:
    lines = f.readlines()
    # Her satırı döngüyle okuyun ve ekrana yazdırın
    for row in lines:
        row = row.replace("\n", "")
        kv = row.split(";")
        destination_courses_ids[kv[0]] = kv[1]

for course in source_courses:
    if course['sis_course_id'] in destination_courses_ids.keys():
        print("sis course bulundu")
        print("*" * 20, course)
        # print(course["id"])
        post_content = post_export_content(course['id'])
        # print("post content id :", post_content['id'])
        # print("course id :", course['id'])
        # time.sleep(3)
        wait_process = True
        show_content = {}
        while wait_process:
            time.sleep(1)
            print(course['id'])
            show_content = get_show_content(course['id'], post_content['id'])
            if 'attachment' in show_content.keys():
                wait_process = False

        attachment = show_content['attachment']

        dest_create_content(destination_courses_ids[course['sis_course_id']], attachment['url'])
        print("--------------" * 20)
