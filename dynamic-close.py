#!/usr/bin/python2
 
import pywingo
import time
 
# Minimum Number of Workspaces (Prevents Uneccessary Errors)
minWorkspaces = 1
 
def main():
 
    # Open Wingo socket
    w = pywingo.Wingo()
 
    # Close Active Client
    w.gribble ('Close (GetActive)')
 
    # Get a list of all available workspaces
    workspaceList = w.gribble('GetWorkspaceList').split()
 
    # Get a list of all clients in visible workspace
    clientList = w.gribble('GetClientList (GetWorkspace)').split()
 
 
    # If only one client was present upon closing
    # and there is more workspaces the minimum allowed,
    # then remove the current workspace
    if len(clientList) == 1 and len(workspaceList) >= minWorkspaces:
        time.sleep(0.1) # NOTE: delay is necessary...why?
        w.gribble('RemoveWorkspace (GetWorkspace)')
 
if __name__ == '__main__':
    main()
