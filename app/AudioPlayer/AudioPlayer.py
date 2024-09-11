import pygame

import sys

pathMap = {
    'success': './sounds/success.wav',
    'failure': './sounds/failure.wav',
}


class AudioPlayer:

    def __init__(self, opts=None):

        if opts is None:
            opts = {}
        self.opts = opts

    def play(self):

        if 'sound_type' not in self.opts:
            print("No sound type specified")

            return

        pygame.mixer.init()

        audio_path = pathMap.get(self.opts['sound_type'], None)

        if audio_path is None:
            print("Audio file not found for the specified type")

            return

        try:

            # 加载音频文件

            pygame.mixer.music.load(audio_path)

            # 播放音频

            pygame.mixer.music.play()

            # 等待音频播放完毕

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)



        except pygame.error as e:

            print(f"Error playing audio: {e}")

            # 通常不建议在音频播放完毕后退出pygame，但这里保留原逻辑

        # 如果需要多次播放音频，请移除pygame.quit()和sys.exit()

        pygame.quit()

        # 如果不需要每次播放后都退出程序，请移除sys.exit()

        # sys.exit()


if __name__ == '__main__':
    p = AudioPlayer({'sound_type': 'success'})

    p.play()
