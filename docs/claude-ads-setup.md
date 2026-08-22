# Claude Ads setup

[Claude Ads](https://github.com/AgriciDaniel/claude-ads) is a Claude Code plugin
for paid-media operations across Google, Meta, YouTube, LinkedIn, TikTok,
Microsoft, Apple, Amazon, Reddit, Pinterest, Snapchat, and X.

## Already configured for this repo

`.claude/settings.json` declares the marketplace and enables the plugin, so
anyone opening this repo in Claude Code is prompted to trust and install it.
No manual steps are needed beyond approving that prompt and restarting.

## Manual install (any other project)

1. Open Claude Code.
2. `/plugin marketplace add AgriciDaniel/claude-ads`
3. `/plugin install claude-ads@ai-marketing-hub-claude-ads`
4. Restart Claude Code so the plugin's skills and agents load.
5. Confirm with `/claude-ads:ads`.

The same steps work from a terminal without the interactive UI:

```sh
claude plugin marketplace add AgriciDaniel/claude-ads
claude plugin install claude-ads@ai-marketing-hub-claude-ads
claude plugin list
```

## Verifying

`/claude-ads:ads` should answer with a prompt along the lines of "I see you've
installed the Claude Ads plugin. What would you like to do with it — set up a
client/account, run an audit, build a plan, or something else?"

If it reports an unknown command, the plugin is installed but the session
predates it — restart Claude Code and try again.

`claude plugin details claude-ads` shows the component inventory and token cost.
Version 2.0.1 ships 34 skills and 25 agents, and adds roughly 6.6k always-on
tokens to every session in a project where it is enabled.

## What you get

- Entry point: `/claude-ads:ads` (conductor skill that routes to the rest).
- Workflow skills: `ads-audit`, `ads-plan`, `ads-create`, `ads-creative`,
  `ads-launch`, `ads-optimize`, `ads-monitor`, `ads-report`, `ads-test`,
  `ads-budget`, `ads-research`, `ads-competitor`, `ads-landing`,
  `ads-attribution`, `ads-server-side-tracking`, `ads-validate`, and more.
- Platform skills: one per ad network (`ads-google`, `ads-meta`, `ads-tiktok`,
  `ads-linkedin`, `ads-amazon`, `ads-apple`, `ads-microsoft`, `ads-youtube`,
  `ads-reddit`, `ads-pinterest`, `ads-snapchat`, `ads-x`).
- Audit subagents per platform, plus creative, policy, regulatory, budget, and
  tracking auditors.

Account-changing actions are gated: the plugin stops at a draft unless you
explicitly approve the mutation.

## Removing it

```sh
claude plugin uninstall claude-ads
claude plugin marketplace remove ai-marketing-hub-claude-ads
```

Delete `.claude/settings.json` (or just its `enabledPlugins` entry) to stop
enabling it for this repo.
