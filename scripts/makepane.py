print('test')
f = open("test", "a")
f.write('test')
f.flush()
f.close()
import libtmux
server = libtmux.Server()
pane = server.list_sessions()[0].list_windows()[0].list_panes()[0].split_window()
