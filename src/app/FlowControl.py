from __init__ import *

class FlowControl:
    
    __PLATFORM_WINDOWS = "windows"
    __PLATFORM_MAC_OS = "darwin"
    __PLATFORM_LINUX = "linux"
    
    __username = ""
    
    __stations = None
    __station = {}
    __extractor = None
    __emp3 = None
    
    def __init__(self):
        self.__reset()
        
    def __reset(self):
        self.__stations = PandoraStations()
        self.__station = None
        self.__extractor = PandoraStationExtractor()
        self.__emp3 = Emp3World()
        
    def start(self):
        self.__reset()
        self.__clrscr()
        print "Options:"
        print "1. Proceed to the interesting part!"
        print "0. Exit the program"
        try:
            option = raw_input("Select an option by entering its preceeding number: ")
        except:
            print 
            sys.exit(1)
        if option.lower().strip()=='exit':
            print "Goodbye..."
            sys.exit(1)
        try:
            option = int(option)
        except:
            self.start()
        if option==1:
            self.__input_username()
        elif option==0:
            print "Goodbye..."
            sys.exit(1)
        else:
            self.start()

    def __input_username(self, wrongUsername=False):
        self.__reset()
        self.__clrscr()
        if wrongUsername:
            print "The username " + self.__username + " has no station. Please use another one."
        try:
            username = raw_input("What's your Pandora username? (Enter 'exit' to go back to the main menu): ")
        except:
            print 
            sys.exit(1)
        if username.lower().strip()=="exit":
            self.start()
        self.__username = username.strip()
        self.__check_usernmae()
        
    def __check_usernmae(self):
        self.__clrscr()
        print "Looking up username " + self.__username + " ..."
        self.__stations.set_profile_username(self.__username)
        if self.__stations.scan():
            self.__print_stations()
        else:
            self.__input_username(True)
            
    def __print_stations(self, invalidInput=False):
        self.__clrscr()
        print "You have " + str(self.__stations.get_count()) + " station(s):"
        print "--------------------------------------------"
        self.__stations.list_stations()
        print "--------------------------------------------"
        if invalidInput:
            print "INVALID INPUT! Please try again..."
        print "Choose your favorite station by entering its preceeding number."
        try:
            option = raw_input("(Or enter 0 to go back and use a nother Pandora account): ")
        except:
            print 
            sys.exit(1)
        try:
            option = int(option)
        except:
            self.__print_stations(True)
        if option<0:
            self.__print_stations(True)
        elif option==0:
            self.__input_username()
        elif option<=self.__stations.get_count():
            self.__station = self.__stations.get_station(option-1)
            self.__print_station_tracks()
        else:
            self.__print_stations(True)
            
    def __print_station_tracks(self, invalidInput=False):
        if not invalidInput:
            self.__clrscr()
            print "Scanning station " + self.__station["name"] + ":"
            print "--------------------------------------------"
            self.__extractor = PandoraStationExtractor()
            count = 0
            if self.__extractor.set_station_id(self.__station["id"]):
                count = self.__extractor.scan()
                if count>0:
                    print "--------------------------------------------"
                else:
                    print "You haven't thumbed up any track in this station."
                    try:
                        raw_input("Press any key to go back to your stations list...")
                    except:
                        print 
                        sys.exit(1)
                    self.__print_stations()
            else:
                print "The station appeared to be invalid. Weird! Please choose another one."
                try:
                    raw_input("Press any key to go back to your stations list...")
                except:
                    print 
                    sys.exit(1)
                self.__print_stations()
        
        print "Options:"
        print "0. Go back to stations list"
        print "1. Proceed to download all thumbed-up tracks in this station"
        validInput = False
        while not validInput:
            try:
                option = raw_input("Select an option by entering its preceeding number: ")
            except:
                print 
                sys.exit(1)
            try:
                option = int(option)
            except:
                validInput = False
                continue
            if option!=0 and option!=1:
                validInput = False
                continue
            validInput = True
            if option==0:
                self.__print_stations()
            else:
                self.__download()
        
    def __download(self):
        self.__clrscr()
        global SAVE_DIR
        saveDir = SAVE_DIR+'/'+self.__station["name"].replace('/', '').strip()
        if not os.path.exists(saveDir) or not os.path.isdir(saveDir):
            try:
                os.makedirs(saveDir)
                print "Created sub folder " + saveDir
            except:
                print "Can not create directory "+saveDir
                saveDir = SAVE_DIR
                print "All of your music files will be saved to " + saveDir
        print
        self.__emp3.set_save_dir(saveDir)
        count = 0
        while self.__extractor.next_list():
            tracks = self.__extractor.get_cur_tracks()
            for t in tracks:
                print t; 
                print "--------------------------------------------"
                self.__emp3.set_keyword(t)
                if self.__emp3.search() > 0:
                    if self.__emp3.download_next():
                        print " --- Successful"
                        count += 1
                    else:
                        print " --- No file was found for this track!"
                else:
                    print " --- No file was found for this track!"
                print
        print "--------------------------------------------"
        self.__finish_download(count)
        
    def __finish_download(self, countDownloads):
        print "Total tracks downloaded: ", str(countDownloads)
        print "Options:"
        print "0. Go back to main menu"
        print "1. Go back to stations list"
        print "2. Switch to another Pandora account"
        validInput = False
        while not validInput:
            try:
                option = raw_input("Select an option by entering its preceeding number: ")
            except:
                print 
                sys.exit(1)
            try:
                option = int(option)
            except:
                validInput = False
                continue
            if option==0:
                self.start()
                validInput = True
            elif option==1:
                self.__print_stations()
                validInput = True
            elif option==2:
                self.__input_username()
                validInput = True
            else:
                validInput = False
            
    def __clrscr(self):
        if sys.platform==self.__PLATFORM_WINDOWS:
            os.system("cls")
        else:
            os.system("clear")
            
            
            