import os

S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY    = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")

#Extensões de arquivos permitidas / Tradução das extensões do sistema para a notação do usuário final
ALLOWED_EXTENSIONS = {
    'application/msword': ['doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['docx'],
    'application/vnd.oasis.opendocument.text': ['odt'],
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['xlsx'],
    'application/vnd.ms-excel': ['xls'],
    'application/vnd.oasis.opendocument.spreadsheet': ['ods'],
    'application/vnd.oasis.opendocument.presentation': ['odp'],
    'application/vnd.ms-powerpoint': ['ppt'],
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['pptx'],
    'text/markdown': ['md'],
    'text/plain': ['txt','csv'],
    'image/png': ['png'],
    'application/pdf': ['pdf'],
    'application/zip': ['zip']
}
# }{
#     'simple': [
#         'pdf', 'png', 'mp4', 'gif', 'avi',  'txt', 'bmp', 'xlm','zip', 'wav', 'md'
#     ],
#     'similar': {
#         'doc': ['docx', 'doc', 'odt'],'xls': ['xls','xlsx', 'ods'], 'jpg': ['jpg', 'jpeg', 'jpe'],
#         'ppt': ['odp',  'pptx','ppt'], 'mp3': ['mpeg', 'mpg', 'mpeg3', 'mp3']
#     }
# }