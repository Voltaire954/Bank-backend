from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf_receipt(transaction, receipt_path):
    os.makedirs(os.path.dirname(receipt_path), exist_ok=True)

    c = canvas.Canvas(receipt_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Transaction Receipt")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 120, f"Transaction ID: {transaction.id}")
    c.drawString(50, height - 140, f"User ID: {transaction.user_id}")
    c.drawString(50, height - 160, f"Account ID: {transaction.account_id}")
    c.drawString(50, height - 180, f"Type: {transaction.transaction_type}")
    c.drawString(50, height - 200, f"Amount: ${transaction.amount}")
    c.drawString(50, height - 220, f"Date: {transaction.date_added}")

    c.showPage()
    c.save()

    return receipt_path
