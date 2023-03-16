import time

from config import last_timestamp, accounts_list
from dataclasses import dataclass
import requests
import sqlite3


@dataclass
class Media:
    id: str
    url: str
    is_video: bool
    caption: str
    product_type: str


def insert_in_db(conn, d: Media):

    global inserted_in_db

    try:
        conn.execute(f"INSERT INTO data (id, url, comment,is_video, is_uploaded, product_type) VALUES ('{d.id}','{d.url}','{d.caption}',{d.is_video}, {False} , '{d.product_type}')")
        conn.commit()
        inserted_in_db += 1
    except:
        try:

            conn.execute(
                f"INSERT INTO data (id, url, comment,is_video, is_uploaded,product_type) VALUES ('{d.id}','{d.url}','{''}',{d.is_video}, {False},'{d.product_type}' )")
            conn.commit()
            inserted_in_db += 1
        except Exception as e:
            print(d)
            print(e)


    # conn.execute("create table data (id varchar(255) , url varchar(255), comment varchar(255), is_video bool, is_uploaded bool,  primary key(id))");

# take browser insta request headers and put in here
headers = {}
if __name__ == '__main__':

    media_list = []
    counter = 0
    inserted_in_db = 0
    conn = sqlite3.connect('content.db')
    for account in accounts_list:
        time.sleep(2)
        header= {}

        BASEURL = f'https://www.instagram.com/{account}/?__a=1&__d=dis'
        try:
            response = requests.get(BASEURL, headers=header).json()
            print('fetched data for ', account)
            if 'edge_felix_video_timeline' in response["graphql"]["user"]:
                for content in response["graphql"]["user"]['edge_felix_video_timeline']['edges']:
                    if 'edge_sidecar_to_children' in content['node']:
                        for nested_content in  content['node']['edge_sidecar_to_children']['edges']:
                            if content['node']['taken_at_timestamp']>= last_timestamp:
                                url = nested_content['node']['video_url'] if nested_content['node']['is_video'] else nested_content['node']['display_url']
                                if nested_content['node']['is_video']:
                                    if ('video_duration' in nested_content['node'] and  nested_content['node']['video_duration']<3.00) or ('video_duration' in nested_content['node'] and  nested_content['node']['video_duration']>900.00):
                                        continue

                                product_type = nested_content['node']['product_type'] if 'product_type' in nested_content['node'] else None
                                try:
                                    caption =  str(nested_content['node']['edge_media_to_caption']["edges"][0]['node']['text']).replace('@', ' ')
                                except:
                                    caption =''
                                med = Media(id=nested_content['node']['id'], is_video=nested_content['node']['is_video'], url=url, caption=caption, product_type=product_type)
                                insert_in_db(conn, med)
                                counter+=1
                                # media_list.append(med)
                    else:
                        if content['node']['taken_at_timestamp'] >= last_timestamp:
                            url = content['node']['video_url'] if content['node']['is_video'] else \
                            content['node']['display_url']
                            product_type = content['node']['product_type'] if 'product_type' in content[
                                'node'] else None
                            if content['node']['is_video']:
                                if ('video_duration' in content['node'] and content['node'][
                                    'video_duration'] < 3.00) or ('video_duration' in content['node'] and content['node'][
                                    'video_duration'] > 900.00):
                                    continue
                            try:
                                caption = str(
                                    content['node']['edge_media_to_caption']["edges"][0]['node']['text']).replace('@',
                                                                                                                         ' ')
                            except:
                                caption = ''
                            med = Media(is_video=content['node']['is_video'],id=content['node']['id'], url=url, caption=caption, product_type=product_type)
                            # media_list.append(med)
                            insert_in_db(conn, med)
                            counter += 1
            if 'edge_owner_to_timeline_media' in response["graphql"]["user"]:
                for content in response["graphql"]["user"]['edge_owner_to_timeline_media']['edges']:
                    if 'edge_sidecar_to_children' in content['node']:
                        for nested_content in  content['node']['edge_sidecar_to_children']['edges']:
                            if content['node']['taken_at_timestamp']>= last_timestamp:
                                url = nested_content['node']['video_url'] if nested_content['node']['is_video'] else nested_content['node']['display_url']
                                product_type = nested_content['node']['product_type'] if 'product_type' in \
                                                                                         nested_content[
                                                                                             'node'] else None
                                if nested_content['node']['is_video']:
                                    if ('video_duration' in nested_content['node'] and nested_content['node'][
                                        'video_duration'] < 3.00) or ('video_duration' in nested_content['node'] and nested_content['node'][
                                        'video_duration'] > 900.00) :
                                        continue
                                try:
                                    caption = str(
                                        nested_content['node']['edge_media_to_caption']["edges"][0]['node']['text']).replace(
                                        '@', ' ')
                                except:
                                    caption = ''
                                med = Media(is_video=nested_content['node']['is_video'],id=nested_content['node']['id'], url=url, caption=caption, product_type=product_type)
                                insert_in_db(conn, med)
                                # media_list.append(med)
                                counter += 1
                    else:
                        if content['node']['taken_at_timestamp'] >= last_timestamp:
                            url = content['node']['video_url'] if content['node']['is_video'] else \
                            content['node']['display_url']
                            product_type = content['node']['product_type'] if 'product_type' in content[
                                'node'] else None
                            if content['node']['is_video']:
                                if ('video_duration' in content['node'] and content['node'][
                                    'video_duration'] < 3.00) or ('video_duration' in content['node'] and content['node'][
                                    'video_duration'] > 900.00):
                                    continue
                            try:
                                caption = str(
                                    content['node']['edge_media_to_caption']["edges"][0]['node']['text']).replace('@',
                                                                                                                         ' ')
                            except:
                                caption = ''
                            med = Media(is_video=content['node']['is_video'],id=content['node']['id'], url=url, caption=caption, product_type=product_type)
                            insert_in_db(conn, med)
                            counter += 1
                            # media_list.append(med)

        except Exception as e:
            print(e)
            print('unable to get info for ', account)
    conn.close()
    print('total media length', str(counter))
    print('total inserted in db', str(inserted_in_db))


