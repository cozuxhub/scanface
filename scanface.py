# Let's add the necessary libraries.
import subprocess
import readline
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

# If the users presses TAB while specifying a directory, these are the codes required for autocompletion.
readline.set_completer_delims(' \t\n=')
readline.parse_and_bind("tab: complete")

# Let's start the tool.
print(Fore.MAGENTA + Style.BRIGHT + "================================================================\n"
                                    "Welcome to the scanface v1.0"
                                    "\ncreated by Ali İrfan Doğan (@cozux) "
                                    "\n================================================================")
confirm = str(input("Please confirm that you will only use this app for CTF solving. I agree yes/no: "))
if confirm.lower() == "yes":
    print("\nFirst, let's do an easy scan on the IP address given to us.")
    # Let's request the variables from the user.
    ip_address = input("What is the target IP address?: ")
    result_destination = input("In which folder should the results be saved? (e.g:/opt/cozscanner): ")
    result_file = input(
        "What should be the file name where we will save the scan? (If there is a filename with that name, scanning will not be performed.) (e.g:cozscan.txt): ")


    # Let's scan the ports with nmap and save a .txt file to the destination entered by the user.
    def nmap_scanning():
        print(Fore.RED + Style.BRIGHT + "\n================================================================\n--  "
                                        "Scanning... Please wait...  "
                                        "--\n================================================================")
        subprocess.call(["nmap", "-sV", "-A", "-p-", "-sS", "-oN", result_destination + "/" + result_file, ip_address])
        print(Fore.GREEN + Style.BRIGHT + "\n================================================================\n--  "
                                          "Scanning is completed! Check out the results  "
                                          "--\n================================================================")


    # If any web server is running, let's check with GoBuster to see if there are hidden destinations.
    def gobuster_scanning():
        # This variable we see has been placed for optional re-scanning.
        gobuster_scans = 0

        def scan_destination(path):
            print(Fore.RED + Style.BRIGHT + "\n===============================================================\n--  "
                                            "Scanning... Please wait...  "
                                            "--\n===============================================================")
            subprocess.call(["gobuster", "dir", "-u", "http://" + ip_address, "-w", path])
            print(Fore.GREEN + Style.BRIGHT + "\n===============================================================\n--  "
                                              "Scanning is completed! Check out the results  "
                                              "--\n===============================================================")

        input("Have you entered the target IP address through the browser and examined it? If you looked and didn't "
              "find anything press enter to continue in theoretically...")
        print(
            Fore.YELLOW + Style.BRIGHT + "\n1) directory-list-1.0.txt\n2) directory-list-2.3-small.txt\n3) directory-list-2.3-medium.txt\n4) "
                                         "directory-list-lowercase-2.3-small.txt\n5) directory-list-lowercase-2.3-medium.txt")

        while True:
            # The user chooses which wordlist to scan. If the number is not entered, it asks the user to make the selection again instead of giving an error.
            try:
                chosen_directory = int(input(
                    "On the web server of the destination IP address, which directory list do you want to scan with?: "))
                if chosen_directory == 1:
                    scan_destination("/usr/share/wordlists/dirbuster/directory-list-1.0.txt")
                elif chosen_directory == 2:
                    scan_destination("/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt")
                elif chosen_directory == 3:
                    scan_destination("/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt")
                elif chosen_directory == 4:
                    scan_destination("/usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt")
                elif chosen_directory == 5:
                    scan_destination("/usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt")
            except:
                print(Fore.RED + Style.BRIGHT + "\nPlease enter a number between 1-5!")
                continue
            else:
                break

        while True:
            # The user enters this loop to also scan directories found after the initial scan.
            gobuster_scans += 1
            if gobuster_scans >= 1:
                new_scan = input("Do you want to add a destination on the IP Address and scan again? yes/no: ")
                if new_scan.lower() == "yes":
                    gb_destination = input("Please write the destination to be added to the IP Address. e.g: /images: ")
                    print(
                        Fore.RED + Style.BRIGHT + "\n===============================================================\n##  "
                                                  "Scanning... Please wait...  "
                                                  "##\n===============================================================")
                    subprocess.call(["gobuster", "dir", "-u", "http://" + ip_address + gb_destination, "-w",
                                     "/usr/share/wordlists/dirbuster/directory-list-1.0.txt"])
                    print(
                        Fore.GREEN + Style.BRIGHT + "\n===============================================================\n##  "
                                                    "Scanning is completed! Check out the results  "
                                                    "##\n===============================================================")
                    gobuster_scans += 1
                    continue
                else:
                    break


    # Let's do a different scanning method with Nikto.
    def nikto():
        input("Let's also see if there is any pHp login page. Press enter to continue...")
        print(Fore.RED + Style.BRIGHT + "\n================================================================\n##  "
                                        "Scanning... Please wait...  "
                                        "##\n================================================================")
        subprocess.call(["nikto", "-h", ip_address])
        print(Fore.GREEN + Style.BRIGHT + "\n================================================================\n##  "
                                          "Scanning is completed! Check out the results  "
                                          "##\n================================================================")


    nmap_scanning()
    input(
        "If you have viewed it, press enter to continue... (To review the nMap results, check out your save location)")
    gobuster_scanning()
    nikto()
    print(Fore.MAGENTA + Style.BRIGHT + "================================================================\n"
                                        "We'll see you again"
                                        "\ncreated by Ali İrfan Doğan (@cozux) "
                                        "\n================================================================")

    # I would like to thank @yemregol for helping me solve some problems I was experiencing.
else:
    exit()
