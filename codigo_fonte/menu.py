import os
import subprocess
import tkinter as tk
from os import name
from datetime import date
import requests
from bs4 import BeautifulSoup
from tkinter import filedialog, messagebox
import platform
from tkinter import ttk
from PIL import Image, ImageTk
anoatual = date.today().year


def baixarsys():
    global sistema, arquitetura

    # Nome do sistema operacional
    sistema = platform.system()

    # Arquitetura do sistema (64 ou 32 bits)
    arquitetura = platform.architecture()[0]

    if name == "nt":
        sistema = "Windows"
    elif name == "posix":
        sistema = "Linux"
    else:
        print("Sistema operacional não reconhecido.")

def open_directory(path):
    if sistema == "Windows":
        subprocess.run(["explorer", path])
    elif sistema == "Linux":
        subprocess.run(["xdg-open", path])
def atualKali():
    global version, tamanho, tamanho32, torrrent_link_32bits, installer_url,torrent,link_32bits
    url = "https://www.kali.org/get-kali/#kali-installer-images"

    # Fazer a solicitação GET para a URL
    response = requests.get(url)

    # Verificar se a solicitação foi bem-sucedida (status 200)
    if response.status_code == 200:
        # Criar um objeto BeautifulSoup para analisar o conteúdo HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar o elemento com a classe "download-card recommended"
        download_card = soup.find(class_="download-card recommended")

        # header-link
        version = soup.find(class_="header-link").get_text(strip=True).replace("Changelog", "")

        # Encontrar ISO 32 bits
        download_32bit = soup.find(id="kali-installer-images__32bit")

        if download_card:
            # Extrair as informações desejadas
            installer_url = download_card.find("a")["href"]
            torrent = installer_url + ".torrent"

            link_32bits = download_32bit.find("a")["href"]
            torrrent_link_32bits = link_32bits + ".torrent"

            tamanho_element = download_card.select_one("[data-size]")
            tamanho = tamanho_element["data-size"] if tamanho_element else "Desconhecido"

            # 32 bits TAMANHO
            tamanho_element32 = download_32bit.select_one("[data-size]")
            tamanho32 = tamanho_element32["data-size"] if tamanho_element32 else "Desconhecido"
        else:
            print("Elemento não encontrado.")
    else:
        print("404 NOT FOUND")

def janela():
    # Criação da janela
    global window
    window = tk.Tk()
    window.title("ISO Kali Linux Atualizada")
    window.geometry("500x400+200+200")
    window.resizable(False, False)
    window.config(background="#1B1B1B")  # Fundo principal

  # Obter o diretório atual do script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Carregar a imagem do ícone
    icon_path = os.path.join(script_dir, "icon.png")
    icon_image = Image.open(icon_path)

    # Definir a imagem como ícone da janela
    window.iconphoto(True, ImageTk.PhotoImage(icon_image))

    # Criar espaçador à esquerda
    spacer_left = tk.Frame(window, width=10, background="#1B1B1B")
    spacer_left.pack(side=tk.LEFT, fill=tk.Y)

    # Criar espaçador à direita
    spacer_right = tk.Frame(window, width=10, background="#1B1B1B")
    spacer_right.pack(side=tk.RIGHT, fill=tk.Y)

    # Criar um Frame com a borda
    frame = tk.Frame(window, bd=2, relief="solid", background="#4F4F4F")  # Borda
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Componentes da janela
    systema_frame = tk.Frame(frame, background="#1B1B1B")
    systema_frame.pack(pady=10)
    systema_label = tk.Label(systema_frame, text="Seu Sistema é:", font=("Arial", 18, 'bold'), background="#4F4F4F",foreground="#FFFFFF")  # Texto principal
    systema_label.pack(side=tk.LEFT)
    systema_value = tk.Label(systema_frame, text=sistema + ""+arquitetura, font=("Arial", 18, 'bold'),
                             foreground="#1B1A45",background="#4F4F4F")  # Texto principal
    systema_value.pack(side=tk.LEFT)

    version_frame = tk.Frame(frame, background="#1B1B1B")
    version_frame.pack(pady=10)
    version_label = tk.Label(version_frame, text="Última Versão: ", font=("Arial", 18, 'bold'), background="#4F4F4F",
                             foreground="#FFFFFF")  # Texto principal
    version_label.pack(side=tk.LEFT)
    version_value = tk.Label(version_frame, text=version, font=("Arial", 18, 'bold'), foreground="#1B1A45",background="#4F4F4F")  # Texto principal
    version_value.pack(side=tk.LEFT)

    tamanho_frame = tk.Frame(frame, background="#4F4F4F")
    tamanho_frame.pack(pady=10)
    tamanho_label = tk.Label(tamanho_frame, text="Tamanho: ", font=("Arial", 18, 'bold'), background="#4F4F4F",
                             foreground="#FFFFFF")  # Texto principal
    tamanho_label.pack(side=tk.LEFT)

    if arquitetura == "64bit":
        tamanho_value = tk.Label(tamanho_frame, text=tamanho, font=("Arial", 18, 'bold'), foreground="#1B1A45",background="#4F4F4F")  # Texto principal
        tamanho_value.pack(side=tk.LEFT)
    else:
        tamanho_value = tk.Label(tamanho_frame, text=tamanho32, font=("Arial", 18, 'bold'), foreground="#1B1A45")  # Texto principal
        tamanho_value.pack(side=tk.LEFT)

    download_label = tk.Label(frame, text="Selecione uma Forma de Download:", font=("Arial", 18, 'bold'),
                              background="#4F4F4F", foreground="#FFFFFF")  # Texto principal
    download_label.pack(pady=10)

    button_frame = tk.Frame(frame, background="#4F4F4F")
    button_frame.pack(pady=10)

    global torrent_button
    torrent_button = tk.Button(button_frame, text="Torrent", command=download_torrent, font=("Arial", 12, 'bold'),
                               bg="#007B5F", fg="#FFFFFF", width=15)  # Botões
    torrent_button.pack(side=tk.LEFT, padx=10)

    global installer_button
    installer_button = tk.Button(button_frame, text="Download Direto", command=download_installer,
                                 font=("Arial", 12, 'bold'), bg="#007B5F", fg="#FFFFFF", width=15)  # Botões
    installer_button.pack(side=tk.LEFT, padx=10)
    # Criar uma barra de progresso
    global progress
    progress = ttk.Progressbar(window, mode="indeterminate", length=100,style="Red.Horizontal.TProgressbar")

    # Definir estilo para a barra de progresso vermelha
    window.style = ttk.Style()
    window.style.configure("Red.Horizontal.TProgressbar", foreground="red", background="red")

    # Executar a janela
    window.mainloop()



