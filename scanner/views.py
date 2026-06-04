from django.shortcuts import render
import re


def home(request):
    if request.method == "POST":
        message = request.POST.get("message", "")
        lower_message = message.lower()

        risk = "Low"
        reasons = []
        categories = []
        score = 0

        scam_words = [
            "urgent",
            "verify",
            "password",
            "bank",
            "click here",
            "gift card",
            "bitcoin",
            "wire transfer",
        ]

        for word in scam_words:
            if word in lower_message:
                reasons.append(f"Detected keyword: {word}")
                score += 15

        urls = re.findall(r"https?://\S+|www\.\S+", message)

        for url in urls:
            reasons.append(f"Detected URL: {url}")
            score += 25

        phone_numbers = re.findall(
            r"(\+?\d{1,2}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}",
            message,
        )

        for phone in phone_numbers:
            reasons.append("Detected phone number")
            score += 10

        emails = re.findall(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            message,
        )

        for email in emails:
            reasons.append(f"Detected email: {email}")
            score += 10

        if "bank" in lower_message:
            categories.append("🏦 Banking Scam")

        if "password" in lower_message or "verify" in lower_message:
            categories.append("🔐 Credential Theft")

        if "bitcoin" in lower_message:
            categories.append("₿ Cryptocurrency Scam")

        if "gift card" in lower_message:
            categories.append("🎁 Gift Card Scam")

        if score > 100:
            score = 100

        if score >= 60:
            risk = "High"
        elif score >= 30:
            risk = "Medium"
        else:
            risk = "Low"

        return render(
            request,
            "submitted.html",
            {
                "message": message,
                "risk": risk,
                "score": score,
                "reasons": reasons,
                "categories": categories,
            },
        )

    return render(request, "index.html")


def about(request):
    return render(request, "about.html")