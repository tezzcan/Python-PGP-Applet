import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import gnupg 

class WindowMain:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gpg.glade")
        self.builder.connect_signals(self)

        self.windowMain = self.builder.get_object('window')
        self.windowRecipent = self.builder.get_object('selectRecipentWindow')

        self.textView1 = self.builder.get_object('textview1')
        self.recipentList = self.builder.get_object('combo1')
        self.rec_name = self.builder.get_object('label_recipent_name')
        self.rec_id = self.builder.get_object('label_recipent_id')
        
        self.gpg = gnupg.GPG()
        self.gpg.encoding = 'utf-8'

        self.windowMain.show()
    
    def on_window_destroy(self, widget, data=None):
        Gtk.main_quit()
    
    def on_button1_clicked(self, widget,data=None):
        print('TEST')
        self.textbuffer = self.textView1.get_buffer() # get buffer for set and get

        start_iter = self.textbuffer.get_start_iter() # getting text from the view
        end_iter = self.textbuffer.get_end_iter()
        got_text = self.textbuffer.get_text(start_iter, end_iter, True)

        if got_text.startswith('-'):
            dialog = Gtk.MessageDialog(
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Decryption initiated.",
            )
            dialog.format_secondary_text("")
            dialog.run()
            dialog.destroy()

            self.decrypt(got_text)

        else:
            dialog = Gtk.MessageDialog(
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Encryption initiated.",
            )
            dialog.format_secondary_text("")
            dialog.run()
            dialog.destroy()

            self.encrypt(got_text)
    
    def on_selectRecipentWindow_show(self,widget,data=None):
        print(self.toCombo)
    
    def on_selectRecipentWindow_destroy(self,widget,data=None):
        print('DESTROY')
        #self.windowRecipent.hide()

    def on_proceedButton1_clicked(self, widget,data=None):
        print("PROCEED CALL")
        self.windowRecipent.hide()

    def on_cancelButton1_clicked(self, widget,data=None):
        self.windowRecipent.hide()
        
    def decrypt(self,pgp_data):
        self.textbuffer.set_text(str(self.gpg.decrypt(pgp_data))) # setting text to the view

    def encrypt(self,raw_data):
        public_keys = self.gpg.list_keys()
        self.toCombo = [{'uid' : "".join(key['uids']),'fingerprint' : key['fingerprint']} for key in public_keys]

        self.windowRecipent.show()


    def main(self):
        Gtk.main()

if __name__ == "__main__":
    app = WindowMain()
    app.main()