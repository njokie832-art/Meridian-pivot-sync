# Meridian Pivot Sync

## Overview
Meridian Pivot Sync is a lightweight, serverless inventory synchronization prototype designed to handle real-time inventory level requests and updates via HTTP triggers. Built using the Google Cloud Functions Framework for Python, this service provides fast, local and cloud-agnostic execution for automated retail and operational stock tracking.

## Core Features
* **Serverless Architecture:** Utilizes Python Functions Framework for rapid local and cloud-based execution.
* **HTTP Inventory Lookups:** Accepts SKU-based queries to instantly retrieve item availability, descriptions, and stock counts.
* **Robust Error Handling:** Validates incoming payloads and query parameters, returning structured JSON error responses for missing parameters or unlisted SKUs.

## Tech Stack
* **Language:** Python 3.x
* **Core Framework:** Google Cloud Functions Framework (`functions-framework`)
* **Version Control:** Git & GitHub

## Getting Started Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt