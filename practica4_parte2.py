from tkinter import Tk # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import numpy as np
import matplotlib.pyplot as plt
from menu import Menu
import cv2 as cv
import numpy as np
import time
from audio_processor import AudioProcessor

def process_graphics_original(menu, audio_processor):

    fig, ax = plt.subplots(figsize=(5, 5))  # Tamaño 500x500 píxeles
    ax.plot(audio_processor.signal_noise)
    ax.set_title('Señal Original (Dominio del Tiempo)')
    ax.set_xlabel('Muestra')
    ax.set_ylabel('Amplitud')

    # Dibujar la figura y convertirla en un array de imagen
    fig.canvas.draw()
    img_plot = np.frombuffer(fig.canvas.renderer.buffer_rgba(), dtype=np.uint8)
    img_plot = img_plot.reshape(fig.canvas.get_width_height()[::-1] + (4,))  # (alto, ancho, RGBA)
    menu.original_graph_time = cv.cvtColor(img_plot, cv.COLOR_RGBA2RGB)

    fig, ax = plt.subplots(figsize=(5, 5))  # Tamaño 500x500 píxeles
    ax.plot(audio_processor.frecuency_noise, np.abs(audio_processor.fft_noise))
    ax.set_title('Señal Original (Dominio de la Frecuencia)')
    ax.set_xlabel('Frecuencia (Hz)')
    ax.set_ylabel('Amplitud')

    # Dibujar la figura y convertirla en un array de imagen
    fig.canvas.draw()
    img_plot = np.frombuffer(fig.canvas.renderer.buffer_rgba(), dtype=np.uint8)
    img_plot = img_plot.reshape(fig.canvas.get_width_height()[::-1] + (4,))  # (alto, ancho, RGBA)
    menu.original_graph_freq = cv.cvtColor(img_plot, cv.COLOR_RGBA2RGB)

    #eliminar figuras
    plt.close('all')


def process_graphics_transformed(menu, audio_processor):
    
    fig, ax = plt.subplots(figsize=(5, 5))  # Tamaño 500x500 píxeles
    ax.plot(audio_processor.signal_transformed)
    ax.set_title('Señal Transformada (Dominio del Tiempo)')
    ax.set_xlabel('Muestra')
    ax.set_ylabel('Amplitud')

    # Dibujar la figura y convertirla en un array de imagen
    fig.canvas.draw()
    img_plot = np.frombuffer(fig.canvas.renderer.buffer_rgba(), dtype=np.uint8)
    img_plot = img_plot.reshape(fig.canvas.get_width_height()[::-1] + (4,))  # (alto, ancho, RGBA)
    menu.transformed_graph_time = cv.cvtColor(img_plot, cv.COLOR_RGBA2RGB)

    fig, ax = plt.subplots(figsize=(5, 5))  # Tamaño 500x500 píxeles
    ax.plot(audio_processor.frecuency_transformed, np.abs(audio_processor.fft_transformed))
    ax.set_title('Señal Transformada (Dominio de la Frecuencia)')
    ax.set_xlabel('Frecuencia (Hz)')
    ax.set_ylabel('Amplitud')

    # Dibujar la figura y convertirla en un array de imagen
    fig.canvas.draw()
    img_plot = np.frombuffer(fig.canvas.renderer.buffer_rgba(), dtype=np.uint8)
    img_plot = img_plot.reshape(fig.canvas.get_width_height()[::-1] + (4,))  # (alto, ancho, RGBA)
    menu.transformed_graph_freq = cv.cvtColor(img_plot, cv.COLOR_RGBA2RGB)

    #eliminar figuras
    try:
        for fig in plt.get_fignums():
            plt.close(fig)
    except Exception as e:
        print(f"Error cerrando figura: {e}")


