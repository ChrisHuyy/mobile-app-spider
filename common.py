#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time, re, sys, subprocess, threading, signal
# from ali_send_sms import send_message
# from ali_send_sms import send_dingding
# from ali_send_sms import get_current_time

class AlertOption(object):
    pass

def send_sms(message):
    option = AlertOption()
    option.ip = "100.85.22.128"
    option.time = get_current_time()
    option.message = message.encode('utf8')
    # send_message(option, '18123957566')

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.output = None

    def run(self, timeout):
        def target():
            # print get_current_time(), 'Start command', self.cmd
            self.process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE)
            out, err = self.process.communicate()
            # print get_current_time(), 'Command return', self.process.returncode, 'output:', out
            self.output = out

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            # print get_current_time(), 'Command timeout, force kill it'
            os.kill(self.process.pid, signal.SIGKILL)
            thread.join()
            return 100000, None
        return self.process.returncode, self.output

def run_command(cmd, timeout=60):
    command = Command(cmd)
    ret,out = command.run(timeout=timeout)
    if ret == 100000:
        # 相关的命令超时了，adb有异常，重连一下吧
        # print get_current_time(), "Try to recovery adb connection"
        time.sleep(5)
        os.system('ps -ef | grep " adb " | awk \'{print $2}\' | xargs -I{} kill -9 {}')
        time.sleep(3)
        os.system('adb start-server')
        time.sleep(3)
        os.system('sudo udevadm control --reload-rules && sudo service udev restart && sudo udevadm trigger')
        time.sleep(3)
        command = Command('adb reverse tcp:8008 tcp:8085')
        ret,out = command.run(timeout=timeout)
        if ret == 100000:
            send_sms(u'adb状态异常，爬虫进行不下去了，退出')
            sys.exit(1)
        command = Command(cmd)
        ret,out = command.run(timeout=timeout)
        if ret == 100000:
            send_sms(u'adb状态异常，爬虫进行不下去了，退出')
            sys.exit(1)
        return ret,out
    else:
        return ret,out

# 判断是否处于锁屏状态
def is_screen_locked():
    ret, out = run_command('adb shell dumpsys window policy|grep isStatusBarKeyguard')
    isStatusBarKeyguard = False
    mShowingLockscreen = False
    out_cnt = 0
    if out != None and out.find('isStatusBarKeyguard=false') < 0:
        isStatusBarKeyguard = True
    if out != None:
        out_cnt = out_cnt + 1
    ret, out = run_command('adb shell dumpsys window policy|grep mShowingLockscreen')
    if out != None and out.find('mShowingLockscreen=false') < 0:
        mShowingLockscreen = True
    if out != None:
        out_cnt = out_cnt + 1
    if out_cnt == 0:
        return True
    return isStatusBarKeyguard or mShowingLockscreen

# 解锁屏幕
def unlock_screen():
    # 这里检查一下屏幕状态，因为屏幕要求必须开启才行
    ret,out = run_command('adb shell dumpsys power | grep state')
    if out == None or out.find('ON') < 0:
        # 屏幕是关着的，开启它
        # print get_current_time(), "Power is off, tap the powner button"
        run_command('adb shell input keyevent 26')
    # print get_current_time(), 'swipe the lock screen to open'
    run_command('adb shell input swipe 900 900 300 300 1000')

# 检查一下adb的状态，如果adb状态异常，那可能需要人工干预一下
def check_adb_status():
    return True

    ret = os.popen('lsusb | awk \'{if($7=="") print $0}\' | grep Device').read()
    if ret == '':
        # 竟然usb连接都断了，要报个警，这种情况是否必须人工处理?
        send_sms(u'adb usb已断开，请重新连接')
        return False
    ret,out = run_command('adb devices | grep device | grep -v "List"')
    if ret != 0 or out == None or out == '':
        # adb连接都断了，要报个警，这种情况是否必须人工处理?
        os.system('sudo udevadm control --reload-rules && sudo service udev restart && sudo udevadm trigger')
        time.sleep(5)
        ret,out = run_command('adb devices | grep device | grep -v "List"')
        if ret != 0 or out == None or out == '':
            send_sms(u'adb usb已断开，请重新连接')
            return False

    # 这里检查一下屏幕状态，因为屏幕要求必须开启才行
    if is_screen_locked():
        # print get_current_time(), "Screen is locked, then we try unlock it"
        unlock_screen()

    ret,out = run_command('adb shell "netstat -npl | grep 127.0.0.1:8008 | grep LISTEN"')
    if ret != 0 or out == None or out == '':
        # 反向代理断开了，重设一次
        run_command('adb reverse tcp:8008 tcp:8085')
        time.sleep(5)
        ret,out = run_command('adb shell "netstat -npl | grep 127.0.0.1:8008 | grep LISTEN"')
        if ret != 0 or out == None or out == '':
            # 反向代理重设不生效，发报警
            send_sms(u'adb reverse代理设置失败')
            return False

    return True

def run_app(appPkg, activity):
    # unlock the screen
    if check_adb_status() == False:
        time.sleep(1)
        sys.exit(1)
    run_command("adb shell input keyevent 82")
    run_command("adb shell am force-stop %s" %(appPkg))
    time.sleep(3)
    run_command("adb shell am start -n %s/%s" %(appPkg, activity))
    # print get_current_time(), "Start app and activity"

def get_ui_xml():
    pid = os.getegid()
    run_command("adb shell rm -rf /sdcard/adb_ui.xml")
    run_command("adb shell uiautomator dump /sdcard/adb_ui.xml")
    run_command("adb pull /sdcard/adb_ui.xml /tmp/android-ui-%d.xml" %(pid))
    # print get_current_time(), "Save ui xml to /tmp/android-ui-%d.xml" %(pid)
    return "/tmp/android-ui-%d.xml" %(pid)

def click(xpos, ypos):
    run_command("adb shell input tap %d %d" %(xpos, ypos))

def swipe(from_x, from_y, to_x, to_y):
    run_command("adb shell input swipe %d %d %d %d" %(from_x, from_y, to_x, to_y))

def get_middle_point(bounds):
    pattern = re.compile("\\[(\d+),(\d+)\\]\\[(\d+),(\d+)\\]")
    items = pattern.findall(bounds)[0]
    xpos = (int(items[0]) + int(items[2]))/2
    ypos = (int(items[1]) + int(items[3]))/2
    return (xpos, ypos)

def get_positions(res_id):
    ui_xml_file = get_ui_xml()
    positions = []
    try:
        import xml.dom.minidom
        DOMTree = xml.dom.minidom.parse(ui_xml_file)
        nodes = DOMTree.documentElement.getElementsByTagName("node")
	
        for node in nodes:
            resource_id = node.getAttribute("resource-id")
            if resource_id == res_id:
                bounds = node.getAttribute("bounds")
                positions.append(get_middle_point(bounds))
        # 删掉文件，防止下次重新加载 
        os.rename(ui_xml_file, ui_xml_file + '.bk')
        return positions
    except:
        return positions



if __name__ == '__main__':
    get_ui_xml()