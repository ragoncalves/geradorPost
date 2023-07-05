import re
import random
import cairo
import os

def criar_card(mensagem, nome_arquivo):
    largura = 1080
    altura = 1920

    imagem = cairo.ImageSurface(cairo.FORMAT_RGB24, largura, altura)
    contexto = cairo.Context(imagem)

    # Escolhe uma cor de fundo aleatória
    cor_fundo = (random.random(), random.random(), random.random())
    contexto.set_source_rgb(*cor_fundo)
    contexto.rectangle(0, 0, largura, altura)
    contexto.fill()

    # Define a fonte e o tamanho do texto
    fonte = "NEW YORK"
    tamanho_fonte = 48

    # Calcula a largura máxima do texto
    largura_maxima = largura * 0.20

    # Quebra o texto em várias linhas
    palavras = mensagem.split()
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        texto_temporario = linha_atual + " " + palavra if linha_atual else palavra
        extensao_temporaria = contexto.text_extents(texto_temporario)
        if extensao_temporaria.width < largura_maxima:
            linha_atual = texto_temporario
        else:
            linhas.append(linha_atual)
            linha_atual = palavra
    linhas.append(linha_atual)

    # Calcula a altura total ocupada pelo texto
    altura_texto = len(linhas) * (contexto.text_extents("H").height + 1.5)

    # Posiciona o texto centralizado na tela
    x = (largura - largura_maxima) / 2
    y = (altura / 2) - altura_texto * 3
   
    # Verifica se o texto ultrapassa as bordas laterais
    if y < tamanho_fonte:
        while y < tamanho_fonte and linhas:
            linhas.pop(0)
            y += contexto.text_extents(linhas[0]).height * 1.5

    # Escreve as linhas de texto
    contexto.set_source_rgb(0, 0, 0)  # Cor preta para o texto
    contexto.select_font_face(fonte, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    contexto.set_font_size(tamanho_fonte)
    for linha in linhas:
        extensao_linha = contexto.text_extents(linha)
        x_linha = x + (largura_maxima - extensao_linha.width) / 2
        contexto.move_to(x_linha, y)
        contexto.show_text(linha)
        y += extensao_linha.height * 1.5

    # Inclui a linha final centralizada, com fonte menor e transparência
    contexto.set_source_rgba(0, 0, 0, 0.4)  # Cor preta com transparência 0.4
    tamanho_fonte_menor = 30
    contexto.set_font_size(tamanho_fonte_menor)
    extensao_linha_final = contexto.text_extents("@MomentoDeLuz")
    x_linha_final = x + (largura_maxima - extensao_linha_final.width) / 2
    y_linha_final = y + extensao_linha.height * 1.5
    contexto.move_to(x_linha_final, y_linha_final)
    contexto.show_text("@MomentoDeLuz")

    imagem.write_to_png(nome_arquivo)
    
    # Salva o arquivo PNG na pasta raiz do código
    diretorio_raiz = os.getcwd()
    caminho_arquivo = os.path.join(diretorio_raiz, nome_arquivo)
    imagem.write_to_png(caminho_arquivo)

    print(diretorio_raiz)
    print(caminho_arquivo)

# Exemplo de uso
mensagem = input("Digite o texto: ")
nome_arquivo = "card.png"  # Nome do arquivo a ser salvo na pasta raiz do código

criar_card(mensagem, nome_arquivo)