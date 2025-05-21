#!/usr/bin/env python3
"""
SignalCraft GUI - Simple graphical interface for SignalCraft
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import subprocess
import sys
import os
from pathlib import Path
import logging
from typing import List, Dict, Any
from config.config import tickers as default_tickers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import configuration
try:
    from chatgpt.client import MODEL_CONFIGS, DEFAULT_CONFIG
    from chatgpt.prompts import AVAILABLE_PROMPTS
except ImportError:
    # Fallback if imports fail
    MODEL_CONFIGS = {
        "o3-mini": {"api_type": "responses", "supports_reasoning": True},
        "gpt-4o": {"api_type": "chat_completions", "supports_reasoning": False},
        "gpt-4": {"api_type": "chat_completions", "supports_reasoning": False},
        "gpt-3.5-turbo": {"api_type": "chat_completions", "supports_reasoning": False}
    }
    DEFAULT_CONFIG = {
        "model": "o3-mini",
        "temperature": 0.9,
        "prompt_type": "market"
    }
    AVAILABLE_PROMPTS = {
        "market": "Market Analysis",
        "ticker": "Ticker Analysis",
        "sector": "Sector Analysis"
    }

class SignalCraftGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SignalCraft Control Panel")
        self.root.geometry("800x600")
        self.root.minsize(640, 480)
        
        # Set theme and styles
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a modern-looking theme
        
        # Configure styles
        self.style.configure('TButton', font=('Helvetica', 12), padding=6)
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))
        
        # Build the UI
        self._create_widgets()
        self._layout_widgets()
        
    def _create_widgets(self):
        """Create all UI widgets"""
        # Header
        self.header_frame = ttk.Frame(self.root, padding="10")
        self.header_label = ttk.Label(
            self.header_frame, 
            text="📊 SignalCraft Control Panel",
            style='Header.TLabel'
        )
        
        # Configuration section
        self.config_frame = ttk.LabelFrame(self.root, text="Configuration", padding="10")
        
        # Model selection
        self.model_label = ttk.Label(self.config_frame, text="AI Model:")
        self.model_var = tk.StringVar(value=DEFAULT_CONFIG.get("model", "o3-mini"))
        self.model_dropdown = ttk.Combobox(
            self.config_frame, 
            textvariable=self.model_var,
            values=list(MODEL_CONFIGS.keys()),
            state="readonly",
            width=20
        )
        
        # Prompt selection
        self.prompt_label = ttk.Label(self.config_frame, text="Analysis Type:")
        self.prompt_var = tk.StringVar(value=DEFAULT_CONFIG.get("prompt_type", "market"))
        self.prompt_dropdown = ttk.Combobox(
            self.config_frame, 
            textvariable=self.prompt_var,
            values=list(AVAILABLE_PROMPTS.keys()),
            state="readonly",
            width=20
        )
        
        # Temperature slider
        self.temp_label = ttk.Label(self.config_frame, text="Temperature:")
        self.temp_var = tk.DoubleVar(value=DEFAULT_CONFIG.get("temperature", 0.9))
        self.temp_slider = ttk.Scale(
            self.config_frame,
            from_=0.1,
            to=1.0,
            variable=self.temp_var,
            orient="horizontal",
            length=200
        )
        self.temp_value_label = ttk.Label(self.config_frame, text=f"{self.temp_var.get():.1f}")
        self.temp_slider.config(command=self._update_temp_label)
        
        # Ticker input section
        self.ticker_label = ttk.Label(self.config_frame, text="Tickers:")
        
        # Add checkbox for default tickers
        self.use_default_tickers_var = tk.BooleanVar(value=False)
        self.use_default_tickers_cb = ttk.Checkbutton(
            self.config_frame,
            text="Use default tickers from config.py",
            variable=self.use_default_tickers_var,
            command=self._toggle_ticker_entry
        )
        
        # Show the default tickers count
        self.default_tickers_label = ttk.Label(
            self.config_frame,
            text=f"({len(default_tickers)} tickers defined in config.py)",
            font=("Helvetica", 10, "italic")
        )
        
        self.ticker_var = tk.StringVar(value="SPY QQQ IWM")
        self.ticker_entry = ttk.Entry(
            self.config_frame, 
            textvariable=self.ticker_var,
            width=40
        )
        
        # Timeframes selection
        self.timeframe_label = ttk.Label(self.config_frame, text="Timeframes:")
        self.timeframe_vars = {
            "5m": tk.BooleanVar(value=True),
            "1h": tk.BooleanVar(value=True),
            "1d": tk.BooleanVar(value=True),
            "1wk": tk.BooleanVar(value=False),
            "1mo": tk.BooleanVar(value=False)
        }
        self.timeframe_frame = ttk.Frame(self.config_frame)
        self.timeframe_checkboxes = {}
        for tf, var in self.timeframe_vars.items():
            self.timeframe_checkboxes[tf] = ttk.Checkbutton(
                self.timeframe_frame,
                text=tf.upper(),
                variable=var
            )
        
        # Action buttons
        self.button_frame = ttk.Frame(self.root, padding="10")
        
        self.run_data_btn = ttk.Button(
            self.button_frame,
            text="1️⃣ Run Data Collection",
            command=self._run_data_collection
        )
        
        self.run_analysis_btn = ttk.Button(
            self.button_frame,
            text="2️⃣ Run AI Analysis",
            command=self._run_analysis
        )
        
        self.run_all_btn = ttk.Button(
            self.button_frame,
            text="🚀 Run Everything",
            command=self._run_all
        )
        
        # Output log
        self.log_frame = ttk.LabelFrame(self.root, text="Output Log", padding="10")
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame, 
            wrap=tk.WORD,
            height=10,
            width=80,
            font=("Courier", 10)
        )
        self.log_text.config(state=tk.DISABLED)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var,
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        
    def _layout_widgets(self):
        """Arrange widgets using grid layout"""
        # Header
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.header_label.grid(row=0, column=0)  # Changed from pack to grid
        
        # Configuration section
        self.config_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.config_frame.columnconfigure(1, weight=1)
        
        # Layout configuration widgets
        self.model_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.model_dropdown.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        self.prompt_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.prompt_dropdown.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        self.temp_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        # Use grid instead of pack for temperature widgets
        temp_frame = ttk.Frame(self.config_frame)
        temp_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        temp_frame.columnconfigure(0, weight=1)
        temp_frame.columnconfigure(1, weight=0)
        
        # Use grid instead of pack for temperature slider and label
        self.temp_slider.grid(row=0, column=0, padx=(0, 5))
        self.temp_value_label.grid(row=0, column=1)
        
        # Update the ticker section layout
        self.ticker_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.use_default_tickers_cb.grid(row=3, column=1, sticky="w", padx=5, pady=(5, 0))
        self.default_tickers_label.grid(row=4, column=1, sticky="w", padx=25, pady=(0, 5))
        self.ticker_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        
        self.timeframe_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.timeframe_frame.grid(row=6, column=1, sticky="w", padx=5, pady=5)
        
        # Use grid for timeframe checkboxes instead of pack
        for i, (tf, checkbox) in enumerate(self.timeframe_checkboxes.items()):
            checkbox.grid(row=0, column=i, padx=5)
        
        # Buttons section - use grid instead of pack
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.run_data_btn.grid(row=0, column=0, padx=5)
        self.run_analysis_btn.grid(row=0, column=1, padx=5)
        self.run_all_btn.grid(row=0, column=2, padx=5)
        
        # Log section
        self.log_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        self.log_text.grid(row=0, column=0, sticky="nsew")  # Changed from pack to grid
        
        # Status bar
        self.status_bar.grid(row=4, column=0, sticky="ew")
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(3, weight=1)
        
        # Make log frame expandable
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)
        
        # Make header frame expandable
        self.header_frame.columnconfigure(0, weight=1)
        
    def _update_temp_label(self, value=None):
        """Update temperature value label when slider moves"""
        self.temp_value_label.config(text=f"{self.temp_var.get():.1f}")
        
    def _log(self, message):
        """Add message to log with timestamp"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        logger.info(message)
        
    def _set_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def _get_selected_timeframes(self) -> List[str]:
        """Get list of selected timeframes"""
        return [tf for tf, var in self.timeframe_vars.items() if var.get()]
        
    def _run_command(self, cmd, description):
        """Run a command in a separate thread and capture output"""
        self._set_status(f"Running: {description}...")
        self._log(f"Starting: {description}")
        self._log(f"Command: {' '.join(cmd)}")
        
        def run():
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    if line:
                        self._log(line.strip())
                
                return_code = process.wait()
                
                if return_code == 0:
                    self._log(f"✅ {description} completed successfully!")
                    self._set_status(f"{description} completed")
                else:
                    self._log(f"❌ {description} failed with code {return_code}")
                    self._set_status(f"{description} failed")
            
            except Exception as e:
                self._log(f"❌ Error during {description}: {str(e)}")
                self._set_status(f"Error: {str(e)}")
        
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        
    def _run_data_collection(self):
        """Run data collection using main.py"""
        timeframes = self._get_selected_timeframes()
        
        # Get tickers based on checkbox selection
        use_defaults = self.use_default_tickers_var.get()
        if use_defaults:
            # Don't need to specify tickers, main.py will use defaults
            tickers = []
            self._log(f"Using default tickers from config.py ({len(default_tickers)} tickers)")
        else:
            tickers = self.ticker_var.get().strip().split()
            if not tickers:
                messagebox.showwarning("Warning", "Please enter at least one ticker")
                return
    
        if not timeframes:
            messagebox.showwarning("Warning", "Please select at least one timeframe")
            return
            
        # Build command
        cmd = [
            sys.executable, 
            "main.py",
            "-tf", *timeframes
        ]
        
        # Only add tickers if custom ones are specified
        if tickers and not use_defaults:
            cmd.extend(["-t", *tickers])
        
        # Run command
        self._run_command(cmd, "Data Collection")
        
    def _run_analysis(self):
        """Run AI analysis using run_narration_test.py"""
        model = self.model_var.get()
        prompt_type = self.prompt_var.get()
        temperature = self.temp_var.get()
        timeframes = [tf.upper() for tf in self._get_selected_timeframes()]
        
        if not timeframes:
            messagebox.showwarning("Warning", "Please select at least one timeframe")
            return
            
        # Build command
        cmd = [
            sys.executable,
            "run_narration_test.py",
            "-m", model,
            "-p", prompt_type,
            "--temp", str(temperature),
            "-t", *timeframes
        ]
        
        # Run command
        self._run_command(cmd, "AI Analysis")
    
    def _run_all(self):
        """Run data collection followed by analysis"""
        self._run_data_collection()
        # Wait a bit before running analysis to ensure data collection has started
        self.root.after(2000, self._run_analysis)
    
    def _toggle_ticker_entry(self):
        """Enable or disable ticker entry based on checkbox state"""
        if self.use_default_tickers_var.get():
            self.ticker_entry.configure(state="disabled")
            # Show a few sample tickers
            sample_tickers = default_tickers[:5] if len(default_tickers) > 5 else default_tickers
            self.ticker_var.set(f"Using {len(default_tickers)} tickers from config.py")
        else:
            self.ticker_entry.configure(state="normal")
            # Reset to default examples if field was empty
            if not self.ticker_var.get() or "Using" in self.ticker_var.get():
                self.ticker_var.set("SPY QQQ IWM")
    
    def _include_full_data(self, file_path, max_rows=100):
        """Read and format data from CSV file for inclusion in the prompt"""
        try:
            import pandas as pd
            df = pd.read_csv(file_path)
            
            # Truncate if file is too large to fit in context window
            if len(df) > max_rows:
                self._log(f"File has {len(df)} rows, truncating to {max_rows}")
                df = df.head(max_rows)
            
            # Format data nicely as a table
            formatted_data = f"Raw data from {file_path.name}:\n```\n"
            formatted_data += df.to_string(index=False)
            formatted_data += "\n```"
            
            return formatted_data
        except Exception as e:
            error_msg = f"Error reading {file_path}: {str(e)}"
            self._log(error_msg)
            return error_msg

def main():
    """Main entry point for the GUI application"""
    root = tk.Tk()
    app = SignalCraftGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()