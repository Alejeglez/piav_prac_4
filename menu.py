import cv2 as cv
import numpy as np


class Menu:

    def __init__(self, img_source):
        self.img = None
        self.img_source = img_source
        self.img_result = img_source
        self.height, self.width = self.img_source.shape[:2]
        self.dimensions_sections = []
        self.dimensions_actions = []
        self.sections = []
        self.heights_sections = []
        self.intervals = []
        self.intervals_action = []
        self.sections_selected = []
        self.actions = ["Aplicar", "Limpiar", "Guardar"]
        self.prepare_graphs()


    def create_menu(self, elements):
        #height of menu should be a sixth of the screen
        self.get_sections(elements)
        self.get_width_section_elements()
        self.get_section_heights()
        self.get_other_heights()
        self.get_width_action_elements()


        self.img = np.zeros((self.heights_action[1], self.width, 3), np.uint8)


        self.draw_sections() 
        self.draw_lower_menu()     

        
    def get_sections(self, elements):
        for sections in elements:
            if len(sections) > 4:
                raise ValueError("No pueden haber más de 4 elementos por sección")
            else:
                self.sections.append(sections)
                self.sections_selected.append([False for _ in sections])
    
    def get_width_section_elements(self):  
        for section in self.sections:
            points = []
            interval = self.width // len(section)
            self.intervals.append(interval)
            for i in range(len(section)):
                points.append([interval * i, interval * (i + 1)])
            self.dimensions_sections.append(points)
    

    def get_width_action_elements(self):
        points = []
        interval = self.width // len(self.actions)  # Calcula el intervalo una vez
        self.intervals_action.append(interval)
        
        # Calcula los puntos solo una vez
        for i in range(len(self.actions)):
            self.dimensions_actions.append([interval * i, interval * (i + 1)])
    

    def get_section_heights(self):
        height_section = self.height // 12
        cumulative_height = 0
        for i in range(len(self.sections)):
            lista_heights = []
            lista_heights.append(cumulative_height)
            lista_heights.append(cumulative_height + height_section)
            cumulative_height += height_section
            self.heights_sections.append(lista_heights)

    def get_other_heights(self):
        height_lower_menu_up = self.height + self.heights_sections[-1][-1]
        height_lower_menu_down = height_lower_menu_up + self.heights_sections[0][1]
        self.heights_action = [height_lower_menu_up, height_lower_menu_down]
        
    def draw_section_element(self, i, j, selected=False):
        if selected == False:
            color = (161, 157, 148)
        else:
            color = (255, 255, 255)

        cv.rectangle(
            self.img,
            (self.dimensions_sections[i][j][0], self.heights_sections[i][0]),
            (self.dimensions_sections[i][j][1], self.heights_sections[i][1]),
            color,
            -1
        )
        cv.rectangle(
            self.img, 
            (self.dimensions_sections[i][j][0], self.heights_sections[i][0]), 
            (self.dimensions_sections[i][j][1], self.heights_sections[i][1]), 
            (0, 0, 0), 1
        )

        element_size = cv.getTextSize(self.sections[i][j], cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]

        element_x = self.dimensions_sections[i][j][0] + (self.intervals[i] - element_size[0]) // 2
        element_y = self.heights_sections[i][0] + ((self.heights_sections[i][1] - self.heights_sections[i][0]) + element_size[1]) // 2


        cv.putText(
            self.img, 
            self.sections[i][j], 
            (element_x, element_y), 
            cv.FONT_HERSHEY_SIMPLEX, 
            0.5, 
            (0, 0, 0), 
            1, 
            cv.LINE_AA
        )


    def draw_sections(self):
        for i in range(len(self.heights_sections)):
            for j in range(len(self.dimensions_sections[i])):
                self.draw_section_element(i, j)

            self.set_img(add_base=True)


        self.set_img(add_base=True)


    def draw_lower_menu(self):
        cv.rectangle(self.img, (0, self.heights_action[0]), (self.width, self.heights_action[1]), (161, 157, 148), -1)

        for i in range(len(self.actions)):
            cv.rectangle(self.img, (self.dimensions_actions[i][0], self.heights_action[0]), (self.dimensions_actions[i][1], self.heights_action[1]), (0, 0, 0), 1)

            element_size = cv.getTextSize(self.actions[i], cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]

            element_x = self.dimensions_actions[i][0] + (self.intervals_action[0] - element_size[0]) // 2

            element_y = self.heights_action[0] + ((self.heights_action[1] - self.heights_action[0]) + element_size[1]) // 2

            cv.putText(self.img, self.actions[i], (element_x, element_y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv.LINE_AA)


    def select_section_element(self, x, y):
        for i in range(len(self.sections_selected)):
            for j in range(len(self.sections_selected[i])):
                if self.sections_selected[i][j]:
                    self.sections_selected[i][j] = False
                    self.draw_section_element(i, j, self.sections_selected[i][j])

        for i in range(len(self.dimensions_sections)):
            for j in range(len(self.dimensions_sections[i])):
                if (self.dimensions_sections[i][j][0] < x < self.dimensions_sections[i][j][1] and
                    self.heights_sections[i][0] < y < self.heights_sections[i][1]):
                                     
                    self.sections_selected[i][j] = not self.sections_selected[i][j]

                    self.draw_section_element(i, j, self.sections_selected[i][j])
        
        cv.imshow("Imagen", self.img)


    def get_section_selected(self):
        for i in range(len(self.sections_selected)):
            for j in range(len(self.sections_selected[i])):
                if self.sections_selected[i][j]:
                    return self.sections[i][j]
        return None
    

    def set_img(self, add_base=False):
        if add_base:
           last_height = self.heights_sections[-1][-1]
           self.img[last_height:self.height+last_height, :self.width] = self.img_source
        
        cv.imshow("Imagen", self.img)
    

    def set_time_graphs(self):
        last_height = self.heights_sections[-1][-1]
        if self.original_graph_time is not None:
            self.img[last_height:self.height+last_height, :self.width//3] = self.original_graph_time

        if self.noise_graph_time is not None:
            self.img[last_height:self.height+last_height, self.width//3:2*self.width//3] = self.noise_graph_time

        if self.transformed_graph_time is not None:
            self.img[last_height:self.height+last_height, 2*self.width//3:] = self.transformed_graph_time
        
        cv.imshow("Imagen", self.img)

    
    def set_freq_graphs(self):
        last_height = self.heights_sections[-1][-1]
        if self.original_graph_freq is not None:
            self.img[last_height:self.height+last_height, :self.width//3] = self.original_graph_freq
        if self.noise_graph_freq is not None:
            self.img[last_height:self.height+last_height, self.width//3:2*self.width//3] = self.noise_graph_freq
        if self.transformed_graph_freq is not None:
            self.img[last_height:self.height+last_height, 2*self.width//3:] = self.transformed_graph_freq
        
        cv.imshow("Imagen", self.img)

    def prepare_graphs(self):
        self.original_graph_time = None
        self.original_graph_freq = None
        self.transformed_graph_time = None
        self.transformed_graph_freq = None
        self.noise_graph_time = None
        self.noise_graph_freq = None