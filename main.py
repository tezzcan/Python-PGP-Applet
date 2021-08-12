import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import AppIndicator3 as AppIndicator

import gnupg 

class WindowMain:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gpg.glade")
        self.builder.connect_signals(self)

        self.indicator = AppIndicator.Indicator.new(
            "menu-indicator", "calendar-tray", AppIndicator.IndicatorCategory.OTHER
        )
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)


        self.windowMain = self.builder.get_object('window')
        self.windowRecipent = self.builder.get_object('selectRecipentWindow')
        self.about = self.builder.get_object('about_dialog')

        self.textView1 = self.builder.get_object('textview1')
        self.recipentList = self.builder.get_object('combo1')
        self.rec_name = self.builder.get_object('label_recipent')
        self.rec_id = self.builder.get_object('label_recipent_id')
        self.recipentStore = self.builder.get_object('recipentStore')

        self.my_accelerators = Gtk.AccelGroup()
        self.windowMain.add_accel_group(self.my_accelerators)


        
        self.gpg = gnupg.GPG()
        self.gpg.encoding = 'utf-8'
        public_keys = self.gpg.list_keys()
        self.toCombo = [{'uid' : "".join(key['uids']),'fingerprint' : key['fingerprint']} for key in public_keys]
        for item in self.toCombo:
            self.recipentStore.append([item['uid']])
        
        # key = Keybinder()
        # key.bind("<control>m", self.test, "SHORTCUT TEST")
        # key.init()

        self.windowMain.show()
    
    def test(self, widget,data=None):
        print(data)

    def on_window_destroy(self, widget, data=None):
        Gtk.main_quit()
    
    def on_submenu_quit_activate(self, widget,data=None):
        Gtk.main_quit()
    
    def on_submenu_list_keys_activate(self, widget, data=None):
        print('LIST KEYS TRIGGER')
    
    def on_button1_clicked(self, widget,data=None):
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

            self.raw_data = got_text
            self.windowRecipent.show()
    
    def on_selectRecipentWindow_show(self,widget,data=None):
        pass
    
    def on_combo1_changed(self,widget,data=None):
        tree_iter = widget.get_active_iter()
        
        if tree_iter is not None:
            model = widget.get_model()
            selected = model[tree_iter][0]
        
        for item in self.toCombo:
            if item['uid'] == selected:
                self.rec_id.set_text(item['fingerprint'])
                self.rec_id.show()
                self.rec_name.show()
        
        

    def on_proceedButton1_clicked(self, widget,data=None):
        #! ENCRYPTION PART        
        encrypted_ascii_data = self.gpg.encrypt(self.raw_data, [f'{self.rec_id.get_text()}'],always_trust=True)
        self.textbuffer.set_text(str(encrypted_ascii_data)) # setting text to the view
        self.windowRecipent.hide()

    def on_cancelButton1_clicked(self, widget,data=None):
        self.windowRecipent.hide()
        
    def decrypt(self,pgp_data):
        self.textbuffer.set_text(str(self.gpg.decrypt(pgp_data))) # setting text to the view        

    def on_about_button_activate(self, widget,data=None):
        self.about.show()

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    app = WindowMain()
    app.main()