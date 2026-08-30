from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    risk_score = None
    reasons = []

    if request.method == "POST":
        email = request.form.get("email", "").lower()

        suspicious_words = [
            "urgent",
            "verify",
            "account",
            "password",
            "click",
            "immediately",
            "suspended",
            "security alert"
        ]

        found_words = []

        for word in suspicious_words:
            if word in email:
                found_words.append(word)

        if len(found_words) >= 2:
            result = "phishing"
            risk_score = min(50 + len(found_words) * 10, 95)

            for word in found_words:
                reasons.append(f"Suspicious keyword detected: {word}")

        elif email.strip() == "":
            result = "empty"

        else:
            result = "safe"
            risk_score = 10

    return render_template(
        "index.html",
        result=result,
        risk_score=risk_score,
        reasons=reasons
    )

if __name__ == "__main__":
    app.run(debug=True)