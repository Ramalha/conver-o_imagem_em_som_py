import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import pygame
import time

pygame.mixer.init()
pygame.init()

posicao_fila_audios = 0

gradient_colors = [
    (0, 0, 0), (25, 25, 25), (51, 51, 51), (76, 76, 76), (102, 102, 102),
    (127, 127, 127), (153, 153, 153), (178, 178, 178), (204, 204, 204), (229, 229, 229)
]

def mapear_para_frequencia(nivel_cinza):
    # Intervalo de tons de cinza: 1 a 10
    # Intervalo de frequências: 500 a 15000 Hz
    tonalidade = [
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10
    ]

    if 1 <= nivel_cinza <= len(tonalidade):
        return tonalidade[nivel_cinza - 1]
    else:
        return None

def converter_para_escala_cinza(cor):
    r, g, b = cor
    nivel_cinza = (r + g + b) // 3
    nivel_escala = int((nivel_cinza / 255) * 9) + 1
    return nivel_escala

def mapear_para_descricao(nivel):
    descricao_cores = [
        "Preto", "Cinza1", "Cinza2", "Cinza3", "Cinza4", "Cinza5",
        "Cinza6", "Cinza7", "Cinza8", "Branco"
    ]
    return descricao_cores[nivel - 1] if 1 <= nivel <= 10 else "Inválido"

def contar_cores_com_frequencia(imagem, tamanho_grade):
    largura, altura = imagem.size
    contagem_cores = [0] * 10
    tonalidades = [0] * 10

    for y in range(0, altura, tamanho_grade[1]):
        for x in range(0, largura, tamanho_grade[0]):
            regiao = imagem.crop((x, y, x + tamanho_grade[0], y + tamanho_grade[1]))
            cor_pixel = tuple(regiao.getdata())[0]
            nivel_cinza = converter_para_escala_cinza(cor_pixel)
            contagem_cores[nivel_cinza - 1] += 1
            tonalidades[nivel_cinza - 1] = mapear_para_frequencia(nivel_cinza)

    return contagem_cores, tonalidades

def criar_cor_hex(cor):
    return "#{:02X}{:02X}{:02X}".format(cor[0], cor[1], cor[2])

def iniciar_aplicacao():
    janela_menu.destroy()
    abrir_janela_importar()

def sair_aplicacao():
    janela_menu.destroy()

def abrir_janela_importar():
    global janela_importar
    janela_importar = TkinterDnD.Tk()
    janela_importar.title("Importar Imagem")

    # Defina a cor de fundo da janela inteira
    janela_importar.configure(bg="#44093c")

    largura_janela = 440
    altura_janela = 230
    largura_tela = janela_importar.winfo_screenwidth()
    altura_tela = janela_importar.winfo_screenheight()
    x = (largura_tela - largura_janela) // 2
    y = (altura_tela - altura_janela) // 2
    janela_importar.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

    janela_importar.configure(bg="#44093c")

    label_importar = tk.Label(janela_importar, text="Arraste a foto.jpg aqui", font=("Helvetica", 15), bg="#44093c",
                              fg="white")
    label_importar.pack(expand=True, fill="both")

    janela_importar.drop_target_register(DND_FILES)
    janela_importar.dnd_bind('<<Drop>>', on_drop)

    janela_importar.mainloop()

audio_paths = {
    1: "tonalidade_1.wav",
    2: "tonalidade_2.wav",
    3: "tonalidade_3.wav",
    4: "tonalidade_4.wav",
    5: "tonalidade_5.wav",
    6: "tonalidade_6.wav",
    7: "tonalidade_7.wav",
    8: "tonalidade_8.wav",
    9: "tonalidade_9.wav",
    10: "tonalidade_10.wav"
}

tons_selecionados = []
fila_audios_selecionados = []
def play_audio(tonalidade):
    global audio_em_execucao
    audio_path = audio_paths.get(tonalidade)
    if audio_path:
        if audio_em_execucao:
            pygame.mixer.music.stop()  # Pare qualquer áudio em execução anteriormente
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        audio_em_execucao = tonalidade


def stop_audio():
    pygame.mixer.music.stop()

def adicionar_tom_selecionado(tonalidade):
    if tonalidade not in tons_selecionados:
        tons_selecionados.append(tonalidade)
        fila_audios_selecionados.append(tonalidade)

