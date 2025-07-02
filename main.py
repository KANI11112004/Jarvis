import tkinter as tk
from tkinter import ttk, font
import threading
from PIL import Image, ImageTk, ImageSequence
import time
import queue
import math
import random

# Import your backend components
from Backend.chatbot import get_response
from Backend.realtime import main as realtime_main
from Backend.model import classify_query
from Backend.SpeechToText import SpeechToText
from Backend.TextToSpeech import TextToSpeech

class JarvisInterface:
    def __init__(self, master):
        self.master = master
        master.title("JARVIS")
        master.geometry("1200x800")
        master.configure(bg='#0a0a0a')
        
        # 1. Initialize style first
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # 2. Initialize state variables
        self.message_queue = queue.Queue()
        self.voice_active = True
        self.listening = False
        self.processing = False
        self.current_mode = "chat"
        self.animation_phase = 0
        self.voice_levels = [0] * 10
        
        # 3. Load assets
        self.load_assets()
        
        # 4. Create main containers
        self.main_panel = ttk.Frame(self.master, style='TFrame')
        self.main_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # 5. Create header and mode selector (outside main panel)
        self.create_header()
        self.create_mode_selector()
        
        # 6. Create both content panels (inside main panel)
        self.create_chat_panel()
        self.create_voice_panel()
        
        # 7. Create status bar (outside main panel)
        self.create_status_bar()
        
        # 8. Set initial state
        self.chat_panel.pack(fill=tk.BOTH, expand=True)
        self.show_welcome_message()
        self.check_queue()
        
    def load_assets(self):
        """Load images and animations"""
        try:
            # Load logo image
            self.logo_img = Image.open("Frontend\\logo.jpg").resize((50, 50))
            self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        except:
            # Fallback if logo not found
            self.logo_photo = self.create_placeholder_image(50, 50, '#00ffaa')
            
        # Voice animation frames
        self.voice_frames = []
        try:
            gif = Image.open("Frontend\\voice.gif")
            for frame in ImageSequence.Iterator(gif):
                frame = frame.resize((300, 300), Image.LANCZOS)
                self.voice_frames.append(ImageTk.PhotoImage(frame))
        except:
            # Fallback animation
            self.voice_frames = [self.create_placeholder_image(300, 300, '#00ffaa')]
        
        self.current_frame = 0
        
    def create_placeholder_image(self, width, height, color):
        """Create a placeholder image"""
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (width, height), '#0a0a0a')
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, width, height), fill=color)
        return ImageTk.PhotoImage(img)
    
    def speak(self, text):
        """Handle text-to-speech conversion"""
        if self.voice_active:
            TextToSpeech(text)
            
    def configure_styles(self):
        """Configure custom styles for widgets"""
        # Base styles
        self.style.configure('TFrame', background='#0a0a0a')
        self.style.configure('TLabel', background='#0a0a0a', foreground='#00ffaa')
        self.style.configure('TButton', 
                           background='#003333', 
                           foreground='#00ffaa',
                           font=('Helvetica', 10, 'bold'),
                           borderwidth=0)
        self.style.map('TButton',
                     background=[('active', '#005555'), ('selected', '#007777')],
                     foreground=[('active', '#ffffff')])
        
        # Mode selector style
        self.style.configure('Mode.TFrame', background='#111111')
        self.style.configure('Mode.TButton', 
                           background='#111111',
                           foreground='#555555',
                           font=('Helvetica', 12, 'bold'),
                           padding=10)
        self.style.map('Mode.TButton',
                     background=[('selected', '#222222')],
                     foreground=[('selected', '#00ffaa')])
        
    def create_header(self):
        """Create the header panel"""
        header_frame = ttk.Frame(self.master, style='TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # Logo
        logo_label = ttk.Label(header_frame, image=self.logo_photo)
        logo_label.pack(side=tk.LEFT)
        
        # Title
        title_font = font.Font(family='Helvetica', size=24, weight='bold')
        title_label = ttk.Label(header_frame, 
                              text="J.A.R.V.I.S", 
                              font=title_font,
                              style='TLabel')
        title_label.pack(side=tk.LEFT, padx=15)
        
        # Subtitle
        subtitle_font = font.Font(family='Helvetica', size=10)
        subtitle_label = ttk.Label(header_frame,
                                 text="Just A Rather Very Intelligent System",
                                 font=subtitle_font,
                                 style='TLabel')
        subtitle_label.pack(side=tk.LEFT, pady=(10,0))
        
        # Voice toggle
        self.voice_toggle = ttk.Button(header_frame,
                                     text="🔊 VOICE ON",
                                     command=self.toggle_voice,
                                     style='TButton')
        self.voice_toggle.pack(side=tk.RIGHT)
        
    def create_mode_selector(self):
        """Create mode selector (Chat/Voice)"""
        mode_frame = ttk.Frame(self.master, style='Mode.TFrame')
        mode_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.chat_mode_btn = ttk.Button(mode_frame,
                                      text="CHAT MODE",
                                      command=lambda: self.switch_mode("chat"),
                                      style='Mode.TButton')
        self.chat_mode_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.voice_mode_btn = ttk.Button(mode_frame,
                                       text="VOICE COMMAND",
                                       command=lambda: self.switch_mode("voice"),
                                       style='Mode.TButton')
        self.voice_mode_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Set initial button states
        self.chat_mode_btn.state(['selected'])
        self.voice_mode_btn.state(['!selected'])
        
    def create_main_panel(self):
        """Create the main panel container and show correct panel"""
        self.main_panel = ttk.Frame(self.master, style='TFrame')
        self.main_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Show the correct panel based on current mode
        if self.current_mode == "chat":
            self.chat_panel.pack(fill=tk.BOTH, expand=True)
        else:
            self.voice_panel.pack(fill=tk.BOTH, expand=True)
        
    def create_chat_panel(self):
        """Create the chat interface"""
        self.chat_panel = ttk.Frame(self.main_panel, style='TFrame')
        
        # Display area
        display_frame = ttk.Frame(self.chat_panel, style='TFrame')
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas with scrollbar
        self.canvas = tk.Canvas(display_frame, bg='#111111', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(display_frame, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create frame inside canvas
        self.text_frame = ttk.Frame(self.canvas, style='TFrame')
        self.text_frame_id = self.canvas.create_window((0, 0), window=self.text_frame, anchor='nw')
        
        # Configure scrolling
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.text_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        
        # Input area
        input_frame = ttk.Frame(self.chat_panel, style='TFrame')
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.chat_entry = ttk.Entry(input_frame, font=('Helvetica', 12))
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10))
        self.chat_entry.bind('<Return>', self.process_input)
        
        send_btn = ttk.Button(input_frame, text="SEND", command=self.process_input)
        send_btn.pack(side=tk.LEFT)
        
        self.chat_entry.focus_set()
        
    def create_voice_panel(self):
        """Create the voice command interface with enhanced visuals"""
        self.voice_panel = ttk.Frame(self.main_panel, style='TFrame')
        
        # Main container with padding
        container = ttk.Frame(self.voice_panel, style='TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Animation display with border
        self.animation_frame = ttk.Frame(container, 
                                    style='TFrame', 
                                    relief='sunken', 
                                    borderwidth=2)
        self.animation_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Voice visualization canvas with gradient background
        self.voice_canvas = tk.Canvas(self.animation_frame, 
                                    bg='#0a0a0a', 
                                    highlightthickness=0)
        self.voice_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Voice control button with improved styling
        control_frame = ttk.Frame(container, style='TFrame')
        control_frame.pack(fill=tk.X, pady=10)
        
        self.voice_btn = tk.Button(control_frame,
                                text="🎤  PRESS TO SPEAK",
                                command=self.toggle_voice_input,
                                font=('Helvetica', 14, 'bold'),
                                bg='#003333',
                                fg='#00ffaa',
                                activebackground='#005555',
                                activeforeground='#ffffff',
                                relief='raised',
                                borderwidth=3,
                                padx=20,
                                pady=10)
        self.voice_btn.pack(fill=tk.X, expand=True)
        
        # Response display with improved styling
        response_frame = ttk.Frame(container, style='TFrame')
        response_frame.pack(fill=tk.BOTH, expand=True)
        
        self.voice_response = tk.Label(response_frame,
                                    text="Waiting for your command...",
                                    wraplength=800,
                                    justify=tk.CENTER,
                                    bg='#111111',
                                    fg='#00ffaa',
                                    font=('Helvetica', 12),
                                    padx=20,
                                    pady=15,
                                    relief='ridge',
                                    borderwidth=2)
        self.voice_response.pack(fill=tk.BOTH, expand=True)
        
        # Status indicator
        self.voice_status = tk.Label(container,
                                text="System Ready",
                                bg='#0a0a0a',
                                fg='#555555',
                                font=('Helvetica', 10))
        self.voice_status.pack(fill=tk.X, pady=(10, 0))
        
        # Start animation and auto-activation
        self.update_voice_animation()
        self.master.after(1000, self.auto_activate_voice)

    def auto_activate_voice(self):
        """Automatically activate voice input when in voice mode"""
        if self.current_mode == "voice" and not self.listening and not self.processing:
            self.toggle_voice_input()
        
    def switch_mode(self, mode):
        """Switch between chat and voice modes"""
        if mode == self.current_mode:
            return
            
        self.current_mode = mode
        
        # Update button states
        self.chat_mode_btn.state(['selected' if mode == "chat" else '!selected'])
        self.voice_mode_btn.state(['selected' if mode == "voice" else '!selected'])
        
        # Switch panels
        if mode == "chat":
            self.voice_panel.pack_forget()
            self.chat_panel.pack(fill=tk.BOTH, expand=True)
        else:
            self.chat_panel.pack_forget()
            self.voice_panel.pack(fill=tk.BOTH, expand=True)
        
    def show_welcome_message(self):
        """Display initial welcome message"""
        self.add_message("JARVIS", "Initializing all systems...", 'jarvis')
        self.add_message("JARVIS", "Systems online. How may I assist you today?", 'jarvis')
        self.speak("Systems online. How may I assist you today?")
        
    def add_message(self, sender, text, msg_type='user'):
        """Add a message to the chat display"""
        # Create message frame
        msg_frame = ttk.Frame(self.text_frame, style='TFrame')
        msg_frame.pack(fill=tk.X, pady=5)
        
        # Configure colors based on message type
        if msg_type == 'jarvis':
            bg = '#112211'
            fg = '#00ffaa'
            prefix = "JARVIS: "
        elif msg_type == 'system':
            bg = '#221111'
            fg = '#ff5555'
            prefix = "SYSTEM: "
        else:
            bg = '#111122'
            fg = '#ffffff'
            prefix = "YOU: "
            
        # Create message label
        msg_label = tk.Label(msg_frame,
                           text=prefix + text,
                           wraplength=800,
                           justify=tk.LEFT,
                           bg=bg,
                           fg=fg,
                           font=('Helvetica', 12),
                           padx=15,
                           pady=10,
                           anchor='w')
        msg_label.pack(fill=tk.X)
        
        # Auto-scroll to bottom
        self.canvas.yview_moveto(1.0)
        
    def update_voice_animation(self):
        """Update the voice animation visualization"""
        if not self.voice_panel.winfo_ismapped():
            self.master.after(100, self.update_voice_animation)
            return
            
        self.voice_canvas.delete("all")
        width = self.voice_canvas.winfo_width()
        height = self.voice_canvas.winfo_height()
        
        if self.listening:
            # Animated voice visualization
            self.current_frame = (self.current_frame + 1) % len(self.voice_frames)
            img = self.voice_frames[self.current_frame]
            
            # Center the image
            x = (width - img.width()) // 2
            y = (height - img.height()) // 2
            self.voice_canvas.create_image(x, y, anchor=tk.NW, image=img)
            
            # Add pulsing circles when listening
            if self.voice_animation_active:
                for i in range(5):
                    radius = 100 + 20 * math.sin(self.animation_phase + i * math.pi/2.5)
                    alpha = int(150 + 100 * math.sin(self.animation_phase + i * math.pi/3))
                    color = f'#00ff{alpha:02x}'
                    self.voice_canvas.create_oval(
                        width//2 - radius, height//2 - radius,
                        width//2 + radius, height//2 + radius,
                        outline=color, width=2
                    )
                
                self.animation_phase += 0.1
                
            # Add voice level indicators
            if random.random() > 0.3:  # Simulate voice input
                self.voice_levels = self.voice_levels[1:] + [random.randint(1, 10)]
            
            # Draw voice level bars
            bar_width = 20
            spacing = 10
            total_width = 10 * bar_width + 9 * spacing
            start_x = (width - total_width) // 2
            
            for i, level in enumerate(self.voice_levels):
                height = level * 10
                x = start_x + i * (bar_width + spacing)
                y1 = height // 2
                y2 = -height // 2
                color = f'#00ff{55 + level * 20:02x}'
                self.voice_canvas.create_rectangle(
                    x, height // 2,
                    x + bar_width, -height // 2,
                    fill=color, outline='',
                    tags="level"
                )
        else:
            # Static visualization when not listening
            img = self.voice_frames[0]
            x = (width - img.width()) // 2
            y = (height - img.height()) // 2
            self.voice_canvas.create_image(x, y, anchor=tk.NW, image=img)
            
            # Add "ready" text
            self.voice_canvas.create_text(
                width // 2, height - 50,
                text="Ready for voice command",
                fill='#00ffaa',
                font=('Helvetica', 14)
            )
            
        self.master.after(50, self.update_voice_animation)
        
    def process_input(self, event=None):
        """Process text input in chat mode"""
        if self.current_mode != "chat":
            return
            
        query = self.chat_entry.get().strip()
        if not query or self.processing:
            return
            
        self.chat_entry.delete(0, tk.END)
        self.add_message("YOU", query)
        self.process_query(query)
        
    def toggle_voice_input(self):
        """Toggle voice input in voice mode"""
        if self.processing:
            return
            
        self.listening = not self.listening
        
        if self.listening:
            self.voice_btn.config(text="🛑 LISTENING...")
            self.voice_animation_active = True
            self.status_var.set("Listening...")
            threading.Thread(target=self.process_voice_input, daemon=True).start()
        else:
            self.voice_btn.config(text="🎤 PRESS TO SPEAK")
            self.voice_animation_active = False
            self.status_var.set("Ready")
        
    def process_voice_input(self):
        """Process voice input from microphone"""
        try:
            query = SpeechToText()
            if query:
                if self.current_mode == "chat":
                    self.message_queue.put(('add_message', "YOU", query))
                else:
                    self.message_queue.put(('voice_response', f"You: {query}"))
                self.message_queue.put(('status', "Processing..."))
                self.process_query(query)
        except Exception as e:
            self.message_queue.put(('status', f"Error: {str(e)}"))
        finally:
            self.message_queue.put(('reset_voice_btn',))
        
    def process_query(self, query):
        """Process query with backend"""
        self.processing = True
        threading.Thread(target=self._process_query_background, args=(query,), daemon=True).start()
        
    def _process_query_background(self, query):
        """Background thread for processing queries"""
        try:
            if query.lower() == 'quit':
                self.message_queue.put(('add_message', "JARVIS", "Shutting down systems...", 'jarvis'))
                self.message_queue.put(('status', "Shutting down..."))
                self.speak("Shutting down systems")
                time.sleep(1)
                self.message_queue.put(('quit',))
                return

            # Classify and process query
            classification = classify_query(query)
            
            if 'general' in classification:
                response = get_response(query)
            elif 'realtime' in classification:
                response = realtime_main(query)
            elif  'automation' in classification:
                response = "Sorry I can't do this right now."
            else:
                response = "I'm not sure how to handle that query. Please try again."
            
            # Update UI based on current mode
            if self.current_mode == "chat":
                self.message_queue.put(('add_message', "JARVIS", response, 'jarvis'))
            else:
                self.message_queue.put(('voice_response', f"JARVIS: {response}"))
                
            if self.voice_active:
                self.speak(response)
                
            # Automatically reactivate voice input in voice mode
            if self.current_mode == "voice":
                self.message_queue.put(('reactivate_voice',))
                
        except Exception as e:
            if self.current_mode == "chat":
                self.message_queue.put(('add_message', "SYSTEM", f"Error: {str(e)}", 'system'))
            else:
                self.message_queue.put(('voice_response', f"SYSTEM ERROR: {str(e)}"))
        finally:
            self.message_queue.put(('status', "Ready"))
            self.message_queue.put(('processing_done',))
        
    def toggle_voice(self):
        """Toggle voice output"""
        self.voice_active = not self.voice_active
        state = "ON" if self.voice_active else "OFF"
        self.voice_toggle.config(text=f"🔊 VOICE {state}")
        self.status_var.set(f"Voice output {state}")
        
    def check_queue(self):
        """Check for messages from background threads"""
        try:
            while True:
                msg = self.message_queue.get_nowait()
                if msg[0] == 'add_message':
                    self.add_message(*msg[1:])
                elif msg[0] == 'status':
                    self.status_var.set(msg[1])
                elif msg[0] == 'reset_voice_btn':
                    if self.current_mode == "voice":
                        self.voice_btn.config(text="🎤 PRESS TO SPEAK")
                    self.listening = False
                    self.voice_animation_active = False
                elif msg[0] == 'reactivate_voice':
                    if self.current_mode == "voice" and not self.processing:
                        self.toggle_voice_input()  # Reactivate voice input
                elif msg[0] == 'processing_done':
                    self.processing = False
                elif msg[0] == 'quit':
                    self.master.quit()
                elif msg[0] == 'voice_response':
                    self.voice_response.config(text=msg[1])
        except queue.Empty:
            pass
        finally:
            self.master.after(100, self.check_queue)
        
    def on_frame_configure(self, event):
        """Update scrollregion when frame size changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        
    def on_canvas_configure(self, event):
        """Update frame width when canvas resizes"""
        canvas_width = event.width
        self.canvas.itemconfig(self.text_frame_id, width=canvas_width)
        
    def create_status_bar(self):
        """Create the status bar at bottom"""
        self.status_var = tk.StringVar()
        self.status_var.set("System Ready")
        
        status_bar = ttk.Frame(self.master, style='TFrame')
        status_bar.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        status_label = ttk.Label(status_bar,
                               textvariable=self.status_var,
                               style='TLabel')
        status_label.pack(side=tk.LEFT)
        
        # Add a subtle progress bar
        self.progress = ttk.Progressbar(status_bar,
                                      mode='determinate',
                                      length=100,
                                      maximum=100)
        self.progress.pack(side=tk.RIGHT)
        self.animate_progress()

    def animate_progress(self):
        """Animate the progress bar"""
        if self.processing:
            self.progress['value'] = (self.progress['value'] + 5) % 100
        else:
            self.progress['value'] = 100
        self.master.after(100, self.animate_progress)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#0a0a0a')
    app = JarvisInterface(root)
    root.mainloop()