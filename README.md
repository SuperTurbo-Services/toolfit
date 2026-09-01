# Toolfit

Official role-based AI skills from [Toolfit](https://toolfit.pro).

One install gives you the skills. Each connector is a one-time setup in your own account.

## Claude Desktop or Cowork

1. Open **Customize** in the left sidebar.
2. Open **Plugins**, choose **+**, then **Add marketplace**.
3. Choose **Add from a repository** and enter `SuperTurbo-Services/toolfit`.
4. Install the plugin for your role.

A paid Claude plan is required. No GitHub account is needed because this repository is public.

## ChatGPT Desktop

Ask Codex to copy the skill folders from `roles/<role>/skills/` into `~/.agents/skills/`, preserving each folder name.

## Available roles

- [Founder](./roles/owner-management) — `toolfit-owner-management`
- [Marketing & Sales](./roles/marketing-sales) — `toolfit-marketing-sales`
- [Developer](./roles/developer) — `toolfit-developer`
- [Product](./roles/product) — `toolfit-product`
- [Finance](./roles/finance) — `toolfit-finance`
- [Operations](./roles/operations) — `toolfit-operations`
- [Recruiter / HR](./roles/recruiter-hr) — `toolfit-recruiter-hr`
- [Academic](./roles/academic) — `toolfit-academic`

Connector folders contain setup guides only. This repository does not ship `.mcp.json`, connector credentials, or bundled MCP configuration.
