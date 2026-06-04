from django.shortcuts import render

def home(request):

    if request.method == "POST":

        message = request.POST.get("message", "")

        risk = "Low"
        reasons = []
        score = 0

        scam_words = [
            "urgent",
            "verify",
            "password",
            "bank",
            "click here",
            "gift card",
            "bitcoin",
            "wire transfer"
        ]

        for word in scam_words:
            if word.lower() in message.lower():
                reasons.append(f"Detected keyword: {word}")
                score += 15

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
                "reasons": reasons
            }
        )

    return render(request, "index.html")