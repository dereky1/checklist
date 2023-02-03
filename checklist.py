"""This is a program to help keep track of list of items
Extracts title and artist info from Apple Music exported XML library
Writes info into CSV file for easier view and use"""
#TODO: Create a checklist

import xml.etree.ElementTree as ET
import io

#function to extract XML data into more usable dictionary
def getDictfromAppleXML(xmlFileName):
        library = {} #stored as number {num: [title, artist]}

        try:
            tree = ET.parse(xmlFileName)
            plist = tree.getroot()
        except:
            print("Unable to parse XML File")
            return 1

        for first_dict in plist: #traverse XML for APPLE Music library Export
            for sec_dict in first_dict:
                if sec_dict.tag == "dict":
                    count = 1 # count used as dictionary key
                    for item in sec_dict:
                        if item.tag == "dict":
                            tag = False # relevant tag has been met e.g. title/artist
                            tagName = ""
                            songInfo = [] # array to store title and artist info
                            for field in item: #This is where track information is held, first item is tag second is value
                                if tag: #title or artist tag has been found and flag has been set to add to an array
                                    songInfo.append("{}:{}".format(tagName,field.text))
                                    tag = False
                                elif field.text == "Name": # Only extracting name and artist info for now
                                    tag = True
                                    tagName = "Title"
                                elif field.text == "Artist":
                                    tag = True
                                    tagName = "Artist"
                            library[count] = songInfo #add song info to dictionary
                            count += 1 # increase dict key count
        return library


#Function to create list
#used to initiate  checklist the first Time
def initCheckList(csvFileName):
    try:#opens up a csv file to export XML data in CSV
        file = io.open(csvFileName, 'w', encoding='utf8')
    except:
        print("Unable to open file for writing")

    for title, artist in getDictfromAppleXML('Library.xml').values(): #extracts title/artist data from dictionary
        file.write("{},{}\n".format(title[6:], artist[7:]))

    file.close() #close file


#Main function
def main():
    ###Create function to check configs
    ###if init == True skip init
    initCheckList("library.csv")

    return 0



if __name__ == "__main__":
    main()
