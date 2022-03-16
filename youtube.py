from pytube import YouTube, Playlist
from os import path, listdir
import datetime  # usado para criar nome único

SAVE_PATH = path.join(path.expanduser("~"), "Videos")


def convert_bytes(num):
    """
    Essa funçao vai converter de B para MB.... GB... etc
    """
    step_unit = 1000.0 # foi arredondado par 1000 pois fic melhor do que 1024 p/ fzer calculo

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit


# pega o tmnho do vídem em segundos e transforma par minutos e horas
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def barra_de_progresso(stream, chunk, bytes_remaining):
    print('*', end='')  # mostra apenas o * sendo concatenado. Simula uma barra de progresso


# Se o víeo já existe no diretório, coloca-se um prefixo único para
# não sobrescrever o vido atual
def com_prefixo(yt):
    prefixo = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    yt.streams \
        .filter(progressive=True, file_extension='mp4') \
        .order_by('resolution') \
        .desc() \
        .first() \
        .download(SAVE_PATH, filename_prefix=prefixo)


# Se não tem o vídeo no diretório, não precisa de prefixo
def sem_prefixo(yt):
    yt.streams \
        .filter(progressive=True, file_extension='mp4') \
        .order_by('resolution') \
        .desc() \
        .first() \
        .download(SAVE_PATH)


def fazer_download(yt):
    tamanho = yt.streams.get_highest_resolution().filesize  # pega o tamanho do vídeo

    print('O Video tem duração de : ', convert(yt.length))
    print('O tamanho do vídeo é: ', convert_bytes(tamanho))
    print('Baixando: ', yt.title, '...')
    print('-' * 80)
    yt.register_on_progress_callback(barra_de_progresso)  # exibe a 'barra de progresso'

    # progressive=True - pega apenas resoluçao até 720, na extensão mp4
    # ordena as resoluções em ordem decrescente, apartir de 720 e pega a primeira
    # faz o download do vídeo
    for file in listdir(SAVE_PATH):
        if yt.title == file:
            # Se já existir o vido, vai baixar cum nome diferente pra não sobrescrever
            com_prefixo(yt)

        else:
            # se não existir o video, baixa ele
            sem_prefixo(yt)


def opcao1():
    print('Seu video será salvo em:', SAVE_PATH)
    link = input('Digite ou cole aqui o link do seu vídeo: ')
    try:
        yt = YouTube(link)  # cria um objeto do tipo YouTue e passa a link

        if yt.check_availability:  # se o vídeo estiver disponível para download, baixe
            fazer_download(yt)  # faz o downlod do video
            print('\nVídeo: ', yt.title, 'baixado com sucesso!!!')
        else:
            print('O vídeo não está disponível')
    except ConnectionError:
        print("Erro: ", ConnectionError)  # Erro de conexão


def opcao2():
    print('Sua playlist será salva em:', SAVE_PATH)
    link = input('Digite ou cole aqui o link da sua playlist: ')
    playlist = Playlist(link)
    maximo = (len(playlist) - len(playlist)) + 1
    for video in playlist:  # para cada video na play list
        try:
            yt = YouTube(video)

            if yt.check_availability:
                print('A Play liste tem ', len(playlist), 'video(s).')
                print('Baixando video: ', maximo, 'de', len(playlist))
                fazer_download(yt)  # faz o download dos videos
                maximo += 1
                print('Foram baixados ', len(playlist), 'video(s) com sucesso.')
                print('-' * 80)
            else:
                print('O vídeo não está disponível')

        except ConnectionError:
            print("Erro: ", ConnectionError)  # Erro de conexão


opcao = ''

while opcao != '3':
    print("""########## MENU ##########
            [1] - Baixar úico vídeo.
            [2] - Baixar uma playlist.
            [3] - Sair""")
    opcao = input('>>>>>> Qual sua opção: ')

    if opcao == '1':
        opcao1()
    elif opcao == '2':
        opcao2()
    elif opcao == '3':
        print('Finaliando...')
