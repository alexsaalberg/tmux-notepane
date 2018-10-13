import libtmux
from subprocess import check_output, CalledProcessError

def get_current_session():
	session_as_bytes = check_output(['tmux', 'display-message', '-p', '"#S"'])
	session_as_str = session_as_bytes.decode()
	return int(session_as_str[1:-2]) #get rid of "#"/n

def get_id_from_pane(pane):
	#pid_as_str = pane.cmd('display-message', '-p', '-F', '#{pane-id}').stdout
	return pane._pane_id

def get_program_from_pid(pid):
	program_as_bytes = check_output(['ps', '-p '+pid, '-o comm='])
	program_as_str = program_as_bytes.decode()
	return program_as_str[:-1] #get rid of /n

def get_leaf_pid(root_pid):
	try:
		child_pid_bytes = check_output(['pgrep', '-P', root_pid])
		child_pid = child_pid_bytes[:-1].decode()
		return get_leaf_pid(child_pid)
	except CalledProcessError:
		return root_pid

def get_pid_from_id(session, pane_id):
	pane_id_list = session.cmd('list-panes', '-F', '#{pane_id}').stdout
	pane_pid_list = session.cmd('list-panes', '-F', '#{pane_pid}').stdout
	#pane_tty_list = session.cmd('list-panes', '-F', '#{pane_tty}').stdout
	#child_pid_list = list(map(get_leaf_pid, pane_pid_list))
	pane_index = pane_id_list.index(pane_id)
	return get_leaf_pid(pane_pid_list[pane_index])


server = libtmux.Server()

session_num = get_current_session()
session = server.list_sessions()[session_num]

active_pane = session.attached_pane
active_pane_id = get_id_from_pane(active_pane)

active_pane_pid = get_pid_from_id(session, active_pane_id)
active_program_name = get_program_from_pid(active_pane_pid)

note_pane = active_pane.split_window(vertical=False)
note_dir = "~/.note/"
note_pane.send_keys("tldr "+active_program_name+" | less -r")
note_pane.send_keys("i", enter=False)
#print(active_pane_pid + ':' + active_program_name)
