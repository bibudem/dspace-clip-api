from clip_client import Client
from docarray import DocumentArray
from typing import overload, Callable, Optional, Dict, Iterable, Union
from annlite.executor import AnnLiteIndexer

class ClientCrud(Client):
    def __init__(self, server: str, credential: dict = {}, **kwargs):
        super().__init__(server, credential, **kwargs)

    @overload
    def delete(
        self,
        content: Union['DocumentArray', Iterable['Document']],
        *,
        batch_size: Optional[int] = None,
        show_progress: bool = False,
        parameters: Optional[Dict] = None,
        on_done: Optional[Callable[['DataRequest'], None]] = None,
        on_error: Optional[Callable[['DataRequest'], None]] = None,
        on_always: Optional[Callable[['DataRequest'], None]] = None,
        prefetch: int = 100,
    ) -> DocumentArray:
        """Delete content.
        :param content: an iterable of content (IDs or other identifiers) to be deleted.
        :param batch_size: the number of elements in each request when sending content.
        :param show_progress: if set, show a progress bar
        :param parameters: additional parameters for the delete operation.
        :param on_done: the callback function executed after successful completion of the delete operation.
        :param on_error: the callback function executed if an error occurs during the delete operation.
        :param on_always: the callback function executed after each delete operation is completed.
        :param prefetch: the number of in-flight batches made by the post() method.
        :return: the result of the delete operation in a DocumentArray.
        """

    def delete(self, document_id, **kwargs):
        print(f"Calling delete : {document_id}")

        # Utilisez le callback on_done pour récupérer les résultats
        response = self._client.post(
            on='/delete',
            data={"document_id": document_id}
        )

        print(f"Response from delete: {response}")

        # Décomposez davantage l'objet DocumentArray
        for document in response:
            print(f"Document ID: {document}")
            print(f"Document text: {document.text}")
            print(f"Document ID: {document.id}")
            # Ajoutez d'autres informations sur le document au besoin

    def deleteAnnlite(self, document_ids, **kwargs):
        try:
            annlite_index = AnnLiteIndexer(n_dim=512, metric='cosine')
            annlite_index.index(document_ids)

            ids = document_ids
            annlite_index.delete({'ids': ids})
            assert len(annlite_index._index) == len(document_ids) - 3
            for doc_id in ids:
                assert doc_id not in annlite_index._index
        finally:
            # Mettre ces deux lignes ici, à la fin de la fonction
            annlite_index.flush()
            annlite_index.close()
