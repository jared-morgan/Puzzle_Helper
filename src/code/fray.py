import pygame

class Fray:
    def __init__(self):
        self.length_of_a_minute = 60
        pass
    
    def find_fray_duration(self, fray_time):
        fray_duration = (pygame.time.get_ticks() - fray_time) // 1000
        rumble_mins = fray_duration // self.length_of_a_minute # length_of_a_minute for quick debugging
        if rumble_mins > 15:
            rumble_mins = 15
        return fray_duration, rumble_mins


    def rumble_timer(self, main, fray_time, rumble_sound_played, rumble_warning_sound):
        fray_duration, rumble_mins = find_rumble_duration(fray_time)
        if fray_duration % 60 < 50: # Change this if you want a warning for the minute mark at a different time
            game_display.fill(black)
            rumble_sound_played = False
        elif fray_duration > 0 and rumble_warning_sound:
            game_display.fill(blue)
            if not rumble_sound_played:
                pygame.mixer.Sound.play(warning)
                rumble_sound_played = True

        if fray_duration > -1:
            rumble_table_start = [rumble_scaling*2+25, 92]
            if is_window_large:

                pygame.draw.rect(game_display, white, (rumble_table_start[0], rumble_table_start[1], (rumble_width*rumble_scaling)+4, (rumble_height*rumble_scaling)+4), 1)  # (x, y, width, height), 2 is the thickness
                pygame.draw.rect(game_display, grey, (rumble_table_start[0]+1, rumble_table_start[1]+1, (rumble_width*rumble_scaling)+2, (rumble_height*rumble_scaling)+2), 1)
                punch_start_location = [rumble_table_start[0]+2, rumble_table_start[1]+2 + (20 * rumble_scaling)]
                greyscale_colour = grey
                colourful_colour = yellow

                for groups in punch_dictionary[rumble_mins]:
                    #Minutes,Groups,Drop-off,Calc Rows,Difference,Base Width
                    
                    drop_off, length, difference, width = punch_dictionary[rumble_mins][groups][0], punch_dictionary[rumble_mins][groups][1], punch_dictionary[rumble_mins][groups][2], punch_dictionary[rumble_mins][groups][3]
                    if 7 < length < 19:
                        text_colour = colourful_colour
                        block_colour = colourful_colour
                        if colourful_colour == yellow:
                            colourful_colour = gold
                        else:
                            colourful_colour = yellow
                    else:
                        text_colour = grey
                        block_colour = greyscale_colour
                        if greyscale_colour == grey:
                            greyscale_colour = white
                        else:
                            greyscale_colour = grey
                    
                    punch_text = my_font_very_small.render(str(groups), True, text_colour)
                    drop_off_text = my_font_very_very_small.render(str(drop_off), True, black)
                    punch_start_location[1] -= difference * rumble_scaling
                    
                    if bars_as_natural_width:
                        pygame.draw.rect(game_display, block_colour, (punch_start_location[0], punch_start_location[1], (rumble_width*rumble_scaling*width/9), (difference*rumble_scaling)))
                    else:
                        pygame.draw.rect(game_display, block_colour, (punch_start_location[0], punch_start_location[1], (rumble_width*rumble_scaling), (difference*rumble_scaling)))
                    if groups > 9:
                        game_display.blit(punch_text, (punch_start_location[0] - (rumble_scaling * 1.5), punch_start_location[1]))
                    else:
                        game_display.blit(punch_text, (punch_start_location[0] - (rumble_scaling * 0.85), punch_start_location[1]))
                    if drop_off_numbers:
                        game_display.blit(drop_off_text, (punch_start_location[0] + (rumble_scaling * 0.1), punch_start_location[1]))
                        
            else:
                number_group_text = my_font_small.render(number_groups[rumble_mins],True, white)
                game_display.blit(number_group_text, (25, 85))
            
            rumble_timer_colour = white

            rumble_time_elapsed_text = my_font_med.render(str(int(math.floor(fray_duration // 60))) + ":" + str(int(math.floor(fray_duration % 60))), True, rumble_timer_colour)
            

            game_display.blit(rumble_time_elapsed_text, (25, 30))
            # pygame.draw.rect(game_display, white, (rumble_table_start[0]+25, rumble_table_start[1], (rumble_width*rumble_scaling)+4-25, (10*rumble_scaling)+4))
            # pygame.draw.rect(game_display, block_colour, (punch_start_location[0], punch_start_location[1], (rumble_width*rumble_scaling*width/9), (difference*rumble_scaling)))
        elif fray_countdown_on:
            rumble_timer_colour = white
            rumble_time_elapsed_text = my_font_med.render("-0:" + str(60-int(math.floor(fray_duration % 60))), True, rumble_timer_colour)
            game_display.blit(rumble_time_elapsed_text, (25, 30))

        return rumble_sound_played