import createMetadata as cm
import sys

if __name__ == "__main__":
    # print (sys.argv)
    inputArg = sys.argv
    if len(inputArg)>1 and inputArg[1] == '-t':
        for tab in inputArg[2:]:
            if tab.isalnum():
                cm.writeMetadata(tab.upper())
            else:
                print ('Please verify the table name')
    elif len(inputArg)>1 and inputArg[1] == '-t':
        print('Invalid argument: '+sys.argv[1])
    else:
        print('Please provide a table name')