import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import subprocess

class WindowMain:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gpg.glade")
        self.builder.connect_signals(self)

        self.windowMain = self.builder.get_object('window')
        self.textView1 = self.builder.get_object('textview1')
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


            recipents = SelectRecipent(self)
            response = recipents.run()
            recipents.destroy()

        
    def decrypt(self,pgp_data):
        cmd = f"echo '{pgp_data}' | gpg --decrypt"
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0].decode("utf-8")
        self.textbuffer.set_text(output) # setting text to the view


    def main(self):
        Gtk.main()


class SelectRecipent(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Select recipent", flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Select recipent from list below")

        box = self.get_content_area()
        box.add(label)
        self.show_all()


if __name__ == "__main__":
    app = WindowMain()
    app.main()