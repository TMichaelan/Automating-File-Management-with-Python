import os, shutil, time, configparser, subprocess, datetime


config = configparser.ConfigParser()
config.read("settings.ini")

path_to_scripts = config["DEFAULT"]["path_to_jsx_scripts"]
PROCESS_PATH = config["DEFAULT"]["process_path"]
path_to_illustrator = config["DEFAULT"]["path_to_illustrator"]
done_folder = config["DEFAULT"]["done_folder"]
folder_list = ["2.5cm", "3.5cm", "4.5cm", "6.5cm", "9.5cm"]


def process_exists(process_name):

    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode('utf-8', 'ignore')
    last_line = output.strip().split('\r\n')[-1]

    return last_line.lower().startswith(process_name.lower())

def execution_process_old():
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

                            # os.system("cd {path_to_illustrator}".format(path_to_illustrator=path_to_illustrator) + " && " + r"start Illustrator.exe {path}\{file_name}".format(path=path, file_name=file_name))

                            os.system("cd {path_to_illustrator}".format(path_to_illustrator=path_to_illustrator))
                            os.system(r"start Illustrator.exe {path}\{file_name}".format(path=path, file_name=file_name))
                            time.sleep(5)

                            if list_element in folder_list:
                                jsx_script = "Batch Print {folder}.jsx".format(folder=list_element)
                                os.system("\"{path_to_scripts}\{jsx_script}\"".format(path_to_scripts=path_to_scripts,jsx_script=jsx_script))
                                time.sleep(5)
                                # CLOSE Illustrator
                                os.system("taskkill /IM Illustrator.exe /F")
                                time.sleep(10)


def execute_jsx(script):

    jsx_script = "Batch Print {folder}.jsx".format(folder=script)
    os.system("\"{path_to_scripts}\{jsx_script}\"".format(path_to_scripts=path_to_scripts, jsx_script=jsx_script))
    time.sleep(5)


def close_illustrator():
    # CLOSE Illustrator
    os.system("taskkill /IM Illustrator.exe /F")
    time.sleep(10)

def execution_process():

    ls_of_folders = os.listdir(PROCESS_PATH)
    list_of_folders = []

    for list_element in ls_of_folders:
        if os.path.isdir(PROCESS_PATH + "\\" + list_element):
            list_of_folders.append(list_element)

    for folder in ls_of_folders:

        path = PROCESS_PATH + '\\' + folder
        file_list = os.listdir(path)

        if folder in list_of_folders:

            for file_name in file_list:

                if process_exists("Illustrator.exe"):
                    os.system("cd {path_to_illustrator}".format(path_to_illustrator=path_to_illustrator))
                    os.system(r"start Illustrator.exe {path}\{file_name}".format(path=path, file_name=file_name))

                    time.sleep(5)
                    execute_jsx(folder)

                else:

                    os.system("cd {path_to_illustrator}".format(path_to_illustrator=path_to_illustrator))
                    os.system(r"start Illustrator.exe")
                    time.sleep(15)

                    os.system("cd {path_to_illustrator}".format(path_to_illustrator=path_to_illustrator))
                    os.system(r"start Illustrator.exe {path}\{file_name}".format(path=path, file_name=file_name))

                    time.sleep(5)
                    execute_jsx(folder)

    close_illustrator()
    folders_list = os.listdir(PROCESS_PATH)

    for i in folders_list:
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        shutil.copytree(PROCESS_PATH + "\\" + i, done_folder + "\\" + folder + "_" + date)
    shutil.rmtree(PROCESS_PATH)



start_time = time.time()
print("[*] Starting...")
time.sleep(1)
execution_process()
print("[*] Finished! Time: " + str(round(time.time() - start_time, 2)) + "s")

