import os
import argparse
import psutil


# prints the list of active processes on a file
def print_processes(active_processes):
    print("PID | Name")
    for active_proc in active_processes:
        print("{0} | {1}".format(active_proc["pid"], active_proc["name"]))
    print("------------")
    print("Total: {0}".format(len(active_processes)))


# kills all active processes
def kill_processes(active_processes):
    for process in active_processes:
        (psutil.Process(process["pid"])).kill()


def main():
    # argument parser
    parser = argparse.ArgumentParser()

    # add CLI arguments
    parser.add_argument('-u', '--unlock', action="store_true",
                        help="If included, automatically unlocks the file/folder selected")
    parser.add_argument('-f', '--file', type=str, help="File/Folder name to unlock", required=True)

    # parse arguments
    args = parser.parse_args()

    # this list will hold all active processes on selected file
    active_processes = []
    # construct the file path to our file
    # we compare every used file path by any process with this file path
    selected_file_path = os.getcwd() + "\\" + args.file

    # check if selected file/folder exists
    if not os.path.exists(selected_file_path):
        print(selected_file_path + " is not a valid path")
    else:
        print("Looking for lock on " + os.getcwd() + "\\" + args.file)

        # loop through all processes that are running
        for process in psutil.process_iter():
            try:
                # check if process is running and if it has any handles
                if process.is_running() and process.num_handles() > 0:
                    # this returns the list of opened files by the current process
                    processes_files = process.open_files()
                    if processes_files:
                        # loops through the list of files used by the current process
                        for file in processes_files:
                            # check if the process has file opened that is actually our file
                            if file.path == selected_file_path:
                                # add process to the list
                                active_processes.append({
                                    "pid": process.pid,
                                    "name": process.name()
                                })
            except psutil.Error as err:
                continue

        if len(active_processes) == 0:
            print("No active processes locking the file")
        else:
            # print all active processes
            print_processes(active_processes)

            # if the unlock argument is there, kill automatically
            if args.unlock is True:
                kill_processes(active_processes)
            else:
                # if there was no unlock argument, prompt to kill
                prompt = input("Would you like to kill all processes that lock this file? [Y / N]: ")
                if prompt.lower() == "y" or prompt.lower() == "yes":
                    kill_processes(active_processes)

        # prompt to delete the file
        prompt = input("Would you like to delete this file? [Y / N]: ")
        if prompt.lower() == "y" or prompt.lower() == "yes":
            os.remove(selected_file_path)
