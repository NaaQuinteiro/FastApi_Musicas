# aqui ficam os modelos da aplicação
from pydantic import BaseModel  # permite a criação de um modelo base 
from typing import Optional # Para declara algo opcional no seu código

class Musica(BaseModel): #por padrão já herda várias coisas, como validação de dados!
    id: Optional[int] = None
    nome: str
    ano_lancamento: int
    duracao: float
    album: str