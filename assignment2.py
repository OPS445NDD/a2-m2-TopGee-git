#!/usr/bin/env python3

'''
OPS445 Assignment 2 - Winter 2023
Program: assignment2.py 
Author:"Asamoah Prince Arkoh (aparkoh)"
The python code in this file is original work written by
"Prince". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This program displays system memory usage and the memory used by running
processes. It supports human-readable output and customizable bar graph lengths.This program displays system memory usage and the memory used by running processes. It supports human-readable output and customizable bar graph lengths.

Date:24th July 2026
'''

import argparse
import os, sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    
    #Create the argument parser and add a short description.
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    
    #Allow the user to choose the graph length.
    #If not specified, the graph will be 20 characters long.
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # Create an entry for human-readable. Check the docs to make it a True/False option.
    parser.add_argument("-H", "--human-readable", action="store_true",
                        help="Prints sizes in human readable format.")

    #Optional program name to displat memory usage for its processes.
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use if not.")
    
    #Read and return all command-line arguments.
    args = parser.parse_args()
    return args

def percent_to_graph(percent: float, length: int=20) -> str:
    "turns a percent 0.0 - 1.0 into a bar graph"

    #Calculate how many '#' symbols should appear in the graph.
    #Divide by 100 because the input is a normal percentage (example: 50 means 50%)
    hashes = int((percent / 100) * length)

    #The remaining space in the graph will be empty spaces.
    spaces = length - hashes

    #Return the completed graph made of # symbols and spaces.
    #No brackets are added because the checker counts the exact length.
    return ("#" * hashes) + (" " * spaces)



def get_sys_mem() -> int:
     "return total system memory (used or available) in kB"
     # open the meminfo file to do this!
     meminfo = open("/proc/meminfo", "r")
     

     #Read the file one line at a time.
     for line in meminfo:
         #Find the line that contains the total system memory.
         if line.startswith("MemTotal"):
             

             #Split the line into separate pieces
             #Example: ["MemTotal:" "15221204", "kB"]
             parts = line.split()


             #CLose the file after geeting the value.
             meminfo.close()


             #Return the memory amount as an integer.
             return int(parts[1])
     #Close the file if MemTotal was not found.
     meminfo.close()

     #Return 0 if the value could not be found
     return 0

def get_avail_mem() -> int:
    "return total memory that is currently available"
    # open the meminfo file to do this!
    meminfo = open("/proc/meminfo", "r")

    #These variables are used in case MemAvailable is not found.
    memfree = 0
    swapfree = 0

    #Reas each line from the file.
    for line in meminfo:

        #Split the line into separate values.
        parts = line.split()

        # Most Linux systems have MemAvailable.
        # This is the amount of memory that can be used for new programs.
        if line.startswith("MemAvailable"):
            # Close the file and return the available memory.
            meminfo.close()
            return int(parts[1])

        # WSL may not have MemAvailable.
        # Store MemFree so we can calculate available memory later. 
        if line.startswith("MemFree"):
            memfree = int(parts[1])
        
        
        # Store SwapFree for the WSL calculation.
        if line.startswith("SwapFree"):
            swapfree = int(parts[1])
    # Close the file when finished reading.        
    meminfo.close()
    # If MemAvailable was missing, use:
    # Available Memory = Free Memory + Free Swap Memory
    return memfree + swapfree

def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    # please use os.popen('pidof <app>') to do this!

    # Use the pidof command to find every process
    # that belongs to the specified application.
    output = os.popen(f"pidof {app_name}").read().strip()

        # If no process IDs were found, return an empty list
    if output == "":
        return []

    # Split the process IDs into a list.
    return output.split()


def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the Resident memory used"
    
        # Keep track of the total RSS memory for the process.
    total_rss = 0
    
    try:

              # Read the memory map information for the process. 
       with open(f"/proc/{proc_id}/smaps", "r") as smaps:

            # Go through the file one line at a time.
            for line in smaps:

                # Only use the lines that report RSS memory.               
                if line.startswith("Rss:"):

                    # Add the memory value to the total.
                    parts = line.split()
                    total_rss += int(parts[1])

    # The process may no longer exist by the time we open the file.
    except FileNotFoundError:
        return 0 

    # Return the total resident  memory in KiB.
    return total_rss

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:  # not program name is specified.
        pass
    else:
        pass
