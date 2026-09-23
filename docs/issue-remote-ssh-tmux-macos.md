# Issue draft: Support remote SSH/tmux Claude Code sessions on macOS via clipboard relay

Hi! Thanks for maintaining this tool. I tested it in a remote Claude Code setup
and found a clipboard edge case that may be worth supporting or documenting.

## Environment

- Local machine: macOS
- Remote machine: Linux
- Claude Code runs on the remote machine over SSH
- Claude Code is inside tmux
- Hook command `/c` is registered and triggered successfully
- The hook can parse the transcript and returns success

## Problem

When running `/c`, Claude Code shows the success message:

```text
✅ 最新回复已复制 Latest response copied!
```

But the copied content does not appear in the local macOS clipboard.

## What I found

The issue seems to be that the hook process runs under Claude Code, and Claude
captures stdout/stderr from the hook. Because of that, clipboard approaches
based on terminal escape output, such as OSC52, do not reliably reach the actual
local terminal.

I also tried tmux clipboard integration:

```bash
tmux set-buffer -w ...
```

This updated the tmux buffer, but did not update the local macOS system
clipboard in this SSH/tmux setup.

## Working workaround

The reliable solution was to use an SSH reverse-forwarded clipboard relay:

1. Run a small clipboard server on macOS, listening only on `127.0.0.1`.
2. The server validates a shared token and calls `pbcopy`.
3. Add an SSH reverse forward:

   ```sshconfig
   Host my-remote
     RemoteForward 127.0.0.1:49352 127.0.0.1:49352
   ```

4. In the remote hook script, send the selected Claude response to
   `127.0.0.1:49352`.
5. The local macOS server receives the text and writes it to the actual macOS
   clipboard.

This made `/c` work end-to-end in a remote SSH + tmux Claude Code session.

## Feature request

Would you be open to adding a documented "remote macOS clipboard relay" mode?

Possible behavior:

- If `COPY_CLAUDE_CLIPBOARD_RELAY=127.0.0.1:49352` is set, send copied text to
  that relay first.
- Fall back to OSC52 / pbcopy / xclip / clip.exe if relay is unavailable.
- Include a small optional macOS relay script and SSH config example.
- Use a token file for basic local authorization.

I have a small proof-of-concept patch prepared if this direction sounds
reasonable.
