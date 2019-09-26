#!/usr/bin/python3
from pprint import pprint;
import os
import requests
import argparse;
import vk_api
from vk_api import audio

class getVkAudio():

    def inputAccessCode(self, remembed=None):
        code = input("Input code: ")
        remembed = True
        return code, remembed

    def auth(self, login, password, user_id):
        vk_session = vk_api.VkApi(login=login, password=password)
        try:
            vk_session.auth()
        except:
            vk_session = vk_api.VkApi(login=login, password=password, auth_handler=self.inputAccessCode)
            vk_session.auth()
        self.vk = vk_session.get_api()
        self.vk_audio = audio.VkAudio(vk_session)

    def main(self):
        try:
            self.path = "downloads/"
            arguments = argparse.ArgumentParser();
            arguments.add_argument("-f", "--folder", default="default");
            arguments.add_argument("-l", "--login", default="login");
            arguments.add_argument("-p", "--password", default="password");  
            arguments.add_argument("-i", "--uid", default="0");
            args = arguments.parse_args();

            self.save_to = self.path+args.folder;
            if not os.path.exists(self.save_to):
                os.makedirs(self.save_to)

            self.auth(args.login,args.password, args.uid);
            print("login ok");
                
            os.chdir(self.save_to)

            try:
                audio = self.vk_audio.get(owner_id=args.uid)
            except:
                print("No Records Found");
                return
            

            print("downloading...");
            it = 0;
            total_download = 0;
            
            for a in audio:
                fn = "{} - {}.mp3".format(a["artist"], a["title"]).replace("/", "_");
                perc = it/len(audio)*100;
                if not os.path.isfile(fn) :
                    resp = requests.get(audio[it]["url"])
                    if resp.status_code == 200:
                        print("progress {}%. {}".format(round(perc, 2), fn));
                        with open(fn, 'wb') as output_file:
                            output_file.write(resp.content)
                            total_download+=1;
                    else:
                        print("ERROR, can't download audio. resp code: {}".format(resp.status_code));
                        return;
                else:
                    print("file exist: {}".format(fn));

                it+=1
            print("Total audio: {}. Total download {}".format(len(audio),total_download));
        except KeyboardInterrupt:
            print("Aborted")

if __name__ == '__main__':
    app = getVkAudio()
    app.main()
    
    
    
    
    
