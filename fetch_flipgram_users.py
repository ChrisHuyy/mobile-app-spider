#!/usr/bin/python
#coding:utf-8

from __future__ import unicode_literals
from common import *

package='com.cheerfulinc.flipagram'
activity='com.cheerfulinc.flipagram.FirstLaunchActivity'
# activity='com.cheerfulinc.flipagram.activity.search.SearchActivity'

back_btn_in_video_page = None
avatar_btn_in_video_page = None

def get_buttom_search_button_position(ui_xml_file):
    positions = []
    import xml.dom.minidom
    DOMTree = xml.dom.minidom.parse(ui_xml_file)
    nodes = DOMTree.documentElement.getElementsByTagName("node")
    print len(nodes)    

    for node in nodes:
        naf = node.getAttribute("NAF")
        index = node.getAttribute("index")
        if naf == 'true' and index == '1':
            bounds = node.getAttribute("bounds")
            positions.append(get_middle_point(bounds))
    # 删掉文件，防止下次重新加载
    os.rename(ui_xml_file, ui_xml_file + '.bk')
    return positions

def get_up_search_button_position(ui_xml_file):
    print os.path.exists(ui_xml_file)
    positions = []
    try:
        import xml.dom.minidom
        DOMTree = xml.dom.minidom.parse(ui_xml_file)
        nodes = DOMTree.documentElement.getElementsByTagName("node")
        print len(nodes)

        for node in nodes:
            resource_id = node.getAttribute("resource-id")
            if resource_id == 'com.cheerfulinc.flipagram:id/searchText':
                bounds = node.getAttribute("bounds")
                positions.append(get_middle_point(bounds))
        # 删掉文件，防止下次重新加载
        os.rename(ui_xml_file, ui_xml_file + '.bk')
        return positions
    except:
        return positions

def get_topic_menu_position(ui_xml_file):
    positions = []
    try:
        import xml.dom.minidom
        DOMTree = xml.dom.minidom.parse(ui_xml_file)
        nodes = DOMTree.documentElement.getElementsByTagName("node")

        for node in nodes:
            resource_id = node.getAttribute("text")
            if resource_id == u'主题标签':
                bounds = node.getAttribute("bounds")
                positions.append(get_middle_point(bounds))
        # 删掉文件，防止下次重新加载
        os.rename(ui_xml_file, ui_xml_file + '.bk')
        return positions
    except:
        return positions

def get_word_position(ui_xml_file,word):
    positions = []
    try:
        import xml.dom.minidom
        DOMTree = xml.dom.minidom.parse(ui_xml_file)
        nodes = DOMTree.documentElement.getElementsByTagName("node")

        for node in nodes:
            resource_id = node.getAttribute("text")
            if resource_id == word:
                bounds = node.getAttribute("bounds")
                positions.append(get_middle_point(bounds))
        # 删掉文件，防止下次重新加载
        os.rename(ui_xml_file, ui_xml_file + '.bk')
        return positions
    except:
        return positions

def get_user_cover_position(ui_xml_file):
    positions = []
    try:
        import xml.dom.minidom
        DOMTree = xml.dom.minidom.parse(ui_xml_file)
        nodes = DOMTree.documentElement.getElementsByTagName("node")

        for node in nodes:
            resource_id = node.getAttribute("resource-id")
            if resource_id == 'com.cheerfulinc.flipagram:id/cover_image':
                bounds = node.getAttribute("bounds")
                positions.append(get_middle_point(bounds))
        # 删掉文件，防止下次重新加载
        os.rename(ui_xml_file, ui_xml_file + '.bk')
        return positions
    except:
        return positions


def get_user_name_position(ui_xml_file):
    positions = []
    try:
        import xml.dom.minidom
        DOMTree = xml.dom.minidom.parse(ui_xml_file)
        nodes = DOMTree.documentElement.getElementsByTagName("node")

        for node in nodes:
            resource_id = node.getAttribute("resource-id")
            if resource_id == 'com.cheerfulinc.flipagram:id/user_name':
                bounds = node.getAttribute("bounds")
                positions.append(get_middle_point(bounds))
        # 删掉文件，防止下次重新加载
        os.rename(ui_xml_file, ui_xml_file + '.bk')
        return positions
    except:
        return positions

def get_video_cover_position(ui_xml_file):
    positions = []
    try:
        import xml.dom.minidom
        DOMTree = xml.dom.minidom.parse(ui_xml_file)
        nodes = DOMTree.documentElement.getElementsByTagName("node")

        for node in nodes:
            resource_id = node.getAttribute("resource-id")
            if resource_id == 'com.cheerfulinc.flipagram:id/cover_image':
                bounds = node.getAttribute("bounds")
                positions.append(get_middle_point(bounds))
        # 删掉文件，防止下次重新加载
        os.rename(ui_xml_file, ui_xml_file + '.bk')
        return positions
    except:
        return positions

