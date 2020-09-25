from Register import *
from Client_XMPP import *
from tabulate import tabulate

if __name__ == '__main__':
    server = '@redes2020.xyz'

    menu = True
    login = False
    group_joined = False

    print("*"*12,"Bienvenido","*"*12)

    menu_not_log = """\nElija una opción:
    1. Registrar un usuario
    2. Log in
    99. Salir
    """
    
    menu_log = """\nElija una opción:
    1. Registrar un usuario
    2. Log out
    3. Mostrar cuentas
    4. Eliminar cuenta
    5. Agregar usuario como contacto
    6. Mostrar detalles de una cuenta
    7. Enviar mensaje (Mensaje directo)
    8. Ingresar a un nuevo grupo
    9. Enviar mensaje (Mensaje de grupo)
    10. Definir mensaje de presencia
    11. Mostrar contactos
    12. Enviar imagen
    13. Mostrar rooms
    99. Salir
    """

    while menu:

        if not(login):
            opcion = input(menu_not_log)
        else:
            opcion = input(menu_log)


        if (opcion == '1'): 
            if (not(login)):
                print ("*"*12,"opcion 1", "*"*12,"\nEn esta opcion se crea un nuevo usuario")
                username = input('Ingrese username: ')
                password = input('Ingrese password: ')
                jid = username + server
                register = Register(jid, password)
                if register.connect():
                    register.process(block=True)
                else:
                    print("Error")
            else: 
                print('Si ya esta logeado, no puede crear otra cuenta')
            
        #Iniciar sesion o cerrar sesion
        elif (opcion == '2'):
            print ("*"*12,"opcion 2", "*"*12,"\nEn esta opcion se inicia o cierra sesion")
            #Si el usuario no se ha logeado, pide usuario y password
            if not(login):
                username = input('Ingrese username: ')
                password = input('Ingrese password: ')
                jid = username + server
                cliente = Client_XMPP(jid, password, username)
                if cliente.connect():
                    cliente.process()
                    print("Se ha logeado correctamente")
                    login = True
                else:
                    print('Error')
            else:
                if cliente.connect():
                    cliente.logout()
                    login = False

        #Mostrar cuentas
        elif opcion == '3':
            print ("*"*12,"opcion 3", "*"*12,"\nEn esta opcion se muestran cuentas")
            if login:
                list_users = cliente.show_Users()
                table = tabulate(list_users, headers=['Email', 'JID', 'Username', 'Name'], tablefmt='grid')
                print(table)
            else:
                print('No ha iniciado sesion')

        #Eliminar cuenta
        elif opcion == '4':
            print ("*"*12,"opcion 4", "*"*12,"\nEliminar cuenta")
            if login:
                cliente.delete_Account()
                login = False
            else:
                print('No ha iniciado sesion')
        
        #Eliminar cuenta
        elif opcion == '5':
            print ("*"*12,"opcion 5", "*"*12,"\nAgregar usuarios como contacto")
            if login:
                user = input("Ingrese al usuario que desea agregar como contacto: ")
                cliente.add_Contact(user+server)
            else:
                print('No ha iniciado sesion')

        #Mostrar detalles de una cuenta
        elif opcion == '6':
            print ("*"*12,"opcion 6", "*"*12,"\nMostrar detalles de una cuenta")
            if login:
                jid = input('Ingrese usuario: ')
                user = cliente.show_one(jid)
                table = tabulate(user, headers=['Email', 'JID', 'Username', 'Name'], tablefmt='grid')
                print(table)
            else:
                print('No ha iniciado sesion')

        #Enviar mensaje (Mensaje directo)
        elif opcion == '7':
            print ("*"*12,"opcion 7", "*"*12,"\nEnviar mensaje (Mensaje directo)")
            if login:
                jid = input("Destinatario: ")
                message = input("Ingrese el mensaje que desea enviarle:\n")
                cliente.send_Direct_Msg(jid, server, message)
            else:
                print('No ha iniciado sesion')

        #Entrar/crear grupo
        elif opcion == '8':
            print ("*"*12,"opcion 8", "*"*12,"\nEntrar a un grupo")
            if login:
                room = input('Ingrese el room al que desee entrar. Si este no existe, se creara uno nuevo con ese nombre.\nnombre: ')
                print(room)
                cliente.create_Room(room)
                group_joined = True
            else:
                print('No ha iniciado sesion')

        #Enviar mensaje (Mensaje grupal)
        elif opcion == '9':
            print ("*"*12,"opcion 9", "*"*12,"\nEnviar mensaje a grupo")
            if login: 
                if group_joined:
                    room = input('Ingrese el room al que desea enviar el mensaje: ')
                    msg = input('Ingrese el mensaje que desea enviarle al grupo:\n')
                    print(room)
                    cliente.send_Msg_group(room, msg)                    
                else:
                    print('Aun no pertenece a ningun grupo, entre a uno primero')
            else:
                print("No ha iniciado sesion")

        #Definir mensaje de presencia
        elif opcion == '10':
            print ("*"*12,"opcion 10", "*"*12,"\nDefinir mensaje de presencia")
            if login:
                opcion = input('Elija su estado:\n1. chat\n2. away\n3. xa\n4. dnd\n')
                msg = input ('Ingese su mensaje: ')
                cliente.change_Status(msg, opcion)
            else:
                print('No ha iniciado sesion')
        
        #Imprimir contactos
        elif opcion == '11':
            print ("*"*12,"opcion 11", "*"*12,"\nMostrar contactos")
            if login:
                list_users = cliente.show_Friends()
                table = tabulate(list_users, headers=['Jid', 'Sub type'], tablefmt='grid')
                print(table)
            else:
                print('No ha iniciado sesion')

        #Enviar imagen
        elif opcion == '12':
            print ("*"*12,"opcion 12", "*"*12,"\nEnviar imagen")
            if login:
                user = input('Destinatario: ')
                file_path = input('file path: ')
                cliente.send_File(user, server, file_path)
            else:
                print('No ha iniciado sesion')

        #Mostrar grupo
        elif opcion == '13':
            print ("*"*12,"opcion 13", "*"*12,"\nMostrar grupos")
            if login:
                rooms = cliente.show_Rooms()
            else:
                print('No ha iniciado sesion')

        #Terminar programa
        elif (opcion == '99'):
            if login:
                if cliente.connect():
                        cliente.logout()
                        login = False 
                print ('\nHa elegido salir. Gracias por utilizar el programa')
                menu = False
            else:
                menu = False
        else:
            print('\nEligió la opcion '+opcion+'. Esta opcion no es valida')