from clip_client import Client
from docarray import DocumentArray
from typing import overload, Callable, Optional, Dict, Iterable, Union
# Importez le module de journalisation
import logging

# Ajoutez ces lignes au début de votre script pour configurer le niveau de journalisation
#logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger(__name__)

class ClientCrud(Client):
    def __init__(self, server: str, credential: dict = {}, **kwargs):
        super().__init__(server, credential, **kwargs)

    def delete(
        self,
        document_id,
        *,
        parameters: Optional[Dict] = None,
        on_done: Optional[Callable[['DataRequest'], None]] = None,
        on_error: Optional[Callable[['DataRequest'], None]] = None,
        on_always: Optional[Callable[['DataRequest'], None]] = None,
        prefetch: int = 100,
        **kwargs
    ) -> 'DocumentArray':
        """Delete a document with the given ID.
        :param document_id: ID of the document to be deleted.
        :param parameters: additional parameters for the delete operation.
        :param on_done: the callback function executed after successful completion of the delete operation.
        :param on_error: the callback function executed if an error occurs during the delete operation.
        :param on_always: the callback function executed after each delete operation is completed.
        :param prefetch: the number of in-flight batches made by the post() method.
        :param kwargs: Additional parameters for the delete operation.
        :return: the result of the delete operation in a DocumentArray.
        """
        # Les images à supprimer doivent être dans
        # un paramètre ids qui contient une liste
        # de ID de Document. Dans notre cas, on aura
        # toujours une seule image à supprimer.
        parameters = parameters or {}
        parameters['ids'] = [document_id]

        # Ajoutez d'autres paramètres nécessaires pour la méthode delete, par exemple, 'timeout', 'headers', etc.
        # Assurez-vous d'ajouter ces paramètres à votre signature de méthode.

        # On appelle simplement la méthode /delete
        # du serveur AnnLite
        self._client.post(
            on='/delete',
            parameters=parameters,
            on_done=on_done,
            on_error=on_error,
            on_always=on_always,
            prefetch=prefetch,
            **kwargs
        )

    def update(
            self,
            content: Optional[DocumentArray],
            *,
            parameters: Optional[Dict] = None,
            on_done: Optional[Callable[['DataRequest'], None]] = None,
            on_error: Optional[Callable[['DataRequest'], None]] = None,
            on_always: Optional[Callable[['DataRequest'], None]] = None,
            prefetch: int = 100,
            **kwargs
        ) -> 'DocumentArray':
            """Update documents.
            :param content: an iterable of content (documents or other data) to be updated.
            :param parameters: additional parameters for the update operation.
            :param on_done: the callback function executed after successful completion of the update operation.
            :param on_error: the callback function executed if an error occurs during the update operation.
            :param on_always: the callback function executed after each update operation is completed.
            :param prefetch: the number of in-flight batches made by the post() method.
            :param kwargs: Additional parameters for the update operation.
            :return: the result of the update operation in a DocumentArray.
            """
            # Implement the logic to update documents using the AnnLite server.
            # You can adapt this method based on the capabilities of your server.
            # Add necessary parameters, error handling, etc.
            # Use self._client.post() to send requests to the server.

            #logger.debug(f"Updating documents: {[doc.tags for doc in content]}")

            content = DocumentArray(content)
            parameters = parameters or {}
            # On appelle simplement la méthode /update
            # du serveur AnnLite
            self._client.post(
               on='/update',
               data=content,
               parameters=parameters,
               on_done=on_done,
               on_error=on_error,
               prefetch=prefetch,
               **kwargs
            )
