"""
Spam Email Detection System
Rule-Based Spam Detection without Machine Learning
"""

import re
import string


class SpamDetector:
    """Main class for spam email detection using rule-based approach"""
    
    def __init__(self):
        """Initialize spam detector with keywords and rules"""
        # Predefined spam keywords
        self.spam_keywords = [
            'free', 'win', 'offer', 'prize', 'click here', 'urgent', 'money',
            'winner', 'congratulations', 'limited time', 'act now', 'buy now',
            'discount', 'save', 'deal', 'special offer', 'guaranteed',
            'risk free', 'no obligation', 'cash', 'bonus', 'reward',
            'claim', 'selected', 'exclusive', 'amazing', 'incredible',
            'miracle', 'secret', 'hidden', 'revealed', 'instant',
            'as seen on', 'order now', 'call now', 'click below',
            'unsubscribe', 'remove', 'opt out', 'viagra', 'pills',
            'pharmacy', 'loan', 'credit', 'debt', 'refinance'
        ]
        
        # Threshold for spam classification
        self.spam_threshold = 3
        
    def preprocess_text(self, text):
        """
        Module 2: Text Preprocessing
        Convert text to lowercase, remove punctuation, normalize
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Keep original for some checks (URLs, capitals)
        return text.strip()
    
    def count_spam_keywords(self, text):
        """
        Module 3: Keyword Matching
        Count number of spam keywords found in email
        """
        text_lower = self.preprocess_text(text)
        count = 0
        found_keywords = []
        
        for keyword in self.spam_keywords:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                count += len(matches)
                found_keywords.append(keyword)
        
        return count, found_keywords
    
    def check_suspicious_urls(self, text):
        """
        Module 4: Rule 1 - Check for suspicious URLs
        """
        # Look for http, https, www patterns
        url_patterns = [
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            r'www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            r'[a-zA-Z0-9.-]+\.(com|net|org|info|biz|ru|tk|ml|ga|cf|gq|xyz|click|download|link)'
        ]
        
        url_count = 0
        for pattern in url_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            url_count += len(matches)
        
        return url_count
    
    def check_excessive_capitals(self, text):
        """
        Module 4: Rule 2 - Check for excessive capital letters
        """
        if len(text) == 0:
            return 0
        
        # Count uppercase letters
        uppercase_count = sum(1 for char in text if char.isupper())
        total_letters = sum(1 for char in text if char.isalpha())
        
        if total_letters == 0:
            return 0
        
        # Calculate percentage of uppercase letters
        uppercase_ratio = uppercase_count / total_letters
        
        # If more than 30% are uppercase, it's suspicious
        if uppercase_ratio > 0.3:
            return 1
        return 0
    
    def check_exclamation_marks(self, text):
        """
        Module 4: Rule 3 - Check for too many exclamation marks
        """
        exclamation_count = text.count('!')
        
        # More than 2 exclamation marks is suspicious
        if exclamation_count > 2:
            return 1
        return 0
    
    def check_repeated_special_chars(self, text):
        """
        Module 4: Rule 4 - Check for repeated special characters
        """
        # Look for patterns like !!!, ???, ***, etc.
        pattern = r'([!?*#$%&])\1{2,}'
        matches = re.findall(pattern, text)
        
        if matches:
            return 1
        return 0
    
    def check_repeated_spam_keywords(self, text):
        """
        Module 4: Rule 5 - Check for repeated spam keywords
        """
        text_lower = self.preprocess_text(text)
        keyword_counts = {}
        
        for keyword in self.spam_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if len(matches) > 1:  # Keyword appears more than once
                keyword_counts[keyword] = len(matches)
        
        # If any keyword appears 3+ times, it's suspicious
        if keyword_counts and max(keyword_counts.values()) >= 3:
            return 1
        return 0
    
    def check_email_structure(self, text):
        """
        Additional rule: Check for suspicious email structure
        """
        score = 0
        
        # Check for all caps words (more than 3 characters)
        all_caps_words = re.findall(r'\b[A-Z]{4,}\b', text)
        if len(all_caps_words) > 2:
            score += 1
        
        # Check for excessive numbers (spam often has phone numbers, prices)
        numbers = re.findall(r'\d+', text)
        if len(numbers) > 5:
            score += 0.5
        
        return score
    
    def calculate_spam_score(self, text):
        """
        Module 4: Rule-Based Analysis
        Calculate total spam score based on all rules
        """
        score = 0
        
        # Rule 1: Spam keywords
        keyword_count, _ = self.count_spam_keywords(text)
        score += min(keyword_count * 0.5, 3)  # Cap at 3 points
        
        # Rule 2: Suspicious URLs
        url_count = self.check_suspicious_urls(text)
        score += min(url_count * 0.5, 2)  # Cap at 2 points
        
        # Rule 3: Excessive capitals
        score += self.check_excessive_capitals(text)
        
        # Rule 4: Exclamation marks
        score += self.check_exclamation_marks(text)
        
        # Rule 5: Repeated special characters
        score += self.check_repeated_special_chars(text)
        
        # Rule 6: Repeated spam keywords
        score += self.check_repeated_spam_keywords(text)
        
        # Rule 7: Email structure
        score += self.check_email_structure(text)
        
        return round(score, 2)
    
    def classify(self, text):
        """
        Module 5: Decision Module
        Classify email as Spam or Not Spam based on threshold
        """
        if not text or len(text.strip()) == 0:
            return "Invalid", 0, {}
        
        spam_score = self.calculate_spam_score(text)
        keyword_count, found_keywords = self.count_spam_keywords(text)
        url_count = self.check_suspicious_urls(text)
        
        # Classification
        if spam_score >= self.spam_threshold:
            classification = "SPAM"
        else:
            classification = "NOT SPAM (HAM)"
        
        # Detailed analysis
        analysis = {
            'spam_score': spam_score,
            'threshold': self.spam_threshold,
            'keyword_count': keyword_count,
            'found_keywords': found_keywords[:10],  # Limit to first 10
            'url_count': url_count,
            'excessive_capitals': bool(self.check_excessive_capitals(text)),
            'exclamation_marks': text.count('!'),
            'repeated_special_chars': bool(self.check_repeated_special_chars(text)),
            'repeated_keywords': bool(self.check_repeated_spam_keywords(text))
        }
        
        return classification, spam_score, analysis
    
    def analyze_from_file(self, filepath):
        """
        Module 1: Read email content from file
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.classify(content)
        except FileNotFoundError:
            return "Error: File not found", 0, {}
        except Exception as e:
            return f"Error: {str(e)}", 0, {}


