# Remote SSH/tmux macOS clipboard relay

When Claude Code runs on a remote Linux host over SSH, the normal Linux
clipboard (`xclip`) belongs to the remote host, not your local Mac. In tmux,
terminal-copy approaches such as OSC52 can also be unreliable because Claude
Code captures hook stdout/stderr before it reaches the attached terminal.

For that setup, use an optional local relay:

1. On macOS, create a shared token:

   ```bash
   openssl rand -base64 32 > ~/.copy-claude-response-relay-token
   chmod 600 ~/.copy-claude-response-relay-token
   ```

2. Start the local relay:

   ```bash
   python3 examples/macos-clipboard-relay.py \
     --token-file ~/.copy-claude-response-relay-token
   ```

3. Add an SSH reverse forward for the remote host:

   ```sshconfig
   Host my-remote
     RemoteForward 127.0.0.1:49352 127.0.0.1:49352
   ```

4. Copy the same token file to the remote host, then configure the hook
   environment:

   ```bash
   export COPY_CLAUDE_CLIPBOARD_RELAY=127.0.0.1:49352
   export COPY_CLAUDE_CLIPBOARD_RELAY_TOKEN_FILE=~/.copy-claude-response-relay-token
   ```

With those variables set, `/c` sends the selected Claude response through the
SSH reverse-forwarded relay first. If the relay is unavailable, the script falls
back to the existing platform clipboard commands.

The relay listens on `127.0.0.1` only and requires the shared token before it
will call `pbcopy`.
