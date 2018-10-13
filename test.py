import libtmux
from subprocess import check_output

def get_current_session():
	session_as_bytes = check_output(['tmux', 'display-message', '-p', '"#S"'])
	session_as_str = session_as_bytes.decode()
	return int(session_as_str[1:-2]) #get rid of "#"/n

def get_id_from_pane(pane):
	pid_as_str = pane.cmd('display-message', '-p', '-F', '#{pane-id}').stdout
	return int(pid_as_str[0])

def get_pid_from_id(pane_id):
	#manual way because using pane.cmd(pane-id) won't work
	pid_as_bytes = check_output(['tmux', 'display-message', '-t', str(pane_id), '-p', '-F', '#pane-id}'])
	print(pid_as_bytes)

def get_program_from_pid(pid):
	program_as_bytes = check_output(['ps', '-p '+pid, '-o comm='])
	program_as_str = program_as_bytes.decode()
	return program_as_str[1:-1] #get rid of - in front and /n at end

server = libtmux.Server()
sessions = server.list_sessions()

session_num = get_current_session()
print("snum", end='')
print(session_num)
session = sessions[session_num]
active_pane = sessions[session_num].attached_pane
active_pane_id = get_id_from_pane(active_pane)
get_pid_from_id(active_pane_id)
'''
pane_pid_list = session.cmd("list-panes", '-F', '#{pane_pid}').stdout
pane_id_list = session.cmd("list-panes", '-F', '#{pane_id}').stdout
print(pane_pid_list)
print(pane_id_list)

pane_pid = pane_pid_list[0]
print(pane_pid)

print( get_program_from_pid(pane_pid) )
print(get_current_session() )

pane_pid = get_pane_pid(pane)
print(type(pane_pid))
print(pane_pid.encode())
print(int(pane_pid))
if(len(pane_pid) > 0):
	print(get_program_from_pid(pane_pid))
'''
