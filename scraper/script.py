import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("CTI Web Scraper")
        self.geometry("900x650")

        # ===== TOP BAR =====
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=10, padx=20, fill="x")

        self.url_entry = ctk.CTkEntry(
            self.top_frame,
            placeholder_text="Entrez une URL (http/https)",
            width=600
        )
        self.url_entry.pack(side="left", padx=10, pady=10, expand=True)

        self.scrape_button = ctk.CTkButton(
            self.top_frame,
            text="Lancer scan CTI",
            command=self.scrape_website
        )
        self.scrape_button.pack(side="left", padx=10, pady=10)

        # ===== RESULT AREA =====
        self.result_frame = ctk.CTkScrollableFrame(self)
        self.result_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.status = ctk.CTkLabel(
            self.result_frame,
            text="En attente d'analyse...",
            font=ctk.CTkFont(size=14, slant="italic")
        )
        self.status.pack(pady=10)

    # ================= SCRAPER =================
    def scrape_website(self):

        url = self.url_entry.get().strip()

        # clear results
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if not url.startswith("http"):
            ctk.CTkLabel(
                self.result_frame,
                text="❌ URL invalide (doit commencer par http/https)",
                text_color="red"
            ).pack(pady=10)
            return

        self.status = ctk.CTkLabel(
            self.result_frame,
            text="🔎 Analyse en cours...",
            font=ctk.CTkFont(size=14, slant="italic")
        )
        self.status.pack(pady=10)
        self.update()

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (CTI-Scraper)"
            }

            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # ===== TITLE =====
            title = soup.title.string.strip() if soup.title else "Pas de titre"

            ctk.CTkLabel(
                self.result_frame,
                text=f"📌 Titre : {title}",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=10)

            # ===== TEXT EXTRACTION =====
            paragraphs = soup.find_all("p")
            text_content = " ".join([p.get_text() for p in paragraphs])

            preview = text_content[:300] if text_content else "Aucun texte exploitable"

            ctk.CTkLabel(
                self.result_frame,
                text="🧠 Aperçu du contenu :",
                font=ctk.CTkFont(weight="bold")
            ).pack(pady=5)

            ctk.CTkLabel(
                self.result_frame,
                text=preview,
                wraplength=800,
                justify="left"
            ).pack(pady=5)

            # ===== LINKS EXTRACTION =====
            links = soup.find_all("a", href=True)

            ctk.CTkLabel(
                self.result_frame,
                text=f"🔗 Liens trouvés : {len(links)}",
                font=ctk.CTkFont(weight="bold")
            ).pack(pady=10)

            for link in links[:15]:  # limite affichage
                full_url = urljoin(url, link["href"])

                ctk.CTkLabel(
                    self.result_frame,
                    text=full_url,
                    text_color="cyan",
                    wraplength=800
                ).pack(anchor="w")

        except requests.exceptions.RequestException as e:
            ctk.CTkLabel(
                self.result_frame,
                text=f"❌ Erreur réseau : {e}",
                text_color="red"
            ).pack(pady=10)

        except Exception as e:
            ctk.CTkLabel(
                self.result_frame,
                text=f"❌ Erreur générale : {e}",
                text_color="red"
            ).pack(pady=10)


# ===== RUN APP =====
if __name__ == "__main__":
    app = App()
    app.mainloop()