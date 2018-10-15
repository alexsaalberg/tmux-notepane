import libtmux

def get_pane_from_ids(session_id, window_id, pane_id):
	server = libtmux.Server()
	session = server.get_by_id(session_id)
	window = session.get_by_id(window_id)
	return window.get_by_id(pane_id)
	

