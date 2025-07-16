import pygame

class sound:
    def __init__(self, file:str, volume:float = 1):
        self.file = file
        self.sound = pygame.Sound(file)
        self.target_volume = volume
        self.volume = volume
        self.volume_change = None

        self.stop_at_zero = False
        self.stopped = False

    def set_volume(self, volume:float):
        self.volume = volume
        self.target_volume = volume
    
    def change_volume(self, target_volume:float, time:int):
        self.target_volume = target_volume
        self.volume_change = (target_volume - self.volume) / time * 1000

    def update(self, delta_time:float):
        if self.volume_change != None:
            self.volume += self.volume_change * delta_time
            if self.volume_change < 0:
                if self.volume < self.target_volume:
                    self.volume = self.target_volume
                    self.volume_change = None
            elif self.volume_change > 0:
                if self.volume > self.target_volume:
                    self.volume = self.target_volume
                    self.volume_change = None
        self.sound.set_volume(self.volume)
        if self.volume == 0 and self.stop_at_zero:
            self.sound.stop()
            self.stopped = True
    
    def play(self, start_volume:float, loops:int = 0, fade_in:int|None = None, target_volume:float|None = None):
        if fade_in == None:
            self.set_volume(start_volume)
            channel = self.sound.play(loops)
        else:
            self.set_volume(start_volume)
            self.change_volume(target_volume, fade_in)
            channel = self.sound.play(loops)
        self.stop_at_zero = False
        self.stopped = False
        return channel

    def stop(self, fade_out:int|None = None):
        if fade_out == None:
            self.set_volume(0)
        else:
            self.change_volume(0, fade_out)
        self.stop_at_zero = True

    @property
    def playing(self):
        return self.volume > 0

    def copy(self):
        return sound(self.file, self.volume)

class sounds:
    def __init__(self):
        self.sounds = {}

    def load_sound(self, name:str, file:str):
        self.sounds[name] = sound(file)

    def get_sound(self, name:str):
        return self.sounds[name]
    
class sound_manager:
    class channel_data:
        def __init__(self, volume:float):
            self.volume = volume
            self.target_volume = volume
            self.volume_change = None

        def set_volume(self, volume:float):
            self.volume = volume
            self.target_volume = volume
        
        def change_volume(self, target_volume:float, time:int):
            self.target_volume = target_volume
            self.volume_change = (target_volume - self.volume) / time * 1000
        
        def update(self, delta_time:float):
            if self.volume_change != None:
                self.volume += self.volume_change * delta_time
                if self.volume_change < 0:
                    if self.volume < self.target_volume:
                        self.volume = self.target_volume
                        self.volume_change = None
                elif self.volume_change > 0:
                    if self.volume > self.target_volume:
                        self.volume = self.target_volume
                        self.volume_change = None

    def __init__(self, channels:int, default_channel_volume:float, master_volume:float = 1):
        pygame.mixer.set_num_channels(channels)
        self.channels:dict[pygame.Channel:str] = {}
        self.channels_data:dict[str:sound_manager.channel_data] = {}
        self.playing_sounds:list[sound] = []

        self.default_channel_volume = default_channel_volume

        self.paused = False

        self.master_volume = master_volume
        self.target_master_volume = master_volume
        self.master_volume_change = None

    def set_channel_type_volume(self, channel_type:str, volume:float):
        if not channel_type in self.channels_data:
            self.channels_data[channel_type] = sound_manager.channel_data(self.default_channel_volume)
        self.channels_data[channel_type].set_volume(volume)

    def change_channel_type_volume(self, channel_type:str, target_volume:float, time:int):
        if not channel_type in self.channels_data:
            self.channels_data[channel_type] = sound_manager.channel_data(self.default_channel_volume)
        self.channels_data[channel_type].change_volume(target_volume, time)

    def set_master_volume(self, volume:float):
        self.master_volume = volume

    def change_master_volume(self, target_volume:float, time:int):
        self.target_master_volume = target_volume
        self.master_volume_change = (target_volume - self.master_volume) / time * 1000
    
    def update_channel_with_channel_data(self, channel_type:str, channel:pygame.Channel):
        if not channel_type in self.channels_data:
            self.channels_data[channel_type] = sound_manager.channel_data(self.default_channel_volume)
        channel.set_volume(self.channels_data[channel_type].volume)

    def play_sound(self, channel_type:str, sound:sound, start_volume:float, loops:int = 0, fade_in:int|None = None, target_volume:float|None = None):
        channel = sound.play(start_volume, loops, fade_in, target_volume)
        self.channels[channel] = channel_type
        self.playing_sounds.append(sound)
        self.update_channel_with_channel_data(channel_type, channel)

    def update(self, delta_time:float):
        if self.master_volume_change != None:
            self.master_volume += self.master_volume_change * delta_time
            if self.master_volume_change < 0:
                if self.master_volume < self.target_master_volume:
                    self.master_volume = self.target_master_volume
                    self.master_volume_change = None
            elif self.master_volume_change > 0:
                if self.master_volume > self.target_master_volume:
                    self.master_volume = self.target_master_volume
                    self.master_volume_change = None

        for channel_data in self.channels_data.values():
            channel_data.update(delta_time)
        
        for channel in self.channels:
            channel_type = self.channels[channel]
            channel.set_volume(self.channels_data[channel_type].volume * self.master_volume)

        for channel in self.channels.copy():
            if channel.get_busy() == False:
                del self.channels[channel]

        for sound in self.playing_sounds.copy():
            sound.update(delta_time)
            if sound.stopped:
                self.playing_sounds.remove(sound)

    def pause(self):
        pygame.mixer.pause()
        self.paused = True

    def unpause(self):
        pygame.mixer.unpause()
        self.paused = False

