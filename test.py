import qrcode
from upitool import UPIPayload

def generate_upi_request_qr_code(upi_id, amount, currency="INR", description="Payment Request"):
    # Create UPI URL
    upi_payload = UPIPayload(
        action="pay",
        vpa=upi_id,
        mc="your-merchant-code",  # Replace with your merchant code (if applicable)
        tid="your-transaction-id",  # Replace with your unique transaction ID
        tr="your-transaction-reference",  # Replace with your transaction reference
        tn=description,
        am=str(amount),
        cu=currency,
    )

    upi_url = upi_payload.get_uri()

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save("upi_request_qr.png")

if __name__ == "__main__":
    # Replace 'your_upi_id' with the actual UPI ID you want to use
    upi_id = "9921309560@ybl"
    
    # Replace 'your_amount' with the dynamic amount you want to request
    amount = 100.00  # Example amount

    generate_upi_request_qr_code(upi_id, amount)
