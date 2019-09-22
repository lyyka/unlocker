import os
import argparse
import psutil, datetime


# prints the list of active processes on a file
def print_processes(active_processes):
    # initiate empty max_lens object
    max_lens = {}

    # go through each dict in list and find max lengths
    max_lens_sum = 0
    for dict in active_processes:
        # go through each key for each dict
        for key in dict:
            # if the key was not initialized before, set it to 0
            if key not in max_lens:
                max_lens[key] = 0
            # decrease max sum by the current key
            max_lens_sum -= max_lens[key]
            # check if max value should be overwritten
            if len(str(dict[key])) > max_lens[key]:
                # overwrite current max value for a given key
                max_lens[key] = len(str(dict[key]))
            # increase max sum by the current key
            # (if changed, will apply new max for that key, if not, will return to same value)
            max_lens_sum += max_lens[key]

    # print opening table line based on sample dict
    opening_header_line = "+"
    for key in active_processes[0]:
        opening_header_line += ((max_lens[key] + 2) * "-" + "+")
    print(opening_header_line)

    # print headers based on sample dict
    headers = "|"
    for key in active_processes[0]:
        headers = headers + (" {0}" + (max_lens[key] - len(str(key)) + 1) * " " + "|").format(key)
    print(headers)
    # print("| PID" + (max_lens["pid"]-2)*" " + "| Name" + (max_lens["name"] - 3)*" " + "|")

    # print table header row break
    header_row_break = "+"
    for key in active_processes[0]:
        header_row_break += ((max_lens[key]+2)*"=" + "+")
    print(header_row_break)

    # print processes
    for active_proc in active_processes:
        # initialize the row
        row = "|"

        # create cells for each key
        for key in active_proc:
            value = active_proc[key]
            row = row + (" {0}" + (max_lens[key]-len(str(active_proc[key]))+1)*" " + "|").format(value)

        # print row
        print(row)

        # print row break
        print((max_lens_sum + len(active_proc.keys()) * 3 + 1) * "-")

    # print total number of processes
    print("Total: {0}".format(len(active_processes)))


# kills all active processes
def kill_processes(active_processes):
    for process in active_processes:
        try:
            (psutil.Process(process["pid"])).kill()
        except BaseException as e:
            print("Could not kill {0}".format(process["name"]))


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
                                    "name": process.name(),
                                    "create_time": datetime.datetime.fromtimestamp(process.create_time()).strftime("%Y-%m-%d %H:%M:%S")
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
            try:
                os.remove(selected_file_path)
                print("File deleted successfully")
            except BaseException as e:
                print("Error occurred while attempting to delete the file")
