from flask import Flask, render_template, request, send_file
from io import BytesIO
from xhtml2pdf import pisa
from ast import literal_eval

app = Flask(__name__)

questions = [
    {"text": "As a Doctor, do you feel your present health plan is exclusive for you or is it a generic one?", "yes_score": 15, "no_score": 0},
    {"text": "Was there an incident where your cashless claim was rejected?", "yes_score": 0, "no_score": 15},
    {"text": "Are you aware of the exclusions and limitations in your current health policy?", "yes_score": 10, "no_score": 0},
    {"text": "Do you have a top-up or super top-up policy for extra medical expenses?", "yes_score": 12, "no_score": 0},
    {"text": "Have you checked if your preferred hospitals offer cashless treatment under your plan?", "yes_score": 8, "no_score": 0},
    {"text": "Is your sum insured updated considering rising medical inflation?", "yes_score": 10, "no_score": 0},
    {"text": "Do you have a dedicated health insurance advisor or support contact?", "yes_score": 10, "no_score": 0},
    {"text": "Do you have health insurance that covers your entire family?", "yes_score": 10, "no_score": 0},
    {"text": "Does your policy include coverage for critical illnesses and major surgeries?", "yes_score": 10, "no_score": 0}
]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', questions=enumerate(questions))

@app.route('/result', methods=['POST'])
def result():
    doctor_name = request.form.get('doctor_name', 'Doctor')
    responses = []
    total_score = 0

    print("=== DEBUG: Submitted Form Values ===")

    for i, q in enumerate(questions):
        ans = request.form.get(f'q{i}')
        print(f'q{i}: {ans}')  # Debug print

        if ans not in ['yes', 'no']:
            ans = 'no'  # Default if not selected or invalid

        score = q['yes_score'] if ans == 'yes' else q['no_score']
        total_score += score

        responses.append({
            "question": q['text'],
            "answer": ans,
            "score": score,
            "color": "green" if score > 0 else "red"
        })

    print(f"Total Score: {total_score}")
    return render_template('result.html', doctor_name=doctor_name, responses=responses, total_score=total_score)

@app.route('/download', methods=['POST'])
def download():
    responses = literal_eval(request.form['responses'])
    total_score = int(request.form['total_score'])
    doctor_name = request.form.get('doctor_name', 'Doctor')

    rendered = render_template('result.html',
                                doctor_name=doctor_name,
                                responses=responses,
                                total_score=total_score,
                                download_mode=True)
    pdf = BytesIO()
    pisa.CreatePDF(rendered, dest=pdf)
    pdf.seek(0)

    clean_name = doctor_name.strip().replace(' ', '_').replace('.', '')
    filename = f"Dr_{clean_name}_Health_Readiness_Scorecard.pdf"
    return send_file(pdf, download_name=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
