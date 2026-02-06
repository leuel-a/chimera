# CodeRabbit Setup Guide

CodeRabbit provides AI-powered code reviews both as a GitHub App (cloud) and via CLI (local development).

## Option 1: GitHub App (Cloud-Based)

CodeRabbit automatically reviews pull requests when installed as a GitHub App. No local setup required.

### Installation Steps

1. **Install CodeRabbit GitHub App:**

   - Visit https://coderabbit.ai
   - Click "Install CodeRabbit"
   - Select your repository or organization
   - Grant necessary permissions

2. **Configuration:**
   - The repository includes `.coderabbit.yaml` for custom settings
   - CodeRabbit will automatically review PRs after installation

## Option 2: Local CLI Development

For local development, you can use CodeRabbit CLI to review uncommitted changes before pushing.

### Prerequisites

- Shell access (bash/zsh)
- Internet connection (for authentication)

### Installation

**Linux/macOS/WSL:**

```bash
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
```

**After installation:**

1. Restart your shell or reload configuration:

   ```bash
   source ~/.bashrc  # or ~/.zshrc
   ```

2. Verify installation:
   ```bash
   coderabbit --version
   ```

### Authentication

**For cloud CodeRabbit:**

```bash
coderabbit auth login
```

Follow the prompts to authenticate via browser.

**For self-hosted CodeRabbit:**

```bash
coderabbit auth login --self-hosted
```

Provide your self-hosted CodeRabbit URL and access token.

### Usage

**Review uncommitted changes:**

```bash
make review-uncommitted
# or directly:
coderabbit review --uncommitted
```

**Review staged changes:**

```bash
make review
# or directly:
coderabbit review
```

**Review specific files:**

```bash
coderabbit review path/to/file.py
```

### Makefile Targets

The project includes convenient Makefile targets:

- `make review` - Review staged changes
- `make review-uncommitted` - Review uncommitted changes

### Configuration

The `.coderabbit.yaml` file in the repository root configures:

- Language-specific settings (Python type checking, security)
- Path exclusions (node_modules, .venv, etc.)
- Focus areas (architecture compliance, TDD, governance)

### Features

- **Pre-commit reviews:** Catch issues before committing
- **Context-aware:** Learns from your team's patterns (paid plans)
- **Instant fixes:** Apply simple fixes with one command
- **Security scanning:** Detects vulnerabilities and security issues

### Troubleshooting

**CLI not found after installation:**

```bash
# Check if it's in PATH
which coderabbit

# If not found, add to PATH manually:
export PATH="$HOME/.local/bin:$PATH"
```

**Authentication issues:**

```bash
# Re-authenticate
coderabbit auth logout
coderabbit auth login
```

**Review not working:**

- Ensure you're authenticated: `coderabbit auth status`
- Check internet connection
- Verify `.coderabbit.yaml` syntax

### Integration with Development Workflow

**Recommended workflow:**

1. Make code changes
2. Stage changes: `git add .`
3. Review before commit: `make review-uncommitted`
4. Address any issues found
5. Commit: `git commit -m "..."`

This ensures code quality before it reaches GitHub and triggers the cloud-based CodeRabbit reviews.

## Resources

- [CodeRabbit CLI Documentation](https://docs.coderabbit.ai/cli)
- [Configuration Options](https://docs.coderabbit.ai/configuration/file-options)
- [CodeRabbit Website](https://coderabbit.ai)