def process_graphics_noise(menu, audio_processor):
        
    fig, ax = plt.subplots(figsize=(5, 5))  # Tamaño 500x500 píxeles
    ax.plot(audio_processor.signal_noise)
    ax.set_title('Con Ruido (Dominio del Tiempo)')
    ax.set_xlabel('Muestra')
    ax.set_ylabel('Amplitud')

    # Dibujar la figura y convertirla en un array de imagen
    fig.canvas.draw()
    img_plot = np.frombuffer(fig.canvas.renderer.buffer_rgba(), dtype=np.uint8)
    img_plot = img_plot.reshape(fig.canvas.get_width_height()[::-1] + (4,))  # (alto, ancho, RGBA)
    menu.noise_graph_time = cv.cvtColor(img_plot, cv.COLOR_RGBA2RGB)

    fig, ax = plt.subplots(figsize=(5, 5))  # Tamaño 500x500 píxeles
    ax.plot(audio_processor.frecuency_noise, np.abs(audio_processor.fft_noise))
    ax.set_title('Ruido (Dominio de la Frecuencia)')
    ax.set_xlabel('Frecuencia (Hz)')
    ax.set_ylabel('Amplitud')

    # Dibujar la figura y convertirla en un array de imagen
    fig.canvas.draw()
    img_plot = np.frombuffer(fig.canvas.renderer.buffer_rgba(), dtype=np.uint8)
    img_plot = img_plot.reshape(fig.canvas.get_width_height()[::-1] + (4,))  # (alto, ancho, RGBA)
    menu.noise_graph_freq = cv.cvtColor(img_plot, cv.COLOR_RGBA2RGB)

    #eliminar figuras
    plt.close('all')
    
def nothing(x):
    pass

def get_options_window(menu, audio_processor):

    if audio_processor.signal is not None:
        if menu.get_section_selected() == "Paso-Alto" or menu.get_section_selected() == "Paso-Bajo":
            if cv.getWindowProperty("Opciones 2 umbrales", cv.WND_PROP_VISIBLE) == 1:
                cv.destroyWindow("Opciones 2 umbrales")
            
            if len(audio_processor.frecuency) > 0:
                max_value = int(max(audio_processor.frecuency))  # Convierte a entero
            else:
                max_value = 100

            if cv.getWindowProperty("Opciones 1 umbral", cv.WND_PROP_VISIBLE) == 0:
                cv.namedWindow("Opciones 1 umbral")
                #crea un tamaño mínimo para la ventana
                cv.resizeWindow("Opciones 1 umbral", 500, 100)
                cv.createTrackbar("Umbral", "Opciones 1 umbral", 0, max_value, nothing)
        
        elif menu.get_section_selected() == "Paso-Banda" or menu.get_section_selected() == "Rechaza-Banda":
            print("Paso-Banda o Rechaza-Banda")
            if cv.getWindowProperty("Opciones 1 umbral", cv.WND_PROP_VISIBLE) == 1:
                cv.destroyWindow("Opciones 1 umbral")
            
            if len(audio_processor.frecuency) > 0:
                max_value = int(max(audio_processor.frecuency))
            else:
                max_value = 100
            
            if cv.getWindowProperty("Opciones 2 umbrales", cv.WND_PROP_VISIBLE) == 0:
                cv.namedWindow("Opciones 2 umbrales")
                cv.resizeWindow("Opciones 2 umbrales", 500, 100)
                cv.createTrackbar("Bajo", "Opciones 2 umbrales", 0, max_value, nothing)
                cv.createTrackbar("Alto", "Opciones 2 umbrales", 0, max_value, nothing)
    
    else:
        print("No hay señal")

