import urllib.request
import urllib
import re
import json
import os
from simple_term_menu import TerminalMenu


def userinputngrab(searchterm): #gets information about a video if given a video title, gets first 5 results
        global video_ids
        global compqueryname
        compqueryname = searchterm.replace(" ","+")

        grabinfo(1)
        grabinfo(2)        
        grabinfo(3)
        grabinfo(4)       
        grabinfo(5)

        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + compqueryname)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

def grabinfo(videoidvar): #gets title, author, duration of each video using the video id variable which pumps it into the 'grabvideoid' function
        grabvideoid(videoidvar)
        searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+videoid+"&key="+api_key+"&part=contentDetails"
        response = urllib.request.urlopen(searchUrl).read()
        data = json.loads(response)
        all_data=data['items']
        contentDetails=all_data[0]['contentDetails']
        duration=contentDetails['duration']

        searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+videoid+"&key="+api_key+"&part=snippet"
        response = urllib.request.urlopen(searchUrl).read()
        data = json.loads(response)
        all_data=data['items']
        snippet=all_data[0]['snippet']
        title=snippet['title']
        author=snippet['channelTitle']

        info = title+"  |  "+author+"  |  "+duration.replace("PT", "").replace("H"," hours ").replace("M"," minutes ").replace("S"," seconds ")
        print(str(videoidvar)+". "+info+"\n")

def grabvideoid(videoidthing): #gets video id out of the array using the number of the video
        global videoid
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + compqueryname)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        videoid = video_ids[int(videoidthing - 1)]

def grabtitle(videoidt): #grabs title with provided video id
        global titleg
        searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+videoidt+"&key="+api_key+"&part=snippet"
        response = urllib.request.urlopen(searchUrl).read()
        data = json.loads(response)
        all_data=data['items']
        snippet=all_data[0]['snippet']
        titleg=snippet['title']

api_key="AIzaSyDbPe8JgP5vav4llRz7-4r1eWMZhc3w1Ro"
print("\n")
print('Welcome to the MP3 stripper! \n')

baseoptions = ["[s] Search Query", "[m] Make Queue", "[l] Input Link", "[q] Quit"]
queueoptions = ["[a] Add To Queue", "[v] View Queue", "[d] Download Queue", "[q] Quit"]
mainMenu = TerminalMenu(baseoptions) #error here, keyword argument of some kind, says it has 3 but can only take 2
queueMenu = TerminalMenu(queueoptions)





while True:
        print("What would you like to do today? Do a Search Query, make a queue, input a link, or quit?")
        baseoptionsIndex = mainMenu.show()
        baseoptionsChoice = baseoptions[baseoptionsIndex]
        if baseoptionsChoice == "[s] Search Query":
                print("\n")

                queryname = input("Which video would you like to strip the mp3 from? ")

                print("\n")

                userinputngrab(queryname)

                while True:
                        userchoice = input("Select a video (1-5): ")
                        if userchoice.isdigit() == True:
                                userchoicenumber = int(userchoice)
                                videonamestr = video_ids[userchoicenumber - 1]
                                os.system("youtube-dl -x -i --audio-format mp3 --audio-quality 0 https://www.youtube.com/watch?v=" + videonamestr)
                                print("\n")
                                break
                        elif userchoice == "q":
                                break
                        else:
                                print("Try a number next time or type 'q' to quit")
                                continue
        elif baseoptionsChoice == "[m] Make Queue":

                        while True:
                                print("\n")

                                print('Would you like to add to the queue, view the queue, download the queue, or quit (a/v/d/q)? ')
                                queueoptionsIndex = queueMenu.show()
                                queueoptionsChoice = queueoptions[queueoptionsIndex]

                                if queueoptionsChoice == "[a] Add To Queue":
                                        print("\n")

                                        qchoice = input("Find a video to add to the queue: ")

                                        print("\n")

                                        userinputngrab(qchoice)

                                        userchoice = input("Select a video (1-5): ")
                                        if userchoice.isdigit() == True:
                                                userchoicenumber = int(userchoice)
                                                videoidnumber = (userchoicenumber - 1)
                                                videonamestr = (video_ids[int(videoidnumber)])
                                                grabtitle(video_ids[videoidnumber])

                                                with open('queue', 'a') as queue:
                                                        queue.write(str(titleg) + "--" + videonamestr + "\n")
                                                print("\n")
                                                break
                                        else: 
                                                print("Try an appropriate option next time or type 'q' to quit")
                                                continue


                                elif queueoptionsChoice == "[v] View Queue":
                                        print("\n")
                                        
                                        with open('queue', 'r') as queue:
                                                line_num = 0
                                                for line in queue.readlines():
                                                        line_num += 1
                                                        data = line.rstrip()
                                                        eltit,bideoid = data.split('--')
                                                        print(str(line_num) + ". " + eltit + "\n")
                                        break

                                elif queueoptionsChoice == "[d] Download Queue":
                                        print("\n")
                                        
                                        with open('queue', 'r+') as queue:
                                                for line in queue.readlines():
                                                        data = line.rstrip()
                                                        eltit,bideoid = data.split('--')
                                                        os.system("youtube-dl -x -i --audio-format mp3 --audio-quality 0 https://www.youtube.com/watch?v=" + bideoid)
                                                queue.truncate(0)
                                        print("\n")
                                        break

                                elif queueoptionsChoice == "[q] Quit":
                                        print("\n")
                                        break
                                else:
                                        print("\n")
                                        print("Try a number next time or type 'q' to quit")
                                        break
        elif baseoptionsChoice == "[l] Input Link":
                while True:
                        link = input("Copy and paste a link of a youtube video/playlist here to download it: ")
                        os.system("youtube-dl -x -i --audio-format mp3 --audio-quality 0 " + link)
                        break
        elif baseoptionsChoice == "[q] Quit":
                print("\n")
                break
        else:
                print("Try an input from the options this time")
                continue


print("All done. Have a nice day!")
print("\n")
