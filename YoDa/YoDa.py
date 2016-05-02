import os
import easygui
import shelve
import requests
import pyperclip
from sys import exit
from urllib import unquote
from subprocess import check_output
from Tkinter import Tk
from re import compile, sub
from BeautifulSoup import BeautifulSoup
from hashlib import md5
from uuid import getnode
from urlparse import urlparse
import HTMLParser
id_hash = md5(str(getnode())).hexdigest()

__author__ = 'Yogi'
__version__ = '1.9.9'

# icon genuinity

if os.path.isfile('icon.ico') and os.path.isfile('icon.png'):
    icon_i = ''.join(str(e) for e in open('icon.ico').readlines())
    icon_p = ''.join(str(e) for e in open('icon.png').readlines())
    if (md5(icon_i).hexdigest() != '89fcd9bcf566cb30d2e86d6e9b9f0bdc' and
        md5(icon_p).hexdigest() != '658e8dc0bf8b9a09b36994abf9242099'):
        easygui.msgbox(title='YoDa by Yogi', msg='One or More File is Invalid or Missing')
        exit(0)
else:
    easygui.msgbox(title='YoDa by Yogi', msg='One or More file is missing or corrupted. Try re-installing the software.')
    exit(0)
# Replacing the tk logo
tk = Tk()
tk.withdraw()
tk.iconbitmap(default='icon.ico')
tk.destroy()
#



