EMBEDDINGS = "GPT4AllEmbeddings"

class Embeddings():
    
    def get_GPT4AllEmbeddings(self):
        from langchain_community.embeddings import GPT4AllEmbeddings
        
        model_name = "nomic-embed-text-v1.f16.gguf"

        gpt4all_kwargs = {'allow_download': 'True'}

        return GPT4AllEmbeddings(
            model_name=model_name,
            gpt4all_kwargs=gpt4all_kwargs
        )
    
    def get_embedings(self):
        if EMBEDDINGS == "GPT4AllEmbeddings":
            self.get_GPT4AllEmbeddings()

embeddingsService = Embeddings()