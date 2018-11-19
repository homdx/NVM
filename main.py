from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import pymysql
import time
from functools import partial

Builder.load_file('template.kv')


def connect_db():
    return pymysql.connect(host = '52.58.142.131', user = 'nvm', password = 'nvm', db = 'nvm', charset = 'utf8')


class LoginScreen(Screen):

    def verify_credentials(self, login, password):
        
        try:
            connection = connect_db()
            mycursor = connection.cursor()
            
            if login == "" or password == "":
                label = self.ids.idsuccess
                label.text = "Пожалуйста, введите корректные данные"
            elif login != "" or password != "":
                mycursor.execute("SELECT * FROM logins WHERE login='%s' AND password ='%s'" % (login, password))
                logindata = mycursor.fetchone()
                
                if logindata is not None:
                    mycursor.execute("SELECT logins.login FROM orders \
                                      INNER JOIN logins ON orders.login_id = logins.login_id \
                                      WHERE logins.login = '%s'" % (login))
                    statusdata = mycursor.fetchone()
                    
                    if statusdata is None:
                        self.parent.current = 'search'
                    else: self.parent.current = 'status'
                    
                if logindata is None:
                    label = self.ids.idsuccess
                    label.text = "Вы ввели неверные данные"
                    
            global loginuser
            loginuser = login
                    
        except:
            label = self.ids.idsuccess
            label.text = "Произошла ошибка"
            
        finally:
            connection.close()


class SearchScreen(Screen):

    def search_auto(self, date, destination, autotype):
        connection = connect_db()
        
        global savedate
        savedate = date
        global savedestination
        savedestination = destination
        
        try:
            mycursor = connection.cursor(pymysql.cursors.DictCursor)
            mycursor.execute("SELECT * FROM cars \
                              INNER JOIN autotype ON cars.autotype_id = autotype.autotype_id \
                              INNER JOIN drivers ON cars.driver_id = drivers.driver_id \
                              WHERE cars.car_id NOT IN(SELECT car_id FROM orders) \
                              AND autotype.name = '%s'" % (autotype))
            global searchdata
            searchdata = mycursor.fetchall()
        
            if len(searchdata) != 0:
                self.parent.current = 'result' 
                
            if len(searchdata) == 0:
                label = self.ids.idsuccess
                label.text = "По вашим критериям свободного транспорта нет"
        
        except:
            label = self.ids.idsuccess
            label.text = "Произошла ошибка"
        
        finally:
            connection.close()
        
    
    def date(self):
        date = self.ids.iddate
        date.text = time.strftime('%Y-%m-%d')
        

class ResultScreen(Screen):
    
    def on_enter(self):
        self.ids.idbox.remove_widget(self.ids.idtextresult)
        resultgrid = GridLayout(rows = len(searchdata[0]))
        self.ids.idbox.add_widget(resultgrid)
        
        for i in range(len(searchdata)):
            resultgrid.add_widget(Button(text = \
            "Марка машины: " + str(searchdata[i].get('model')) + \
            ", Госномер: " + str(searchdata[i].get('gosnomer')) + \
            ", Грузоподъемность: " + str(searchdata[i].get('gruzopodemnost')) + \
            "\nВодитель: " + str(searchdata[i].get('fio')),
            on_release = partial(self.order_auto, searchdata[i].get('car_id'), searchdata[i].get('driver_id') )))


    def order_auto(self, *args):
        connection = connect_db()
        
        try:
            mycursor = connection.cursor()
            
            mycursor.execute("SELECT logins.login_id FROM logins WHERE logins.login = '%s'" % (loginuser))
            login_id = mycursor.fetchone()
            
            mycursor.execute("INSERT INTO orders (date, destination, car_id, driver_id, login_id) VALUES ('%s', '%s', '%s', '%s', '%s')" % (savedate, savedestination, args[0], args[1], login_id[0]))
            connection.commit()
            
            box = GridLayout(rows = 2, row_force_default=True, row_default_height=40)
            box.add_widget(Label(text = 'Ваша заявка принята'))
            okbutton = Button(text = 'OK')
            box.add_widget(okbutton)
            
            popup = Popup(title = 'Заявка принята', content=box, size_hint=(.4, .25), auto_dismiss=False)
            popup.open()
            
            okbutton.bind(on_press = self.go_statusscreen)
            okbutton.bind(on_release = popup.dismiss)
        
        except:
            self.ids.idbox.add_widget(Label(text = 'Произошла ошибка', color = (1,0,0,1)))
        
        finally:
            connection.close()
            
    def go_statusscreen(self, *args):
        self.manager.current = 'status'

    def on_leave(self):
        box = self.ids.idbox
        box.clear_widgets()


class StatusScreen(Screen):
    
    def on_enter(self):
        
        try:
            connection = connect_db()
            mycursor = connection.cursor(pymysql.cursors.DictCursor)
            mycursor.execute("SELECT * FROM orders \
                              INNER JOIN cars ON orders.car_id = cars.car_id \
                              INNER JOIN drivers ON orders.driver_id = drivers.driver_id \
                              INNER JOIN logins ON orders.login_id = logins.login_id \
                              WHERE logins.login = '%s';" % (loginuser))
            statusdata = mycursor.fetchall()
            
            self.ids.idstatusgrid.remove_widget(self.ids.idstatustext)
            for i in statusdata:
                self.ids.idstatusgrid.add_widget(Label(text = \
                    "Дата: " + str(i.get('date')) + \
                    ", Куда: " + str(i.get('destination')) + \
                    "\nМарка машины: " + str(i.get('model')) + \
                    ", Госномер: " + str(i.get('gosnomer')) + \
                    ", Грузоподъемность: " + str(i.get('gruzopodemnost')) + \
                    "\nВодитель: " + str(i.get('fio')),
                    size_hint = (.9, .1)))
                cancelbutton = Button(text = 'Отменить', size_hint = (.1, .1))
                self.ids.idstatusgrid.add_widget(cancelbutton)
                cancelbutton.bind(on_release = partial(self.cancel_order, str(i.get('gosnomer'))))
            
        except:
            self.ids.idstatusgrid.add_widget(Label(text = 'Произошла ошибка', color = (1,0,0,1)))
            
        finally:
            connection.close()
            
    def on_leave(self):
        grid = self.ids.idstatusgrid
        grid.clear_widgets()                

    def update_screen(self, *args):
        self.manager.current = 'status'
        
    def cancel_order(self, *args):
        
        try:
            connection = connect_db()
            mycursor = connection.cursor()
            mycursor.execute("DELETE orders FROM orders \
                              INNER JOIN cars ON cars.car_id = orders.car_id \
                              WHERE cars.gosnomer = '%s'" % (args[0]))
            connection.commit()
            
            box = GridLayout(rows = 2, row_force_default=True, row_default_height=40)
            box.add_widget(Label(text = 'Заказ отменен'))
            okbutton = Button(text = 'OK')
            box.add_widget(okbutton)
            
            popup = Popup(title = 'Отмена заказа', content=box, size_hint=(.4, .25), auto_dismiss=False)
            popup.open()
            
            okbutton.bind(on_press = self.update_screen)
            okbutton.bind(on_release = popup.dismiss)
        
        except:
            pass
            
        finally:
            connection.close()
            

class NVM(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen())
        sm.add_widget(SearchScreen())
        sm.add_widget(ResultScreen())
        sm.add_widget(StatusScreen())
        return sm
        

if __name__ == '__main__':
    NVM().run()
