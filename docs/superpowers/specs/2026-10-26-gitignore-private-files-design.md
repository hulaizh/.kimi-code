# Gitignore Private Files Design

## Purpose

Keep portable Kimi Code settings in the public repository while preventing credentials, identifiers, runtime state, histories, cached data, and machine-local workspace information from being committed.

## Design

Create a root `.gitignore` using an explicit denylist. Ignore `credentials/`, `oauth/`, and `device_id`; timestamped `config.toml` backups; local binaries, caches, histories, locks, logs, sessions, telemetry, updates, and user history; workspace indexes, trust data, workspace metadata, and region; and locally installed plugins.

Leave `.gitignore`, `config.toml`, `tui.toml`, and this design document available for tracking. Do not modify configuration or private files.

## Verification

Run `git status --short --untracked-files=all` to confirm that only intended public files remain untracked. Use `git check-ignore` to verify that credential, OAuth, session, log, cache, history, workspace, and local plugin paths are ignored.
