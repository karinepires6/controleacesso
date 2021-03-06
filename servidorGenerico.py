import zmq
import zerorpc
import time
import sys 
#import interface_complexobd as ComplexoService

socketInterfaceBD = zerorpc.Client()
portaInterfaceBD = "5557"
socketInterfaceBD.connect("tcp://ec2-3-219-203-114.compute-1.amazonaws.com:"+portaInterfaceBD)


usuario_permitidos_predios = socketInterfaceBD.listaUsuariosPermitidosNosPredios()
usuario_permitidos_andar = socketInterfaceBD.listaUsuariosPermitidosPorAndar()
predios_disponiveis = socketInterfaceBD.listaPredios()
andares_disponiveis = socketInterfaceBD.listaUsuariosPermitidosPorAndar()


'''
usuario_permitidos_predios = ComplexoService.listaUsuariosPermitidosNosPredios()
usuario_permitidos_andar = ComplexoService.listaUsuariosPermitidosPorAndar()
predios_disponiveis = ComplexoService.listaPredios()
andares_disponiveis = ComplexoService.listaUsuariosPermitidosPorAndar()
'''
#realiza a autenticacao e liberacao do acesso ao predio ou andar
def Autentica(id_user, id_predio, id_andar, cargo):
    if id_predio == "None" and id_andar == "None":
        return {"mensagem": "Não há solicitacao de acesso para predio e nem andar", "tipoErro": 1}##erro tipo 1 não há solicitacao
    elif id_predio != "None" and id_andar == "None":
        for y in range(len(predios_disponiveis)):
            if int(id_predio) == predios_disponiveis[y].get("id_predio"):
                for x in range(len(usuario_permitidos_predios)):
                    if int(id_user) == usuario_permitidos_predios[x].get("id_usuario"):
                        return {"mensagem": "Acesso liberado no predio %s" % id_predio, "id_predio": id_predio, "tipoErro": 2} ## erro tipo 2 
                    else:
                        return {"mensagem":"%s não autorizado a acessar o predio %s" % (cargo, id_predio), "tipoErro": 3} ## erro tipo 3  
            else:
                return {"mensagem": "O predio nao existe", "tipoErro": 4} ## erro tipo 4 
    elif id_predio != "None" and id_andar != "None":
        for y in range(len(predios_disponiveis)):
            if int(id_predio) == predios_disponiveis[y].get("id_predio"):
                for x in range(len(andares_disponiveis)):
                    if int(id_andar) == andares_disponiveis[x].get("id_andar"):
                        for z in range(len(usuario_permitidos_andar)):
                            if int(id_user) == usuario_permitidos_andar[z].get("id_usuario"):
                                return {"mensagem": "Acesso liberado no predio %s, andar %s" % (id_predio, id_andar), "id_predio": id_predio, "id_andar": id_andar, "tipoErro": 5} ## erro tipo 5
                            else:
                                return {"mensagem": "Usuario %s nao possui permissao para acessar o predio %s no andar %s" % (id_user, id_predio, id_andar), "tipoErro": 6}
                    else:
                        return {"mensagem":"O Andar não existe", "tipoErro": 7}
            else:
                return {"mensagem": "O predio nao existe", "tipoErro": 4} ## erro tipo 4 
    else:
        return {"mensagem": "Acesso Invalido", "tipoErro": 8}


def main():

    while True:
        context = zmq.Context()
        porta_servidor = "5559"
        socketReceberRequisicao = context.socket(zmq.REP)
        socketReceberRequisicao.bind("tcp://*:"+ porta_servidor) 

        mensagem_Chegada = socketReceberRequisicao.recv()

        mensagem_Chegada = mensagem_Chegada.decode()
        id_user, id_predio, id_andar, cargo =  mensagem_Chegada.split()

        print("%s %s %s %s" % (id_user, id_predio, id_andar, cargo))
        print(mensagem_Chegada)
        mensagem_Saida = Autentica(id_user, id_predio, id_andar, cargo)
        

        socketReceberRequisicao.send_string("%s" % mensagem_Saida)

        socketInterfaceBD.fecharConexao()

if __name__ == "__main__":
    main()
