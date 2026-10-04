import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.signal import square
from math import pi, sin, sqrt

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Outil de Traitement d'Image et de Signal")
        self.geometry("1000x750")
        self.configure(bg="#f0f0f0")
        self.current_image = None
        self.original_image = None
        self.current_frame = None
        
        # Configuration du style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 10), padding=6)
        self.style.configure('Title.TLabel', font=('Arial', 18, 'bold'), background="#f0f0f0")
        self.style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'), background="#f0f0f0")
        self.style.configure('TFrame', background="#f0f0f0")
        self.style.configure('TEntry', padding=5)
        
        self.show_main_menu()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_main_menu(self):
        self.clear_frame()
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        self.current_frame = frame

        # Titre principal
        ttk.Label(frame, text="Outil de Traitement d'Image et de Signal", style='Title.TLabel').pack(pady=(20, 40))
        
        # Conteneur des boutons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)
        
        # Bouton Mode Image
        img_btn = ttk.Button(button_frame, text="Mode Image", command=self.show_image_mode, width=25)
        img_btn.pack(pady=10, ipady=15)
        img_btn.configure(style='Accent.TButton')
        
        # Bouton Mode Signal
        sig_btn = ttk.Button(button_frame, text="Mode Signal", command=self.show_signal_mode, width=25)
        sig_btn.pack(pady=10, ipady=15)
        sig_btn.configure(style='Accent.TButton')
        
        # Style personnalisé pour les boutons accentués
        self.style.configure('Accent.TButton', background='#4a6baf', foreground='white', 
                            font=('Arial', 12, 'bold'), padding=10)

    def show_image_mode(self):
        self.clear_frame()
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.current_frame = main_frame

        # Panneau gauche pour les contrôles
        control_frame = ttk.Frame(main_frame, width=250, style='TFrame')
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        control_frame.pack_propagate(False)

        # Panneau droit pour l'affichage de l'image
        image_frame = ttk.Frame(main_frame, style='TFrame')
        image_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Bouton Retour
        back_btn = ttk.Button(control_frame, text="← Retour au Menu", command=self.show_main_menu)
        back_btn.pack(pady=10, fill=tk.X)

        # Bouton Charger l'image
        load_btn = ttk.Button(control_frame, text="Charger une Image", command=lambda: self.load_image(display_image))
        load_btn.pack(pady=10, fill=tk.X)

        # Opérations sur l'image
        operations = [
            ("Niveaux de Gris", self.grayscale),
            ("Inverser les Couleurs", self.invert),
            ("Appliquer un Flou", self.blur),
            ("Rogner l'Image", self.crop),
            ("Afficher les Dimensions", self.show_dimensions),
            ("Afficher l'Histogramme", self.show_histogram),
            ("Égaliser l'Histogramme", self.equalize)
        ]

        for text, cmd in operations:
            btn = ttk.Button(control_frame, text=text, command=lambda c=cmd: c(display_image))
            btn.pack(pady=5, fill=tk.X)

        # Contrôles de redimensionnement
        resize_frame = ttk.LabelFrame(control_frame, text="Redimensionner l'Image", padding=10)
        resize_frame.pack(pady=10, fill=tk.X)

        ttk.Label(resize_frame, text="Largeur:").grid(row=0, column=0, sticky=tk.W)
        self.entry_width = ttk.Entry(resize_frame, width=8)
        self.entry_width.grid(row=0, column=1, padx=5)

        ttk.Label(resize_frame, text="Hauteur:").grid(row=1, column=0, sticky=tk.W)
        self.entry_height = ttk.Entry(resize_frame, width=8)
        self.entry_height.grid(row=1, column=1, padx=5)

        resize_btn = ttk.Button(resize_frame, text="Redimensionner", 
                              command=lambda: self.resize_image(display_image))
        resize_btn.grid(row=2, column=0, columnspan=2, pady=5, sticky=tk.EW)

        # Affichage de l'image
        self.image_label = ttk.Label(image_frame)
        self.image_label.pack(expand=True, pady=20)

        def display_image(img):
            if img:
                img_resized = img.resize((500, 400))
                self.current_image = img
                photo = ImageTk.PhotoImage(img_resized)
                self.image_label.configure(image=photo)
                self.image_label.image = photo

    def load_image(self, display_callback):
        path = filedialog.askopenfilename(filetypes=[("Fichiers image", "*.jpg *.png *.bmp")])
        if path:
            img = Image.open(path)
            self.original_image = img
            display_callback(img)

    def grayscale(self, display_callback):
        if self.current_image:
            gray = ImageOps.grayscale(self.current_image)
            display_callback(gray)

    def invert(self, display_callback):
        if self.current_image:
            inv = ImageOps.invert(self.current_image.convert('RGB'))
            display_callback(inv)

    def blur(self, display_callback):
        if self.current_image:
            img_cv = cv2.cvtColor(np.array(self.current_image), cv2.COLOR_RGB2BGR)
            blurred = cv2.GaussianBlur(img_cv, (7, 7), 0)
            display_callback(Image.fromarray(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)))

    def crop(self, display_callback):
        if self.current_image:
            cropped = self.current_image.crop((50, 50, 250, 250))
            display_callback(cropped)

    def resize_image(self, display_callback):
        if self.current_image:
            try:
                new_w = int(self.entry_width.get())
                new_h = int(self.entry_height.get())
                resized = self.current_image.resize((new_w, new_h))
                display_callback(resized)
            except:
                messagebox.showerror("Erreur", "Dimensions invalides")

    def show_dimensions(self, _):
        if self.current_image:
            w, h = self.current_image.size
            total = w * h
            messagebox.showinfo("Dimensions", f"Largeur: {w}\nHauteur: {h}\nPixels Totaux: {total:,}")

    def show_histogram(self, _):
        if self.current_image:
            gray = np.array(self.current_image.convert("L"))
            plt.figure(figsize=(8, 4))
            plt.hist(gray.flatten(), bins=256, range=(0, 256), color='#4a6baf')
            plt.title("Histogramme de l'Image")
            plt.xlabel("Valeur du Pixel")
            plt.ylabel("Fréquence")
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()

    def equalize(self, display_callback):
        if self.current_image:
            img_cv = cv2.cvtColor(np.array(self.current_image), cv2.COLOR_RGB2GRAY)
            eq = cv2.equalizeHist(img_cv)
            display_callback(Image.fromarray(eq))

    def show_signal_mode(self):
        self.clear_frame()
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.current_frame = main_frame

        # Panneau gauche pour les contrôles
        control_frame = ttk.Frame(main_frame, width=250, style='TFrame')
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        control_frame.pack_propagate(False)

        # Bouton Retour
        back_btn = ttk.Button(control_frame, text="← Retour au Menu", command=self.show_main_menu)
        back_btn.pack(pady=10, fill=tk.X)

        # Paramètres d'entrée
        param_frame = ttk.LabelFrame(control_frame, text="Paramètres du Signal", padding=10)
        param_frame.pack(pady=10, fill=tk.X)

        ttk.Label(param_frame, text="Fréquence:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_f = ttk.Entry(param_frame)
        self.entry_f.grid(row=0, column=1, pady=2, padx=5)

        ttk.Label(param_frame, text="Amplitude:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_a = ttk.Entry(param_frame)
        self.entry_a.grid(row=1, column=1, pady=2, padx=5)

        ttk.Label(param_frame, text="Phase (rad):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.entry_ph = ttk.Entry(param_frame)
        self.entry_ph.grid(row=2, column=1, pady=2, padx=5)

        # Contrôles pour le signal carré
        square_frame = ttk.LabelFrame(control_frame, text="Signal Carré", padding=10)
        square_frame.pack(pady=10, fill=tk.X)

        ttk.Button(square_frame, text="Afficher Signal Carré", 
                 command=lambda: self.afficher_signal(self.generer_signal())).pack(fill=tk.X, pady=2)
        ttk.Button(square_frame, text="Variations Carré", 
                 command=lambda: self.handle_variations(self.generer_signal(), np.sign, "Variations du Signal Carré")).pack(fill=tk.X, pady=2)
        ttk.Button(square_frame, text="Infos Carré", 
                 command=lambda: self.handle_infos(self.generer_signal(), np.sign)).pack(fill=tk.X, pady=2)

        # Contrôles pour le signal sinusoïdal
        sin_frame = ttk.LabelFrame(control_frame, text="Signal Sinusoïdal", padding=10)
        sin_frame.pack(pady=10, fill=tk.X)

        ttk.Button(sin_frame, text="Afficher Signal Sinusoïdal", 
                 command=lambda: self.afficher_signal(self.generer_signal(square_mode=False))).pack(fill=tk.X, pady=2)
        ttk.Button(sin_frame, text="Variations Sinusoïde", 
                 command=lambda: self.handle_variations(self.generer_signal(square_mode=False), np.sin, "Variations du Signal Sinusoïdal")).pack(fill=tk.X, pady=2)
        ttk.Button(sin_frame, text="Infos Sinusoïde", 
                 command=lambda: self.handle_infos(self.generer_signal(square_mode=False), np.sin)).pack(fill=tk.X, pady=2)

    def generer_signal(self, square_mode=True):
        try:
            f = float(self.entry_f.get())
            a = float(self.entry_a.get())
            ph = float(self.entry_ph.get())
            t = 1 / f
            temp = np.linspace(0, 2 * t, 1000)
            if square_mode:
                s = a * square(2 * np.pi * f * temp + ph)
            else:
                s = a * np.sin(2 * np.pi * f * temp + ph)
            return temp, s, f, t, a, ph
        except:
            messagebox.showerror("Erreur", "Valeurs d'entrée invalides")
            return None, None, 0, 0, 0, 0

    def afficher_signal(self, data):
        temp, s, *_ = data
        if temp is not None:
            plt.figure(figsize=(8, 4))
            plt.plot(temp, s, color='#4a6baf', linewidth=2)
            plt.title("Signal")
            plt.xlabel("Temps")
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()

    def handle_variations(self, data, func, title):
        temp, _, f, _, _, _ = data
        if temp is not None:
            amps = [2, 3, 4]
            phases = [0, pi / 4, pi / 2]
            colors = ['#4a6baf', '#af4a6b', '#6baf4a']
            
            plt.figure(figsize=(8, 4))
            for a, ph, color in zip(amps, phases, colors):
                s = a * func(2 * pi * f * temp + ph)
                plt.plot(temp, s, label=f"A={a}, φ={round(ph, 2)}", color=color)
            plt.legend()
            plt.grid(alpha=0.3)
            plt.title(title)
            plt.tight_layout()
            plt.show()

    def handle_infos(self, data, func):
        temp, s, f, t, a, ph = data
        if temp is not None:
            moyenne = np.mean(s)
            puissance = np.mean(s**2)
            efficace = sqrt(puissance)
            periodique = np.allclose(s, np.roll(s, int(t*1000)))

            temp_pair = np.linspace(-2*t, 2*t, 1000)
            w = a * func(2*pi*f*-temp_pair)
            s_sym = a * func(2*pi*f*temp_pair)
            if np.allclose(s_sym, w):
                parite = "Signal pair"
            elif np.allclose(s_sym, -w):
                parite = "Signal impair"
            else:
                parite = "Ni pair ni impair"

            info_text = (
                f"Fréquence = {f:.2f} Hz\n"
                f"Période = {t:.2f} s\n"
                f"Valeur moyenne = {moyenne:.2f}\n"
                f"Valeur efficace = {efficace:.2f}\n"
                f"Puissance = {puissance:.2f}\n"
                f"Périodique: {'Oui' if periodique else 'Non'}\n"
                f"{parite}"
            )
            
            messagebox.showinfo("Informations sur le Signal", info_text)

if __name__ == '__main__':
    app = Application()
    app.mainloop()