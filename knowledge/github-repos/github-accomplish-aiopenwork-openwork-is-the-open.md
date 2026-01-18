---
title: "GitHub - accomplish-ai/openwork: Openwork™ is the open source Al coworker that lives on your desktop"
source: https://github.com/accomplish-ai/openwork
type: github-repo
extracted: 2026-01-18T12:45:30.628322
domain: github.com
word_count: 895
processing_status: completed
---

# GitHub - accomplish-ai/openwork: Openwork™ is the open source Al coworker that lives on your desktop

## Description
Openwork™ is the open source Al coworker that lives on your desktop - accomplish-ai/openwork

## Content

accomplish-ai

/

openwork

Public

Notifications

You must be signed in to change notification settings

Fork

198

Star

1.2k

Openwork™ is the open source Al coworker that lives on your desktop

www.accomplish.ai/openwork/

License

MIT license

1.2k

stars

198

forks

Branches

Tags

Activity

Star

Notifications

You must be signed in to change notification settings

accomplish-ai/openwork

main
Branches
Tags
Go to file
Code
Open more actions menu
Folders and files
Name
Name
Last commit message
Last commit date
Latest commit

History
44 Commits
.github
.github

apps/
desktop
apps/
desktop

packages/
shared
packages/
shared

.dockerignore
.dockerignore

.gitignore
.gitignore

CLAUDE.md
CLAUDE.md

CONTRIBUTING.md
CONTRIBUTING.md

LICENSE
LICENSE

README.md
README.md

SECURITY.md
SECURITY.md

package.json
package.json

pnpm-lock.yaml
pnpm-lock.yaml

pnpm-workspace.yaml
pnpm-workspace.yaml

View all files
Repository files navigation

Openwork™ - Open Source AI Desktop Agent

Openwork is an open source AI desktop agent that automates file management, document creation, and browser tasks locally on your machine. Bring your own API keys (OpenAI, Anthropic, Google, xAI) or run local models via Ollama.

Runs locally on your machine. Bring your own API keys or local models. MIT licensed.

Download Openwork for Mac (Apple Silicon)

·

Openwork website

·

Openwork blog

·

Openwork releases

What makes it different

🖥️  It runs locally

Your files stay on your machine

You decide which folders it can touch

Nothing gets sent to Openwork (or anyone else)

🔑  You bring your own AI

Use your own API key (OpenAI, Anthropic, etc.)

Or run with
Ollama
(no API key needed)

No subscription, no upsell

It's a tool—not a service

📖  It's open source

Every line of code is on GitHub

MIT licensed

Change it, fork it, break it, fix it

⚡  It acts, not just chats

File management

Document creation

Custom automations

Skill learning

What it actually does

📁 File Management

✍️ Document Writing

🔗 Tool Connections

Sort, rename, and move files based on content or rules you give it

Prompt it to write, summarize, or rewrite documents

Works with Notion, Google Drive, Dropbox, and more (through local APIs)

⚙️ Custom Skills

🛡️ Full Control

Define repeatable workflows, save them as skills

You approve every action. You can see logs. You can stop it anytime.

Use cases

Clean up messy folders by project, file type, or date

Draft, summarize, and rewrite docs, reports, and meeting notes

Automate browser workflows like research and form entry

Generate weekly updates from files and notes

Prepare meeting materials from docs and calendars

Supported models and providers

OpenAI

Anthropic

Google

xAI

Ollama (local models)

Privacy and local-first

Openwork runs locally on your machine. Your files stay on your device, and you choose which folders it can access.

System requirements

macOS (Apple Silicon)

Windows support coming soon

How to use it

Takes 2 minutes to set up.

Step

Action

Details

1

Install the App

Download the DMG and drag it into Applications

2

Connect Your AI

Use your own OpenAI or Anthropic API key, or Ollama. No subscriptions.

3

Give It Access

Choose which folders it can see. You stay in control.

4

Start Working

Ask it to summarize a doc, clean a folder, or create a report. You approve everything.

Download for Mac (Apple Silicon)

Screenshots and Demo

A quick look at Openwork on macOS, plus a short demo video.

Watch the demo →

FAQ

Does Openwork run locally?

Yes. Openwork runs locally on your machine and you control which folders it can access.

Do I need an API key?

You can use your own API keys (OpenAI, Anthropic, Google, xAI) or run local models via Ollama.

Is Openwork free?

Yes. Openwork is open source and MIT licensed.

Which platforms are supported?

macOS (Apple Silicon) is available now. Windows support is coming soon.

Development

pnpm install
pnpm dev

That's it.

Prerequisites

Node.js 20+

pnpm 9+

All Commands

Command

Description

pnpm dev

Run desktop app in dev mode

pnpm dev:clean

Dev mode with clean start

pnpm build

Build all workspaces

pnpm build:desktop

Build desktop app only

pnpm lint

TypeScript checks

pnpm typecheck

Type validation

pnpm -F @accomplish/desktop test:e2e

Playwright E2E tests

Environment Variables

Variable

Description

CLEAN_START=1

Clear all stored data on app start

E2E_SKIP_AUTH=1

Skip onboarding flow (for testing)

Architecture

apps/
desktop/        # Electron app (main + preload + renderer)
packages/
shared/         # Shared TypeScript types

The desktop app uses Electron with a React UI bundled via Vite. The main process spawns
OpenCode
CLI using
node-pty
to execute tasks. API keys are stored securely in the OS keychain.

See
CLAUDE.md
for detailed architecture documentation.

Contributing

Contributions welcome! Feel free to open a PR.

#
Fork → Clone → Branch → Commit → Push → PR

git checkout -b feature/amazing-feature
git commit -m
'
Add amazing feature
'

git push origin feature/amazing-feature

Openwork website
·
Openwork blog
·
Openwork releases
·
Issues
·
Twitter

MIT License · Built by
Accomplish

Keywords:
AI agent, AI desktop agent, desktop automation, file management, document creation, browser automation, local-first, macOS, privacy-first, open source, Electron, computer use, AI assistant, workflow automation, OpenAI, Anthropic, Google, xAI, Claude, GPT-4, Ollama

About

Openwork™ is the open source Al coworker that lives on your desktop

www.accomplish.ai/openwork/

Resources

Readme

License

MIT license

Contributing

Contributing

Security policy

Security policy

Uh oh!

There was an error while loading.
Please reload this page
.

Activity

Custom properties

Stars

1.2k

stars

Watchers

9

watching

Forks

198

forks

Report repository

Releases

2

tags

Packages

0

No packages published

Contributors

9

Languages

TypeScript

96.5%

JavaScript

2.3%

Other

1.2%

---

## Metadata

**Source:** [https://github.com/accomplish-ai/openwork](https://github.com/accomplish-ai/openwork)
**Type:** github-repo
**Extracted:** 2026-01-18T12:45:30.627619
**Extractor:** fallback
**Word Count:** 895
