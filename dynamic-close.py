#!/usr/bin/python2

import pywingo

x = pywingo.Wingo()

#Alright hopefully this makes an array lmao

workspaceList = x.gribble('GetWorkspaceList')

#split function

workspaces = workspaceList.split()

#Kill Function

for workspace in workspaces:
	result = x.gribble('GetClientList "%s"' % workspace)
	if not result:
		if workspace != 'trm':
			x.gribble('RemoveWorkspace "%s"' % workspace)