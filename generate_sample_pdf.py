from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "Clean Water Initiative 2024")

    # Subtitle
    c.setFont("Helvetica", 14)
    c.drawString(100, 720, "Annual Impact Report")

    # Body Text
    c.setFont("Helvetica", 12)
    text = """
    The Global Water Crisis is escalating. Over 2 billion people lack access to safe drinking water.
    
    Our Mission:
    To provide sustainable water solutions to rural communities in need.
    
    Key Statistics:
    - We have installed 500 new wells this year.
    - 15,000 families now have access to clean water.
    - Waterborne diseases have dropped by 40% in our target regions.
    
    Call to Action:
    We need your help to double our impact in 2025. A donation of just $50 provides clean water for a family for a year.
    Join us in making water a basic human right, not a luxury.
    """
    
    y = 680
    for line in text.split('\n'):
        c.drawString(100, y, line.strip())
        y -= 20

    c.save()

if __name__ == "__main__":
    create_pdf("sample_report.pdf")
    print("Created sample_report.pdf")
