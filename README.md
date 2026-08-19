# GenLayer Multi-Source Adjudication Engine

A decentralized AI-powered adjudication system built with GenLayer Intelligent Contracts.

This project demonstrates how GenLayer can be used as a reusable verification layer for real-world claims by combining:

- Multi-source evidence collection
- Source normalization
- Independent webpage verification
- Explicit fetch failure handling
- AI consensus-based adjudication
- Challenge and dispute lifecycle management


## Problem

Traditional verification systems usually depend on:

- A single trusted authority
- A single webpage
- Centralized review processes

This creates problems:

- Sources can become unavailable
- Evidence can be manipulated
- Decisions cannot be independently reproduced


## Solution

GenLayer Multi-Source Adjudication Engine allows users to create verification cases.

Each case contains:

- A claim that needs verification
- Verification criteria
- Multiple independent evidence sources

The Intelligent Contract then:

1. Normalizes submitted URLs
2. Fetches evidence from each source independently
3. Records successful and failed fetch attempts
4. Uses GenLayer decentralized AI consensus to evaluate evidence
5. Produces a transparent APPROVED or REJECTED decision
6. Allows challenges after resolution


## Architecture

