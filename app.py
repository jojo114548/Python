from flask import Flask,request,jsonify,render_template,url_for,redirect
import json ,os,uuid

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
  
def deletar_usuario(id):
  usuarios=carregar_usuarios()

  usuarios_filtrados=[usuario for usuario in usuarios if usuario.get("id")!=id]
  
  if len(usuarios)==len(usuarios_filtrados):
    return False
  try:
   with open("usuarios.json","w",encoding="utf-8") as arquivo:
     json.dump(usuarios_filtrados, arquivo,indent=4)
   return True
  except:
   return False


def atualizar_usuario(id,novos_dados):
  usuarios=carregar_usuarios()
  atualizado=False

  for usuario in usuarios:
    if usuario["id"] == id:
      usuario.update(novos_dados)  # atualiza os campos
      atualizado = True
      break

  else:
        return False
  try:
   with open("usuarios.json","w",encoding="utf-8") as arquivo:
     json.dump(usuarios, arquivo,indent=4)
   return True
  except:
   return False

@app.route("/") #caminho
def home():
   return render_template("cadastro-usuarios.html") #abrir o formulario como home (inicial)
  
@app.route("/cadastro-usuarios", methods=["POST"])
def cadastrar_usuario():

    #recuperando os dados digitados
    nome=request.form.get("nome")
    email=request.form.get("email")
    cpf=request.form.get("cpf")
    senha=request.form.get("senha")
    idade=request.form.get("idade")
    #dicionario
    usuario={
      "id":str(uuid.uuid4()),
      "nome":nome,
      "cpf":cpf,
      "email":email,
      "idade":idade,
      "senha":senha    
      }
    #adicionando o usuario na função salvar usuario e assim salvando no arquivo json 
    status=salvar_usuario(usuario)

    if status:#se salvou 
      usuario = carregar_usuarios()
      return render_template("usuario.html", usuario = usuario)
    
@app.route("/usuario/", methods=["GET"])
def buscar_usuarios():
  usuario = carregar_usuarios()
  return render_template("usuario.html", usuario = usuario)

@app.route("/usuario/json", methods=["GET"])
def buscar_usuarios_json():
    usuario = carregar_usuarios()
    return jsonify(usuario)


@app.route("/usuario/<id>",methods=["DELETE"])
def excluir_usuario(id):
  sucesso=deletar_usuario(id)
  if sucesso:
    return jsonify({"message": "Usuario deletado com sucesso"}), 200
  else:
    return jsonify({"message": "Erro ao deletar usuario"}), 400

@app.route('/usuario/<id>',methods=["PUT"])
def editar_usuario(id):
  novos_dados = request.json  
  sucesso = atualizar_usuario(id,novos_dados)
  if sucesso:
     return jsonify({"message": "Usuario atualizado com sucesso"}), 200
  else:
    return jsonify({"message": "Erro ao atualizar usuario"}), 400

@app.route('/procurar/',methods=["GET"])
def usuarios_procurar():
    nome=request.args.get("nome")
    usuarios=carregar_usuarios()

    return render_template("procurar.html",nome=nome,usuarios=usuarios,status=None)

if __name__=='__main__':
  app.run(debug=True)


