"""
Simple test script for spam detector
Tests the system with example emails
"""

from spam_detector import SpamDetector


def test_spam_detector():
    """Test the spam detector with example emails"""
    detector = SpamDetector()
    
    print("=" * 70)
    print("SPAM DETECTOR TEST SUITE")
    print("=" * 70)
    print()
    
    # Test 1: Spam email
    print("TEST 1: Spam Email")
    print("-" * 70)
    spam_text = """
    Subject: CONGRATULATIONS!!! YOU'VE WON $1,000,000!!!
    
    Dear Winner,
    You have been SELECTED as the GRAND PRIZE WINNER!!!
    CLICK HERE NOW: http://www.fake-winner-site.com/claim
    URGENT!!! FREE MONEY!!! ACT NOW!!!
    """
    
    classification, score, analysis = detector.classify(spam_text)
    print(f"Classification: {classification}")
    print(f"Spam Score: {score}")
    print(f"Keywords Found: {analysis.get('keyword_count', 0)}")
    print()
    
    # Test 2: Ham email
    print("TEST 2: Legitimate Email (HAM)")
    print("-" * 70)
    ham_text = """
    Subject: Meeting Reminder
    
    Hi Team,
    I wanted to remind everyone about our meeting tomorrow at 2:00 PM.
    Please come prepared with your status updates.
    
    Best regards,
    John Smith
    """
    
    classification, score, analysis = detector.classify(ham_text)
    print(f"Classification: {classification}")
    print(f"Spam Score: {score}")
    print(f"Keywords Found: {analysis.get('keyword_count', 0)}")
    print()
    
    # Test 3: Mixed email
    print("TEST 3: Mixed Content Email")
    print("-" * 70)
    mixed_text = """
    Subject: Special Offer
    
    Hello,
    We're offering a 15% discount this month.
    Visit our website at www.legitimate-store.com
    
    Thank you,
    Customer Service
    """
    
    classification, score, analysis = detector.classify(mixed_text)
    print(f"Classification: {classification}")
    print(f"Spam Score: {score}")
    print(f"Keywords Found: {analysis.get('keyword_count', 0)}")
    print()
    
    # Test 4: Test from file
    print("TEST 4: Reading from File")
    print("-" * 70)
    try:
        classification, score, analysis = detector.analyze_from_file("example_spam_email.txt")
        if not classification.startswith("Error"):
            print(f"Classification: {classification}")
            print(f"Spam Score: {score}")
            print("File read successfully!")
        else:
            print(classification)
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print()
    print("=" * 70)
    print("TEST SUITE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    test_spam_detector()

