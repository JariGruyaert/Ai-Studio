---
title: "GitHub - lemonhu/open-entity-relation-extraction: Knowledge triples extraction and knowledge base construction based on dependency syntax for open domain text."
source: https://github.com/lemonhu/open-entity-relation-extraction
type: github-repo
extracted: 2026-01-18T12:45:26.278556
domain: github.com
word_count: 378
processing_status: completed
---

# GitHub - lemonhu/open-entity-relation-extraction: Knowledge triples extraction and knowledge base construction based on dependency syntax for open domain text.

## Description
Knowledge triples extraction and knowledge base construction based on dependency syntax for open domain text. - lemonhu/open-entity-relation-extraction

## Content

lemonhu

/

open-entity-relation-extraction

Public

Notifications

You must be signed in to change notification settings

Fork

118

Star

537

Knowledge triples extraction and knowledge base construction based on dependency syntax for open domain text.

License

MIT license

537

stars

118

forks

Branches

Tags

Activity

Star

Notifications

You must be signed in to change notification settings

lemonhu/open-entity-relation-extraction

master
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
21 Commits
code
code

data
data

img
img

resource
resource

.gitignore
.gitignore

LICENSE
LICENSE

README.md
README.md

requirements.txt
requirements.txt

View all files
Repository files navigation
open-entity-relation-extraction

Knowledge triples extraction (entities and relations extraction) and knowledge base construction based on dependency syntax for open domain text.

基于依存句法分析，实现面向开放域文本的知识三元组抽取（实体和关系抽取）及知识库构建。

Welcome to watch, star or fork.

Example

"中国国家主席习近平访问韩国，并在首尔大学发表演讲"

We can extract knowledge triples from the sentence as follows:

(中国, 国家主席, 习近平)

(习近平, 访问, 韩国)

(习近平, 发表演讲, 首尔大学)

Project Structure

knowledge_extraction/
|-- code/  # code directory
|   |-- bean/
|   |-- core/
|   |-- demo/  # procedure entry
|   |-- tool/
|-- data/ # data directory
|   |-- input_text.txt  # input text file
|   |-- knowledge_triple.json  # output knowledge triples file
|-- model/  # ltp models, can be downloaded from http://ltp.ai/download.html, select ltp_data_v3.4.0.zip
|-- resource  # dictionaries dirctory
|-- requirements.txt  # dependent python libraries
|-- README.md  # project description

Requirements

This repo was tested on Python 3.5+. The requirements are:

jieba>=0.39

pyltp>=0.2.1

Quickstart

cd
./code/demo/
python extract_demo.py

Seven DSNF paradigms

References

If you use the code, please kindly cite the following paper:

Jia S, Li M, Xiang Y. Chinese Open Relation Extraction and Knowledge Base Establishment[J]. ACM Transactions on Asian and Low-Resource Language Information Processing (TALLIP), 2018, 17(3): 15.

About

Knowledge triples extraction and knowledge base construction based on dependency syntax for open domain text.

Topics

python3

information-extraction

knowledge-base

relation-extraction

paper-implementations

entity-relation

knowledge-extraction

open-domain

Resources

Readme

License

MIT license

Uh oh!

There was an error while loading.
Please reload this page
.

Activity

Stars

537

stars

Watchers

11

watching

Forks

118

forks

Report repository

Releases

No releases published

Packages

0

No packages published

Uh oh!

There was an error while loading.
Please reload this page
.

Contributors

2

Uh oh!

There was an error while loading.
Please reload this page
.

Languages

Python

100.0%

---

## Metadata

**Source:** [https://github.com/lemonhu/open-entity-relation-extraction](https://github.com/lemonhu/open-entity-relation-extraction)
**Type:** github-repo
**Extracted:** 2026-01-18T12:45:26.277974
**Extractor:** fallback
**Word Count:** 378
