from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

# Cores
cor_red = (141,3,51)
cor_pastel_dark = (212,178,119)
cor_black = (0,0,0)
cor_branco = (255,255,255)

def gerar_imagem_alta_definicao_com_imagem(sigla, extenso, cor_sigla, caminho_imagem, nome_arquivo_saida, cor_pastel_dark):
    largura = 900
    altura = 230
    resolucao = 300
    
    # Criar imagem transparente
    imagem = Image.new("RGBA", (largura, altura), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(imagem)

    # Referências de tamanho
    largura_texto_sigla = draw.textlength(sigla, font=fonte_principal(122))
    largura_texto_extenso = draw.textlength(extenso, font=fonte_secundaria(20))
    
    # Inserir uma imagem pré-definida
    brasao = Image.open(caminho_imagem).convert("RGBA")
    largura_brasao = 190
    altura_brasao = 190
    x_brasao = 10
    y_brasao = 5
    brasao = brasao.resize((largura_brasao, altura_brasao))
    imagem.paste(brasao, (x_brasao, y_brasao), brasao)
    
    # Desenhar um círculo ao redor da imagem
    raio = 95
    centro_x = x_brasao + 95
    centro_y = 99
    draw.ellipse((centro_x - raio, centro_y - raio, centro_x + raio, centro_y + raio),
                 outline=cor_pastel_dark, width=6)

    # Desenhar uma linha
    x0_linha = 190
    if largura_texto_extenso > largura_texto_sigla + 70:
        x1_linha = x0_linha + largura_texto_sigla + 80
    else:
        x1_linha = x0_linha + largura_texto_sigla + 40

    largura_linha = x1_linha - x0_linha
    draw.line([(x0_linha, 140),
               (x1_linha, 140)],
               fill=cor_pastel_dark,
               width=5)
    
    # Converter a sigla para maiúsculas
    sigla = sigla.lower()

    # Inserir sigla
    x0_sigla = 210
    draw.text((x0_sigla, 3), sigla, font=fonte_principal(122), fill=cor_sigla)
    
    # Converter o nome por extenso para maiúsculas
    extenso = extenso.upper()

    # Inserir nome por extenso
    if largura_texto_extenso > largura_linha - 20:
        words = extenso.split()
        c = 0
        texto_incremental = ""
        texto_incremental_2 = ""
        while draw.textlength(texto_incremental, font=fonte_secundaria(20)) < largura_linha - 150:
            texto_incremental += words[c] + " "
            c += 1
        
        largura_incremental = draw.textlength(texto_incremental, font=fonte_secundaria(20))

        if largura_incremental > largura_linha - 30:
            while c < len(words) and draw.textlength(texto_incremental_2, font=fonte_secundaria(20)) < largura_linha - 150:
                texto_incremental_2 += words[c] + " "
                c += 1


        novo_extenso = texto_incremental + '\n'
        if texto_incremental_2:
            novo_extenso += texto_incremental_2 + '\n'
        for w in words[c:]:
            novo_extenso += w + " "

        draw.text((x0_sigla + 7, 152), novo_extenso, font=fonte_secundaria(20), fill="black")
    else:
        draw.text((x0_sigla + 7, 152), extenso, font=fonte_secundaria(20), fill="black")
    
    imagem.save(nome_arquivo_saida + ".png", dpi=(resolucao, resolucao), format="PNG", optimize=True)

def fonte_principal(sz):
    # Função para definir a fonte principal
    return ImageFont.truetype("assets/Montserrat-Bold.ttf", size=sz)

def fonte_secundaria(sz):
    # Função para definir a fonte secundária
    return ImageFont.truetype("assets/Montserrat-SemiBold.ttf", size=sz)

# Rota para a página inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sigla = request.form['sigla']
        extenso = request.form['extenso']
        cor_escolhida = request.form['cor']

        if cor_escolhida == 'black':
            cor_sigla = cor_black
            cor_name = 'preto'
        elif cor_escolhida == 'red':
            cor_sigla = cor_red
            cor_name = 'vermelho'
        else:
            # Padrão para cor preta
            cor_sigla = cor_black
            cor_name = 'preto'
        
        caminho_imagem = 'assets/brasao-normal.png'
        nome_do_arquivo = f"{sigla}_{cor_name}"
        gerar_imagem_alta_definicao_com_imagem(sigla, extenso, cor_sigla, caminho_imagem, nome_do_arquivo, cor_pastel_dark)
        return send_file(nome_do_arquivo + ".png", as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
