# Bibliotecas 
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status, Response
from models import Musica
import json
import requests
import http.client


# instanciando a api
app = FastAPI()


# constante que indica que os ids da minha base de dados equivalem a estes ids do Deezer
MUSICAS = {
    1:351595631,
    2:129231818,
    3:2355587775,
    4:2315441485
}


# base de dados
musicas = {
    1: {
        "nome_musica": "There's Nothing Holdin' Me Back",
        "ano_lancamento": 2016,
        "duracao": 3.19,
        "album": "Illuminate",
    },

    2: {
        "nome_musica": "Burning Love",
        "ano_lancamento": 1972,
        "duracao": 2.50,
        "album": "Burning Love and Hits from His Movies",
    },

    3: {
        "nome_musica": "Enchanted",
        "ano_lancamento": 2008,
        "duracao": 3.53,
        "album": 'Fearless',
    },

    4: {
        "nome_musica":"Car Keys (Ayla)",
        "ano_lancamento": 2018,
        "duracao": 1.45,
        "album": "Alok Presents Brazilian Bass - Part 1",
    }
}



@app.get('/musicas')
async def get_musicas():
    return musicas


# método get consumindo api da Ana Mária
@app.get('/musicasCantores')
async def get_musicas():
    request = requests.get("http://10.234.90.3:8000/cantores") #pega a api desejada 
    cantores = json.loads(request.content) #pega o conteudo e converte pra json

    d4  ={} #salvando o conteudo dos dicionario dentro de um novo dicionario
    for chave in cantores.keys():
        d1 = cantores[chave]
        d2 = musicas[int(chave)]
        d3 = dict(d1, **d2)
        d4[chave] = d3

    return d4


@app.get('/musicas/{id_musica}')
async def get_musicas_id(id_musica):
    # tratando o erro de quando insere-se um id inexistente 
    try:
        id_musica = int(id_musica)
        musica = musicas[id_musica]
        musica.update({"id": id_musica})
        return musica
    
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Música não encontrada')
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Por favor, inserir inteiros.')
    

# método get com id especifico consumindo a API de músicas do Deezer
@app.get('/musica_link/{id_musica}')
async def get_musicas_id(id_musica):
    # tratando o erro de quando insere-se um id inexistente 
    try:
        id_musica = int(id_musica)
        musica = musicas[id_musica]
        musica.update({"id": id_musica})

        url = f'https://deezerdevs-deezer.p.rapidapi.com/track/{MUSICAS[id_musica]}' # link da api 

        print(url)

        headers = {
            "X-RapidAPI-Key": "f7f5182486mshc35a209e947abcdp12f459jsna69f73fc791e",
            "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
        }

        res = requests.get(url, headers=headers)
 
        data = res.json()
        data_link = data["link"] # pedidno apenas o atributo link da api
        link  = {"link da música deezer:": data_link}
        return musica, link
    
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Música não encontrada')
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Por favor, inserir inteiros.')


# método post
@app.post('/musicas', status_code=status.HTTP_201_CREATED)
async def post_musica(musica: Musica):
    if musica.id not in musicas:
        next_id = len(musicas)+1
        musicas[next_id] = musica
        del musica.id
        return musica
    else:
        raise  HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Musica com o id {musica.id} já existente")


# método put
@app.put('/musicas/{id_musica}')
async def put_musica(id_musica: int, musica: Musica):
    if id_musica in musicas:
        musicas[id_musica] = musica
        musica.id = id_musica
        del musica.id
        return musica
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Musica não encontrada")
    

# método delete
@app.delete('/musicas/{id_musica}')
async def delete_musica(id_musica: int):
    if id_musica in musicas:
        del musicas[id_musica]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Essa música não existe.")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)