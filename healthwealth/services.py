from healthwealth.exceptions import HealthWealthException
from .models import Document, DocumentAccess, User
import os
import uuid


class DocumentAccessService:
    def grant_document_access(self, email, document_id):
        existing_user = User.objects.filter(email=email)
        if not existing_user:
            raise HealthWealthException(f'No user found with email {email}')
        user = existing_user.first()

        existing_document = Document.objects.filter(id=document_id)
        if not existing_document:
            raise HealthWealthException('No document found with existing ID')
        document = existing_document.first()

        current_access = DocumentAccess.objects.filter(user=user, document=document)
        if current_access:
            raise HealthWealthException(f'User {email} already has access to the document')

        DocumentAccess(user=user, document=document).save()


class DocumentService:

    def _allow_user_access(self, user, file):
        DocumentAccess(user=user, document=file).save()

    def save_file(self, user, file_form, title, description, issuer_name=None, issued_date=None, category=None):
        """
        Replace the file's original name into uuid,
        so the file won't be overwrite each other on S3.
        """

        _, file_extension = os.path.splitext(file_form.name)
        file_name = file_form.name
        file_id = uuid.uuid4()
        file_form.name = '{}{}'.format(str(file_id), file_extension)

        uploaded_file = Document(
            id=file_id,
            file_name=file_name,
            title=title,
            uploaded_by=user,
            description=description,
            category=category,
            document_url=file_form,
            file_type=file_extension,
            issuername=issuer_name,
            issueddate=issued_date,
        )

        uploaded_file.save()
        self._allow_user_access(user, uploaded_file)

        return uploaded_file
