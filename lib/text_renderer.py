import constants
from fonts import font

def clear_whole_line(tft): 
    tft.fill_rect(0, 120 - constants.FONT_HEIGHT, constants.DISPLAY_W, constants.FONT_HEIGHT*2, constants.BLACK)

def clear_two_whole_lines(tft): 
    tft.fill_rect(0, 120 - constants.FONT_HEIGHT, constants.DISPLAY_W, constants.FONT_HEIGHT*4, constants.BLACK)

def clear_three_whole_lines(tft): 
    tft.fill_rect(0, 120 - constants.FONT_HEIGHT, constants.DISPLAY_W, constants.FONT_HEIGHT*6, constants.BLACK)

def render_text_line_center(tft, text, color): 
    x = 120 - len(text)*constants.FONT_WIDTH
    y = 120 - constants.FONT_HEIGHT
    tft.text(font, text, x, y, color)

def render_two_text_lines_center(tft, text1, text2, color): 
    tft.text(font, text1, 120-(len(text1)*constants.FONT_WIDTH), 120-constants.FONT_HEIGHT, color)
    tft.text(font, text2, 120-(len(text2)*constants.FONT_WIDTH), 120+constants.FONT_HEIGHT, color)

def render_three_text_lines_center(tft, text1, text2, text3, color): 
    tft.text(font, text1, 120-(len(text1)*constants.FONT_WIDTH), 120-constants.FONT_HEIGHT*3, color)
    tft.text(font, text2, 120-(len(text2)*constants.FONT_WIDTH), 120, color)
    tft.text(font, text3, 120-(len(text3)*constants.FONT_WIDTH), 120+constants.FONT_HEIGHT*3, color)
