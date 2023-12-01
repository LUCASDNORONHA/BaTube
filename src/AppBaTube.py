from tkinter import *
from pytube import YouTube
from tkinter import ttk
from pytube.exceptions import PytubeError
import os
import threading
from tkinter import messagebox

# Definindo o número da versão
__version__ = "1.0.0"

def validar_entrada():
    """Função para validar a URL do vídeo e o diretório de destino."""
    url = entrada_url.get()
    pasta_destino = entrada_destino.get()

    if not url or not pasta_destino:
        messagebox.showerror("Erro de Validação", "Por favor, preencha todos os campos.")
        return False

    if not os.path.isdir(pasta_destino):
        messagebox.showerror("Erro de Validação", "O diretório de destino não é válido.")
        return False

    return True

def baixar_video():
    global download_em_andamento
    if download_em_andamento:
        messagebox.showinfo("Aviso", "O download já está em andamento.")
        return

    if not validar_entrada():
        return

    url = entrada_url.get()
    try:
        youtube = YouTube(url)
        pasta_destino = entrada_destino.get()
        qualidade = escolha_qualidade.get() or "highest"

        video = youtube.streams.filter(res=qualidade).first()

        if not video:
            raise PytubeError("Formato de vídeo indisponível. Escolha outra qualidade.")

        status_label.config(text="Iniciando o download...")
        botao_baixar.config(state=DISABLED)  # Desativa o botão durante o download

        def download_thread():
            global download_em_andamento
            try:
                video.download(output_path=pasta_destino)
                status_label.config(text="Download concluído!")
                messagebox.showinfo("Download Concluído", "O download foi concluído com sucesso!")
            except PytubeError as pytube_error:
                status_label.config(text=f"Erro Pytube: {str(pytube_error)}")
                messagebox.showerror("Erro Pytube", f"Ocorreu um erro durante o download: {str(pytube_error)}")
            except Exception as e:
                status_label.config(text=f"Erro: {str(e)}")
                messagebox.showerror("Erro", f"Ocorreu um erro durante o download: {str(e)}")
            finally:
                download_em_andamento = False
                botao_baixar.config(state=NORMAL)  # Ativa o botão após o download

        download_em_andamento = True
        threading.Thread(target=download_thread, daemon=True).start()

    except PytubeError as pytube_error:
        status_label.config(text=f"Erro Pytube: {str(pytube_error)}")
        messagebox.showerror("Erro Pytube", f"Ocorreu um erro ao processar o link: {str(pytube_error)}")
    except Exception as e:
        status_label.config(text=f"Erro: {str(e)}")
        messagebox.showerror("Erro", f"Ocorreu um erro ao processar o link: {str(e)}")

# Configuração da janela principal
janela = Tk()
janela.title(f"BaTube v{__version__}")  # Adiciona o número da versão à barra de título

# Definindo as dimensões da janela principal
largura_janela = 400
altura_janela = 380
pos_x = (janela.winfo_screenwidth() // 2) - (largura_janela // 2)
pos_y = (janela.winfo_screenheight() // 2) - (altura_janela // 2)
janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

# Bloqueando a capacidade de redimensionar a janela
janela.resizable(False, False)

# Adicionando ícone à barra de título
icone_path = r"C:\Users\lucas\BaTube-Project\resources\LogoIcon.ico"
janela.iconbitmap(icone_path)

# Criando e posicionando widgets
label_url = Label(janela, text="Insira o link do vídeo:")
label_url.pack(pady=10)

entrada_url = Entry(janela, width=50)
entrada_url.pack(pady=10)

label_destino = Label(janela, text="Escolha o diretório de destino:")
label_destino.pack(pady=10)

entrada_destino = Entry(janela, width=50)
entrada_destino.pack(pady=10)

# Adicionando uma opção de menu suspenso para escolher a qualidade do vídeo
label_qualidade = Label(janela, text="Escolha a qualidade:")
label_qualidade.pack(pady=10)

opcoes_qualidade = ["720p", "480p", "360p", "240p"]  # Adapte conforme necessário
escolha_qualidade = ttk.Combobox(janela, values=opcoes_qualidade)
escolha_qualidade.pack(pady=10)

botao_baixar = Button(janela, text="Baixar Vídeo", command=baixar_video)
botao_baixar.pack(pady=20)

status_label = Label(janela, text="")
status_label.pack()

# Adicionando uma variável global para controlar o estado do download
download_em_andamento = False

# Iniciar o loop da interface gráfica
janela.mainloop()
