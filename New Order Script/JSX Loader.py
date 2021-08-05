import os, shutil, time

PROCESS_PATH = 'C:\\Users\\bigap\\Desktop\\Print Postage'
folder_list = ["2.5cm", "3.5cm", "4.5cm", "6.5cm", "9.5cm"]

# Separate the PDFs from PSDs
def execution():
    # Remove the MAC folder
    try:
        shutil.rmtree(PROCESS_PATH + '\\__MACOSX')
    except:
        pass

        ls_of_folders = os.listdir(PROCESS_PATH)
        list_of_folders = []

        for list_element in ls_of_folders:
            if os.path.isdir(PROCESS_PATH + "\\" + list_element):
                list_of_folders.append(list_element)

        print(list_of_folders)
        # # Going through the root folder
        for folder in list_of_folders:

            file_list = os.listdir(PROCESS_PATH + "\\" + folder)

            for file_name in file_list:

                x = file_name + ' /c "JSX Scripts\\Batch Print PSD {folder}.jsx"'.format(folder=folder)
                print(x)
                # os.system(x)



start_time = time.time()
print("[*] Starting...")
time.sleep(1)
execution()
print("[*] Finished! Time: " + str(round(time.time() - start_time, 2)) + "s")

