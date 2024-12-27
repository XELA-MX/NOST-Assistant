import customtkinter
import openai
import tiktoken
import threading
import time
from markdown_it import MarkdownIt  # Para procesar Markdown
import sys

# Configura tu clave API
openai.api_key = ""


# Función para calcular los tokens utilizados
def calcular_tokens_usados(messages, modelo="gpt-4o"):
    encoding = tiktoken.encoding_for_model(modelo)
    total_tokens = 0
    for message in messages:
        for key, value in message.items():
            total_tokens += len(encoding.encode(value))
    total_tokens += 3 * len(messages) + 2
    return total_tokens

# Asistente que recuerda el contexto solo durante la sesión
def mini_asistente(query, messages, modelo="gpt-4", max_tokens=500):
    try:
        # Añade la consulta del usuario al historial
        messages.append({"role": "user", "content": query})

        # Calcula el número de tokens usados hasta ahora
        tokens_usados = calcular_tokens_usados(messages, modelo)

        # Verifica si los tokens restantes permiten hacer la solicitud
        if tokens_usados > max_tokens - 100:  # Deja margen para la respuesta
            return "Lo siento, el historial de la conversación es muy largo. Por favor, reinicia la conversación."

        # Solicita a la API con el historial completo
        response = openai.ChatCompletion.create(
            model=modelo,
            messages=messages,
            temperature=0.5,
            max_tokens=150  # Máximo de tokens para la respuesta
        )

        # Obtiene la respuesta del asistente
        assistant_response = response.choices[0].message.content.strip()

        # Añade la respuesta al historial
        messages.append({"role": "assistant", "content": assistant_response})

        return assistant_response
    except Exception as e:
        return f"Error: {str(e)}"

# Interfaz gráfica con conexión a la IA
def loadApp():
    # Inicializa el historial con el mensaje del sistema
    messages = [{"role": "system", "content": "Eres un asistente útil que recuerda el historial de la conversación durante la sesión."}]

    # Dimensiones de la ventana
    screen_width = customtkinter.CTk().winfo_screenwidth()
    screen_height = customtkinter.CTk().winfo_screenheight()

    app = customtkinter.CTk()
    ctk = customtkinter

    # Configuración de la ventana
    app.title("NOST - Asistente")
    app.geometry(f"{screen_width//3}x{screen_height//2}")

    # Configurar filas y columnas para centrar
    app.grid_rowconfigure(0, weight=1)  # Centrar verticalmente
    app.grid_columnconfigure(0, weight=1)  # Centrar horizontalmente

    # Marco para el contenido del chat
    chat_frame = ctk.CTkFrame(app)
    chat_frame.grid(column=0, row=0, sticky="nsew", padx=10, pady=10)

    # Configurar el grid dentro del marco
    chat_frame.grid_rowconfigure(0, weight=1)  # Para que el cuadro de texto crezca
    chat_frame.grid_columnconfigure(0, weight=1)

    # Cuadro de texto para mensajes
    message_box = ctk.CTkTextbox(chat_frame, height=200, state="disabled", wrap="word")
    message_box.grid(column=0, row=0, sticky="nsew", padx=10, pady=10)

    # Campo de entrada para el usuario
    user_input = ctk.CTkEntry(app, placeholder_text="Escribe tu mensaje aquí...")
    user_input.grid(column=0, row=2, padx=10, pady=(10, 0), sticky="ew")

    # Variable para controlar hilos
    stop_event = threading.Event()

    # MarkdownIt para procesar el formato
    md = MarkdownIt()

    def procesar_markdown_a_texto(markdown_text):
        """
        Convierte texto Markdown a texto plano legible.
        """
        result = ""
        for line in markdown_text.splitlines():
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):  # Manejar listas
                result += f"{line}\n"
            elif line.startswith("**") and line.endswith("**"):  # Manejar negritas
                result += f"{line.strip('**')}\n"
            else:
                result += f"{line}\n"
        return result.strip()

    # Función para animar puntos pensantes con límite de tiempo
    def animar_puntos(label, stop_event):
        while not stop_event.is_set():  # Continúa mientras no se detenga el evento
            for puntos in ["", ".", "..", "..."]:
                if stop_event.is_set():
                    break
                if label.winfo_exists():  # Verifica si el label aún existe
                    label.configure(text=f"Pensando{puntos}")
                time.sleep(0.5)  # Cambia la velocidad de la animación

    # Función para enviar el mensaje
    def send_message():
        user_message = user_input.get()
        if user_message.strip():
            # Mostrar el mensaje del usuario en el cuadro de texto
            message_box.configure(state="normal")
            message_box.insert("end", f"Usuario: {user_message}\n")
            message_box.configure(state="disabled")
            message_box.see("end")  # Desplazar hacia abajo

            # Mostrar "Pensando..." mientras se genera la respuesta
            thinking_label = ctk.CTkLabel(app, text="Pensando...", font=("Arial", 14))
            thinking_label.grid(column=0, row=4, padx=10, pady=10)

            # Limpiar el campo de entrada
            user_input.delete(0, "end")

            # Evento para detener la animación
            stop_event.clear()

            # Función para manejar la respuesta en segundo plano
            def generar_respuesta():
                # Animar puntos en un hilo separado
                animar_thread = threading.Thread(target=animar_puntos, args=(thinking_label, stop_event))
                animar_thread.start()

                # Obtener respuesta de la IA
                assistant_response = mini_asistente(user_message, messages)

                # Detener la animación al terminar
                stop_event.set()
                animar_thread.join()
                if thinking_label.winfo_exists():  # Verifica si el label aún existe
                    thinking_label.destroy()

                # Procesar respuesta Markdown
                respuesta_formateada = procesar_markdown_a_texto(assistant_response)

                # Mostrar la respuesta en el cuadro de texto
                message_box.configure(state="normal")
                message_box.insert("end", f"NOST: {respuesta_formateada}\n")
                message_box.configure(state="disabled")
                message_box.see("end")  # Desplazar hacia abajo

            # Ejecutar la generación de respuesta en un hilo separado
            respuesta_thread = threading.Thread(target=generar_respuesta)
            respuesta_thread.start()

    # Función para manejar eventos de teclas
    def key_handler(event):
        if event.keysym == "Return":  # Enter presionado
            if event.state & 0x0001:  # Shift presionado
                user_input.insert("insert", "\n")  # Insertar nueva línea
            else:
                send_message()  # Enviar mensaje
                return "break"  # Evitar que se agregue una nueva línea

    user_input.bind("<KeyPress>", key_handler)  # Vincular el manejador de teclas

    send_button = ctk.CTkButton(app, text="Enviar", command=send_message)
    send_button.grid(column=0, row=3, padx=10, pady=10, sticky="ew")

    # Función para manejar el cierre de la ventana
    def on_closing():
        stop_event.set()  # Detener hilos activos
        app.destroy()  # Cerrar la aplicación
        sys.exit()

    # Vincular el cierre de la ventana
    app.protocol("WM_DELETE_WINDOW", on_closing)

    app.mainloop()

# Inicia la aplicación
if __name__ == "__main__":
    loadApp()