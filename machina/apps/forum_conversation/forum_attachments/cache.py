from io import BytesIO
from django.conf import settings
from django.core.cache import InvalidCacheBackendError, caches
from django.core.exceptions import ImproperlyConfigured
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.utils.datastructures import MultiValueDict
from machina.conf import settings as machina_settings


class AttachmentCache:
    def __init__(self):
        self.backend = self.get_backend()

    def get_backend(self):
        try:
            cache = caches[machina_settings.ATTACHMENT_CACHE_NAME]
        except InvalidCacheBackendError:
            raise ImproperlyConfigured(
                'The attachment cache backend ({}) is not configured'.format(
                    machina_settings.ATTACHMENT_CACHE_NAME,
                ),
            )
        return cache

    def set(self, key, files):
        files_states = {}
        for name, upload in files.items():
            state = {
                'name': upload.name,
                'size': upload.size,
                'content_type': upload.content_type,
                'charset': upload.charset,
                'content': upload.file.read(),
            }
            files_states[name] = state
            upload.file.seek(0)
        self.backend.set(key, files_states)

    def get(self, key):
        upload = None
        files_states = self.backend.get(key)
        files = MultiValueDict()
        if files_states:
            for name, state in files_states.items():
                f = BytesIO()
                f.write(state['content'])
                if state['size'] > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                    upload = TemporaryUploadedFile(
                        state['name'],
                        state['content_type'],
                        state['size'],
                        state['charset'],
                    )
                    upload.file = f
                else:
                    f = BytesIO()
                    f.write(state['content'])
                    upload = InMemoryUploadedFile(
                        file=f,
                        field_name=name,
                        name=state['name'],
                        content_type=state['content_type'],
                        size=state['size'],
                        charset=state['charset'],
                    )
                files[name] = upload
                upload.file.seek(0)
        return files

    def delete(self, key):
        self.backend.delete(key)


cache = AttachmentCache()
