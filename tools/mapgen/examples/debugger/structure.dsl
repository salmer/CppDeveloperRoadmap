# Debugger cluster — multi-child tree + pink hint callouts with curved arrows
# to several targets. `hint [id] -> t1, t2, ...` is a floating annotation.

[debugger] grade=junior
  [dbg_knowledge] grade=junior
  [dbg_messages]  grade=junior
  [dbg_symbols]   grade=junior
  [windbg] grade=optional
  [gdb]    grade=optional
  [lldb]   grade=optional

hint [h_errors]  -> dbg_messages
hint [h_cmdline] -> windbg, gdb, lldb
