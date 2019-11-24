import os
import mimetypes
import arrow
import magic
from resources import get_file_extensions

def datetimeformat(date_str):
    dt = arrow.get(date_str)
    return dt.humanize()


def file_type_magic(file, size):
    fileBuffer = file.read(size)  # Faz a leitura de todo o conteúdo do arquivo e armazena no buffer

    with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
        fileType = m.id_buffer(fileBuffer)
        m.close()
    print('\n\n-----------------------------------------------')
    print(fileType)
    return fileType


def file_extension(file, size):
    file_extension, extension = '',''

    os_file_extension = get_file_extensions()

    fileType = file_type_magic(file, size)

    if os.path.splitext(file.filename)[1]:
        extension = os.path.splitext(file.filename)[1][1::]

    #Verifico se o tipo de arquivo é válido
    if fileType in os_file_extension.keys():
        #Verifico se o nome do arquivo possui extensão
        if extension == '':
            file_extension = os_file_extension[fileType][0]
        else:
            #Verifico se a extensão está contida no tipo de arquivo válido
            if extension in os_file_extension[fileType]:
                file_extension = extension
            #Caso a extenao do arquivo esteja diferente do conteúdo, irei respeitar o conteúdo
            else:
                file_extension = os_file_extension[fileType][0]

    # else:
    #     file_extension = fileType.split('/')[1]

    return file_extension
