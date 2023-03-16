import sqlite3

import  time
from pywinauto.application import Application
from pywinauto import mouse
from pywinauto import keyboard
import urllib.request
import os
import glob
import moviepy.editor as mp
import uuid
app = Application(backend='uia').start(u"C:\Program Files\Google\Chrome\Application\chrome.exe --force-renderer-accessibility")
time.sleep(1)
# connect with it
app = app.connect(title_re=u'New Tab - Google Chrome', found_index=0,class_name_re='Chrome_WidgetWin_1')
window = app.window(title_re=u'New Tab - Google Chrome', found_index=0,class_name_re='Chrome_WidgetWin_1')
window.set_focus()
window.maximize()
x = window.child_window(title='INSSIST | Instagram Assistant', found_index=0, control_type='MenuItem', top_level_only=False)
x.set_focus()
z = x._calc_click_coords()
mouse.click(coords=z)
time.sleep(3)

insta_window = app.window(title='INSSIST | Assistant for Instagram - Google Chrome', found_index=0,class_name_re='Chrome_WidgetWin_1')


def change_upload_status(conn, id):
    conn.execute(f"UPDATE data SET is_uploaded = 1 WHERE  id = '{id}';")
    conn.commit()


def all_db_data(limit=5):
    # 25 is api publish limit
    conn = sqlite3.connect('content.db')
    r = conn.execute(f"select * from data where is_uploaded = 0 order by is_video desc limit 30")
    data = r.fetchall()
    conn.close()
    return data


def resize_vidoe(input):

    clip = mp.VideoFileClip(input)
    new_widht = int((clip.h * 4) / 5) + 1
    clip_resized = clip.resize((new_widht, clip.h))
    print(clip_resized.h, clip_resized.w)
    output = r'C:\Users\riyaz\PycharmProjects\ins_bot\temp\movie.mp4'
    clip_resized.write_videofile(output, fps=60)
    return output

def insta_gui_upload(insta_window, data_path, is_video, caption):
    insta_window.set_focus()
    while range(5):
        try:
            x = insta_window.child_window(title='New Post', found_index=0, control_type='MenuItem', top_level_only=False)
            z = x._calc_click_coords()
            mouse.click(coords=z)
            time.sleep(2)

            x = insta_window.child_window(title='PHOTO / VIDEO', found_index=0, control_type='Text', top_level_only=False)
            z = x._calc_click_coords()
            mouse.click(coords=z)
            time.sleep(2)


            filename = insta_window.child_window(title='File name:', class_name='Edit', found_index=0,top_level_only=False)
            filename.set_edit_text(data_path)

            insta_window.child_window(title='Open', class_name='Button', found_index=0, top_level_only=False).click()
            break
        except:
            continue



    if is_video:
        time.sleep(20)
    else:
        time.sleep(4)
    insta_window.child_window(title='Next',  found_index=0,top_level_only=False).click()

    insta_window.child_window(title='Write a caption…',control_type='Edit',  found_index=0,top_level_only=False).set_edit_text(caption)

    insta_window.child_window(title='Share',  found_index=0,top_level_only=False).click()
    time.sleep(10)

def insta_gui_reels_upload(insta_window, data_path, is_video, caption):
    insta_window.set_focus()
    while range(5):
        try:
            x = insta_window.child_window(title='New Post', found_index=0, control_type='MenuItem', top_level_only=False)
            z = x._calc_click_coords()
            mouse.click(coords=z)
            time.sleep(2)

            x = insta_window.child_window(title='REELS', found_index=0, control_type='Text', top_level_only=False)
            z = x._calc_click_coords()
            mouse.click(coords=z)
            time.sleep(2)


            filename = insta_window.child_window(title='File name:', class_name='Edit', found_index=0,top_level_only=False)
            filename.set_edit_text(data_path)

            insta_window.child_window(title='Open', class_name='Button', found_index=0, top_level_only=False).click()
            break
        except:
            continue



    if is_video:
        time.sleep(20)
    insta_window.child_window(title='Next',  found_index=0,top_level_only=False).click()

    insta_window.child_window(title='Write a caption…',control_type='Edit',  found_index=0,top_level_only=False).set_edit_text(caption)

    insta_window.child_window(title='Share',  found_index=0,top_level_only=False).click()
    time.sleep(10)

def insta_gui_story_upload(insta_window, data_path, is_video, caption):
    insta_window.set_focus()
    while range(5):
        try:
            x = insta_window.child_window(title='New Post', found_index=0, control_type='MenuItem', top_level_only=False)
            z = x._calc_click_coords()
            mouse.click(coords=z)
            time.sleep(2)

            x = insta_window.child_window(title='STORY', found_index=0, control_type='Text', top_level_only=False)
            z = x._calc_click_coords()
            mouse.click(coords=z)
            time.sleep(2)


            filename = insta_window.child_window(title='File name:', class_name='Edit', found_index=0,top_level_only=False)
            filename.set_edit_text(data_path)

            insta_window.child_window(title='Open', class_name='Button', found_index=0, top_level_only=False).click()
            break
        except:
            continue



    if is_video:
        time.sleep(10)
    else:
        time.sleep(3)
    x = insta_window.child_window(title='Add to your story',  found_index=0,control_type='Text', top_level_only=False)
    z = x._calc_click_coords()
    mouse.click(coords=z)


    time.sleep(30)