def main():
    """Command-line interface for spam detector"""
    detector = SpamDetector()
    
    print("=" * 60)
    print("Spam Email Detection System")
    print("=" * 60)
    print("\nChoose an option:")
    print("1. Enter email text directly")
    print("2. Read from file")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        print("\nEnter email content (press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line == '':
                break
            lines.append(line)
        email_text = '\n'.join(lines)
        
        if email_text.strip():
            classification, score, analysis = detector.classify(email_text)
            print("\n" + "=" * 60)
            print("RESULT:")
            print("=" * 60)
            print(f"Classification: {classification}")
            print(f"Spam Score: {score} (Threshold: {analysis.get('threshold', 3)})")
            print(f"\nDetails:")
            print(f"  - Spam Keywords Found: {analysis.get('keyword_count', 0)}")
            if analysis.get('found_keywords'):
                print(f"  - Keywords: {', '.join(analysis['found_keywords'])}")
            print(f"  - URLs Found: {analysis.get('url_count', 0)}")
            print(f"  - Excessive Capitals: {analysis.get('excessive_capitals', False)}")
            print(f"  - Exclamation Marks: {analysis.get('exclamation_marks', 0)}")
            print(f"  - Repeated Special Chars: {analysis.get('repeated_special_chars', False)}")
            print(f"  - Repeated Spam Keywords: {analysis.get('repeated_keywords', False)}")
        else:
            print("No email content provided.")
    
    elif choice == '2':
        filepath = input("Enter file path: ").strip()
        classification, score, analysis = detector.analyze_from_file(filepath)
        
        if classification.startswith("Error"):
            print(f"\n{classification}")
        else:
            print("\n" + "=" * 60)
            print("RESULT:")
            print("=" * 60)
            print(f"Classification: {classification}")
            print(f"Spam Score: {score} (Threshold: {analysis.get('threshold', 3)})")
            print(f"\nDetails:")
            print(f"  - Spam Keywords Found: {analysis.get('keyword_count', 0)}")
            if analysis.get('found_keywords'):
                print(f"  - Keywords: {', '.join(analysis['found_keywords'])}")
            print(f"  - URLs Found: {analysis.get('url_count', 0)}")
            print(f"  - Excessive Capitals: {analysis.get('excessive_capitals', False)}")
            print(f"  - Exclamation Marks: {analysis.get('exclamation_marks', 0)}")
            print(f"  - Repeated Special Chars: {analysis.get('repeated_special_chars', False)}")
            print(f"  - Repeated Spam Keywords: {analysis.get('repeated_keywords', False)}")
    
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()