repeticoes_desejadas = 2  # Defina o número de repetições desejadas
em_loop = False  # Inicialmente, não estamos em loop
loop_ativo = False
audio_em_execucao = None

repeticoes_atual = 0

def play_todos_audios(frame):
    global posicao_fila_audios
    global em_loop
    global loop_ativo
    global repeticoes_atual
    global repeticoes_desejadas  # Adicione esta linha

    if not loop_ativo:
        if em_loop:
            em_loop = False
            return

        repeticoes_desejadas = 2  # Defina o número de repetições desejadas sempre como 2

        if len(fila_audios_selecionados) > 0:
            if posicao_fila_audios < len(fila_audios_selecionados):
                # Reproduza o próximo áudio na fila
                play_audio(fila_audios_selecionados[posicao_fila_audios])
                posicao_fila_audios += 1

                # Configure um temporizador para chamar a função novamente após o término do áudio
                frame.after(300, play_todos_audios, frame)
            else:
                # Todos os áudios foram reproduzidos uma vez
                if repeticoes_atual < 1:
                    posicao_fila_audios = 0  # Redefina a posição para o início
                    repeticoes_atual += 1
                    play_todos_audios(frame)  # Chame a função novamente para a próxima repetição
                else:
                    # Alternar para o modo de loop contínuo após as repetições
                    em_loop = True
                    posicao_fila_audios = 0  # Redefina a posição para o início
                    play_todos_audios(frame)  # Chame a função novamente para começar o loop
    else:
        pygame.mixer.music.stop()  # Pare todos os sons
        loop_ativo = False

def gerar_som(contagem_cores, tonalidades):
    top_cores = sorted(range(len(contagem_cores)), key=lambda i: contagem_cores[i], reverse=True)[:8]

    frame_aba_audio = tk.Frame(notebook)
    notebook.add(frame_aba_audio, text="Áudio")  # Adicione uma nova aba com o nome "Áudio"

    # Configurar a cor de fundo da janela do notebook
    style = ttk.Style()
    style.configure('TNotebook', background='#44093c')  # Defina a cor de fundo do notebook

    # Defina a cor de fundo de todos os frames relacionados
    frame_aba_audio.configure(bg="#44093c")

    for i, cor_index in enumerate(top_cores):
        descricao = mapear_para_descricao(cor_index + 1)
        tonalidade = tonalidades[cor_index]
        cor_pixel = gradient_colors[cor_index]
        cor_hex = criar_cor_hex(cor_pixel)

        frame_cor_info = tk.Frame(frame_aba_audio, bg="#44093c")
        frame_cor_info.pack(anchor=tk.W, pady=11)

        retangulo_cor = tk.Canvas(frame_cor_info, bg=cor_hex, width=20, height=20, highlightthickness=0,
                                  relief="ridge")
        retangulo_cor.pack(side=tk.LEFT, padx=(0, 5))
        retangulo_cor.create_rectangle(0, 0, 20, 20, fill=cor_hex, outline="#2f3b5d")

        texto_info = tk.Label(frame_cor_info, text=f"{descricao}: Tom {tonalidade} ", font=("Helvetica", 12),
                              bg="#44093c", fg="white")
        texto_info.pack(side=tk.LEFT, anchor=tk.W)

        botao_play = tk.Button(
            frame_cor_info, text="Play",
            command=lambda t=tonalidade: (adicionar_tom_selecionado(t), play_audio(t))
        )
        botao_play.pack(side=tk.RIGHT)

    botao_play_todos = tk.Button(
        frame_aba_audio, text="Reproduzir Todos", font=("Helvetica", 13), bg="#44093c", fg="white",
        command=lambda: play_todos_audios(frame_aba_audio)  # Chame a função com o novo frame como argumento
    )
    botao_play_todos.pack(side=tk.BOTTOM, pady=10)

    # Abra a aba "Áudio" ao clicar no botão "Gerar Som"
    notebook.select(frame_aba_audio)  # Abra a aba "Áudio"