### loop #####
data = all_db_data()
print('db data')
print(data)
counter = 0

conn = sqlite3.connect('content.db')
for d in data:
    try:
        caption = d[2] + " #likeforlikes #love #followforfollowback #photooftheday #bhfyp #babe  #instadaily #picoftheday #likeforfollow #beautiful #fashion  #smile #style #life #nature #cute #insta #model #viral  #music #travel #memes #girl #selfie #liker  #loveyourself #trending #tiktok #viral #photoshoot "
        url = d[1]


        if d[3]:
            data_path = os.path.abspath('./temp/00000001.mp4')

        else:
            data_path = os.path.abspath('./temp/00000001.jpg')
        print(data_path)
        urllib.request.urlretrieve(url, data_path)

        if d[3]:
            data_path = resize_vidoe(data_path)


        is_reel = d[5] == 'clips'
        is_igtv = d[5] == 'igtv'
        insta_gui_upload(insta_window, data_path, d[3], caption)

        if is_reel:
            import shutil

            original = data_path
            target = fr'C:\Users\riyaz\PycharmProjects\ins_bot\reels\{str(uuid.uuid4())}.mp4'
            shutil.copyfile(original, target)
            # insta_gui_reels_upload(insta_window,data_path, d[3], caption)
        if counter< 20:
            insta_gui_story_upload(insta_window,data_path,d[3],'')
            counter+=1

        # if is_igtv:
        # # call igtv upload

        change_upload_status(conn, d[0])

        files = glob.glob('./temp/*')
        for f in files:
            os.remove(f)
        time.sleep(30)
    except Exception as e:
        keyboard.send_keys('{ENTER}')
        files = glob.glob('./temp/*')
        if d[3]:
            change_upload_status(conn, d[0])
        for f in files:
            os.remove(f)
        print(e)
conn.close()



##########################################################
# # open new incognito
# keyboard.send_keys('^+N')
# window = app.window(title=u'New Tab - Google Chrome (Incognito)', found_index=0,class_name_re='Chrome_WidgetWin_1')
# window.set_focus()
# window.maximize()
# address=window.child_window(title='Address and search bar')
# address.type_keys('www.instagram.com{ENTER}')
# # keyboard.send_keys('')
# # time.sleep(4)
# insta_page = app.window(title='Instagram - Google Chrome (Incognito)', class_name='Chrome_WidgetWin_1', found_index=0)
# insta_page.wait(wait_for='visible', timeout=15)
# insta_page.set_focus()
# # insta_page.print_control_identifiers()
# # insta_page.dump_tree()
# usernme = insta_page.child_window(title='Phone number, username, or email',  found_index=0,control_type='Edit',top_level_only=False)
# usernme.set_edit_text('adultmeme714')
# usernme = insta_page.child_window(title='Password',  found_index=0,control_type='Edit',top_level_only=False)
# usernme.set_edit_text('Riyaz@203')
# mouse.click(coords=(1238,448))
# time.sleep(10)
# mouse.click(coords=(963,650))
# time.sleep(4)
# mouse.click(coords=(1051,726))
#
#
#
#
# #### for loop #################
# # new post
# mouse.click(coords=(1353,125))
# time.sleep(1)
# # add button
# mouse.click(coords=(964,654))
# time.sleep(3)
#
# # set image path
# x = r"C:\Users\riyaz\Dropbox\My PC (LAPTOP-RR8FP430)\Pictures\Predator\Predator_3840x2160.jpg"
# filename =  app.window(title='Create new post • Instagram - Google Chrome (Incognito)').child_window(title='File name:', class_name='Edit', found_index=0,top_level_only=False)
# filename.set_edit_text(x)
#
# filename =  app.window(title='Create new post • Instagram - Google Chrome (Incognito)').child_window(title='Open', class_name='Button', found_index=0,top_level_only=False)
# filename.click()
#
#
# mouse.click(coords=(1249,220))
# time.sleep(2)
# mouse.click(coords=(1468,220))
# time.sleep(2)
#
#
# filename =  app.window(title='Create new post • Instagram - Google Chrome (Incognito)').child_window(title='Write a caption...', control_type='Edit', found_index=0,top_level_only=False)
# caption='test'
# filename.set_edit_text(caption)
# mouse.click(coords=(1439,223))
# time.sleep(10)
#
# mouse.click(coords=(1877,121))
#