def load_back_btn_and_avatar_btn(ui_xml_file):
    global back_btn_in_video_page
    global avatar_btn_in_video_page
    import xml.dom.minidom
    DOMTree = xml.dom.minidom.parse(ui_xml_file)
    nodes = DOMTree.documentElement.getElementsByTagName("node")

    for node in nodes:
        resource_id = node.getAttribute("resource-id")
        if resource_id == 'com.smile.gifmaker:id/back_btn':
            bounds = node.getAttribute("bounds")
            back_btn_in_video_page = get_middle_point(bounds)
        elif resource_id == 'com.smile.gifmaker:id/avatar':
            bounds = node.getAttribute("bounds")
            avatar_btn_in_video_page = get_middle_point(bounds)

def process_one_video(pos_in_feed_list):
    click(pos_in_feed_list[0], pos_in_feed_list[1])
    time.sleep(5)

    if back_btn_in_video_page == None or avatar_btn_in_video_page == None:
        ui_xml_file = get_ui_xml()
        print "back and btn done: " + ui_xml_file
        load_back_btn_and_avatar_btn(ui_xml_file)

    print "avatar_btn_in_video_page: " + str(avatar_btn_in_video_page)
    #点击头像，通过Java代理程序进行抓包，在Java代理程序中中分析它的响应格式
    click(avatar_btn_in_video_page[0], avatar_btn_in_video_page[1])
    time.sleep(5)
    # 从用户页返回列表页
    click(back_btn_in_video_page[0], back_btn_in_video_page[1])
    time.sleep(5)
    # 从列表页返回用户页
    click(back_btn_in_video_page[0], back_btn_in_video_page[1])

def loop_get_ui_xml():
    timer = 15
    while timer > 0:
        ui_xml_file = get_ui_xml()
        if os.path.exists(ui_xml_file):
            print 'file found'
            return ui_xml_file
            break
        else:
            print 'still finding %d' % timer
            time.sleep(1)
            ui_xml_file = get_ui_xml()
            if os.path.exists(ui_xml_file):
                print 'file found'
                return ui_xml_file
        timer = timer - 1

def run_flipgram(interval):

    # if the program is alive
    begin = (long)(time.time()*1000)

    run_app(package, activity)

    current = (long)(time.time() * 1000)

    if current - begin > interval:
        # print get_current_time(), "Run time is over, just exit kuaishou"
        return
    # 做一个下拉刷新，注意，坐标在不同机型可能不一样，后续看是否要兼容一下

    swipe(100, 100, 100, 900)
    # 获取当前界面的所有元素信息，以xml表示

    #get search buttom
    ui_xml_file = loop_get_ui_xml()
    print ui_xml_file
    positions = get_buttom_search_button_position(ui_xml_file)
    print 'top search buttom :',positions
    click(positions[0][0], positions[0][1])


    # get search input
    ui_xml_file = loop_get_ui_xml()
    print ui_xml_file    
    positions = get_up_search_button_position(ui_xml_file)
    print 'search input buttom :',positions
    click(positions[0][0], positions[0][1])

    # get topic buttom
    ui_xml_file = loop_get_ui_xml()
    print ui_xml_file
    positions = get_topic_menu_position(ui_xml_file)
    print 'search tag buttom :',positions
    click(positions[0][0], positions[0][1])
    ui_xml_file = loop_get_ui_xml()
    print ui_xml_file

    # input text
    input_text("india")
    ui_xml_file = loop_get_ui_xml()
    print ui_xml_file


    positions = get_word_position(ui_xml_file, "#india")
    click(positions[0][0], positions[0][1])
    ui_xml_file = loop_get_ui_xml()
    print ui_xml_file

    positions = get_user_cover_position(ui_xml_file)
    print positions
    # == TODO 遍历，逐个去点击 ==
    click(positions[0][0], positions[0][1])
    ui_xml_file = loop_get_ui_xml()
    print ui_xml_file

    positions = get_user_name_position(ui_xml_file)
    click(positions[0][0], positions[0][1])
    print 'sleeping for 10 seconds...'
    time.sleep(10)
    swipe(100, 100, 100, 12000)  #? 没有滑动？
    ui_xml_file = loop_get_ui_xml()
    print ui_xml_file

    # TODO 解析用户名、页面中的元素（观看数，粉丝数，关注数，发送到服务器端），发送到服务器端

    #尝试看它的页面
    positions = get_video_cover_position(ui_xml_file)
    print positions
    click(positions[0][0], positions[0][1])
    ui_xml_file = loop_get_ui_xml()
    print ui_xml_file

    # 返回上层
    #call_system_return()
    # == 结束遍历 ==

if __name__ == '__main__':
    run_flipgram(10000000000000L)