class ConfigClass:
        def __init__(self):
                if not os.path.isdir(os.environ['APPDATA']+r'\FeedAbyte'):
                        os.makedirs(os.environ['APPDATA']+r'\FeedAbyte\YoDa')
                if not os.path.isdir(os.environ['APPDATA']+r'\FeedAbyte\YoDa'):
                        os.mkdir(os.environ['APPDATA']+r'\FeedAbyte\Yoda')
                if not os.path.isfile(os.environ['APPDATA']+r'\FeedAbyte\YoDa\config'):
                        self.create_default()

        def create_default(self):
                if os.path.isfile(os.environ['APPDATA']+r'\FeedAbyte\YoDa\config'):
                        os.remove(os.environ['APPDATA']+r'\FeedAbyte\YoDa\config')
                path_config = {'idm': {'path': os.environ['PROGRAMFILES']+r'\Internet Download Manager\IDMan.exe',
                                       'cmd': '[path] /d [url]'},
                               'flashget': {'path': os.environ['PROGRAMFILES']+r'\FlashGet Network\FlashGet 3\FlashGet3.exe',
                                            'cmd': '[path] [url]'}}
                config_file = shelve.open(os.environ['APPDATA']+r'\FeedAbyte\YoDa\config')
                config_file['path_config'] = path_config
                config_file.close()
                
        def update_config(self):
                def add_edit(op='Add', update_what=None):
                        config_file = shelve.open(os.environ['APPDATA']+r'\FeedAbyte\YoDa\config', writeback=True)
                        if op == 'Add':
                                tup = 'new'
                        else:
                                tup = ''
                        if op == 'Add':
                                name = easygui.enterbox(title='YoDa by Yogi', msg='Please enter a name for the Download Manager, Leave blank if you want me to choose one :)')
                        path = easygui.fileopenbox(title='YoDa by Yogi', msg='Please select the %s path for Download Manager' % tup, filetypes=['*.exe'],
                                                   default=(os.environ['PROGRAMFILES']+'\\'))
                        if not os.path.isfile(path):
                                easygui.msgbox(title='YoDa by Yogi', msg='Path cannot be blank. Please try again providing valid path')
                                exit(0)
                        command = easygui.enterbox(title='YoDa by Yogi',msg='Please enter the %s YoDa syntax of command(Ref. ReadMe) for the given Download Manager'%tup)
                        if not command:
                                easygui.msgbox(title='YoDa by Yogi', msg='Command can not be blank. Please try adding again with proper command')
                                exit(0)
                        if path and command:
                                if not path.endswith('.exe'):
                                        choice_box = ['No it\'s alright', 'Oops! I\'m mistaken']
                                        now_what = easygui.buttonbox(title='YoDa by Yogi', msg='You are on Windows. Ain\'t you? Shouldn\'t it be .exe file?',
                                                                     choices=choice_box)
                                        if now_what == choice_box[1]:
                                                easygui.msgbox(title='YoDa by Yogi', msg='It\'s ok. Let\'s try again.')
                                                exit(0)
                        if op == 'Add':
                                if not name:
                                        name = os.path.basename(path).split('.')[0]
                                for i in config_file['path_config']:
                                    if name == i:
                                            bba = easygui.buttonbox(title='YoDa by Yogi',
                                                                    msg='A download manager with the name already exists(Ref ReadMe(Add.1))',
                                                                    choices=['Overwrite', 'Try with different name'])
                                            if bba == 'Try with different name':
                                                    name = easygui.enterbox(title='YoDa by Yogi',msg='Enter new name for the download manager')
                                if not name:
                                        name = path.split('.')[0]
                                config_file['path_config'][name] = {'path': path, 'cmd': command}
                                config_file.sync()
                                config_file.close()
                                easygui.msgbox(title='YoDa by Yogi',msg='Values has been updated successfully')
                        if op == 'Edit':
                                config_file['path_config'][update_what] = {'path': path, 'cmd': command}
                                config_file.sync()
                                config_file.close()
                                easygui.msgbox(title='YoDa by Yogi',msg='Values has been updated successfully')
                
                do_what = easygui.buttonbox(title='YoDa by Yogi', msg="Choose operation", choices=['Add', 'Edit', 'Delete', 'Reset to Default'])
                if do_what:
                        if do_what == 'Reset to Default':
                                self.create_default()
                        elif do_what == 'Add':
                                add_edit('Add')
                        else:
                                view = self.read_config()
                                ch = [i[0] for i in view]
                                if len(ch) < 1:
                                        cch = easygui.buttonbox(title='YoDa by Yogi', msg='No entries to %s, Add atleast one first' % do_what, choices=['Ok', 'Reset to Default'])
                                        if cch == 'Reset to Default':
                                                self.create_default()
                                                easygui.msgbox(title='YoDa by Yogi', msg='Settings has been restored successfully')
                                                exit(0)
                                        else:
                                                exit(0)
                                update_what = easygui.choicebox(title='YoDa by Yogi', msg='Choose an entry to %s' % do_what, choices=ch)
                                if update_what:
                                        config_file = shelve.open(os.environ['APPDATA']+r'\FeedAbyte\YoDa\config', writeback=True)
                                        if do_what == 'Delete':
                                                del config_file['path_config'][update_what]
                                                config_file.sync()
                                                config_file.close()
                                        if do_what == 'Edit':
                                                add_edit('Edit', update_what)
                                else:
                                        easygui.msgbox(title="YoDa by Yogi", msg="You haven't selected any entry")
                else:
                        easygui.msgbox(title='YoDa by Yogi', msg='You haven\'t selected any operation')

        def read_config(self):
            if not os.path.isfile(os.environ['APPDATA']+r'\FeedAbyte\YoDa\config'):
                    return
            config_file = shelve.open(os.environ['APPDATA']+r'\FeedAbyte\YoDa\config')
            config_info = config_file['path_config']
            config_info_l = []
            for dms in config_info:
                path_cmd = [dms]
                for i in ['path', 'cmd']:
                        path_cmd.append(config_info[dms][i])
                config_info_l.append(path_cmd)
            return config_info_l


configObj = ConfigClass()


