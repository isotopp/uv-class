---
title: "Using uv to manage python projects"
weight: 10
bookCollapseSection: true
date: 2025-12-22T00:00:00Z
description: |

---

{{% details title="**Summary**" open=true %}}
`uv` is a tool for managing Python projects.
It includes dependency management, but it does not stop there.

To explain `uv` properly, we need to explore how Python projects are created,
maintained, and distributed throughout their entire lifecycle.
{{% /details %}}

# What we do

This guide explains how to structure and maintain modern Python projects using `uv`.
Our audience is students or Python junior developers. 

# What we assume you know

We assume basic familiarity with Python, sufficient to follow code examples and understand the projects we build.

We assume you work with an IDE and have access to a Python installation.

We will use `git` to manage our codebase and Markdown for documentation.
We assume you are comfortable with basic `git` operations and understand fundamental Markdown concepts.

# What we teach

Our goal is to explain modern Python project structure and the workflows required to create and maintain Python projects over time,
and how `uv` supports that, providing consistency and reproducibility across different versions of Python.

We are biased toward native Python.
We do not cover modules written in C or other languages, nor how to manage projects that depend on them.

We are opinionated. We favor `src`-structured packages created with `uv init --package` over flat Python projects, and we explain why.

We use entry points and starter scripts to expose packages as command-line programs.

We discuss versioning, packaging, installation, and distribution of Python packages, and how `uv` supports these workflows.
