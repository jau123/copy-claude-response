# Claude Code Response Copier

<div align="center">

### 🇨🇳 [**中文文档 Chinese Documentation**](README.zh-CN.md) 🇨🇳

</div>

> 🍎 **macOS Enhanced Version** with full cross-platform support
>
> Based on [Twizzes/copy-claude-response](https://github.com/Twizzes/copy-claude-response) · [Pull Request #2](https://github.com/Twizzes/copy-claude-response/pull/2) pending

A Claude Code hook that adds `/c`, `/copy`, and `/copy-response` commands to quickly copy Claude's responses to your clipboard.

![Demo](img/demo.gif)

## Features

- 📋 **Quick Copy**: `/c` copies the latest response (also supports `/copy` and `/copy-response`)
- 🔢 **Numbered Access**: `/c 3` copies a specific response
- 📝 **List Responses**: `/c list` shows available responses with previews
- 🔍 **Search Responses**: `/c find "keyword"` finds responses containing text
- ⏰ **Timestamps**: Shows when each response was created
- 🖥️ **Cross-Platform**: Works on macOS, Linux, and Windows/WSL
- ⚡ **Short Alias**: Use `/c` for fastest access

## Installation

### Prerequisites

**All Platforms:**
- Bash 4.0+ (for associative arrays)
- `jq` for JSON parsing
- Platform-specific clipboard utility

**macOS:**
```bash
# Install Bash 5.0+ (macOS default is 3.2)
brew install bash

# Install coreutils (provides gtac)
brew install coreutils

# Install jq
brew install jq
```

**Linux:**
```bash
# Install xclip (for clipboard) and jq
sudo apt install xclip jq

# Or for RPM-based systems
sudo yum install xclip jq
```

**Windows/WSL:**
```bash
# Install jq (clip.exe is built-in)
sudo apt install jq
```

### Setup Steps

1. **Download the script:**

   ```bash
   curl -o copy-claude-response https://raw.githubusercontent.com/jau123/copy-claude-response/main/copy-claude-response
   chmod +x copy-claude-response
   ```

2. **Place it somewhere in your PATH** (or note the full path):

   ```bash
   mv copy-claude-response ~/.local/bin/
   ```

3. **Configure the hook** in your Claude Code settings (`~/.claude/settings.json`):

   ```json
   {
     "hooks": {
       "UserPromptSubmit": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "~/.local/bin/copy-claude-response"
             }
           ]
         }
       ]
     }
   }
   ```

4. **Create a slash command definition** (fixes "Unknown slash command" error):

   Create file: `~/.claude/commands/c.md`

   ```markdown
   Copy Claude's responses to clipboard.

   Usage:
   - /c - copy latest response
   - /c 2 - copy response #2
   - /c list - list recent responses
   - /c find "keyword" - search responses
   ```

   This enables Claude Code to recognize the `/c` command and trigger the hook.

5. **Restart Claude Code**

## Usage

### Basic Commands

| Command | Description |
|---------|-------------|
| `/c` | Copy the latest Claude response |
| `/c 2` | Copy response #2 |
| `/c list` | List last 10 responses with previews |
| `/c list 5` | List last 5 responses |
| `/c find "error"` | Find responses containing "error" |

> **Note:** Also supports longer forms `/copy` and `/copy-response`

### Examples

**Copy latest response:**

```
/c
```

> ✅ 最新回复已复制 Latest response copied!

**List recent responses:**

```
/c list
```

```
Available responses (1-3):
    3 [ 2.1 min ago]: Here's the updated function with error handling...
    2 [15.3 min ago]: I'll help you debug this issue. First, let's check...
    1 [ 1.2 hrs ago]: To implement this feature, we need to modify...
```

**Search for specific content:**

```
/c find "git commit"
```

```
Searching for "git commit":
    2 [15.3 min ago]: I'll help you debug this issue. First, let's check...
    5 [ 2.1 hrs ago]: You can create a git commit using the following...
Found 2 matching responses
```

## How It Works

The script:

1. **Intercepts** `/c` (or `/copy`, `/copy-response`) commands before Claude processes them
2. **Parses** the conversation transcript to extract Claude's responses
3. **Groups** multi-part responses by request ID for complete responses
4. **Copies** the selected response to your system clipboard
5. **Blocks** the command from reaching Claude to prevent confusion

## Platform Support

- **macOS**: Uses `pbcopy`
- **Linux**: Uses `xclip` (install with `sudo apt install xclip`)
- **Windows/WSL**: Uses `clip.exe` via PowerShell for proper UTF-8 handling

## Troubleshooting

**"Unknown slash command: c" error?**

- Create the slash command definition file: `~/.claude/commands/c.md` (see step 4 in Installation)
- Restart Claude Code

**Hook not working?**

- Run `/hooks` in Claude Code to verify the hook is registered
- Check that the script path is correct and executable: `ls -l ~/.local/bin/copy-claude-response`
- Use `claude --debug` to see hook execution details

**"Error: This script requires Bash 4.0 or higher" (macOS)?**

```bash
# Install Bash 5.0+
brew install bash

# Option 1: Update PATH so new bash is found first
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Option 2: Update script shebang to use specific bash
# Edit first line to: #!/opt/homebrew/bin/bash
```

**"Error: Neither 'tac' nor 'gtac' command found" (macOS)?**

```bash
brew install coreutils
```

**Clipboard not working?**

- **Linux**: Install xclip: `sudo apt install xclip`
- **WSL**: Ensure Windows clipboard integration is enabled
- **macOS**: pbcopy should work by default
- **Remote SSH/tmux to macOS**: see
  [Remote SSH/tmux macOS clipboard relay](docs/remote-ssh-tmux-macos.md)
  for an optional SSH reverse-forwarded `pbcopy` relay.

**No responses found?**

- The script only finds text responses from Claude
- Responses with only tool calls won't appear in the list

**Hook not triggering?**

- Ensure the slash command file exists at `~/.claude/commands/c.md`
- The hook intercepts the command BEFORE Claude processes it
- Check hook registration with `/hooks` command

## Limitations

- Only copies text responses from Claude (responses with only tool calls won't appear)
- The slash command WILL NOT AUTO-COMPLETE (this is because we hook UserPromptSubmit, which existing slash commands don't trigger)
- Requires `jq` for JSON parsing
- Platform-specific clipboard utilities must be installed

## Requirements

- Claude Code with hooks support
- Bash 4.0+ (for associative arrays)
  - macOS: Install via `brew install bash`
  - Linux/WSL: Usually pre-installed
- `jq` for JSON parsing
  - macOS: `brew install jq`
  - Linux: `sudo apt install jq`
- Platform-specific clipboard utility:
  - macOS: `pbcopy` (built-in)
  - Linux: `xclip` (`sudo apt install xclip`)
  - Windows/WSL: `clip.exe` (built-in)
- GNU coreutils (macOS only):
  - `brew install coreutils` (provides `gtac`)

## Contributing

Found a bug or have a feature request? Please open an issue or submit a pull request!

## Credits

Original project by [Twizzes](https://github.com/Twizzes/copy-claude-response).

This fork adds:
- Full macOS compatibility (Bash 4.0+ detection, tac/gtac auto-detection, BSD date support)
- `/c` shortcut command
- Chinese documentation
- Enhanced error messages and troubleshooting guide

## License

Apache License 2.0 - feel free to modify and share!