class YoDa:
    """Tries catching address of predefined download managers by itself"""
    def __init__(self, path=None):
        # Downloader Path
        self.path = path
        # Mode Flag; 0 Default, 1 Independent
        self.mode = 0
        self.download_address = ''
        # Command of DM
        self.cmd = ''
        # Name of the file
        self.name = ''

    def trigger(self):
        operation_ = easygui.buttonbox(title='YoDa by Yogi', msg='Choose the operation',
                                       choices=['Download', 'Link only', 'Settings', 'About', 'Update', 'Exit'])
        if not operation_ or operation_ == 'Exit':
            exit(0)
        if operation_ == 'About':
            abt_us = ("""\t\t          YoDa_v%s\n
This software downloads the videos and audios from almost all popular media sites using your download manager.
Developed by\t: Yogi
e-mail\t\t: acetheultimate(at)gmail(dot)com
Website\t\t: http://video.feedabyte.com
""") % __version__

            about_choice = easygui.buttonbox(title="YoDa by Yogi", msg=abt_us, choices=['Back', 'ReadMe', 'Exit'],
                                             image='icon.png')
            
            if about_choice == 'Back':
                self.trigger()
            if about_choice == 'ReadMe':
                os.startfile('ReadMe.txt')
                exit(0)
            else:
                exit(0)
            exit(0)
        if operation_ == 'Update':
            try:
                response = requests.get('http://devzone.pe.hu/YoDa/updates.php').text
                response = BeautifulSoup(response)
                self.download_address = response.find('a')
                self.download_address = 'http://devzone.pe.hu/YoDa'+self.download_address['href'][1:]
                qual = response.text.split(':')
                self.name = qual
                if qual[0] > 'YoDa_v'+__version__:
                    self.mode = 2
                else:
                    easygui.msgbox(title='YoDa by Yogi', msg='Voila! You are Up to Date :)')
                    exit(0)
            except requests.exceptions.ConnectionError:
                easygui.msgbox('Connection Error! Please check your internet connectivity')
                exit(0)
        if operation_ == 'Settings':
            configObj.update_config()
            exit(0)
        if operation_ == 'Download':
            self.mode = 0
        if operation_ == 'Link only':
            self.mode = 1
        self.path_selector()

    def path_selector(self):
        if self.mode != 1:
            configs = configObj.read_config()
            count = 1
            path_list = []
            for i in configs:
                tup = ''
                if not os.path.isfile(i[1]):
                    tup = '(broken link)'
                path_list.append('%d.%s%s' % (count, i[0], tup))
                count += 1
            if len(path_list):
                self.path = easygui.choicebox(title="YoDa by Yogi", msg="You have set following download managers",
                                              choices=path_list)
                if not self.path:
                    easygui.msgbox(title='YoDa by Yogi', msg="You haven't selected any Download Manger")
                    exit(0)
                if 'broken' in self.path:
                    broken_choice = ['Continue to url only mode', 'Exit']
                    broken_op = easygui.buttonbox(title='YoDa by Yogi', msg=('Your path to the download manager doesn' +
                                                                             '\'t seem to be working'),
                                                  choices=broken_choice)
                    if broken_op == broken_choice[0]:
                        self.mode = 1
                    else:
                        exit(0)
                if self.path:
                    index = int(self.path.split('.')[0])-1
                    self.path = configs[index][1]
                    self.cmd = configs[index][2]
            else:
                stal_op = easygui.ynbox(title='YoDa by Yogi', msg=('You haven\'t configured any download manager' +
                                                                   '. Continue to URL only mode?'),
                                        choices=['Continue', 'Exit'])
                if stal_op:
                    self.mode = 1
                else:
                    exit(0)
            if self.mode == 2:
                qual = self.name[1]
                self.name = self.name[0]
                self.getter({qual: self.download_address})
            else:
                self.link_input()
        else:
            self.link_input()
    def link_input(self):
        try:
            cb_text = pyperclip.paste()
        except:
            cb_text = ''
        d_url = ''
        word_list = ['.com', 'www', 'http', 'https']
        for i in word_list:
            if i in cb_text:
                d_url = cb_text
                break
        d_url = easygui.enterbox(title='YoDa by Yogi', msg="Please paste/enter the link here",
                                 default=d_url, ok_text='Download')
        if not d_url:
            easygui.msgbox(title="YoDa by Yogi", msg="You haven't entered any link. We're exiting now.")
            exit(0)
        self.url_processing(d_url)

    def url_processing(self, d_url=None):
        """
        Enter the link of the video, it would return downloadable link of the video
        """
        if not d_url:
            exit(0)

        site_parse = urlparse(d_url).netloc
        url = "http://keepvid.com/?url=%s" % d_url
        header = {
            'user-agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9) Gecko/2008062417 (Gentoo) Iceweasel/3.0.1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'accept-language': 'en-us,en;q=0.5', 'accept-charset': 'utf-8'
        }
        try:
            try:
                requests.get('http://devzone.pe.hu/YoDa/count.php?id=%s&site=%s&version=%s' % (id_hash, site_parse,
                                                                                               __version__))
            except requests.exceptions.ConnectionError:
                pass
            response = requests.get(url, headers=header)
            response = response.text
            soup = BeautifulSoup(response)
            downloadable = {}
            bogus_links = 0
            for i in soup.findAll('div', attrs={'id':'info'}):
                bogus_links += len(i.findAll('a'))
            
            for div in soup.findAll('div', attrs={'id': 'dl'}):
                links_ = div.findAll('a')
                urls_ = [i['href'] for i in links_]
                print urls_
                type_ = [i.text for i in links_]
                pars = HTMLParser.HTMLParser()
                self.name = pars.unescape(type_[bogus_links-1])
                quality_ = [i.text for i in div.findAll('b') if i.text != "*NEW*"]
                for typ, qual, link in zip(type_[bogus_links:], quality_, urls_[bogus_links:]):
                    typ = typ.replace('&raquo; Download ', '').replace(' &laquo;', '')
                    name = typ + ((5-len(typ))+6)*' ' + qual
                    downloadable[name] = pars.unescape(link)
        except requests.exceptions.ConnectionError:
            error_c = easygui.buttonbox(title='YoDa by Yogi',
                                        msg="Please check your internet connectivity and try again",
                                        choices=['Retry', 'Exit'])
            if error_c == 'Retry':
                self.url_processing(d_url)
            else:
                exit(0)
        except:
            easygui.msgbox(title="YoDa by Yogi", msg=("Error! Please report to the developer with the "+
                                                              "link you were trying."))
            exit(0)
        if len(downloadable):
            self.getter(dict_=downloadable)
        else:
            getter_er_c = easygui.ynbox(title='YoDa by Yogi', msg=('The website from which you want to download ' +
                                                                   'might not be supported currently(Ref ReadMe).' +
                                                                   ' Try downloading with supported website'),
                                        choices=['Retry', 'Exit'])
            if getter_er_c:
                self.link_input()
            else:
                exit(0)

    def getter(self, dict_=None):
        if not dict_:
            easygui.msgbox(title='YoDa by Yogi', msg='Dictionary file is not provided.')
            exit(0)
        qual = easygui.choicebox(title='YoDa by Yogi', msg='Pick a quality for %s' % self.name,
                                 choices=sorted(dict_), ok_button='Download')
        if qual:
            link_d = dict_[qual]
        else:
            exit(0)
        pattern = compile('%25')
        tup = pattern.subn('%', link_d)
        self.download_address = unquote(tup[0])
        if self.download_address:
            self.doer(address=self.download_address, mode=self.mode)
        else:
            exit(0)
            
    def doer(self, address, mode=None):

        if mode == 1:
            pyperclip.copy(address)
            msg = ('Link successfully copied to clipboard. Paste it to get it downloaded from any download manager' +
                   ' or browser.\nThank you for using YoDa :)')
            end_c_box = ['Continue', 'Close']
        else:
            command = self.cmd_decode(self.cmd)
            try:
                result = check_output(command, shell=True)
                if result:
                    print result
                msg = ('Download has been started as per configurations. If it hasn\'t, Please check your ' +
                       'configurations again. If you want to copy the downloadable url. You can click the button')
            except:
                msg = ('Unfortunately, We are unable to trigger the download but we\'ve got the link for you. Please click'+
                       ' the button below to copy it and to manually start the download.')
                 
            end_c_box = ['Continue', 'Copy Link to Clipboard', 'Close']

        end_c = easygui.buttonbox(title='YoDa by Yogi', msg=msg, choices=end_c_box, image='icon.png')
        if end_c == 'Continue':
            self.trigger()
        if end_c == 'Copy Link to Clipboard':
            pyperclip.copy(self.download_address)
            cc_box = easygui.buttonbox(title="YoDa by Yogi", msg=('Link successfully copied to clipboard. Paste it ' +
                                                                  'to get it downloaded from any download manager or' +
                                                                  ' browser.\nThank you for using YoDa :)'),
                                       choices=["Continue", "Exit"], image='icon.png')
            if cc_box == 'Continue':
                self.trigger()
            else:
                exit(0)
        else:
            exit(0)

    def cmd_decode(self, cmd):
        cmd = cmd.replace('[path]', '"'+self.path+'"')
        cmd = cmd.replace('[url]', '"'+self.download_address+'"')
        cmd = cmd.replace('[name]', '"'+self.name+'"')
        return cmd

if '__main__' == __name__:
    obj = YoDa()
    obj.trigger()
