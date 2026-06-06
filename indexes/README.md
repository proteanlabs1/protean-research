# Indexes

Machine-readable navigation for the archive, rebuilt from the artifacts on disk
on every generation run.

| File | Contents |
| --- | --- |
| `manifest.jsonl` | One line per artifact: `kind`, `slug`, `title`, `path`, `topics`, `generated_at`, `content_hash`. |
| `latest.json` | The latest artifact of each kind, the current `manifest_hash`, and the artifact count. |
| `topics.json` | Topic → list of artifact paths. |
| `families.json` | Candidate-family slug → journal path. |
| `contradictions.json` | Open and resolved contradiction paths. |
| `weekly.json` | Weekly "State of Protean" review paths. |

The `manifest_hash` is a sha256 over each artifact's `(path, content_hash)`. It
changes only when artifact content changes, which is how the publisher decides
whether to commit.

Schemas: [`../schemas/public_manifest.schema.json`](../schemas/public_manifest.schema.json).
