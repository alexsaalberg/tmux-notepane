import os
import sys
import libtmux
import subprocess
from subprocess import call, check_output, CalledProcessError

option_prefix = "notepane-"

#tmux options
def set_tmux_option(option, value):
	call(["tmux", "set-option", "-g", option, value])

def set_tmux_user_option(option, value):
	set_tmux_option("@" + option_prefix + option, value)

def get_tmux_option(option):
	try:
		result = check_output(["tmux", "show-option", "-q", "-g", option])
		if len(result) == 0:
			return ''
		tokens = result.decode()[:-1].split(' ') #remove \n split into option and value
		#tmux show-option @asdf
		#returns (if result is 1
		#@asdf "1"
		return tokens[1][1:-1] #remove ""
	except CalledProcessError: #option does not exist, return default of ""
		return ""

def get_tmux_user_option(option):
	return get_tmux_option("@" + option_prefix + option)

def get_id_from_pane(pane):
	#if type(pane) is libtmux.pane.Pane:
	return pane._pane_id
	#return '00'

def designate_panes(mainpane, notepane):
	mainpane_id = get_id_from_pane(mainpane)
	notepane_id = get_id_from_pane(notepane)
	set_tmux_user_option(notepane_id+"isNotepaneOf", mainpane_id)
	set_tmux_user_option(mainpane_id+"isMainpaneOf", notepane_id)

def undesignate_panes(mainpane, notepane):
	mainpane_id = get_id_from_pane(mainpane)
	notepane_id = get_id_from_pane(notepane)
	undesignate_panes_from_ids(mainpane_id, notepane_id)

def undesignate_panes_from_ids(mainpane_id, notepane_id):
	set_tmux_user_option(notepane_id+"isNotepaneOf", "")
	set_tmux_user_option(mainpane_id+"isMainpaneOf", "")


def is_notepane(pane):
	pane_id = get_id_from_pane(pane)
	return len(get_tmux_user_option(pane_id+"isNotepaneOf")) > 0

def has_notepane(pane):
	pane_id = get_id_from_pane(pane)
	notepane_id = get_tmux_user_option(pane_id+"isMainpaneOf")
	if len(notepane_id) == 0:
		return False
	if not pane_exists(notepane_id):
		undesignate_panes_from_ids(pane_id, notepane_id)
		return False
	return True

def create_notepane(pane):	
	note_pane = pane.split_window(vertical=False, attach=False)
	note_pane.send_keys("tldr vim")
	designate_panes(pane, note_pane)

def remove_notepane(pane):
	pane.cmd('kill-pane')

def get_notepane_from_mainpane(pane):
	return get_pane_from_id(get_tmux_user_option(pane_id+"isMainpaneOf"))

def get_mainpane_from_notepane(pane):
	return get_pane_from_id(get_tmux_user_option(pane_id+"isNotepaneOf"))

def get_pane_from_ids(s, w, p):
	return libtmux.Server().get_by_id(s).get_by_id(w).get_by_id(p)

def toggle_notepane(pane):
	if has_notepane(pane):
		notepane = get_notepane_from_mainpane(pane)
		undesignate_panes(pane, notepane)
		remove_notepane(notepane)
	else:
		create_notepane(pane)

def get_pane_from_id(pane_id):
	ids_as_bytes = check_output(['tmux', 'display-message', '-t', pane_id, '-p', '#{session_id} #{window_id}'], stderr=subprocess.STDOUT)
	ids_as_str = ids_as_bytes[:-1].decode()
	ids = ids_as_str.split(' ')
	session_id = ids[0]
	window_id = ids[1]
	return get_pane_from_ids(session_id, window_id, pane_id)

def pane_exists(pane_id):
	try: 
		get_pane_from_id(pane_id)
	except:
		#e = sys.exc_info()[0]
		return False
	return True

argv = sys.argv
pane_id = argv[1]
pane = get_pane_from_id(pane_id)

if is_notepane(pane):
	toggle_notepane(get_mainpane_from_notepane(pane))
else:
	toggle_notepane(pane)

sys.exit(0)
