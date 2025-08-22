from flask import Flask,request,jsonify,render_template
import json ,os

app=Flask(__name__)

def carregar_usuarios():
    try:#Permite que o programa continue a executar mesmo quando ocorrem erros, evitando interrupções inesperadas
     if os.path.exists("usuarios.json"):
       with open("usuarios.json","r",encoding="utf-8") as arquivo:#lendo
         return json.load(arquivo)
     else:
       return [] #vazio se não existir o arquivo
    except:
      return [] #retorna vazio se der erro
    

def salvar_usuario(usuario):
  
  usuarios=carregar_usuarios()

  try:
    #adicionar novo usuario
    usuarios.append(usuario)

    with open("usuarios.json","w",encoding="utf-8") as arquivo:#criando
      json.dump(usuarios, arquivo,indent=4)

      return True #retorna true se deu tudo certo ao salvar 
  except:
    return False #se der erro ao salvar 
  
@app.route("/") #caminho
def home():
   return render_template("formulario.html") #abrir o formulario como home (inicial)
  
@app.route("/cadastro-usuarios", methods=["POST"])
def cadastrar_usuario():

    #recuperando os dados digitados
    nome=request.form.get("nome")
    email=request.form.get("email")
    idade=request.form.get("idade")
    senha=request.form.get("senha")
    #dicionario
    usuario={
      "nome":nome,
      "email":email,
      "idade":idade,
      "senha":senha    
      }
    #adicionando o usuario na função salvar usuario e assim salvando no arquivo json 
    status=salvar_usuario(usuario)

    if status:#se salvou 
       usuario=carregar_usuarios()
       return render_template("dados.html",usuario=usuario)

@app.route("/usuario",methods=["GET"])
def usuario():
  usuario=carregar_usuarios()
  return jsonify(usuario)
if __name__=='__main__':#inicia em modo desenvolvedor 
  app.run(debug=True)


