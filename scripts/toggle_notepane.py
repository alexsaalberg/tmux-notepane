import os
import sys
import libtmux
import subprocess
from subprocess import call, check_output, CalledProcessError

option_prefix = "notepane-"

debug = False

def log(s):
	if debug:
		print(s)

#tmux options helper function
def set_tmux_option(option, value):
	call(["tmux", "set-option", "-g", option, value])

def unset_tmux_option(option):
	call(["tmux", "set-option", "-g", "-u", option])

def set_tmux_user_option(option, value):
	set_tmux_option("@" + option_prefix + option, value)

def unset_tmux_user_option(option):
	unset_tmux_option("@" + option_prefix + option)

def get_tmux_option(option):
	result = check_output(["tmux", "show-option", "-q", "-g", option])
	if len(result) == 0: #option not set, return default of ''
		return ''
	tokens = result.decode()[:-1].split(' ') #remove \n, split into option and value
	#'tmux show-option @asdf' will return (if value is 1) '@asdf "1"'
	value = tokens[1][1:-1] #remove ""
	log("get_tmux_option("+option+"): "+value)
	return value 

def get_tmux_user_option(option):
	return get_tmux_option("@" + option_prefix + option)

#notepane specific tmux option helper functions
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
	unset_tmux_user_option(notepane_id+"isNotepaneOf")
	unset_tmux_user_option(mainpane_id+"isMainpaneOf")

def is_notepane(pane):
	pane_id = get_id_from_pane(pane)
	return len(get_tmux_user_option(pane_id+"isNotepaneOf")) > 0

def has_notepane(pane):
	pane_id = get_id_from_pane(pane)
	notepane_id = get_tmux_user_option(pane_id+"isMainpaneOf")
	log("has_notepane() notepane_id:"+notepane_id)
	if len(notepane_id) == 0:
		return False
	if not pane_exists(notepane_id):
		undesignate_panes_from_ids(pane_id, notepane_id)
		return False
	return True

#pid, program, and pane_id stuff
def get_id_from_pane(pane):
	return pane._pane_id

def get_pid(pane):
	pane_pid = pane.cmd('display-message', '-p', '#{pane_pid}').stdout[0]
	return pane_pid

def get_pane_from_ids(s, w, p):
	return libtmux.Server().get_by_id(s).get_by_id(w).get_by_id(p)

def get_pane_from_id(pane_id):
	ids_as_bytes = check_output(['tmux', 'display-message', '-t', pane_id, '-p', '#{session_id} #{window_id}'], stderr=subprocess.STDOUT)
	ids_as_str = ids_as_bytes[:-1].decode()
	ids = ids_as_str.split(' ')
	session_id = ids[0]
	window_id = ids[1]
	return get_pane_from_ids(session_id, window_id, pane_id)

def get_program_from_pid(pid):
	program_as_bytes = check_output(['ps', '-p '+pid, '-o comm='])
	program_as_str = program_as_bytes.decode()
	return program_as_str[:-1] #get rid of /n

def get_clean_program(prog):
	if prog == '-bash':
		return 'bash'
	return prog

def get_leaf_pid(root_pid):
	try:
		child_pid_bytes = check_output(['pgrep', '-P', root_pid])
		child_pid = child_pid_bytes[:-1].decode() #[:-1]: get ride of \n
		return get_leaf_pid(child_pid)
	except CalledProcessError:
		return root_pid

def pane_exists(pane_id):
	try:
		#get_pane_from_id(pane_id)
		output_as_bytes = check_output(['tmux', 'display-message', '-t', pane_id, '-p'])
		output_as_str = output_as_bytes[:-1].decode()
		log("pane_exists: "+output_as_str)
		#get_pane_from_id(pane_id)
	except:
		e = sys.exc_info()[0]
		log(e)
		log("pane"+pane_id+" does NOT exist!")
		return False
	log("pane"+pane_id+" exists")
	return True

def get_active_pane():
	ids_as_bytes = check_output(['tmux', 'display-message', '-p', '#{session_id} #{window_id} #{pane_id}'], stderr=subprocess.STDOUT)
	ids_as_str = ids_as_bytes[:-1].decode()
	ids = ids_as_str.split(' ')
	session_id = ids[0]
	window_id = ids[1]
	pane_id = ids[2]
	return get_pane_from_ids(session_id, window_id, pane_id)

#notepane core stuff
def get_clean_active_program(pane):
	leaf_pid = get_leaf_pid(get_pid(pane))
	mainpane_prog = get_clean_program(get_program_from_pid(leaf_pid))
	return mainpane_prog

def make_note_dir():
	try:
		dir_path = os.path.expanduser('~/.note')
		os.mkdir(dir_path)
	except:
		log("~/.note already exists")
		#do nothing

def launch_note_program(notepane, mainpane):
	mainpane_prog = get_clean_active_program(mainpane)
	make_note_dir()
	notepane.send_keys("vim ~/.note/"+mainpane_prog+".note")

def launch_man(notepane, mainpane):
	mainpane_prog = get_clean_active_program(mainpane)
	notepane.send_keys("man "+mainpane_prog)

def create_notepane(pane):	
	notepane = pane.split_window(vertical=False, attach=False)
	launch_note_program(notepane, pane)
	designate_panes(pane, notepane)

def get_notepane_from_mainpane(pane):
	return get_pane_from_id(get_tmux_user_option(get_id_from_pane(pane)+"isMainpaneOf"))

def get_mainpane_from_notepane(pane):
	try:
		return get_pane_from_id(get_tmux_user_option(get_id_from_pane(pane)+"isNotepaneOf"))
	except:
		return pane

def remove_notepane(notepane):
	notepane.send_keys(str(chr(27)), enter=False) #send esc
	notepane.send_keys(":w") #save
	notepane.cmd('kill-pane')

def toggle_notepane(pane):
	log("Toggling mainpane"+get_id_from_pane(pane))
	if has_notepane(pane):
		notepane = get_notepane_from_mainpane(pane)
		undesignate_panes(pane, notepane)
		remove_notepane(notepane)
	else:
		log("mainpane has no notepane")
		create_notepane(pane)


pane = get_active_pane()

if is_notepane(pane):
	log("Active pane"+get_id_from_pane(pane)+" is a notepane")
	toggle_notepane(get_mainpane_from_notepane(pane))
else:
	toggle_notepane(pane)

sys.exit(0)