def on_drop(event): 
    global janela_analise
    global janela_importar
    global notebook
    caminho_imagem = event.data
    caminho_imagem = caminho_imagem.strip('{}')

    if caminho_imagem:
        imagem_original = Image.open(caminho_imagem)
        tamanho_grade = (10, 10)

        janela_importar.destroy()

        janela_analise = TkinterDnD.Tk()
        janela_analise.title("Análise de Pixels")

        # Criar uma instância do Notebook para abas
        largura_janela_notebook = 1100
        altura_janela_notebook = 510
        notebook = ttk.Notebook(janela_analise, width=largura_janela_notebook, height=altura_janela_notebook)
        notebook.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure('TNotebook', background='#44093c')  # Defina a cor de fundo do notebook

        # Adicione a primeira aba (Gráfico de Pizza)
        frame_aba_grafico = tk.Frame(notebook)
        notebook.add(frame_aba_grafico, text="Gráfico de Pizza")  # Adicione uma aba com o nome "Gráfico de Pizza"
        frame_aba_grafico.configure(bg="#44093c")
        contagem_cores, frequencias = contar_cores_com_frequencia(imagem_original, tamanho_grade)

        # Criação do gráfico de pizza
        total_pixels = sum(contagem_cores)
        legendoca = [f"{mapear_para_descricao(i + 1)} - {contagem_cores[i] / total_pixels * 100:.2f}%" for i in
                     range(10)]

        # Defina normalized_colors aqui ou use a variável gradient_colors diretamente
        normalized_colors = [(r / 255, g / 255, b / 255) for r, g, b in gradient_colors]

        fig, ax = plt.subplots(figsize=(7, 2), facecolor="#44093c")  # Configura a cor de fundo do gráfico
        wedges, _ = ax.pie(contagem_cores, colors=normalized_colors, wedgeprops={'edgecolor': '#2f3b5d'})
        ax.set_title("Distribuição de Cores Em %", color="white")

        # Incorpora o gráfico na interface Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame_aba_grafico)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=False)  # Aumente o valor de 'expand'

        # Ajuste o posicionamento da legenda
        plt.legend(wedges, legendoca, title="Pixels em Escala", loc="lower right", bbox_to_anchor=(1, -0, 0.5, 1))

        # Criação do Frame para os retângulos de cores e informações
        frame_cores_info = tk.Frame(frame_aba_grafico, bg="#44093c")
        frame_cores_info.pack(side=tk.LEFT, padx=8, pady=10, fill=tk.Y)

        # Criação dos retângulos de cores e informações
        for nivel, quantidade in enumerate(contagem_cores):  # Substitua "contagem" por "contagem_cores"
            descricao = mapear_para_descricao(nivel + 1)
            cor_pixel = gradient_colors[nivel]
            cor_hex = criar_cor_hex(cor_pixel)

            frame_cor_info = tk.Frame(frame_cores_info, bg="#44093c")
            frame_cor_info.pack(anchor=tk.W, pady=11)

            retangulo_cor = tk.Canvas(frame_cor_info, bg=cor_hex, width=20, height=20, highlightthickness=0,
                                      relief="ridge")
            retangulo_cor.pack(side=tk.LEFT, padx=(0, 5))
            retangulo_cor.create_rectangle(0, 0, 20, 20, fill=cor_hex, outline="#2f3b5d")

            texto_info = tk.Label(frame_cor_info, text=f"{descricao}: {quantidade} - pixels", font=("Helvetica", 12),
                                  bg="#44093c", fg="white")
            texto_info.pack(side=tk.LEFT, anchor=tk.W)

        # Botão para gerar som
        botao_gerar_som = tk.Button(frame_aba_grafico, text="Gerar Som", font=("Helvetica", 13), bg="#44093c", fg="white",
                                    command=lambda: gerar_som(contagem_cores, frequencias))
        botao_gerar_som.pack(side=tk.BOTTOM, pady=10)

        janela_analise.mainloop()

janela_menu = TkinterDnD.Tk()
janela_menu.title("Menu")

largura_janela_menu = 240
altura_janela_menu = 150
largura_tela = janela_menu.winfo_screenwidth()
altura_tela = janela_menu.winfo_screenheight()
x = (largura_tela - largura_janela_menu) // 2
y = (altura_tela - altura_janela_menu) // 2
janela_menu.geometry(f"{largura_janela_menu}x{altura_janela_menu}+{x}+{y}")

janela_menu.configure(bg="#44093c")

botao_iniciar = tk.Button(janela_menu, text="Iniciar", font=("Helvetica", 16), bg="#44093c", fg="white",
                          command=iniciar_aplicacao)
botao_iniciar.pack(pady=20)

botao_sair = tk.Button(janela_menu, text="Sair", font=("Helvetica", 16), bg="#44093c", fg="white",
                       command=sair_aplicacao)
botao_sair.pack()

janela_menu.mainloop()
