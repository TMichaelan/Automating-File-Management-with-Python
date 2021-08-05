import os, shutil, time


'''
    * Separates the files
    * Fixed the multiplication issue (73 out of 93 lol)
    * Fixed the v1 v2 issue (in case the process is small
      and there are no 2.5cm or 4.5cm)
    * Logged the success rate
    * Doesn't run on the same files multiple times
    * Added a v3 for 2.5cm
    * Errors: None
'''


#Mark's paths
PROCESS_PATH = 'C:\\Users\\Mark\\Desktop\\Process'
POSTAGE_PATH = 'C:\\Users\\Mark\\Desktop\\Print Postage'


#Separate the PDFs from PSDs
def pdf_psd():
    #Remove the MAC folder
    try:
        shutil.rmtree(PROCESS_PATH + '\\__MACOSX')
    except:
        pass

    #Getting the names of all the folders
    #This is where it breaks, must separate zips, rars
    #and junk from actual folders
    ls_of_folders = os.listdir(PROCESS_PATH)
    list_of_folders = []

    #Different logic since the first one didn't work for some reason
    for list_element in ls_of_folders:
        if os.path.isdir(PROCESS_PATH + "\\" + list_element):
            list_of_folders.append(list_element)

    #Going through the root folder
    for folder in list_of_folders:
        #Mixed combo differs from the rest, has 3 folders inside
        if folder != "Mixed Combo" and folder != "Mixed combo" and folder != "mixed combo" and folder != "mixed Combo":
            os.mkdir(POSTAGE_PATH + "\\" + folder)
            #Getting file list
            file_list = os.listdir(PROCESS_PATH + "\\" + folder)
            
            #Separation process
            for file_name in file_list:
                if file_name[-4:] == ".pdf":
                    shutil.copy(PROCESS_PATH + "\\" + folder + "\\" + file_name, POSTAGE_PATH + "\\" + folder)
                    os.remove(PROCESS_PATH + "\\" + folder + "\\" + file_name)


                elif file_name[-4:] != ".psd" and folder != "ISO":
                    os.remove(PROCESS_PATH + "\\" + folder + "\\" + file_name)

                elif file_name[-4:] != ".eps" and folder == "ISO":
                    os.remove(PROCESS_PATH + "\\" + folder + "\\" + file_name)

                else:
                    if file_name[0] == "x" and folder != "ISO":

                        #Fixed the multiplication error
                        number = ""
                        for i in range(1, len(file_name)):
                            if file_name[i].isdigit():
                                number += str(file_name[i])
                            else:
                                break

                        if number != "":
                            for i in range(int(number)):
                                new_name = file_name[:-4] + "_" + str(i + 1) + "_of_" + str(number) + ".psd"
                                shutil.copy(PROCESS_PATH + "\\" + folder + "\\" + file_name, PROCESS_PATH + "\\" + folder + "\\" + new_name)
                            os.remove(PROCESS_PATH + "\\" + folder + "\\" + file_name)

                    elif file_name[0] == "x" and folder == "ISO":
                        number = ""
                        for i in range(1, len(file_name)):
                            if file_name[i].isdigit():
                                number += str(file_name[i])
                            else:
                                break

                        if number != "":
                            for i in range(int(number)):
                                new_name = file_name[:-4] + "_" + str(i + 1) + "_of_" + str(number) + ".eps"
                                shutil.copy(PROCESS_PATH + "\\" + folder + "\\" + file_name,
                                            PROCESS_PATH + "\\" + folder + "\\" + new_name)
                            os.remove(PROCESS_PATH + "\\" + folder + "\\" + file_name)



        else:
            os.mkdir(POSTAGE_PATH + "\\" + folder)
            #Getting folder list
            folder_list = os.listdir(PROCESS_PATH + "\\" + folder)
            for f in folder_list:
                try:
                    if f[-9:] == ".DS_Store":
                        os.remove(PROCESS_PATH + "\\" + folder + "\\" + f)
                        continue
                    os.mkdir(POSTAGE_PATH + "\\" + folder + "\\" + f)
                    #Files inside each of the 3 folders
                    f_list = os.listdir(PROCESS_PATH + "\\" + folder + "\\" + f)

                    #Separation process
                    for f_name in f_list:
                        if f_name[-4:] == ".pdf" :
                            shutil.copy(PROCESS_PATH + "\\" + folder + "\\" + f + "\\" + f_name, POSTAGE_PATH + "\\" + folder)
                            os.rmdir(POSTAGE_PATH + "\\" + folder + "\\" + f)
                            os.remove(PROCESS_PATH + "\\" + folder + "\\" + f + "\\" + f_name)
                        elif f_name[-4:] != ".psd":
                            os.remove(PROCESS_PATH + "\\" + folder + "\\" + f + "\\" + f_name)


                        else:
                            #Multiplication of PSDs
                            if f_name[0] == "x":

                                #Fixed the multiplication error
                                number = ""
                                for i in range(1, len(f_name)):
                                    if f_name[i].isdigit():
                                        number += str(f_name[i])
                                    else:
                                        break
                                
                                if number != "":
                                    for i in range(int(number)):
                                        new_name = f_name[:-4] + "_" + str(i + 1) + "_of_" + str(number) + ".psd"
                                        shutil.copy(PROCESS_PATH + "\\" + folder + "\\" + f + "\\" + f_name, PROCESS_PATH + "\\" + folder + "\\" + f + "\\" + new_name)
                                    os.remove(PROCESS_PATH + "\\" + folder + "\\" + f + "\\" + f_name)
                except Exception as e:
                    print(e)
                    continue

def split(n_folders):
    #This splits the folders 4.5 and 3.5 into v1 and v2
    folder_list = ["2.5cm", "3.5cm", "4.5cm", "6.5cm", "9.5cm"]
    #Get file list
    for folder in folder_list:
        try:
            #Get the file list
            file_list = os.listdir(PROCESS_PATH + "\\" + folder)
            #Create nine folders
            for i in range(n_folders):
                os.mkdir(PROCESS_PATH + "\\" + folder + "\\" +  folder + "_v" + str(i + 1))
            counter = 0
            number = len(file_list)
            #Start the first few separations
            for i in range(number % n_folders):
                for j in range((number // n_folders) + 1):
                    shutil.move(PROCESS_PATH + "\\" + folder + "\\" + file_list[counter], PROCESS_PATH + "\\" + folder + "\\" + folder + "_v" + str(i + 1))
                    counter += 1
            for i in range(number % n_folders, n_folders):
                for j in range(number // n_folders):
                    shutil.move(PROCESS_PATH + "\\" + folder + "\\" + file_list[counter], PROCESS_PATH + "\\" + folder + "\\" + folder + "_v" + str(i + 1))
                    counter += 1
        except Exception as e:
            print(e)
            continue

def check_if_ran():
    #Check if there are split files in the root
    if "2.5cm_v1" in os.listdir(PROCESS_PATH + "\\2.5cm"):
        return True
    return False

if not check_if_ran():
    start_time = time.time()
    #First separate
    print("[*] Starting the separation...")
    time.sleep(1)
    pdf_psd()
    print("[*] Files separated successfully!")
    #Actually let's split after separation, makes life easier
    print("[*] Splitting large directories...")
    n_folders = 12
    split(n_folders)
    print("[*] Folders split successfully!")
    print("[*] Finished! Time: " + str(round(time.time() - start_time, 2)) + "s")

else:
    print("[!] Already ran on these files!")
