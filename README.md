# Prompt Engineering Playground

An interactive Streamlit application that demonstrates three fundamental Prompt Engineering techniques using Large Language Models (LLMs):

* **Zero & Few-Shot Prompting**
* **Chain-of-Thought (CoT) Prompting**
* **Advanced CoT / Tree-of-Thought-Inspired Reasoning**

The project is designed as an educational tool to help students understand how different prompting strategies affect an AI model's responses and reasoning capabilities.

---

## 🚀 Features

### 1️⃣ Customer Support Email Responder (Zero & Few-Shot Prompting)

* Generate professional customer support replies.
* Compare:

  * **Zero-Shot Prompting** (instruction only)
  * **Few-Shot Prompting** (instruction + examples)
* Displays the exact prompt used.
* Simulates a real-world customer support automation system.

---

### 2️⃣ Structured Reasoning Simulator (Chain-of-Thought)

* Solve mathematical and logical problems step-by-step.
* Streams reasoning in real time.
* Automatically extracts reasoning steps.
* Generates a visual reasoning flow diagram.
* Displays the prompt used to generate reasoning.

---

### 3️⃣ Multi-Path Reasoning Evaluator (Advanced CoT)

* Generates multiple independent reasoning paths.
* Evaluates all paths and selects the best solution.
* Visualizes reasoning as a tree structure.
* Highlights the chosen reasoning path.
* Displays final evaluation and answer.

---



# 🏗️ Project Architecture

```text
                         User Input
                              │
                              ▼
                      Streamlit Interface
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
 Zero/Few-Shot          Chain of Thought      Advanced CoT
 Email Responder        Reasoning Engine      Multi-Path Evaluator
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                        Local LLM (Ollama)
                          qwen3.5:4b
                              │
                              ▼
                         Generated Output
```

---

# 🧠 Prompt Engineering Concepts

## Zero-Shot Prompting

The model is given only an instruction.

Example:

```text
Write a professional response to the following customer email.
```

### Characteristics

* No examples provided.
* Relies entirely on the model's prior knowledge.
* Fast and simple.

---

## Few-Shot Prompting

The model is provided with examples before the actual task.

### Characteristics

* Better formatting consistency.
* More reliable responses.
* Easier to control model behavior.

---

## Chain-of-Thought (CoT)

The model is instructed to explain its reasoning step-by-step before giving the final answer.

### Benefits

* Improves reasoning accuracy.
* Makes model decisions more interpretable.
* Useful for mathematical and logical problems.

---

## Advanced CoT / Tree of Thoughts

The model generates multiple independent solutions and evaluates them before selecting the best answer.

### Benefits

* Better decision-making.
* Reduces reasoning errors.
* Mimics human problem-solving strategies.

---

# ⚠️ Important Note

The reasoning shown by the application is:

> **Generated reasoning traces from the model and not the model's hidden internal thoughts.**

Modern LLM APIs and local models do not expose their actual internal transformer computations.

---

# 🛠️ Tech Stack

* Python 3.10+
* Streamlit
* Ollama
* Qwen3.5:4b
* Graphviz
* Python-dotenv

---

# 📂 Project Structure

```text
Prompt-Engineering-Playground/
│
├── app.py
├── requirements.txt
├── README.md
│
├── pages/
│   ├── zero_few_shot.py
│   ├── cot.py
│   └── advanced_cot.py
│
├── utils/
│   ├── prompts.py
│   ├── ollama_client.py
│   └── helpers.py
│
├── assets/
│   └── screenshots/
│
└── .streamlit/
    └── config.toml
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd Prompt-Engineering-Playground
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Install Ollama

Download and install:

[Ollama Official Website](https://ollama.com?utm_source=chatgpt.com)

---

## Pull the model

```bash
ollama pull qwen3.5:4b
```

---

## Start Ollama

```bash
ollama serve
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

---

# 📦 Requirements

```text
streamlit
ollama
graphviz
python-dotenv
```

---

# 🎯 Use Cases

### Education

* Learning Prompt Engineering
* Understanding AI reasoning

### Demonstrations

* AI workshops
* College presentations
* LLM demonstrations

### Research

* Comparing prompting techniques
* Evaluating reasoning behaviors

---

# 📖 Example Workflow

### Zero/Few-Shot

```text
Customer Email
        ↓
Prompt Template
        ↓
LLM Response
        ↓
Generated Reply
```

---

### Chain of Thought

```text
Problem
      ↓
Reasoning Step 1
      ↓
Reasoning Step 2
      ↓
Reasoning Step 3
      ↓
Final Answer
```

---

### Advanced CoT

```text
Problem
      ↓
 Path 1
 Path 2
 Path 3
      ↓
Evaluation
      ↓
Best Solution
      ↓
Final Answer
```

---

# 🎓 Learning Outcomes

After using this application, users will understand:

* What Prompt Engineering is.
* Differences between Zero-Shot and Few-Shot prompting.
* How Chain-of-Thought prompting works.
* How multi-path reasoning improves decision-making.
* How local LLMs can be integrated into applications.

---

# 🔮 Future Improvements

* Support additional local models.
* Compare outputs from multiple LLMs.
* Save reasoning history.
* Export reasoning diagrams.
* Add benchmark datasets.
* Add prompt performance analytics.

---

# 👨‍💻 Author

**Vedant Dhadge**
B.Tech Computer Engineering
Sanjivani College of Engineering, Maharashtra, India

---

# 📄 License

This project is intended for educational and learning purposes. Feel free to modify and extend it for academic use.
