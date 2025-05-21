from urllib.parse import quote

def generate_mailto_link(email: str, subject: str, body: str) -> str:
    """
    Generate a mailto link with properly URL-encoded subject and body.
    
    Args:
        email (str): Recipient's email address
        subject (str): Email subject
        body (str): Email body text
    
    Returns:
        str: Complete mailto link
    """
    # URL encode the subject and body
    encoded_subject = quote(subject)
    encoded_body = quote(body)
    
    # Construct the mailto link
    mailto_link = f"mailto:{email}?subject={encoded_subject}&body={encoded_body}"
    
    return mailto_link 