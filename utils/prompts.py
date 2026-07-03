# Prompts and samples for Prompt Engineering Playground

# ==========================================
# PAGE 1: Zero & Few-Shot Support Responder
# ==========================================

PAGE1_SAMPLES = {
    "Order Delayed": """Customer Name: Rahul Sharma
        Customer Email: rahul.sharma@gmail.com
        Order ID: ORD-458921

        Subject: Order Still Not Delivered

        Hello,

        I ordered a wireless mouse on June 20, but the estimated delivery date has already passed and I still haven't received my package. Could you please check the status of my order and let me know when I can expect it?

        Thank you,
        Rahul Sharma""",
    "Damaged Product": """Customer Name: Ananya Patel
Customer Email: ananya.patel@gmail.com
Order ID: ORD-672154

Subject: Received Damaged Product

Hi,

I received my new headphones today, but the left side is not working and the box was damaged when it arrived. I would like a replacement as soon as possible.

Regards,
Ananya Patel""",
    "Wrong Item": """Customer Name: Priya Nair
Customer Email: priya.nair@gmail.com
Order ID: ORD-918432

Subject: Incorrect Product Received

Dear Support Team,

I ordered a blue backpack, but I received a black one instead. Please advise on how I can get the correct item.

Sincerely,
Priya Nair"""
}

def get_zero_shot_prompt(email: str) -> str:
    return f"""You are a professional customer support executive. Reply politely to the following customer email.

Customer Email:
"{email}"
"""

def get_few_shot_prompt(email: str) -> str:
    return f"""You are a professional customer support executive. Reply politely to the following customer email.

Here are examples of how to respond:

Customer:
"My order is delayed."

Response:
"We apologize for the delay. Our team is checking your shipment and will update you shortly."

Customer:
"I received a damaged product."

Response:
"We're sorry to hear that. Please share photos of the product and we will arrange a replacement."

Now, reply to this customer email:

Customer:
"{email}"
"""

# ==========================================
# PAGE 2: Chain of Thought Reasoning
# ==========================================

PAGE2_SAMPLES = {
    "Train Distance": "A train travels 60 km in 1 hour. How long to travel 150 km?",
    "Farmer's Chickens": "If a farmer has 20 chickens and buys 15 more, then sells 10, how many remain?",
    "Number Series": "Find the next number in the series: 2,4,8,16,?"
}

def get_cot_prompt(question: str) -> str:
    return f"""You are a careful problem-solver who thinks out loud.

Solve the problem below by:
1. Understanding what the problem is asking.
2. Breaking it into smaller, manageable steps.
3. Explaining each step clearly as if teaching someone.
4. Double-checking your work.
5. Stating your final answer clearly.

Do not skip steps. Show every part of your thinking.

Problem:
{question}
"""

# ==========================================
# PAGE 3: Advanced CoT (Multi-Path)
# ==========================================

PAGE3_SAMPLES = {
    "Bat & Ball Riddle": "A bat and a ball cost ₹110. The bat costs ₹100 more than the ball. What is the price of the ball?",
    "Three Switches Riddle": "Three switches control one bulb in another room. How can you determine which switch controls the bulb?",
    "100 Lockers Riddle": "There are 100 lockers and 100 students opening and closing lockers in turns. Which lockers remain open?"
}

def get_path_prompt(problem: str, path_number: int, total_paths: int) -> str:
    """
    Prompt for one independent reasoning path.
    Each call uses a slightly different instruction so the model
    approaches the problem from a fresh angle.
    """
    styles = [
        "Use an algebraic or arithmetic approach.",
        "Use a logical deduction approach, reasoning from first principles.",
        "Use a visual or intuitive approach, drawing on common sense.",
        "Use a process-of-elimination approach.",
        "Use an analogy or real-world comparison to reason through the problem.",
    ]
    style = styles[(path_number - 1) % len(styles)]
    return f"""You are an independent expert solver (Path {path_number} of {total_paths}).

{style}

Think out loud step by step and arrive at a clear final answer.
Do not reference other paths or solvers.

Problem:
{problem}
"""


def get_evaluator_prompt(problem: str, paths: list[str]) -> str:
    """Final evaluator prompt that picks the best reasoning path."""
    numbered_paths = "\n\n".join(
        f"--- Path {i+1} ---\n{p}" for i, p in enumerate(paths)
    )
    return f"""You are an expert evaluator. You have been given a problem and {len(paths)} independent solutions.

Your job:
1. Read each solution carefully.
2. Identify any mistakes or logical errors in each.
3. Compare the strengths and weaknesses of each approach.
4. Determine which solution is most reliable and correct.
5. State the final answer clearly and explain why you chose it.

Problem:
{problem}

{numbered_paths}

Now provide your evaluation and final answer.
"""


def get_advanced_cot_prompt(problem: str, num_paths: int) -> str:
    """Legacy single-prompt version (kept for reference)."""
    return get_evaluator_prompt(problem, [f"[Path {i+1} placeholder]" for i in range(num_paths)])
