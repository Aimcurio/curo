# Project Directory Policy

## Principles & Guardrails
1. **Target Path Extraction:** Check if an explicit target folder, drive, or repository path was provided in the prompt, kickoff brief, or command arguments.
2. **Path Clarification:** If no target directory is specified and no active workspace exists, prompt the user for their preferred destination path before writing code (do not default to scratch directories).
3. **Cross-Drive Operations:** When moving or creating files across drives (e.g., `C:` to `E:`), verify absolute paths and ensure all configuration files, `node_modules`, and build checks (`npm run build`) pass cleanly in the final target directory.
