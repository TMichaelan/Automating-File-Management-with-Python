import os, shutil, time

PROCESS_PATH = r'C:\Users\bigap\Desktop\Process'
path_to_illustrator = r"C:\Program Files\Adobe\Adobe Illustrator CC 2019\Support Files\Contents\Windows"
path_to_scripts = r"D:\PROJECTS\PYproj\Python Automation\Automating-File-Management-with-Python\New Order Script\JSX Scripts Illustrator"
folder_list = ["2.5cm", "3.5cm", "4.5cm", "6.5cm", "9.5cm"]

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
                ls_of_folders_1 = os.listdir(PROCESS_PATH + '\\' + list_element)

                for list_element_1 in ls_of_folders_1:

                    path = PROCESS_PATH + '\\' + list_element + '\\' + list_element_1

                    if os.path.isdir(path):

                        file_list = os.listdir(path)

                        for file_name in file_list:
                            os.system("cd {path_to_illustrator}".format(path_to_illustrator = path_to_illustrator))
                            os.system(r"start Illustrator.exe {path}\{file_name}".format(path=path,file_name = file_name))
                            time.sleep(10)
                            if list_element in folder_list:
                                jsx_script = "Batch Print {folder}.jsx".format(folder=list_element)
                                os.system("\"{path_to_scripts}\{jsx_script}\"".format(path_to_scripts=path_to_scripts,jsx_script=jsx_script))
                                time.sleep(5)
                                os.system("taskkill /IM Illustrator.exe /F")


start_time = time.time()
print("[*] Starting...")
time.sleep(1)
execution()
print("[*] Finished! Time: " + str(round(time.time() - start_time, 2)) + "s")

