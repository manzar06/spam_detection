"""
Spam Email Detection System - GUI Interface
Rule-Based Spam Detection with Tkinter
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from spam_detector import SpamDetector


class SpamDetectorGUI:
    """GUI application for spam email detection"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Spam Email Detection System")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Initialize detector
        self.detector = SpamDetector()
        
        # Color scheme (avoiding purple gradient)
        self.colors = {
            'bg_primary': '#2C3E50',      # Dark blue-gray
            'bg_secondary': '#34495E',   # Medium blue-gray
            'bg_light': '#ECF0F1',       # Light gray
            'accent': '#3498DB',         # Blue
            'accent_dark': '#2980B9',    # Dark blue
            'success': '#27AE60',        # Green
            'warning': '#E67E22',        # Orange
            'danger': '#E74C3C',         # Red
            'text_light': '#FFFFFF',     # White
            'text_dark': '#2C3E50'       # Dark text
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_light'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Spam Email Detection System",
            font=('Arial', 20, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_light']
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Rule-Based Detection | No Machine Learning Required",
            font=('Arial', 10),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_light']
        )
        subtitle_label.pack()
        
        # Input section
        input_frame = tk.LabelFrame(
            main_frame,
            text="Email Content",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark'],
            padx=10,
            pady=10
        )
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Text area for email input
        self.email_text = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            width=70,
            height=15,
            font=('Arial', 11),
            bg='white',
            fg=self.colors['text_dark'],
            relief=tk.SOLID,
            borderwidth=1
        )
        self.email_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Placeholder text
        placeholder = "Enter or paste email content here...\n\nExample:\nSubject: You've Won $1,000,000!\n\nCongratulations! You have been selected to win..."
        self.email_text.insert('1.0', placeholder)
        self.email_text.config(fg='gray')
        
        def on_focus_in(event):
            if self.email_text.get('1.0', 'end-1c') == placeholder:
                self.email_text.delete('1.0', tk.END)
                self.email_text.config(fg=self.colors['text_dark'])
        
        def on_focus_out(event):
            if not self.email_text.get('1.0', 'end-1c').strip():
                self.email_text.insert('1.0', placeholder)
                self.email_text.config(fg='gray')
        
        self.email_text.bind('<FocusIn>', on_focus_in)
        self.email_text.bind('<FocusOut>', on_focus_out)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_light'])
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        btn_style = {
            'font': ('Arial', 11, 'bold'),
            'cursor': 'hand2',
            'relief': tk.RAISED,
            'borderwidth': 2,
            'padx': 20,
            'pady': 8
        }
        
        analyze_btn = tk.Button(
            button_frame,
            text="Analyze Email",
            bg=self.colors['accent'],
            fg=self.colors['text_light'],
            activebackground=self.colors['accent_dark'],
            activeforeground=self.colors['text_light'],
            command=self.analyze_email,
            **btn_style
        )
        analyze_btn.pack(side=tk.LEFT, padx=5)
        
        load_file_btn = tk.Button(
            button_frame,
            text="Load from File",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_light'],
            activebackground=self.colors['bg_primary'],
            activeforeground=self.colors['text_light'],
            command=self.load_from_file,
            **btn_style
        )
        load_file_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            bg=self.colors['warning'],
            fg=self.colors['text_light'],
            activebackground='#D35400',
            activeforeground=self.colors['text_light'],
            command=self.clear_text,
            **btn_style
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Results section
        results_frame = tk.LabelFrame(
            main_frame,
            text="Analysis Results",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dark'],
            padx=10,
            pady=10
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Result display
        self.result_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            width=70,
            height=12,
            font=('Arial', 10),
            bg='white',
            fg=self.colors['text_dark'],
            relief=tk.SOLID,
            borderwidth=1,
            state=tk.DISABLED
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_bar = tk.Label(
            main_frame,
            text="Ready | Enter email content and click 'Analyze Email'",
            font=('Arial', 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_light'],
            anchor=tk.W,
            padx=10,
            pady=5
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def get_email_content(self):
        """Get email content from text area"""
        content = self.email_text.get('1.0', tk.END).strip()
        placeholder = "Enter or paste email content here...\n\nExample:\nSubject: You've Won $1,000,000!\n\nCongratulations! You have been selected to win..."
        
        if content == placeholder or not content:
            return None
        return content
    
    def analyze_email(self):
        """Analyze the email content"""
        email_content = self.get_email_content()
        
        if not email_content:
            messagebox.showwarning("Warning", "Please enter email content to analyze.")
            return
        
        # Perform analysis
        classification, score, analysis = self.detector.classify(email_content)
        
        # Display results
        self.display_results(classification, score, analysis)
        
        # Update status
        self.status_bar.config(text=f"Analysis Complete | Result: {classification} | Score: {score}")
    
    def display_results(self, classification, score, analysis):
        """Display analysis results in the result text area"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        
        # Determine color based on classification
        if classification == "SPAM":
            result_color = self.colors['danger']
        else:
            result_color = self.colors['success']
        
        # Format results
        result_text = f"{'='*60}\n"
        result_text += f"CLASSIFICATION: {classification}\n"
        result_text += f"{'='*60}\n\n"
        
        result_text += f"Spam Score: {score:.2f} / {analysis.get('threshold', 3)}\n"
        result_text += f"Threshold: {analysis.get('threshold', 3)}\n\n"
        
        result_text += f"{'-'*60}\n"
        result_text += "DETAILED ANALYSIS:\n"
        result_text += f"{'-'*60}\n\n"
        
        result_text += f"Spam Keywords Found: {analysis.get('keyword_count', 0)}\n"
        if analysis.get('found_keywords'):
            keywords_str = ', '.join(analysis['found_keywords'])
            if len(keywords_str) > 80:
                keywords_str = keywords_str[:80] + "..."
            result_text += f"  Keywords: {keywords_str}\n"
        result_text += "\n"
        
        result_text += f"Suspicious URLs: {analysis.get('url_count', 0)}\n"
        result_text += f"Excessive Capital Letters: {'Yes' if analysis.get('excessive_capitals', False) else 'No'}\n"
        result_text += f"Exclamation Marks: {analysis.get('exclamation_marks', 0)}\n"
        result_text += f"Repeated Special Characters: {'Yes' if analysis.get('repeated_special_chars', False) else 'No'}\n"
        result_text += f"Repeated Spam Keywords: {'Yes' if analysis.get('repeated_keywords', False) else 'No'}\n"
        
        result_text += f"\n{'='*60}\n"
        result_text += "EXPLANATION:\n"
        result_text += f"{'='*60}\n\n"
        
        if classification == "SPAM":
            result_text += "This email has been classified as SPAM based on:\n"
            result_text += "- High spam keyword count\n"
            result_text += "- Suspicious patterns detected\n"
            result_text += "- Spam score exceeds threshold\n"
        else:
            result_text += "This email appears to be legitimate (HAM):\n"
            result_text += "- Low spam keyword count\n"
            result_text += "- No suspicious patterns detected\n"
            result_text += "- Spam score below threshold\n"
        
        self.result_text.insert('1.0', result_text)
        
        # Highlight classification line
        self.result_text.tag_add("classification", "2.0", "2.end")
        self.result_text.tag_config("classification", foreground=result_color, font=('Arial', 12, 'bold'))
        
        self.result_text.config(state=tk.DISABLED)
    
    def load_from_file(self):
        """Load email content from a file"""
        filepath = filedialog.askopenfilename(
            title="Select Email File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.email_text.config(state=tk.NORMAL, fg=self.colors['text_dark'])
                self.email_text.delete('1.0', tk.END)
                self.email_text.insert('1.0', content)
                self.email_text.config(state=tk.NORMAL)
                
                self.status_bar.config(text=f"File loaded: {filepath}")
                messagebox.showinfo("Success", "File loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
                self.status_bar.config(text="Error loading file")
    
    def clear_text(self):
        """Clear the email text area"""
        self.email_text.config(state=tk.NORMAL)
        self.email_text.delete('1.0', tk.END)
        self.email_text.config(state=tk.NORMAL)
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        self.status_bar.config(text="Cleared | Ready for new input")


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = SpamDetectorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

