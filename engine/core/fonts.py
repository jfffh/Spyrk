import pygame

class font:
    def __init__(self, file:str|None, sizes:list):
        self.font_sizes = {}
        for size in sizes:
            self.font_sizes[size] = pygame.Font(file, size)

    def draw_text(self, surface:pygame.Surface, position:tuple, x_alignment:str, y_alignment:str, font_size:int, text:str, color:tuple, bold:bool = False, italics:bool = False, underline:bool = False, text_wrap:int|None = None) -> pygame.FRect:
        def align_rect(rect:pygame.FRect, position:tuple, x_alignment:str, y_alignment:str):
            if x_alignment == ALIGN_CENTER:
                rect.centerx = position[0]
            elif x_alignment == ALIGN_RIGHT:
                rect.right = position[0]
            elif x_alignment == ALIGN_LEFT:
                rect.left = position[0]
            if y_alignment == ALIGN_CENTER:
                rect.centery = position[1]
            elif y_alignment == ALIGN_TOP:
                rect.top = position[1]
            elif y_alignment == ALIGN_BOTTOM:
                rect.bottom = position[1]
        
        text_rect:pygame.FRect|None = None

        font:pygame.Font = self.font_sizes[font_size]

        font.set_bold(bold)
        font.set_italic(italics)
        font.set_underline(underline)

        line_size = font.get_linesize()

        if text_wrap == None:
            if "\n" in text:
                text_lines = text.splitlines()
                for i in range(len(text_lines)):
                    text_image = font.render(text_lines[i], True, color)
                    rect = text_image.get_rect()
                    if y_alignment == ALIGN_BOTTOM:
                        align_rect(rect, (position[0], position[1] - i * line_size), x_alignment, y_alignment)
                    else:
                        align_rect(rect, (position[0], position[1] + i * line_size), x_alignment, y_alignment)
                    surface.blit(text_image, rect)
                    if text_rect == None:
                        text_rect = rect
                    else:
                        text_rect = text_rect.union(rect)
            else:
                text_image = font.render(text, True, color)
                rect = text_image.get_rect()
                align_rect(rect, position, x_alignment, y_alignment)
                surface.blit(text_image, rect)
                text_rect = rect
        else:
            words = text.split(" ")
            text_images:list[pygame.Surface] = []
            line_length = 0
            y = position[1]
            while len(words) > 0:
                word = words[0]
                if "\n" in word and "\n" != word:
                    new_words = word.split("\n")
                    word = new_words[0]
                    words.pop(0)
                    words.insert(0, word)
                    words.insert(1, "\n")
                    words.insert(2, new_words[1])
                text_image = font.render(word + " ", True, color)
                if line_length + text_image.get_width() > text_wrap or word == "\n":
                    x = 0
                    line_image = pygame.Surface((line_length, line_size), pygame.SRCALPHA)
                    for image in text_images:
                        rect = image.get_rect()
                        rect.left = x
                        rect.top = 0
                        line_image.blit(image, rect)
                        x += image.get_width()
                    
                    rect = line_image.get_rect()
                    align_rect(rect, (position[0], y), x_alignment, y_alignment)
                    surface.blit(line_image, rect)

                    text_images.clear()
                    line_length = 0
                    if y_alignment == ALIGN_BOTTOM:
                        y -= line_size
                    else:
                        y += line_size

                    if text_rect == None:
                        text_rect = rect
                    else:
                        text_rect = text_rect.union(rect)
                
                if word != "\n":
                    line_length += text_image.get_width()
                    text_images.append(text_image)
                words.pop(0)

            x = 0
            text_image = pygame.Surface((line_length, line_size), pygame.SRCALPHA)
            for image in text_images:
                rect = image.get_rect()
                rect.left = x
                rect.top = 0
                text_image.blit(image, rect)
                x += image.get_width()
            rect = text_image.get_rect()
            align_rect(rect, (position[0], y), x_alignment, y_alignment)
            surface.blit(text_image, rect)
            if text_rect == None:
                text_rect = rect
            else:
                text_rect = text_rect.union(rect)

        return text_rect

    def draw_lines_of_text(self, surface:pygame.Surface, position:tuple, x_alignment:str, y_alignment:str, font_size:int, text_lines:list[str], color:tuple, bold:bool = False, italics:bool = False, underline:bool = False, text_wrap:int|None = None) -> pygame.FRect:
        def align_rect(rect:pygame.FRect, position:tuple, x_alignment:str, y_alignment:str):
            if x_alignment == ALIGN_CENTER:
                rect.centerx = position[0]
            elif x_alignment == ALIGN_RIGHT:
                rect.right = position[0]
            elif x_alignment == ALIGN_LEFT:
                rect.left = position[0]
            if y_alignment == ALIGN_CENTER:
                rect.centery = position[1]
            elif y_alignment == ALIGN_TOP:
                rect.top = position[1]
            elif y_alignment == ALIGN_BOTTOM:
                rect.bottom = position[1]
        
        text_rect:pygame.FRect|None = None

        font:pygame.Font = self.font_sizes[font_size]

        font.set_bold(bold)
        font.set_italic(italics)
        font.set_underline(underline)

        line_size = font.get_linesize()

        for i in range(len(text_lines)):
            text_image = font.render(text_lines[i], True, color)
            rect = text_image.get_rect()
            if y_alignment == ALIGN_BOTTOM:
                align_rect(rect, (position[0], position[1] - i * line_size), x_alignment, y_alignment)
            else:
                align_rect(rect, (position[0], position[1] + i * line_size), x_alignment, y_alignment)
            surface.blit(text_image, rect)
            if text_rect == None:
                text_rect = rect
            else:
                text_rect = text_rect.union(rect)

        return text_rect

    def get_line_size(self, font_size:int):
        return self.font_sizes[font_size].get_linesize()

    def draw_text_onto_new_surface(self, font_size:int, text:str, color:tuple, bold:bool = False, italics:bool = False, underline:bool = False):
        font:pygame.Font = self.font_sizes[font_size]
        font.set_bold(bold)
        font.set_italic(italics)
        font.set_underline(underline)
        return font.render(text, True, color)


ALIGN_CENTER = "center"
ALIGN_RIGHT = "right"
ALIGN_LEFT = "left"
ALIGN_TOP = "top"
ALIGN_BOTTOM = "bottom"