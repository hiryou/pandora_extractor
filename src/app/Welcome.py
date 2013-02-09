from __init__ import *

class Welcome:
    @staticmethod
    def disclaimer():
        print
        print "#################################################################################" 
        print "# Welcome to PandoraExtractor, a free software which helps you download your    #"
        print "# favorite music from Pandora to your local computer under mp3 files.           #"
        print "# ----------------------------------------------------------------------------  #"
        print "# Despite the name 'PandoraExtractor', this program does not stream any song    #"
        print "# from Pandora, nor does Pandora have such mp3 storage for their digital music. #"
        print "# PandoraExtractor simply reads the list of thumbed-up tracks in your account   #"
        print "# and download them from other free mp3 music provider websites.                #"
        print "# ----------------------------------------------------------------------------  #"
        print "# The program is restrictedly desgined for personal usage. If you intend to     #"
        print "# use it for other benefits, please take your own risks!                        #"
        print "# ----------------------------------------------------------------------------  #"
        print "# Made by Long Nguyen <longuyen@pdx.edu>                                        #"
        print "#################################################################################"
        print
        try:
            raw_input("Press any key to continue...")
        except:
            print 
            sys.exit(1)