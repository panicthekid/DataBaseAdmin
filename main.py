import sys
import os
from subprocess import call
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PyQt5.uic import loadUi
from SSHLibrary import SSHLibrary
ssh = SSHLibrary()


class VentanaPrincipal(QMainWindow):#se tiene que modificar si es un dialogo

    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('main.ui', self)#carga la ventana conversor
        self.btnBackup1.clicked.connect(self.abrirBackup)
        self.btnBackup2.clicked.connect(self.abrirBackup)
        self.btnMon1.clicked.connect(self.abrirMoni)
        self.btnMon2.clicked.connect(self.abrirMoni)
        self.btnRep1.clicked.connect(self.abrirRep)
        self.btnRep2.clicked.connect(self.abrirRep)
        self.btnConectar.clicked.connect(self.conectar)
    def abrirBackup(self):
        self.close()
        otraVentana = Backup(self)
        otraVentana.show()
    def abrirMoni(self):
        self.close()
        otraVentana = Monitoreo(self)
        otraVentana.show()
    def abrirRep(self):
        self.close()
        otraVentana = Replicas(self)
        otraVentana.show()
    def conectar(self):
         host = self.txtHost.toPlainText()
         user = self.txtUserLog.toPlainText()
         pswd = self.txtPswd.toPlainText()
         time = ssh.open_connection("{}".format(host), timeout=None)
         ssh.login("{}".format(user), "{}".format(pswd))
         if time == 1:
             self.txtConectado.setText("Conexion establecida correctamente")
         else :
             self.txtConectado.setText("Conexion no establecida")

         
        
class Backup(QDialog):
        
    def __init__(self, parent=None):
        super(Backup, self).__init__(parent)
        loadUi('backup.ui', self)
        self.btnHome.clicked.connect(self.abrirHome)
        self.btnList.clicked.connect(self.listaDB)
        self.btnHacerB.clicked.connect(self.haceBackUp)

    def abrirHome(self):
        self.parent().show()
        self.close()
    def listaDB(self):
        alo = ssh.execute_command("mysql -u root --password=******* -e 'show databases' ")
        self.txtBd.setText(alo)
        
    def haceBackUp(self):
        ssh.execute_command(" mysqldump --user=root --password=******* --lock-tables --all-databases > /media/backups/allDB$(date '+%Y-%m-%d-%H:%M').sql")
        self.comBack.setText("Guardado con exito con el nombre: allDB-FECHA-HORA.sql en la ruta /media/backups")
        com = ssh.execute_command("ls -m /media/backups")
        self.txtBack.setText(com)

        
        
        
class Monitoreo(QDialog):
    def __init__(self, parent=None):
        super(Monitoreo, self).__init__(parent)
        loadUi('monitoreo.ui', self)
        self.btnHome.clicked.connect(self.abrirHome)
        self.btnStatus.clicked.connect(self.status)
        self.btnUsers.clicked.connect(self.users)
        self.btnGrants.clicked.connect(self.grants)
        self.btnBinlogs.clicked.connect(self.binlogs)
    def abrirHome(self):
        self.parent().show()
        self.close()
    def status(self):
        stat = ssh.execute_command("systemctl status mariadb |grep active")
        self.txtStatus.setText(stat)
    def users(self):
        users = ssh.execute_command("mysql -u root --password=******** -e 'select user, host from mysql.user' ")
        self.txtUsers.setText(users)
    def grants(self):
        grants = ssh.execute_command('''mysql -u root --password=******* -e "select distinct concat('SHOW GRANTS FOR ', QUOTE(user), '@', QUOTE(host), ';') as query from mysql.user;"''')
        self.txtGrants.setText(grants)
    def binlogs(self):
        binlogs = ssh.execute_command('mysql -u root --password=******* -e "SHOW BINLOG EVENTS IN "mysql-bin.000001""')
        self.txtBinlogs.setText(binlogs)

