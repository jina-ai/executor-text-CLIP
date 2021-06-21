from jina import Document, DocumentArray, Executor, requests
import torch
import clip

class ClipTextEncoder(Executor):
    """Encode text into embeddings."""

    def __init__(self,
                 model_name: str = 'ViT-B/32',
                 default_traversal_path: str = 'r',
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model, _ = clip.load(model_name, 'cpu')
        self.default_traversal_path = default_traversal_path

    @requests
    def encode(self, docs: DocumentArray, **kwargs):
        if docs:
            with torch.no_grad():
                for doc in docs:
                    input_torch_tensor = clip.tokenize(doc.content)
                    embed = self.model.encode_text(input_torch_tensor)
                    doc.embedding = embed.cpu().numpy().flatten()
            return docs
