import logging
import tk
import customtkinter as ctk
from tkinter import messagebox as msg


def delete_item(self, id, item_id, logged_user_id):
        try:
            # Verifica se o usuário logado é o mesmo registrado na DB
            if logged_user_id != id:
                return False, "Unauthorized: Cannot delete item of another user."
            
            result = self.logins.delete_one({'_id': item_id})
            if result.deleted_count > 0:
                return True, "Item deleted successfully."
            else:
                return False, "Item not found."
        except Exception as e:
            logging.error(f"Failed to delete item: {e}")
            return False, "Failed to delete item: an error occurred."