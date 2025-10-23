# 🏥 Automated Doctor–Patient Appointment Scheduling System  
### 🤖 Powered by Generative Data • Hungarian Algorithm • RAG Chatbot

---

## 🧩 Problem Statement
# Team-Vet
## Raju , Ram singhth, Nagaraju , Mahesh , santhosh

In healthcare environments, managing doctor–patient appointments efficiently is a complex task due to:

- ⏰ Overlapping appointment requests  
- ⚖️ Uneven doctor workloads  
- 🧾 Manual scheduling errors  
- 📅 Limited patient visibility into available slots  

These challenges often lead to **long waiting times**, **unoptimized schedules**, and **low patient satisfaction**.

💡 **Objective:**  
Design an **automated appointment scheduling system** that:
1. Generates synthetic yet realistic doctor–patient datasets.  
2. Uses the **Hungarian algorithm** for **optimal doctor–patient–time allocation**.  
3. Implements a **RAG (Retrieval-Augmented Generation) chatbot** for patients to **query, register, and check appointment availability** naturally.  

---

## 🌟 Overview

This project integrates **optimization algorithms** and **LLM-based conversational AI** to create a complete automation pipeline for healthcare scheduling.

Patients can:
- 🗓️ Check available time slots  
- 📅 Register or cancel appointments  
- 🤖 Interact with a chatbot to inquire about schedules, doctors, or availability  

The system ensures:
- 🔹 Balanced doctor workloads  
- 🔹 Minimal waiting times  
- 🔹 Real-time intelligent responses

---

## 🎯 Key Features

### 🧬 1. Data Generation
- Generates **synthetic datasets** for doctors and patients.
- Creates appointment records (`appointments.csv`) with random yet realistic scheduling patterns.

### ⚙️ 2. Hungarian Algorithm (Optimal Matching)
- Assigns patients to doctors **optimally** by minimizing cost (waiting time or mismatch).
- Ensures **conflict-free scheduling** and **load-balanced assignments**.

### 💬 3. RAG Chatbot
- Uses **Retrieval-Augmented Generation** to answer natural language queries:
  - “Who is Lucy’s doctor on November 3rd?”
  - “What time is Dr. Grace Johnson available?”
- Retrieves relevant appointment records using **semantic search** (FAISS/Chroma).
- Generates human-like answers using **GPT-based LLMs**.

### 🗓️ 4. Appointment Management
- Maintains a **live appointment table** for all doctors and patients.
- Supports **dynamic slot checking**, **rescheduling**, and **cancellations**.

---

## 🧠 System Architecture

```mermaid
flowchart TD
    A[🧬 Data Generator] --> B[⚙️ Hungarian Scheduler]
    B --> C[🧠 RAG Chatbot Layer]
    C --> D[💬 User Interface]

    subgraph Data
        A1[Doctors Dataset]
        A2[Patients Dataset]
        A3[Appointments CSV]
    end

    A1 --> A
    A2 --> A
    A3 --> A
    C -->|Embeddings + Vector Store| E[(FAISS/ChromaDB)]