class Replicas(QDialog):
    def __init__(self, parent=None):
        super(Replicas, self).__init__(parent)
        loadUi('replicasmain.ui', self)
        self.btnHome.clicked.connect(self.abrirHome)
        self.btnMaster1.clicked.connect(self.abrirReplica1)
        self.btnMaster2.clicked.connect(self.abrirReplica2)
        self.btnMaster3.clicked.connect(self.abrirReplica3)
    def abrirHome(self):
        self.parent().show()
        self.close()
    def abrirReplica1(self):
        self.close()
        otraVentana = Replicas1(self)
        otraVentana.show()
    def abrirReplica2(self):
        self.close()
        otraVentana = Replicas2(self)
        otraVentana.show()
    def abrirReplica3(self):
        self.close()
        otraVentana = Replicas3(self)
        otraVentana.show()
        
class Replicas1(QDialog):
    def __init__(self, parent=None):
        super(Replicas1, self).__init__(parent)
        loadUi('replicas.ui', self)
        self.btnHome.clicked.connect(self.abrirHome)
        self.btnConectar1.clicked.connect(self.conexion1)
        self.btnConectar2.clicked.connect(self.conexion2)
        self.btnConectar3.clicked.connect(self.slave1)

    def abrirHome(self):
        self.parent().show()
        self.close()
        
    def conexion1(self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=****** -e 'show databases' ")
        self.txtBase1.setText(alo)
    def conexion2 (self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=****** -e 'show databases' ")
        self.txtBase2.setText(alo)

    def slave1(self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=******* -e 'show databases' ")
        self.txtBase3.setText(alo)

        
class Replicas2(QDialog):
    def __init__(self, parent=None):
        super(Replicas2, self).__init__(parent)
        loadUi('replicas2.ui', self)
        self.btnHome.clicked.connect(self.abrirHome)
        self.btnConectar1.clicked.connect(self.conexion1)
        self.btnConectar2.clicked.connect(self.conexion2)
        self.btnSlave1.clicked.connect(self.slave1)
        self.btnSlave2.clicked.connect(self.slave2)

    def abrirHome(self):
        self.parent().show()
        self.close()
        
    def conexion1(self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=****** -e 'show databases' ")
        self.txtBase1.setText(alo)
    def conexion2 (self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=****** -e 'show databases' ")
        self.txtBase2.setText(alo)
    
    def slave1(self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=centos_123 -e 'show databases' ")
        self.txtSlave1.setText(alo)
    def slave2 (self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=****** -e 'show databases' ")
        self.txtSlave2.setText(alo)
    
                
class Replicas3(QDialog):
    def __init__(self, parent=None):
        super(Replicas3, self).__init__(parent)
        loadUi('replicas3.ui', self)
        self.btnHome.clicked.connect(self.abrirHome)
        self.btnConectar1.clicked.connect(self.conexion1)
        self.btnConectar2.clicked.connect(self.conexion2)
        self.btnConectar3.clicked.connect(self.conexion3)

    def abrirHome(self):
        self.parent().show()
        self.close()
        
    def conexion1(self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=****** -e 'show databases' ")
        self.txtBase3.setText(alo)
    def conexion2 (self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=****** -e 'show databases' ")
        self.txtBase3.setText(alo)
    def conexion3 (self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=******* -e 'show databases' ")
        self.txtBase3.setText(alo)
    def slave1(self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=******* -e 'show databases' ")
        self.txtBase3.setText(alo)
    def slave2 (self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=****** -e 'show databases' ")
        self.txtBase3.setText(alo)
    def slave3 (self):
        time = ssh.open_connection("192.168.x.x", timeout=None)
        ssh.login("root", "******")
        #if time == 1:
        #     self.txtConectado2.setText("Conexion establecida correctamente")
        #else :
        #     self.txtConectado2.setText("Conexion no establecida")
        alo = ssh.execute_command("mysql -u root --password=****** -e 'show databases' ")
        self.txtBase3.setText(alo)
        
        
    
app = QApplication(sys.argv)
main = VentanaPrincipal()
main.show()
sys.exit(app.exec_())