def show_progress():
    progress.start()

def hide_progress():
    progress.stop()
    progress.place_forget()

def download_torrent():
    def hide_label():
        lb.config(text="Download concluído!", font=('Arial', 20), background="grey")
        lb.after(2000, lb.destroy)

    def show_label():
        lb.config(text="Baixando.....", font=('Arial', 20), background="grey")
        lb.after(2000, hide_label)

    torrent_button.config(state=tk.DISABLED, disabledforeground='white')
    selecionar_local = filedialog.askdirectory()

    if selecionar_local:
        try:
            if sistema == "Windows" and arquitetura == "64bit":
                subprocess.run(["curl", "-o", f"{selecionar_local}\\{torrent.split('/')[-1]}", torrent],
                               shell=True)
                lb = tk.Label(window, text="Baixando.....")
                lb.pack()
                show_label()
                torrent_button.config(state=tk.NORMAL)



            elif sistema == "Linux" and arquitetura == "64bit":
                subprocess.run(["wget", torrent], shell=True)
                subprocess.run(["mv", torrent.split('/')[-1], selecionar_local], shell=True)
                lb = tk.Label(window, text="Baixando.....")
                lb.pack()
                show_label()
                torrent_button.config(state=tk.NORMAL)


            elif sistema == "Windows" and arquitetura == "32bit":
                subprocess.run(["curl", "-o", f"{selecionar_local}\\{torrent.split('/')[-1]}", torrent],
                               shell=True)
                lb = tk.Label(window, text="Baixando.....")
                lb.pack()
                show_label()
                torrent_button.config(state=tk.NORMAL)


            elif sistema == "Linux" and arquitetura == "32bit":
                subprocess.run(["wget", torrrent_link_32bits], shell=True)
                subprocess.run(["mv", torrrent_link_32bits.split('/')[-1], selecionar_local], shell=True)
                lb = tk.Label(window, text="Baixando.....")
                lb.pack()
                show_label()
                torrent_button.config(state=tk.NORMAL)



        except Exception as e:
            lb = tk.Label(window, text="Erro durante o download.", font=('Arial', 20), background="grey")
            lb.pack()
            torrent_button.config(state=tk.NORMAL)

        # Ocultar a barra de progresso
        hide_progress()




def download_installer():
    def hide_label():
        lb.config(text="Download concluído!", font=('Arial', 20), background="grey")
        lb.after(2000, lb.destroy)
    def show_label():
        lb.config(text="Baixando.....", font=('Arial', 20), background="grey")
        lb.after(2000, hide_label)


    installer_button.config(state=tk.DISABLED, disabledforeground='white')
    selecionar_local = filedialog.askdirectory()

    if selecionar_local:
        try:
            if sistema == "Windows" and arquitetura == "64bit":
                subprocess.run(["curl", "-o", f"{selecionar_local}\\{installer_url.split('/')[-1]}", installer_url], shell=True)
                lb = tk.Label(window, text="Baixando.....")
                lb.pack()
                show_label()
                torrent_button.config(state=tk.NORMAL)



            elif sistema == "Linux" and arquitetura == "64bit":
                subprocess.run(["wget", "-P", selecionar_local, installer_url], shell=True)
                lb = tk.Label(window, text="Baixando.....")
                lb.pack()
                show_label()
                torrent_button.config(state=tk.NORMAL)



            elif sistema == "Linux" and arquitetura == "32bit":
                subprocess.run(["wget", "-P", selecionar_local, link_32bits], shell=True)
                lb = tk.Label(window, text="Baixando.....")
                lb.pack()
                show_label()
                torrent_button.config(state=tk.NORMAL)



            elif sistema == "Windows" and arquitetura == "32bit":
                subprocess.run(["curl", "-o", f"{selecionar_local}\\{link_32bits.split('/')[-1]}", link_32bits], shell=True)
                lb = tk.Label(window, text="Baixando.....")
                lb.pack()
                show_label()
                torrent_button.config(state=tk.NORMAL)


        except Exception as e:
            lb = tk.Label(window, text="Baixando.....")
            lb.pack()
            show_label()
            torrent_button.config(state=tk.NORMAL)
            # Chamada da função para abrir o diretório selecionado


baixarsys()
atualKali()
janela()