def select_action_image(menu, x, y):

    if menu.dimensions_actions[0][0] < x < menu.dimensions_actions[0][1]:
        if menu.get_section_selected() != "":
            if cv.getWindowProperty("Opciones 1 umbral", cv.WND_PROP_VISIBLE) == 1:
                if menu.get_section_selected() == "Paso-Alto":
                    audio_processor.highpass_filter(int(cv.getTrackbarPos("Umbral", "Opciones 1 umbral")))
                elif menu.get_section_selected() == "Paso-Bajo":
                    audio_processor.lowpass_filter(int(cv.getTrackbarPos("Umbral", "Opciones 1 umbral")))
                
                audio_processor.apply_fft_transformed()

                process_graphics_transformed(menu, audio_processor)
                cv.imshow("Imagen", menu.img)
            
            elif cv.getWindowProperty("Opciones 2 umbrales", cv.WND_PROP_VISIBLE) == 1:
                if menu.get_section_selected() == "Paso-Banda":
                    audio_processor.bandpass_filter(cv.getTrackbarPos("Bajo", "Opciones 2 umbrales"), cv.getTrackbarPos("Alto", "Opciones 2 umbrales"))
                elif menu.get_section_selected() == "Rechaza-Banda":
                    audio_processor.bandstop_filter(cv.getTrackbarPos("Bajo", "Opciones 2 umbrales"), cv.getTrackbarPos("Alto", "Opciones 2 umbrales"))

                audio_processor.apply_fft_transformed()

                process_graphics_transformed(menu, audio_processor)
                cv.imshow("Imagen", menu.img)
    
    elif menu.dimensions_actions[1][0] < x < menu.dimensions_actions[1][1]:
        audio_processor.clear()
        menu.prepare_graphs()
            
    elif menu.dimensions_actions[2][0] < x < menu.dimensions_actions[2][1]:
        
        if audio_processor.signal_transformed is not None:
            audio_processor.save_transformed_audio()


def mouse(event, x, y, flags, param):
    global menu, audio_processor

    if flags == 1:
        if y > menu.heights_sections[0][0] and y < menu.heights_sections[0][1]:
            menu.select_section_element(x, y)
            
            if menu.get_section_selected() == "Seleccionar Archivo":
                Tk().withdraw()
                filename = askopenfilename()
                if filename == "":
                    return
                else:
                    audio_processor.read_audio(filename)
                    menu.prepare_graphs()
                    menu.set_img(add_base=True)
                    process_graphics_original(menu, audio_processor)
                    process_graphics_noise(menu, audio_processor)
            
            if menu.get_section_selected() == "Tiempo":
                menu.set_time_graphs()
            
            if menu.get_section_selected() == "Frecuencia":
                menu.set_freq_graphs()
            
            if cv.getWindowProperty("Opciones 1 umbral", cv.WND_PROP_VISIBLE) == 1:
                cv.destroyWindow("Opciones 1 umbral")

            elif cv.getWindowProperty("Opciones 2 umbrales", cv.WND_PROP_VISIBLE) == 1:
                cv.destroyWindow("Opciones 2 umbrales")    
        

        if y > menu.heights_sections[1][0] and y < menu.heights_sections[1][1]:
            menu.select_section_element(x, y)
            get_options_window(menu, audio_processor)

        if y > menu.heights_sections[2][0] and y < menu.heights_sections[2][1]:
            menu.select_section_element(x, y)
            time.sleep(0.01)
            
            if menu.get_section_selected() == "Original":
                audio_processor.reproduce_signal(audio_processor.signal)
            
            if menu.get_section_selected() == "Ruido":
                audio_processor.reproduce_signal(audio_processor.signal_noise)
            
            if menu.get_section_selected() == "Corregido":
                audio_processor.reproduce_signal(audio_processor.signal_transformed)
        
        if y > menu.heights_action[0] and y < menu.heights_action[1]:
            select_action_image(menu, x, y)

img_source = np.zeros((500, 1500, 3), np.uint8)
menu = Menu(img_source)
menu.create_menu(elements=[["Seleccionar Archivo", "Tiempo", "Frecuencia"], ["Paso-Alto", "Paso-Bajo", "Paso-Banda", "Rechaza-Banda"], ["Original", "Ruido", "Corregido"]])
audio_processor = AudioProcessor()
cv.imshow("Imagen", menu.img)
cv.setMouseCallback("Imagen", mouse)
cv.waitKey(0)
cv.destroyAllWindows()