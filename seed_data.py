import requests
import time

BASE_URL = "http://127.0.0.1:8000"

CUSTOMERS = [
    {"name": "Priya Sharma", "email": "priya.sharma@example.com", "subscription_tier": "Enterprise", "customer_value": "High"},
    {"name": "Rahul Mehta", "email": "rahul.mehta@example.com", "subscription_tier": "Pro", "customer_value": "Medium"},
    {"name": "Ananya Iyer", "email": "ananya.iyer@example.com", "subscription_tier": "Basic", "customer_value": "Low"},
    {"name": "Vikram Singh", "email": "vikram.singh@example.com", "subscription_tier": "Enterprise", "customer_value": "High"},
    {"name": "Sneha Reddy", "email": "sneha.reddy@example.com", "subscription_tier": "Pro", "customer_value": "Medium"},
    {"name": "Arjun Nair", "email": "arjun.nair@example.com", "subscription_tier": "Basic", "customer_value": "Low"},
    {"name": "Kavya Rao", "email": "kavya.rao@example.com", "subscription_tier": "Enterprise", "customer_value": "High"},
    {"name": "Aditya Kumar", "email": "aditya.kumar@example.com", "subscription_tier": "Pro", "customer_value": "Medium"},
]

# (customer_index, category, message) — mix of tones, categories, tiers
TICKETS = [
    (0, "Security Issue", "Someone logged into my account from an unknown device, I'm very worried about my data security!"),
    (0, "Billing Dispute", "I've been charged twice this month and support hasn't responded in 3 days, this is unacceptable."),
    (1, "Technical Issue", "The dashboard keeps crashing whenever I try to export a report."),
    (1, "General Inquiry", "Can you tell me if there's a mobile app available?"),
    (2, "General Inquiry", "Just wanted to ask about your refund policy."),
    (2, "Technical Issue", "The search feature isn't returning any results for me."),
    (3, "Billing Dispute", "This is the third time I've been billed incorrectly, I am extremely frustrated and considering cancelling my enterprise plan."),
    (3, "Account Issue", "I need to update my company's billing address, could you guide me?"),
    (4, "Technical Issue", "Great news - the bug I reported last week is completely fixed now, thank you so much!"),
    (4, "General Inquiry", "What are your support hours on weekends?"),
    (5, "Security Issue", "I think my password was leaked, please help me secure my account immediately!"),
    (5, "General Inquiry", "How do I change my notification preferences?"),
    (6, "Billing Dispute", "Absolutely furious - my enterprise invoice is wrong for the second month running and no one has fixed it despite multiple emails!"),
    (6, "Technical Issue", "Thanks for the quick fix on the API timeout issue, really appreciate the fast turnaround!"),
    (7, "Account Issue", "I can't seem to log in, it says my account is locked."),
    (7, "General Inquiry", "Just checking, do you support SSO login for teams?"),
]


def seed():
    print("Creating customers...")
    customer_ids = []
    for c in CUSTOMERS:
        res = requests.post(f"{BASE_URL}/customers/", json=c)
        if res.status_code == 200:
            customer_ids.append(res.json()["id"])
            print(f"  Created: {c['name']} (id={res.json()['id']})")
        else:
            print(f"  Failed for {c['name']}: {res.text}")

    print("\nCreating tickets (this runs real NLP analysis per ticket, may take a bit)...")
    for idx, category, message in TICKETS:
        customer_id = customer_ids[idx]
        payload = {"customer_id": customer_id, "category": category, "message": message}
        res = requests.post(f"{BASE_URL}/tickets/", json=payload)
        if res.status_code == 200:
            data = res.json()
            priority = data["current_priority"]
            print(f"  Ticket #{data['id']} ({category}) -> {priority}")
        else:
            print(f"  Failed: {res.text}")
        time.sleep(0.1)  # small delay, easier on the server

    print("\nSeeding complete!")


if __name__ == "__main__":
    seed()